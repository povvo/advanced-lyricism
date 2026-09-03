#!/usr/bin/env python3
"""Map words to syllables, stress and pronunciation candidates."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from lyric_utils import words,analyze_word,read_text_arg,pronunciation_backend,configure_pronunciation_overrides,support_state

def analyse(text):
    lines=[];tot=known=syl=0
    sources={}
    for i,line in enumerate(text.splitlines(),1):
        toks=[]
        for w in words(line):
            a=analyze_word(w);tot+=1;syl+=a["syllables"]
            ok=bool(a["phonemes"]); known+=int(ok); sources[a["source"]]=sources.get(a["source"],0)+1
            toks.append(a)
        if toks:
            stress="".join(t["stress"] or "?"*t["syllables"] for t in toks)
            lines.append({"line":i,"text":line,"tokens":toks,"syllables":sum(t["syllables"] for t in toks),"stress":stress})
    cov=known/tot if tot else 0.0
    state=support_state(cov)
    return {
        "schema":"advanced-lyricism.phoneme-map.v2",
        "support_status":{
            "state":state,
            "dictionary_coverage":round(cov,4),
            "backend":pronunciation_backend(),
            "safe_claims":["syllable counts for all tokens","phonemes/stress only for dictionary/override-covered tokens"],
            "forbidden_claims":[] if state=="full" else ["absence of rhyme or stress pattern for uncovered tokens"]
        },
        "summary":{"tokens":tot,"syllables":syl,"dictionary_tokens":known,"heuristic_tokens":tot-known,"sources":sources},
        "lines":lines,
        "limits":[
            "CMUdict is primarily General American English; supplied/local pronunciation outranks dictionary output.",
            "unknown words get syllable heuristics but no invented phonemes/stress."
        ]
    }

def main():
    ap=argparse.ArgumentParser(description="Emit phoneme/stress/syllable JSON for lyric text.")
    g=ap.add_mutually_exclusive_group();g.add_argument("-i","--input",type=Path);g.add_argument("-t","--text")
    ap.add_argument("--pronunciation-json",type=Path,help="Optional word->ARPABET override map.")
    ap.add_argument("--summary",action="store_true",help="Emit only support status and aggregate counts.")
    ap.add_argument("-o","--output",type=Path);a=ap.parse_args()
    if a.pronunciation_json: configure_pronunciation_overrides(a.pronunciation_json)
    d=analyse(read_text_arg(a.input,a.text))
    if a.summary:d={"schema":d["schema"],"support_status":d["support_status"],"summary":d["summary"],"limits":d["limits"]}
    s=json.dumps(d,ensure_ascii=False,indent=2)
    if a.output:a.output.write_text(s,encoding="utf-8")
    else:print(s)
    return 0
if __name__=="__main__":raise SystemExit(main())
