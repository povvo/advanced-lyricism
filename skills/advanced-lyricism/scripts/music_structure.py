#!/usr/bin/env python3
"""Derive inspectable phrase/boundary/repetition cues from Advanced Lyricism music JSON."""
from __future__ import annotations
import argparse,json,math,statistics
from pathlib import Path
from collections import defaultdict,Counter

KICKS={35,36}; SNARES={38,40}; HATS={42,44,46}

def jaccard(a,b):
    a=set(a);b=set(b)
    if not a and not b:return 1.0
    return len(a&b)/max(1,len(a|b))
def med(xs):return statistics.median(xs) if xs else None
def normdiff(a,b,scale):
    if a is None or b is None:return 0.0
    return min(1.0,abs(a-b)/scale)

def midi_structure(d):
    sub=int(d.get("timing",{}).get("analysis_subdivision",16))
    bars=defaultdict(list)
    for n in d.get("notes",[]):
        m=n.get("metric") or {};bar=m.get("bar")
        if bar is not None:bars[int(bar)].append(n)
    rows=[]
    for b in sorted(bars):
        ns=bars[b];pit=[n["pitch"] for n in ns if not n.get("is_drum")]
        slots=[int((n.get("metric") or {}).get("slot_in_bar",0)) for n in ns]
        drum=[n for n in ns if n.get("is_drum")]
        kicks=[int(n["metric"]["slot_in_bar"]) for n in drum if n.get("pitch") in KICKS and n.get("metric")]
        snares=[int(n["metric"]["slot_in_bar"]) for n in drum if n.get("pitch") in SNARES and n.get("metric")]
        hats=[int(n["metric"]["slot_in_bar"]) for n in drum if n.get("pitch") in HATS and n.get("metric")]
        # Weak-position proxy only when 16-slot bar; otherwise just omit.
        if sub==16 and slots:
            strong={0,4,8,12}; medium={2,6,10,14}
            weak=sum(1 for s in slots if s%16 not in strong|medium)
            sync=weak/len(slots)
        else:sync=None
        rows.append({"bar":b,"note_onsets":len(ns),"pitched_onsets":len(pit),"drum_onsets":len(drum),
                     "occupied_slots":sorted(set(slots)),"negative_space_slots":[x for x in range(sub) if x not in set(s%sub for s in slots)] if sub<=32 else [],
                     "pitch_median":med(pit),"pitch_min":min(pit) if pit else None,"pitch_max":max(pit) if pit else None,
                     "velocity_mean":round(statistics.fmean([n.get("velocity",0) for n in ns]),3) if ns else 0,
                     "kick_slots":sorted(set(kicks)),"snare_slots":sorted(set(snares)),"hat_slots":sorted(set(hats)),
                     "syncopation_proxy":round(sync,4) if sync is not None else None})
    boundaries=[]
    for a,b in zip(rows,rows[1:]):
        density=abs(a["note_onsets"]-b["note_onsets"])/max(1,a["note_onsets"],b["note_onsets"])
        reg=normdiff(a["pitch_median"],b["pitch_median"],12)
        pat=1-jaccard([x%sub for x in a["occupied_slots"]],[x%sub for x in b["occupied_slots"]])
        score=.45*density+.25*reg+.30*pat
        if score>=.38:
            boundaries.append({"before_bar":b["bar"],"score":round(score,4),
                               "signals":{"density_change":round(density,4),"register_change":round(reg,4),"onset_pattern_change":round(pat,4)}})
    repeats=[]
    for i,a in enumerate(rows):
        for b in rows[i+1:min(i+9,len(rows))]:
            sim=jaccard([x%sub for x in a["occupied_slots"]],[x%sub for x in b["occupied_slots"]])
            pd=normdiff(a["pitch_median"],b["pitch_median"],12)
            score=.7*sim+.3*(1-pd)
            if score>=.82:repeats.append({"bars":[a["bar"],b["bar"]],"similarity":round(score,4)})
    return {"schema":"advanced-lyricism.music-structure.v1","source_schema":d.get("schema"),"mode":"midi",
            "subdivision":sub,"bars":rows,"boundary_candidates":boundaries,"repetition_candidates":repeats[:100],
            "limits":["boundary/repetition scores are feature cues, not formal-analysis verdicts",
                      "syncopation proxy is descriptive occupancy on weak slots and does not model all metrical hearing"]}

def audio_structure(d,beats_per_bar=4):
    beats=d.get("beat_features",[]);rows=[]
    for i in range(0,len(beats),beats_per_bar):
        chunk=beats[i:i+beats_per_bar]
        if not chunk:continue
        rows.append({"bar":len(rows)+1,"beat_start":chunk[0]["beat"],"beat_end":chunk[-1]["beat"],
                     "start_seconds":chunk[0]["time"],"end_seconds":round(chunk[-1]["time"]+chunk[-1]["duration"],6),
                     "onset_strength_mean":round(statistics.fmean(x["onset_strength_mean"] for x in chunk),6),
                     "onset_strength_max":round(max(x["onset_strength_max"] for x in chunk),6),
                     "rms_mean":round(statistics.fmean(x["rms_mean"] for x in chunk),6),
                     "spectral_centroid_mean":round(statistics.fmean(x["spectral_centroid_mean"] for x in chunk),3)})
    boundaries=[]
    def rel(a,b,k):
        x=a[k];y=b[k];return abs(x-y)/max(1e-9,abs(x),abs(y))
    for a,b in zip(rows,rows[1:]):
        energy=rel(a,b,"rms_mean");onset=rel(a,b,"onset_strength_mean");timbre=min(1,abs(a["spectral_centroid_mean"]-b["spectral_centroid_mean"])/3000)
        score=.45*energy+.35*onset+.20*timbre
        if score>=.35:boundaries.append({"before_bar":b["bar"],"score":round(score,4),
                                         "signals":{"energy_change":round(energy,4),"onset_change":round(onset,4),"timbre_change":round(timbre,4)}})
    return {"schema":"advanced-lyricism.music-structure.v1","source_schema":d.get("schema"),"mode":"audio",
            "beats_per_planning_bar":beats_per_bar,"bars":rows,"boundary_candidates":boundaries,
            "limits":["audio bars are grouped from estimated beats and may be phase- or meter-wrong",
                      "half/double-time ambiguity remains; verify by ear or score"]}

def analyse(d,beats_per_bar=4):
    sc=d.get("schema","")
    if "music-event-ir" in sc:return midi_structure(d)
    if "audio-event-ir" in sc:return audio_structure(d,beats_per_bar)
    raise ValueError("input JSON must be advanced-lyricism.music-event-ir.v1 or audio-event-ir.v1")

def main():
    ap=argparse.ArgumentParser(description="Derive bar-level density, grouping, repetition and boundary cues from music-event JSON.")
    ap.add_argument("input",type=Path);ap.add_argument("--beats-per-bar",type=int,default=4);ap.add_argument("-o","--output",type=Path)
    a=ap.parse_args()
    try:d=json.loads(a.input.read_text(encoding="utf-8"));out=analyse(d,a.beats_per_bar)
    except Exception as e:
        print(json.dumps({"ok":False,"error":{"type":type(e).__name__,"message":str(e)}}));return 1
    s=json.dumps(out,ensure_ascii=False,indent=2)
    if a.output:a.output.write_text(s,encoding="utf-8")
    else:print(s)
    return 0
if __name__=="__main__":raise SystemExit(main())
