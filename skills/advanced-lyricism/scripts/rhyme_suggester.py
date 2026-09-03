#!/usr/bin/env python3
"""Generate pronunciation-based perfect and slant rhyme candidates."""
from __future__ import annotations
import argparse,json,re,collections
from pathlib import Path
from lyric_utils import (
    cmu,pronunciations,rhyme_tail,sequence_similarity,syllable_count_pron,stress_pattern,
    norm_word,analyze_word,split_phoneme,ARPABET_VOWELS,configure_pronunciation_overrides,
    pronunciation_backend
)

def nuclei(pron):
    return [split_phoneme(p)[0] for p in rhyme_tail(pron) if split_phoneme(p)[0] in ARPABET_VOWELS]

def raw_score(tp,cp):
    sim=sequence_similarity(rhyme_tail(tp),rhyme_tail(cp));ts=stress_pattern(tp);cs=stress_pattern(cp)
    sb=1 if ts==cs else .75 if ts and cs and ts[-1:]==cs[-1:] else .5
    sylpen=abs(syllable_count_pron(tp)-syllable_count_pron(cp))*.06
    return max(0,min(1,sim*.82+sb*.18-sylpen))

def relation(tp,cp,score):
    tt=[split_phoneme(x)[0] for x in rhyme_tail(tp)];ct=[split_phoneme(x)[0] for x in rhyme_tail(cp)]
    if tt and tt==ct:return "exact-tail"
    if nuclei(tp) and nuclei(tp)==nuclei(cp):return "vowel-led"
    if score>=.72:return "close-slant"
    return "wide-slant"

def suffix_key(w,n=3):
    w=re.sub(r"[^a-z]","",norm_word(w));return w[-n:] if len(w)>=n else w

def suggest(target,limit=30,wordlist=None,min_score=.42,max_per_suffix=2):
    ds=cmu();tps=pronunciations(target)
    if not ds or not tps:
        return {
            "schema":"advanced-lyricism.rhyme-suggestions.v3",
            "target":target,
            "support_status":{"state":"blocked","backend":pronunciation_backend()},
            "error":"pronunciation dictionary/target pronunciation unavailable",
            "candidates":[],
            "limits":["Do not substitute orthographic suffix guessing for unavailable phonological analysis."]
        }
    ws=[x.strip().split()[0] for x in Path(wordlist).read_text(errors="ignore").splitlines() if x.strip()] if wordlist else ds.keys()
    target_a=analyze_word(target);best={}
    for w in ws:
        nw=norm_word(w)
        if nw==norm_word(target) or not re.search("[A-Za-z]",nw):continue
        ps=pronunciations(nw)
        if not ps:continue
        pairs=[(raw_score(tp,cp),tp,cp) for tp in tps for cp in ps]
        s,tp,cp=max(pairs,key=lambda x:x[0])
        if s>=min_score:
            a=analyze_word(nw)
            best[nw]={"word":nw,"score":round(s,4),"relation":relation(tp,cp,s),"phonemes":a["phonemes"],
                      "stress":a["stress"],"syllables":a["syllables"],"rhyme_tail":a["rhyme_tail"],
                      "orthographic_suffix":suffix_key(nw)}
    raw=sorted(best.values(),key=lambda x:(-x["score"],abs(x["syllables"]-target_a["syllables"]),x["word"]))
    selected=[];counts=collections.Counter();target_suffix=suffix_key(target)
    buckets=collections.defaultdict(list)
    for x in raw:buckets[x["relation"]].append(x)
    order=["exact-tail","vowel-led","close-slant","wide-slant"]
    while len(selected)<limit and any(buckets.values()):
        progressed=False
        for rel in order:
            bucket=buckets[rel]
            while bucket:
                x=bucket.pop(0);sk=x["orthographic_suffix"]
                cap=max_per_suffix if sk!=target_suffix else max(1,max_per_suffix)
                if counts[sk]<cap:
                    selected.append(x);counts[sk]+=1;progressed=True;break
            if len(selected)>=limit:break
        if not progressed:break
    if len(selected)<limit:
        seen={x["word"] for x in selected}
        for x in raw:
            if x["word"] not in seen:
                selected.append(x);seen.add(x["word"])
                if len(selected)>=limit:break
    for i,x in enumerate(raw,1):x["raw_rank"]=i
    return {
        "schema":"advanced-lyricism.rhyme-suggestions.v3","target":target,
        "support_status":{"state":"full","backend":pronunciation_backend(),
                           "safe_claims":["dictionary-backed candidate similarity for combination with semantic, voice and performance selection"]},
        "target_pronunciations":tps,
        "settings":{"min_score":min_score,"max_per_orthographic_suffix":max_per_suffix},
        "candidates":selected[:limit],"raw_top":raw[:min(limit,20)],
        "limits":["Returns phonetic rhyme candidates for integrated selection",
                  "Combine CMUdict coverage with supplied/local pronunciation",
                  "Orthographic suffix diversity broadens the search while repeated morphology remains available"]
    }

def main():
    ap=argparse.ArgumentParser(description="Return diversified exact/slant rhyme candidates by phoneme tail, stress and syllable shape.")
    ap.add_argument("target");ap.add_argument("-n","--limit",type=int,default=30)
    ap.add_argument("--wordlist",type=Path);ap.add_argument("--min-score",type=float,default=.42)
    ap.add_argument("--max-per-suffix",type=int,default=2);ap.add_argument("--pronunciation-json",type=Path)
    ap.add_argument("-o","--output",type=Path);a=ap.parse_args()
    if not 1<=a.limit<=500 or not 1<=a.max_per_suffix<=100 or not 0<=a.min_score<=1:
        print(json.dumps({"ok":False,"error":{"type":"input","message":"limit/max-per-suffix must be positive and min-score 0..1"}}));return 2
    if a.pronunciation_json: configure_pronunciation_overrides(a.pronunciation_json)
    d=suggest(a.target,a.limit,a.wordlist,a.min_score,a.max_per_suffix);s=json.dumps(d,ensure_ascii=False,indent=2)
    if a.output:a.output.write_text(s,encoding="utf-8")
    else:print(s)
    return 3 if d.get("support_status",{}).get("state")=="blocked" else 0
if __name__=="__main__":raise SystemExit(main())
