#!/usr/bin/env python3
"""Generate candidate metrical slot patterns for cadence exploration."""
from __future__ import annotations
import argparse,json,random,math
from pathlib import Path

FAMILIES={
 "straight16":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
 "eighths":[0,2,4,6,8,10,12,14],
 "offbeats":[2,6,10,14],
 "gallop":[0,2,3,4,6,7,8,10,11,12,14,15],
 "half-time":[0,2,4,6,8,10,12,14],
 "triplet12":[0,1,2,3,4,5,6,7,8,9,10,11],
 "syncopated":[0,3,5,6,8,11,13,14],
}
STRONG16={0:1.0,4:.9,8:1.0,12:.9,2:.6,6:.6,10:.6,14:.6}
STRONG12={0:1.0,3:.9,6:1.0,9:.9}

def resample_slots(base,source_slots,target_slots):
    if source_slots==target_slots:return list(base)
    return sorted(set(min(target_slots-1,round(x*target_slots/source_slots)) for x in base))

def fit_count(slots,count,total,rng,variation=.18):
    s=list(slots)
    if count<=0:return []
    if count<len(s):
        # preserve anchors, drop less central candidates with seeded jitter
        scored=[]
        strong=STRONG12 if total==12 else STRONG16
        for x in s:scored.append((strong.get(x,.35)+rng.uniform(-variation,variation),x))
        return sorted(x for _,x in sorted(scored,reverse=True)[:count])
    if count>len(s):
        pool=[x for x in range(total) if x not in s];rng.shuffle(pool);s+=pool[:max(0,count-len(s))]
    return sorted(s[:count])

def candidates(syllables:int,family:str,count:int,seed:int,pickup:bool):
    rng=random.Random(seed)
    fams=list(FAMILIES) if family=="auto" else [family]
    out=[]
    for i in range(count):
        f=fams[i%len(fams)] if family=="auto" else family
        total=12 if f=="triplet12" else 16
        base=FAMILIES[f]
        local=random.Random(seed+i*7919)
        target=fit_count(base,syllables,total,local)
        pickup_slots=[]
        if pickup and syllables>=2:
            # represent pickup separately: negative slots are previous-bar subdivisions
            pickup_slots=[-2,-1] if total==16 else [-1]
            target=fit_count(base,max(0,syllables-len(pickup_slots)),total,local)
        strong=STRONG12 if total==12 else STRONG16
        out.append({"id":i+1,"family":f,"grid_slots":total,"pickup_slots":pickup_slots,"syllable_slots":target,
                    "stress_anchor_candidates":[x for x in target if strong.get(x,0)>=.9],
                    "negative_space_slots":[x for x in range(total) if x not in target]})
    return {"schema":"advanced-lyricism.cadence-candidates.v1","syllables":syllables,"seed":seed,"candidates":out,
            "limits":["slot maps are planning geometries, not measured performance",
                      "triplet12 and straight16 use different subdivision spaces",
                      "lexical stress, syntax, breath, swing and actual beat events still need checking"]}

def main():
    ap=argparse.ArgumentParser(description="Generate reproducible cadence slot candidates for a target syllable count.")
    ap.add_argument("--syllables",type=int,required=True);ap.add_argument("--family",choices=["auto"]+list(FAMILIES),default="auto")
    ap.add_argument("-n","--count",type=int,default=8);ap.add_argument("--seed",type=int,default=0);ap.add_argument("--pickup",action="store_true")
    ap.add_argument("-o","--output",type=Path);a=ap.parse_args()
    if not 1<=a.syllables<=64 or not 1<=a.count<=100:
        print(json.dumps({"ok":False,"error":{"type":"input","message":"syllables must be 1..64 and count 1..100"}}));return 2
    d=candidates(a.syllables,a.family,a.count,a.seed,a.pickup);s=json.dumps(d,indent=2)
    if a.output:a.output.write_text(s,encoding="utf-8")
    else:print(s)
    return 0
if __name__=="__main__":raise SystemExit(main())
