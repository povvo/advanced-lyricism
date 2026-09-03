#!/usr/bin/env python3
"""Parse Advanced Lyricism delivery notation into structured performance events."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from lyric_utils import read_text_arg, words, line_syllables

TOKEN_PATTERNS=[
 ("breath",re.compile(r"//|\(B\)",re.I)),
 ("pause",re.compile(r"\.\.\.|…+")),
 ("pitch_slide",re.compile(r"~")),
 ("pitch_direction",re.compile(r"[↑↓]")),
 ("tone_or_flow",re.compile(r"\[([^\]]+)\]")),
 ("adlib",re.compile(r"\((?!B\))([^()\n]+)\)",re.I)),
 ("sustain",re.compile(r"_+")),
]
CAP_RE=re.compile(r"\b[A-Z][A-Z0-9'’-]{1,}\b")

def parse_line(line:str,index:int):
    events=[]
    for typ,pat in TOKEN_PATTERNS:
        for m in pat.finditer(line):
            ev={"type":typ,"start":m.start(),"end":m.end(),"surface":m.group(0)}
            if m.lastindex:ev["value"]=m.group(1)
            events.append(ev)
    for m in CAP_RE.finditer(line):
        events.append({"type":"emphasis","start":m.start(),"end":m.end(),"surface":m.group(0),"value":m.group(0)})
    events.sort(key=lambda e:(e["start"],e["end"],e["type"]))
    syll=line_syllables(re.sub(r"\[[^\]]+\]|\([^)]*\)|//|[~↑↓_]|\.{3,}|…+"," ",line))
    breaths=sum(e["type"]=="breath" for e in events)
    return {"line":index,"text":line,"syllables_estimate":syll,"events":events,"breaths":breaths,
            "has_pitch_instruction":any(e["type"] in {"pitch_slide","pitch_direction"} for e in events)}

def parse(text:str):
    rows=[parse_line(line,i) for i,line in enumerate([x for x in text.splitlines() if x.strip()],1)]
    total_syl=sum(x["syllables_estimate"] for x in rows)
    breaths=sum(x["breaths"] for x in rows)
    marked=sum(len(x["events"]) for x in rows)
    no_breath=[x["line"] for x in rows if x["syllables_estimate"]>=18 and not x["breaths"]]
    return {
      "schema":"advanced-lyricism.delivery-ir.v1",
      "summary":{"lines":len(rows),"syllables_estimate":total_syl,"events":marked,"breaths":breaths,
                 "dense_lines_without_marked_breath":no_breath},
      "lines":rows,
      "legend":{"//":"breath","(B)":"breath","CAPS":"emphasis","(...)":"ad-lib","...":"pause","~":"pitch slide",
                "↑/↓":"pitch direction","[label]":"tone/flow instruction","_":"sustain"},
      "limits":["notation describes intended performance, not measured performance",
                "capitalisation can be orthographic rather than emphatic; review flagged events in context"]
    }

def main():
    ap=argparse.ArgumentParser(description="Parse breath, emphasis, ad-lib, pause, pitch, tone and sustain notation into JSON.")
    g=ap.add_mutually_exclusive_group()
    g.add_argument("-i","--input",type=Path);g.add_argument("-t","--text")
    ap.add_argument("-o","--output",type=Path)
    a=ap.parse_args()
    d=parse(read_text_arg(a.input,a.text))
    s=json.dumps(d,ensure_ascii=False,indent=2)
    if a.output:a.output.write_text(s,encoding="utf-8")
    else:print(s)
    return 0
if __name__=="__main__":raise SystemExit(main())
