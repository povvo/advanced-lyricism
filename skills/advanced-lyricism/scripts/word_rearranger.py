#!/usr/bin/env python3
"""Rearrange supplied words and clauses into controlled variants."""
from __future__ import annotations
import argparse,json,random,re
from pathlib import Path
from lyric_utils import words,read_text_arg
BOUND=re.compile(r"(?<=[,;:—–-])\s+|\s+(?=\b(?:but|and|because|while|when|if|though|although|so|yet)\b)",re.I)
def chunks(line):
    c=[x.strip() for x in BOUND.split(line) if x.strip()]
    return c if len(c)>1 else [line.strip()]
def variants(line,n=8,seed=0,lock_end=True):
    rng=random.Random(seed);cs=chunks(line);out=[];seen={line.strip()}
    def add(mode,parts):
        v=" ".join(str(x).strip() for x in parts if str(x).strip());src=words(line);dst=words(v)
        if lock_end and src and dst and dst[-1].lower()!=src[-1].lower():return
        if v and v not in seen:seen.add(v);out.append({"mode":mode,"text":v})
    if len(cs)>1:
        add("reverse-clauses",reversed(cs))
        for k in range(1,len(cs)):add(f"rotate-{k}",cs[k:]+cs[:k])
        for _ in range(max(12,n*3)):
            p=cs[:];rng.shuffle(p);add("seeded-clause-permutation",p)
            if len(out)>=n:break
    ws=line.split()
    if len(out)<n and len(ws)>=5:
        tail=[ws[-1]] if lock_end else [];core=ws[:-1] if lock_end else ws;third=max(1,len(core)//3)
        b=[core[:third],core[third:2*third],core[2*third:]]
        for order in ([1,0,2],[2,0,1],[0,2,1]):add("block-reorder",[" ".join(b[i]) for i in order]+tail)
    return out[:n]
def main():
    ap=argparse.ArgumentParser(description="Generate constrained clause/block rearrangements while optionally preserving final rhyme word.");g=ap.add_mutually_exclusive_group()
    g.add_argument("-i","--input",type=Path);g.add_argument("-t","--text");ap.add_argument("-n","--count",type=int,default=8);ap.add_argument("--seed",type=int,default=0);ap.add_argument("--unlock-end",action="store_true");ap.add_argument("-o","--output",type=Path);a=ap.parse_args()
    rows=[{"line":i,"source":line,"variants":variants(line,a.count,a.seed+i,not a.unlock_end)} for i,line in enumerate([x for x in read_text_arg(a.input,a.text).splitlines() if x.strip()],1)]
    d={"schema":"advanced-lyricism.word-rearrangements.v1","settings":{"seed":a.seed,"lock_end":not a.unlock_end},"lines":rows,
       "limits":["variants preserve source material but may alter grammar, emphasis or meaning; evaluate before use"]}
    s=json.dumps(d,ensure_ascii=False,indent=2)
    if a.output:a.output.write_text(s,encoding="utf-8")
    else:print(s)
    return 0
if __name__=="__main__":raise SystemExit(main())
