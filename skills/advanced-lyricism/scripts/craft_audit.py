#!/usr/bin/env python3
"""Audit lexical, density, repetition, lineation and phonological features.

Unavailable phonological measurements are NULL/UNKNOWN, never encoded as zero.
"""
from __future__ import annotations
import argparse,json,re,statistics,sys
from collections import Counter
from pathlib import Path
from lyric_utils import (
    words,analyze_word,sequence_similarity,pronunciation_backend,support_state,
    configure_pronunciation_overrides
)

def content_lines(text):
    out=[]
    for raw in text.splitlines():
        s=raw.strip()
        if not s: continue
        if re.fullmatch(r"[\[(].*[\])]",s): continue
        out.append(s)
    return out

def scheme_for(end_words):
    labels=[];families=[];alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    known_end=0
    for word in end_words:
        a=analyze_word(word);tail=a["rhyme_tail"]
        if not tail:
            labels.append("?");continue
        known_end+=1
        best_i=None;best_s=0.0
        for i,fam in enumerate(families):
            s=sequence_similarity(tail,fam["tail"])
            if s>best_s:best_i,best_s=i,s
        if best_i is not None and best_s>=.58:
            labels.append(families[best_i]["label"])
            families[best_i]["words"].append(word);families[best_i]["members"]+=1
            families[best_i]["similarities"].append(round(best_s,3))
        else:
            label=alphabet[len(families)] if len(families)<len(alphabet) else f"R{len(families)+1}"
            families.append({"label":label,"tail":tail,"words":[word],"members":1,"similarities":[]})
            labels.append(label)
    clean=[]
    for fam in families:
        clean.append({
            "label":fam["label"],"tail":" ".join(fam["tail"]),"members":fam["members"],"words":fam["words"],
            "mean_match":round(statistics.mean(fam["similarities"]),3) if fam["similarities"] else 1.0
        })
    family_members=sum(f["members"] for f in clean if f["members"]>=2)
    return labels,clean,known_end,family_members

def internal_echoes(line_words):
    tails=[]
    for w in line_words:
        a=analyze_word(w)
        if a["rhyme_tail"]:tails.append((w,a["rhyme_tail"]))
    comparable=0;echoes=0
    for i in range(len(tails)):
        for j in range(i+1,len(tails)):
            if tails[i][0].lower()==tails[j][0].lower():continue
            comparable+=1
            if sequence_similarity(tails[i][1],tails[j][1])>=.72:echoes+=1
    return echoes,comparable

def analyse(text,bpm=None):
    lines=content_lines(text)
    token_lines=[words(line) for line in lines]
    analyses=[[analyze_word(w) for w in row] for row in token_lines]
    all_a=[a for row in analyses for a in row]
    all_words=[a["normalized"] for a in all_a]
    syllable_rows=[sum(a["syllables"] for a in row) for row in analyses]
    known=sum(bool(a["phonemes"]) for a in all_a); total=len(all_a)
    coverage=known/total if total else 0.0

    end_words=[row[-1] for row in token_lines if row]
    scheme,families,known_end,family_members=scheme_for(end_words)
    end_cov=known_end/len(end_words) if end_words else 0.0
    repeated_end={k:v for k,v in Counter(w.lower() for w in end_words).items() if v>1}

    internal_rows=[];echo_total=0;comp_total=0
    for row in token_lines:
        e,c=internal_echoes(row[:-1]) if len(row)>2 else (0,0)
        internal_rows.append({"echo_pairs":e if c else None,"comparable_pairs":c})
        echo_total+=e;comp_total+=c

    punctuation_end=sum(1 for line in lines if re.search(r"[.!?;:]$",line))
    vocab=set(all_words)
    phon_state=support_state(coverage)

    result={
        "schema":"advanced-lyricism.craft-audit.v2",
        "support_status":{
            "state":phon_state,
            "pronunciation_coverage":round(coverage,4),
            "backend":pronunciation_backend(),
            "safe_claims":[
                "line/word counts","lexical diversity","syllable-density estimates",
                "repeated literal end words","terminal punctuation/lineation proxies"
            ] + (["dictionary-covered rhyme families/internal echoes"] if known else []),
            "forbidden_claims":[] if phon_state=="full" else [
                "zero rhyme-family coverage means no audible rhyme",
                "zero internal echoes means no internal rhyme",
                "unknown scheme positions are non-rhymes"
            ]
        },
        "lines":len(lines),"words":len(all_words),"unique_words":len(vocab),
        "lexical_diversity":round(len(vocab)/len(all_words),3) if all_words else 0.0,
        "syllables":{
            "per_line":syllable_rows,
            "mean":round(statistics.mean(syllable_rows),2) if syllable_rows else 0.0,
            "min":min(syllable_rows) if syllable_rows else 0,
            "max":max(syllable_rows) if syllable_rows else 0,
            "stdev":round(statistics.pstdev(syllable_rows),2) if len(syllable_rows)>1 else 0.0,
            "coefficient_of_variation":round(statistics.pstdev(syllable_rows)/statistics.mean(syllable_rows),3)
                if len(syllable_rows)>1 and statistics.mean(syllable_rows) else 0.0
        },
        "pronunciation":{
            "known_tokens":known,"heuristic_tokens":total-known,"coverage":round(coverage,3),
            "backend":pronunciation_backend()
        },
        "end_rhyme":{
            "end_words":end_words,
            "scheme":" ".join(scheme),
            "families":families,
            "known_end_words":known_end,
            "endword_pronunciation_coverage":round(end_cov,3),
            "family_coverage_of_known_endwords":round(family_members/known_end,3) if known_end else None,
            "family_coverage_of_all_endwords":round(family_members/len(end_words),3) if end_words and known_end else None,
            "repeated_end_words":repeated_end
        },
        "internal_sound":{
            "per_line":internal_rows,
            "comparable_pairs":comp_total,
            "total_echo_pairs":echo_total if comp_total else None,
            "echo_pairs_per_100_words":round(100*echo_total/len(all_words),2) if comp_total and all_words else None,
            "status":"available" if comp_total else "unavailable"
        },
        "lineation":{
            "terminal_punctuation_ratio":round(punctuation_end/len(lines),3) if lines else 0.0,
            "enjambment_like_ratio":round((len(lines)-punctuation_end)/len(lines),3) if lines else 0.0,
            "warning":"Line-end punctuation is only a coarse lineation proxy; use technique_opportunity for syntax-aware heuristics."
        },
        "integrated_craft_dimensions":[
            "semantic specificity and freshness","narrative causality, agency, and consequence",
            "voice and register credibility","reference accuracy and cultural fit",
            "beat fit, microtiming, stress shifts, and breath under performance"
        ]
    }
    if bpm:
        bar_seconds=240.0/bpm;mean_syl=result["syllables"]["mean"]
        result["tempo_context"]={
            "bpm":bpm,"four_four_bar_seconds":round(bar_seconds,3),
            "text_only_mean_syllables_per_second_if_one_line_per_bar":round(mean_syl/bar_seconds,2) if bar_seconds else None,
            "warning":"One-line-per-bar is a diagnostic assumption, not a performance fact."
        }
    return result

def markdown_report(d):
    s=d["syllables"];r=d["end_rhyme"];p=d["pronunciation"];i=d["internal_sound"]
    fam=r["family_coverage_of_known_endwords"]
    echo=i["total_echo_pairs"]
    out=[
        "# Craft audit",
        f"- Support state: {d['support_status']['state']} | pronunciation coverage: {p['coverage']}",
        f"- Lines: {d['lines']} | Words: {d['words']} | Lexical diversity: {d['lexical_diversity']}",
        f"- Syllables/line: mean {s['mean']}, range {s['min']}–{s['max']}, stdev {s['stdev']}",
        f"- End-rhyme scheme: {r['scheme'] or '—'}",
        f"- Rhyme-family coverage (known endings only): {fam if fam is not None else 'unavailable'}",
        f"- Internal sound echoes: {echo if echo is not None else 'unavailable'}",
        f"- Enjambment-like line endings: {d['lineation']['enjambment_like_ratio']}",
    ]
    if r["repeated_end_words"]:
        out.append("- Repeated literal end words: "+", ".join(f"{k}×{v}" for k,v in r["repeated_end_words"].items()))
    out += ["","Integrate these craft dimensions: "+"; ".join(d["integrated_craft_dimensions"])+"."]
    return "\n".join(out)

def main():
    ap=argparse.ArgumentParser(description="Audit lexical, density, repetition, lineation and phonological features.")
    src=ap.add_mutually_exclusive_group();src.add_argument("path",nargs="?");src.add_argument("--text")
    ap.add_argument("--bpm",type=float);ap.add_argument("--format",choices=["json","markdown"],default="json")
    ap.add_argument("--pronunciation-json",type=Path)
    a=ap.parse_args()
    if a.pronunciation_json: configure_pronunciation_overrides(a.pronunciation_json)
    if a.text is not None:text=a.text
    elif a.path:text=Path(a.path).read_text(encoding="utf-8")
    else:text=sys.stdin.read()
    d=analyse(text,a.bpm)
    print(markdown_report(d) if a.format=="markdown" else json.dumps(d,indent=2,ensure_ascii=False))
    return 0

if __name__=="__main__":raise SystemExit(main())
