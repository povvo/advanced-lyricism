#!/usr/bin/env python3
"""Map opening, internal and ending rhyme anchors."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from lyric_utils import words,analyze_word,sequence_similarity,read_text_arg,configure_pronunciation_overrides,support_state,pronunciation_backend

def choose_positions(line):
    ws=words(line)
    if not ws:return {}
    idxs={"opening":0,"mid":max(0,min(len(ws)-1,round((len(ws)-1)*.5))),"ending":len(ws)-1}
    out={}
    for label,i in idxs.items():
        a=analyze_word(ws[i])
        out[label]={
            "token_index":i+1,"word":ws[i],"rhyme_tail":a["rhyme_tail"],
            "stress":a["stress"],"source":a["source"],"comparable":bool(a["rhyme_tail"])
        }
    return out

def similarity(a,b):
    ta=a.get("rhyme_tail") or []; tb=b.get("rhyme_tail") or []
    if not ta or not tb:
        return None
    return round(sequence_similarity(ta,tb),4)

def analyse(text,threshold=.58):
    lines=[x for x in text.splitlines() if x.strip()]
    rows=[{"line":i+1,"text":line,"anchors":choose_positions(line)} for i,line in enumerate(lines)]
    links=[]; known_anchors=total_anchors=0
    for row in rows:
        for a in row["anchors"].values():
            total_anchors+=1;known_anchors+=int(a["comparable"])
    for a,b in zip(rows,rows[1:]):
        for pos in ("opening","mid","ending"):
            aa=a["anchors"].get(pos);bb=b["anchors"].get(pos)
            if not aa or not bb:continue
            s=similarity(aa,bb)
            links.append({
                "lines":[a["line"],b["line"]],"position":pos,"words":[aa["word"],bb["word"]],
                "comparable":s is not None,"similarity":s,"active":None if s is None else s>=threshold
            })
    active=[x for x in links if x["active"] is True]
    comparable=[x for x in links if x["comparable"]]
    bypos={p:sum(1 for x in active if x["position"]==p) for p in ("opening","mid","ending")}
    comp_bypos={p:sum(1 for x in comparable if x["position"]==p) for p in ("opening","mid","ending")}
    opp=[]
    for p,n in bypos.items():
        if len(rows)>=4 and comp_bypos[p]>=2 and n==0:
            opp.append({"technique":"positional-rhyme-development","position":p,
                        "operation":f"audition one recurring {p} sound anchor across two adjacent bars if it serves meaning"})
    cov=known_anchors/total_anchors if total_anchors else 0.0
    return {
        "schema":"advanced-lyricism.rhyme-grid.v2",
        "threshold":threshold,
        "support_status":{
            "state":support_state(cov),
            "anchor_pronunciation_coverage":round(cov,4),
            "backend":pronunciation_backend(),
            "safe_claims":["token positions always","phonological similarity only where comparable=true"],
            "forbidden_claims":["unknown tails are rhyme matches","absence of positional rhyme from non-comparable links"]
        },
        "lines":rows,
        "adjacent_position_links":links,
        "summary":{
            "active_links":len(active),"comparable_links":len(comparable),"unknown_links":len(links)-len(comparable),
            "active_by_position":bypos,"comparable_by_position":comp_bypos
        },
        "opportunities":opp,
        "limits":[
            "positions are token-proportion approximations, not beat-aligned coordinates",
            "accent and performed timing can strengthen or erase dictionary-based similarity"
        ]
    }

def main():
    ap=argparse.ArgumentParser(description="Audit opening/mid/ending rhyme relations across adjacent lines.")
    g=ap.add_mutually_exclusive_group();g.add_argument("-i","--input",type=Path);g.add_argument("-t","--text")
    ap.add_argument("--threshold",type=float,default=.58)
    ap.add_argument("--pronunciation-json",type=Path)
    ap.add_argument("--summary",action="store_true",help="Emit support status, aggregate link counts and opportunities only.")
    ap.add_argument("-o","--output",type=Path);a=ap.parse_args()
    if not 0<=a.threshold<=1:
        print(json.dumps({"ok":False,"error":{"type":"input","message":"threshold must be 0..1"}}));return 2
    if a.pronunciation_json: configure_pronunciation_overrides(a.pronunciation_json)
    d=analyse(read_text_arg(a.input,a.text),a.threshold)
    if a.summary:d={"schema":d["schema"],"threshold":d["threshold"],"support_status":d["support_status"],"summary":d["summary"],"opportunities":d["opportunities"],"limits":d["limits"]}
    s=json.dumps(d,ensure_ascii=False,indent=2)
    if a.output:a.output.write_text(s,encoding="utf-8")
    else:print(s)
    return 0
if __name__=="__main__":raise SystemExit(main())
