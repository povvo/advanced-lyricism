#!/usr/bin/env python3
"""Generate reproducible bar-level parameter curves for lyric section planning."""
from __future__ import annotations
import argparse, json, math, random
from pathlib import Path

DEFAULT_DIMS=("density","tension","rhyme_density","image_distance","emotional_exposure")

def clamp(x): return max(0.0,min(1.0,float(x)))

def base_curve(shape:str,n:int,start:float,peak:float,end:float,rng:random.Random):
    if n<=1:return [clamp(end)]
    xs=[i/(n-1) for i in range(n)]
    if shape=="build":
        vals=[start+(peak-start)*(x**1.15) for x in xs]
    elif shape=="release":
        vals=[peak+(end-peak)*(x**1.15) for x in xs]
    elif shape=="arch":
        # piecewise asymmetric enough to keep a late peak
        p=.68
        vals=[start+(peak-start)*(x/p) if x<=p else peak+(end-peak)*((x-p)/(1-p)) for x in xs]
    elif shape=="wave":
        vals=[clamp((start+end)/2 + (peak-max(start,end))*math.sin(math.pi*x*2-math.pi/2)) for x in xs]
        lo=min(start,end); hi=peak
        vals=[lo+(hi-lo)*(0.5-0.5*math.cos(2*math.pi*x)) for x in xs]
    elif shape=="stair":
        thirds=[start,(start+peak)/2,peak,(peak+end)/2,end]
        vals=[thirds[min(4,int(x*5))] for x in xs]
    elif shape=="randomwalk":
        v=start; vals=[v]
        drift=(end-start)/(n-1)
        for _ in range(1,n):
            v=clamp(v+drift+rng.uniform(-.12,.12))
            vals.append(v)
        # softly land near requested end without erasing local path
        delta=end-vals[-1]
        vals=[clamp(v+delta*(i/(n-1))) for i,v in enumerate(vals)]
    else:
        raise ValueError(f"unknown shape {shape}")
    return [clamp(v) for v in vals]

def generate(bars:int,shape:str,dimensions:list[str],seed:int,start:float,peak:float,end:float,jitter:float):
    rng=random.Random(seed)
    curves={}
    for di,d in enumerate(dimensions):
        local=random.Random(seed*1009+di*9173+17)
        vals=base_curve(shape,bars,start,peak,end,local)
        if jitter:
            vals=[clamp(v+local.uniform(-jitter,jitter)) for v in vals]
        curves[d]=[round(v,4) for v in vals]
    rows=[]
    for i in range(bars):
        rows.append({"bar":i+1, **{d:curves[d][i] for d in dimensions}})
    return {
      "schema":"advanced-lyricism.arc-plan.v1",
      "bars":bars,"shape":shape,"seed":seed,
      "parameters":{"start":start,"peak":peak,"end":end,"jitter":jitter},
      "dimensions":dimensions,"curve":rows,
      "usage":[
        "Treat values as relative planning pressures, not quality scores.",
        "Isolate one dimension when diagnosing cause; combine dimensions only after the effect is legible.",
        "Use contrast and return rather than forcing every dimension to peak together."
      ]
    }

def main():
    ap=argparse.ArgumentParser(description="Generate deterministic bar-level craft parameter curves.")
    ap.add_argument("--bars",type=int,default=16)
    ap.add_argument("--shape",choices=["build","release","arch","wave","stair","randomwalk"],default="arch")
    ap.add_argument("--dimensions",default=",".join(DEFAULT_DIMS),help="Comma-separated planning dimensions.")
    ap.add_argument("--seed",type=int,default=0)
    ap.add_argument("--start",type=float,default=.25);ap.add_argument("--peak",type=float,default=.9);ap.add_argument("--end",type=float,default=.4)
    ap.add_argument("--jitter",type=float,default=0.0)
    ap.add_argument("-o","--output",type=Path)
    a=ap.parse_args()
    if not 1<=a.bars<=512 or any(not 0<=x<=1 for x in (a.start,a.peak,a.end,a.jitter)):
        print(json.dumps({"ok":False,"error":{"type":"input","message":"bars must be 1..512 and numeric parameters 0..1"}}));return 2
    dims=[x.strip() for x in a.dimensions.split(",") if x.strip()]
    if not dims:
        print(json.dumps({"ok":False,"error":{"type":"input","message":"at least one dimension required"}}));return 2
    d=generate(a.bars,a.shape,dims,a.seed,a.start,a.peak,a.end,a.jitter)
    s=json.dumps(d,ensure_ascii=False,indent=2)
    if a.output:a.output.write_text(s,encoding="utf-8")
    else:print(s)
    return 0
if __name__=="__main__":raise SystemExit(main())
