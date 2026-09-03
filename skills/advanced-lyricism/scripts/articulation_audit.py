#!/usr/bin/env python3
"""Map consonant density, transitions and articulation pressure by line."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from lyric_utils import words,analyze_word,split_phoneme,CONS_FEATURES,SIBILANTS,line_syllables,read_text_arg,configure_pronunciation_overrides,support_state,pronunciation_backend

def issues(line):
    stream=[];known_words=0;wl=words(line)
    analyses=[analyze_word(w) for w in wl]
    for wi,(w,a) in enumerate(zip(wl,analyses)):
        if a["phonemes"]: known_words+=1
        for ph in a["phonemes"]:
            b,_=split_phoneme(ph);stream.append((b,wi,w))
    out=[]
    for i in range(max(0,len(stream)-3)):
        win=stream[i:i+4]
        if sum(p in SIBILANTS for p,_,_ in win)>=3:
            out.append({"type":"sibilant_cluster","phonemes":[p for p,_,_ in win],"words":sorted(set(w for _,_,w in win))})
    for i in range(len(stream)-2):
        tri=stream[i:i+3];fs=[CONS_FEATURES.get(p) for p,_,_ in tri]
        if all(fs) and len(set(f[0] for f in fs))==1 and len(set(f[1] for f in fs))<=2:
            out.append({"type":"repeated_articulatory_gesture","phonemes":[p for p,_,_ in tri],"words":sorted(set(w for _,_,w in tri))})
    for i in range(len(wl)-1):
        a=analyses[i];b=analyses[i+1]
        if a["phonemes"] and b["phonemes"]:
            pa=split_phoneme(a["phonemes"][-1])[0];pb=split_phoneme(b["phonemes"][0])[0]
            fa=CONS_FEATURES.get(pa);fb=CONS_FEATURES.get(pb)
            if fa and fb and fa[0]==fb[0]=="stop" and pa!=pb:
                out.append({"type":"stop_to_stop_boundary","between":[wl[i],wl[i+1]],"phonemes":[pa,pb]})
    seen=set();uniq=[]
    for x in out:
        k=json.dumps(x,sort_keys=True)
        if k not in seen:seen.add(k);uniq.append(x)
    cov=known_words/len(wl) if wl else 0.0
    return uniq,cov

def analyse(text,bpm=140):
    rows=[];covs=[]
    for i,line in enumerate([x for x in text.splitlines() if x.strip()],1):
        sy=line_syllables(line);sps=sy/(240/bpm);risk="high" if sps>6.5 else "medium" if sps>5 else "low"
        iss,cov=issues(line);covs.append(cov)
        rows.append({
            "line":i,"text":line,"syllables":sy,"syllables_per_second_if_one_bar":round(sps,3),
            "density_risk":risk,"phoneme_coverage":round(cov,4),
            "issues":iss if cov>0 else None,
            "phoneme_issue_status":"available" if cov>0 else "unavailable"
        })
    cov=sum(covs)/len(covs) if covs else 0.0
    return {
        "schema":"advanced-lyricism.articulation-audit.v2",
        "settings":{"bpm":bpm,"one_line_one_bar":True},
        "support_status":{
            "state":support_state(cov),"mean_line_phoneme_coverage":round(cov,4),"backend":pronunciation_backend(),
            "safe_claims":["density risk always","phoneme transition issues only where phoneme_coverage > 0"],
            "forbidden_claims":[] if cov>0 else ["no articulation issues detected"]
        },
        "lines":rows,
        "limits":["phoneme-transition screen, not a physiological model","actual articulation depends on accent, coarticulation, pocket and rehearsal"]
    }

def main():
    ap=argparse.ArgumentParser(description="Flag density and phoneme-transition articulation risks.")
    g=ap.add_mutually_exclusive_group();g.add_argument("-i","--input",type=Path);g.add_argument("-t","--text")
    ap.add_argument("--bpm",type=float,default=140);ap.add_argument("--pronunciation-json",type=Path);ap.add_argument("--summary",action="store_true",help="Emit support status and line risk counts only.");ap.add_argument("-o","--output",type=Path);a=ap.parse_args()
    if a.bpm<=0:
        print(json.dumps({"ok":False,"error":{"type":"input","message":"bpm must be > 0"}}));return 2
    if a.pronunciation_json: configure_pronunciation_overrides(a.pronunciation_json)
    d=analyse(read_text_arg(a.input,a.text),a.bpm)
    if a.summary:
        rc={k:sum(1 for x in d["lines"] if x["density_risk"]==k) for k in ("low","medium","high")};issues=sum(len(x["issues"] or []) for x in d["lines"])
        d={"schema":d["schema"],"settings":d["settings"],"support_status":d["support_status"],"summary":{"lines":len(d["lines"]),"density_risk_counts":rc,"phoneme_issues_detected":issues if d["support_status"]["state"]!="unavailable" else None},"limits":d["limits"]}
    s=json.dumps(d,ensure_ascii=False,indent=2)
    if a.output:a.output.write_text(s,encoding="utf-8")
    else:print(s)
    return 0
if __name__=="__main__":raise SystemExit(main())
