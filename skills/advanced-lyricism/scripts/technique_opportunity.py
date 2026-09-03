#!/usr/bin/env python3
"""Locate enjambment, suspension, caesura, density, scheme and callback opportunities."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from lyric_utils import words,norm_word,FUNCTION_WORDS,line_syllables,terminal_word,read_text_arg,rhyme_signature
TERM=re.compile(r"[.!?;:][\"')\]]*$");PAUSE=re.compile(r"[,;:—–-]")
DET={"a","an","the","this","that","these","those","my","your","his","her","its","our","their"}
PREP={"of","to","in","on","at","from","with","without","into","onto","over","under","through","for","by","as"}
CONJ={"and","or","but","because","although","though","while","when","if","unless","so","yet"}
AUX={"is","am","are","was","were","be","been","being","do","does","did","have","has","had","can","could","will","would","shall","should","may","might","must"}
def c(x):return round(max(0,min(1,x)),3)
def opportunity(text):
    raw=[x for x in text.splitlines() if x.strip()];syl=[line_syllables(x) for x in raw];out=[]
    for i,line in enumerate(raw):
        ws=words(line);last=norm_word(ws[-1]) if ws else "";nxt=raw[i+1] if i+1<len(raw) else ""
        if nxt and not TERM.search(line.rstrip()):
            score=.46;ev=["no terminal punctuation at boundary"]
            if last in FUNCTION_WORDS:score+=.28;ev.append(f"ends on function word '{last}'")
            if last in DET|PREP|CONJ|AUX:score+=.14;ev.append("ending word predicts grammatical continuation")
            out.append({"line":i+1,"boundary_after_line":i+1,"technique":"enjambment","confidence":c(score),"signals":ev,
                        "operation":"test sonic closure here while syntax carries into the next bar"})
            if last in DET|PREP|CONJ:
                out.append({"line":i+1,"boundary_after_line":i+1,"technique":"suspension","confidence":c(score+.08),
                            "signals":[f"weak grammatical word '{last}' can withhold its complement"],
                            "operation":"audition a deliberate pause/bar turn before the demanded content word"})
        if len(ws)>=7:
            lo=max(2,int(len(ws)*.58));hi=min(len(ws)-1,int(len(ws)*.9)+1)
            cand=[{"after_token":j,"word":ws[j-1],"next_word":ws[j]} for j in range(lo,hi) if norm_word(ws[j-1]) in DET|PREP|CONJ|AUX]
            if cand:out.append({"line":i+1,"technique":"bar-line-suspension-placement","confidence":.72,
                                "signals":[f"{len(cand)} late-line grammatical hinge(s)"],"candidates":cand[:4],
                                "operation":"test moving the break onto a hinge while preserving the following content word as delayed resolution"})
        if PAUSE.search(line) and len(ws)>=5:
            out.append({"line":i+1,"technique":"caesura-or-breath","confidence":.58,
                        "signals":["existing clause boundary creates a timing hinge"],"operation":"audition a rest, breath, ad-lib pocket or pocket reset here"})
    if len(syl)>=4:
        if max(syl)-min(syl)<=2 and sum(syl)/len(syl)>=8:
            out.append({"section":[1,len(raw)],"technique":"density-contrast","confidence":.66,
                        "signals":[f"syllable counts are flat ({min(syl)}–{max(syl)} across {len(syl)} lines)"],
                        "operation":"test one deliberate gear change: compress, expand, pause, or change subdivision around a semantic turn"})
        for i in range(1,len(syl)):
            if abs(syl[i]-syl[i-1])>=5:
                out.append({"line":i+1,"technique":"gear-change-audit","confidence":.7,
                            "signals":[f"density changes from {syl[i-1]} to {syl[i]} syllables"],
                            "operation":"decide whether this acceleration/deceleration is intentional; if yes, mark the transition"})
    sigs=[rhyme_signature(terminal_word(x)).get("tail",[]) if terminal_word(x) else [] for x in raw]
    run=[i for i in range(1,len(sigs)) if sigs[i] and sigs[i-1] and sigs[i][:2]==sigs[i-1][:2]]
    if len(run)>=2:
        out.append({"section":[1,len(raw)],"technique":"scheme-displacement","confidence":.62,
                    "signals":[f"{len(run)+1} adjacent endings share a close rhyme-tail prefix"],
                    "operation":"test moving one expected end rhyme mid-bar, delaying it, or breaking the scheme before returning"})
    occ={}
    for i,line in enumerate(raw):
        for w in {norm_word(x) for x in words(line) if len(norm_word(x))>=5 and norm_word(x) not in FUNCTION_WORDS}:occ.setdefault(w,[]).append(i+1)
    for w,ls in sorted([(w,ls) for w,ls in occ.items() if len(ls)>=2 and max(ls)-min(ls)>=3],key=lambda x:(-len(x[1]),x[0]))[:8]:
        out.append({"lines":ls,"technique":"callback-or-motif-development","confidence":.55,"signals":[f"distinctive token '{w}' recurs"],
                    "operation":"if intentional, change one property on the return so repetition carries new consequence"})
    out=sorted(out,key=lambda x:(-x.get("confidence",0),x.get("line",999)))
    return {"schema":"advanced-lyricism.technique-opportunities.v1","summary":{"lines":len(raw),"opportunities":len(out)},"opportunities":out,
            "limits":["Returns heuristic craft affordances.","Syntax is approximated without a full parser.","Rewriting is handled by the connected transform and generation stages."]}
def main():
    ap=argparse.ArgumentParser(description="Flag plausible enjambment, suspension, caesura, density, scheme and callback opportunities.");g=ap.add_mutually_exclusive_group()
    g.add_argument("-i","--input",type=Path);g.add_argument("-t","--text");ap.add_argument("-o","--output",type=Path);a=ap.parse_args()
    s=json.dumps(opportunity(read_text_arg(a.input,a.text)),ensure_ascii=False,indent=2)
    if a.output:a.output.write_text(s,encoding="utf-8")
    else:print(s)
    return 0
if __name__=="__main__":raise SystemExit(main())
