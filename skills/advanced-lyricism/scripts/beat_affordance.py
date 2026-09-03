#!/usr/bin/env python3
"""Pair lyric lines with musical bar cues to expose candidate stress/space affordances."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from lyric_utils import line_syllables,line_stress,read_text_arg

def analyse(text,structure,start_bar=1):
    lines=[x for x in text.splitlines() if x.strip()]
    bars={int(x["bar"]):x for x in structure.get("bars",[]) if "bar" in x}
    rows=[]
    for i,line in enumerate(lines):
        b=start_bar+i;m=bars.get(b,{})
        sy=line_syllables(line);stress=line_stress(line)
        row={"line":i+1,"bar":b,"text":line,"syllables":sy,
             "lexical_primary_stresses":sum(1 for x in stress if x==1)}
        if structure.get("mode")=="midi":
            anchors=sorted(set((m.get("kick_slots") or [])+(m.get("snare_slots") or [])))
            row.update({"candidate_percussive_anchor_slots":anchors,
                        "candidate_negative_space_slots":m.get("negative_space_slots",[]),
                        "instrument_onset_density":m.get("note_onsets"),
                        "note":"Audition stressed content words near anchors; audition breaths/holds/ad-libs in negative space. Do not force one-to-one alignment."})
        elif structure.get("mode")=="audio":
            row.update({"beat_energy":m.get("rms_mean"),"onset_strength":m.get("onset_strength_mean"),
                        "note":"Use energy/onset change as a section-pressure signal; exact syllable placement requires listening or symbolic timing."})
        rows.append(row)
    return {"schema":"advanced-lyricism.beat-affordance.v1","music_mode":structure.get("mode"),"start_bar":start_bar,"rows":rows,
            "limits":["sequential line-to-bar pairing is a planning assumption","musical space does not imply vocal space in a finished mix",
                      "agent must audition cadence and preserve natural language stress"]}

def main():
    ap=argparse.ArgumentParser(description="Map lyric lines to candidate musical anchors/negative space from music-structure JSON.")
    ap.add_argument("structure",type=Path);g=ap.add_mutually_exclusive_group();g.add_argument("-i","--input",type=Path);g.add_argument("-t","--text")
    ap.add_argument("--start-bar",type=int,default=1);ap.add_argument("-o","--output",type=Path);a=ap.parse_args()
    try:s=json.loads(a.structure.read_text(encoding="utf-8"));d=analyse(read_text_arg(a.input,a.text),s,a.start_bar)
    except Exception as e:
        print(json.dumps({"ok":False,"error":{"type":type(e).__name__,"message":str(e)}}));return 1
    out=json.dumps(d,ensure_ascii=False,indent=2)
    if a.output:a.output.write_text(out,encoding="utf-8")
    else:print(out)
    return 0
if __name__=="__main__":raise SystemExit(main())
