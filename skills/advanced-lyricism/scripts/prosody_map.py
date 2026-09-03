#!/usr/bin/env python3
"""Map syllable density, lexical stress and candidate metrical grids."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from lyric_utils import line_syllables,line_stress,read_text_arg,stress_coverage,support_state,configure_pronunciation_overrides,pronunciation_backend

def strength(slot,sub):
    spb=max(1,sub//4);pos=slot%spb;beat=slot//spb
    if pos==0:return 1.0 if beat in (0,2) else .9
    if spb%2==0 and pos==spb//2:return .6
    return .25

def fit(stress,sub,offset):
    if not stress:return {"cost":None,"assignments":[],"known_stress":0}
    space=sub/max(1,len(stress));rows=[];costs=[]
    for i,st in enumerate(stress):
        q=round(offset+i*space);bar=q//sub;slot=q%sub;w=strength(slot,sub)
        if st is None:
            cost=None
        else:
            cost=(1-w if st==1 else .65*(1-w) if st==2 else .55*w)
            costs.append(cost)
        rows.append({"syllable_index":i+1,"stress":st,"bar_offset":bar,"slot":slot,"metric_strength":round(w,3),"cost":round(cost,4) if cost is not None else None})
    return {"cost":round(sum(costs)/len(costs),4) if costs else None,"assignments":rows,"known_stress":len(costs)}

def analyse(text,bpm=140.,subdivision=16):
    ls=[];dens=[];all_stress=[]
    for n,line in enumerate([x for x in text.splitlines() if x.strip()],1):
        sy=line_syllables(line);st=line_stress(line);all_stress.extend(st)
        rawfits=[{"offset":o,**fit(st,subdivision,o)} for o in range(max(1,subdivision//4))]
        fits=sorted([x for x in rawfits if x["cost"] is not None],key=lambda x:x["cost"])
        cov=stress_coverage(st)
        # Grid rankings are withheld when less than half of syllable stress is known.
        ranked=fits[:3] if cov>=.5 else []
        clash=[i+1 for i in range(len(st)-1) if st[i] in (1,2) and st[i+1] in (1,2)]
        lapse=[i+1 for i in range(len(st)-2) if st[i:i+3]==[0,0,0]]
        dens.append(sy)
        ls.append({
            "line":n,"text":line,"syllables":sy,
            "syllables_per_second_if_one_bar":round(sy/(240/bpm),3),
            "stress":st,"stress_coverage":round(cov,4),
            "best_grid_projections":ranked,
            "projection_status":"available" if ranked else "unavailable_or_insufficient_coverage",
            "lexical_stress_clash_candidates":clash if cov>0 else None,
            "lexical_stress_lapse_candidates":lapse if cov>0 else None
        })
    dif=[abs(dens[i]-dens[i-1]) for i in range(1,len(dens))]
    cov=stress_coverage(all_stress)
    return {
        "schema":"advanced-lyricism.prosody-map.v2",
        "settings":{"bpm":bpm,"subdivision":subdivision,"assumption":"one supplied line = one planning bar"},
        "support_status":{
            "state":support_state(cov),"stress_coverage":round(cov,4),"backend":pronunciation_backend(),
            "safe_claims":["syllable density always","lexical-stress/grid projections only when line stress_coverage >= 0.5"],
            "forbidden_claims":[] if cov>=.5 else ["best stress-grid fit","stress clash/lapse absence"]
        },
        "summary":{"lines":len(ls),"mean_syllables":round(sum(dens)/len(dens),3) if dens else 0,
                   "max_adjacent_density_jump":max(dif) if dif else 0},
        "lines":ls,
        "limits":["Text cannot reveal actual pocket, swing, rubato, breath or performed syllable duration.",
                  "Grid projections are planning views; perceived meter is relational and may conflict with notation."]
    }

def main():
    ap=argparse.ArgumentParser(description="Project lyric stress/density onto candidate metric slots.")
    g=ap.add_mutually_exclusive_group();g.add_argument("-i","--input",type=Path);g.add_argument("-t","--text")
    ap.add_argument("--bpm",type=float,default=140);ap.add_argument("--subdivision",type=int,default=16,choices=[4,8,12,16,24,32])
    ap.add_argument("--pronunciation-json",type=Path);ap.add_argument("--summary",action="store_true",help="Emit support status, density summary and per-line coverage only.");ap.add_argument("-o","--output",type=Path);a=ap.parse_args()
    if a.bpm<=0:
        print(json.dumps({"ok":False,"error":{"type":"input","message":"bpm must be > 0"}}));return 2
    if a.pronunciation_json: configure_pronunciation_overrides(a.pronunciation_json)
    d=analyse(read_text_arg(a.input,a.text),a.bpm,a.subdivision)
    if a.summary:d={"schema":d["schema"],"settings":d["settings"],"support_status":d["support_status"],"summary":d["summary"],"lines":[{"line":x["line"],"syllables":x["syllables"],"syllables_per_second_if_one_bar":x["syllables_per_second_if_one_bar"],"stress_coverage":x["stress_coverage"],"projection_status":x["projection_status"]} for x in d["lines"]],"limits":d["limits"]}
    s=json.dumps(d,ensure_ascii=False,indent=2)
    if a.output:a.output.write_text(s,encoding="utf-8")
    else:print(s)
    return 0
if __name__=="__main__":raise SystemExit(main())
