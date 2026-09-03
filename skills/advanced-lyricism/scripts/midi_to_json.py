#!/usr/bin/env python3
"""Convert Standard MIDI Files into JSON with raw and derived timing."""
from __future__ import annotations
import argparse,json,os,math,sys
from pathlib import Path
DEFAULT_TEMPO=500000
def req():
    disabled={x.strip().lower() for x in os.environ.get("ADVANCED_LYRICISM_DISABLE_PROVIDERS","").split(",") if x.strip()}
    first=None
    if "mido" not in disabled:
        try:
            import mido
            return mido
        except Exception as e:
            first=e
    else:
        first=RuntimeError("installed mido disabled for runtime test")
    try:
        from vendor import mido
        return mido
    except Exception as second:
        print(json.dumps({"ok":False,"error":{"type":"dependency","message":"MIDI parser unavailable","detail":{"installed_mido":str(first),"bundled_mido":str(second)}}}))
        raise SystemExit(3)
def absmsgs(track):
    t=0
    for i,m in enumerate(track):
        t+=int(m.time);yield t,i,m
def maps(mid,mido):
    tempo=[{"tick":0,"tempo":DEFAULT_TEMPO,"bpm":float(mido.tempo2bpm(DEFAULT_TEMPO))}]
    ts=[{"tick":0,"numerator":4,"denominator":4}]
    key=[]
    for ti,tr in enumerate(mid.tracks):
        for t,_,m in absmsgs(tr):
            if m.type=="set_tempo":tempo.append({"tick":t,"tempo":int(m.tempo),"bpm":float(mido.tempo2bpm(m.tempo)),"track":ti})
            elif m.type=="time_signature":ts.append({"tick":t,"numerator":m.numerator,"denominator":m.denominator,"track":ti})
            elif m.type=="key_signature":key.append({"tick":t,"key":m.key,"track":ti})
    def dedup(xs):
        d={}
        for x in sorted(xs,key=lambda z:z["tick"]):d[x["tick"]]=x
        return [d[k] for k in sorted(d)]
    return dedup(tempo),dedup(ts),sorted(key,key=lambda x:x["tick"])
def t2s(t,tempo,ppq):
    sec=0.;prev=0;cur=DEFAULT_TEMPO
    for e in tempo:
        et=e["tick"]
        if et<=0:cur=e["tempo"];continue
        if et>=t:break
        sec+=(et-prev)*cur/1e6/ppq;prev=et;cur=e["tempo"]
    return sec+(t-prev)*cur/1e6/ppq
def segs(ts,ppq):
    out=[];gbar=1
    for i,e in enumerate(ts):
        start=e["tick"];tpb=ppq*4/e["denominator"];tpbar=tpb*e["numerator"]
        if out:
            p=out[-1];dur=start-p["start_tick"];p["end_tick"]=start
            gbar=p["global_bar_start"]+max(1,math.ceil(dur/p["ticks_per_bar"]-1e-12))
        out.append({"index":i,"start_tick":start,"end_tick":None,"numerator":e["numerator"],"denominator":e["denominator"],
                    "ticks_per_beat":tpb,"ticks_per_bar":tpbar,"global_bar_start":gbar})
    return out
def metric(t,segs,sub):
    s=segs[0]
    for x in segs:
        if x["start_tick"]<=t:s=x
        else:break
    local=max(0,t-s["start_tick"]);b0=int(local//s["ticks_per_bar"]);inside=local-b0*s["ticks_per_bar"]
    beat0=int(inside//s["ticks_per_beat"]);frac=inside/s["ticks_per_beat"]-beat0;spb=max(1,round(sub/4))
    slot=round(frac*spb)
    if slot>=spb:slot=0;beat0+=1
    return {"time_signature_segment":s["index"],"bar":s["global_bar_start"]+b0,"beat":beat0+1,"beat_fraction":round(frac,6),
            "subdivision":sub,"slot_in_beat":slot,"slot_in_bar":beat0*spb+slot}
def note_name(p):
    n=["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"];return f"{n[p%12]}{p//12-1}"
def convert(path,subdivision=16,include_messages=False):
    mido=req();mid=mido.MidiFile(path);tempo,ts,key=maps(mid,mido);sg=segs(ts,mid.ticks_per_beat)
    notes=[];tracks=[]
    for ti,tr in enumerate(mid.tracks):
        act={};ev=[]
        for t,mi,m in absmsgs(tr):
            row={"tick":t,"message_index":mi,**m.dict(),"seconds":round(t2s(t,tempo,mid.ticks_per_beat),6),"metric":metric(t,sg,subdivision)}
            ev.append(row)
            if m.type=="note_on" and m.velocity>0:act.setdefault((getattr(m,"channel",0),m.note),[]).append((t,m.velocity,mi))
            elif m.type=="note_off" or (m.type=="note_on" and m.velocity==0):
                k=(getattr(m,"channel",0),m.note)
                if act.get(k):
                    st,v,si=act[k].pop(0);en=max(st,t)
                    notes.append({"track":ti,"channel":k[0],"pitch":m.note,"note_name":note_name(m.note),"velocity":v,
                                  "start_tick":st,"end_tick":en,"duration_ticks":en-st,
                                  "start_seconds":round(t2s(st,tempo,mid.ticks_per_beat),6),"end_seconds":round(t2s(en,tempo,mid.ticks_per_beat),6),
                                  "duration_seconds":round(t2s(en,tempo,mid.ticks_per_beat)-t2s(st,tempo,mid.ticks_per_beat),6),
                                  "metric":metric(st,sg,subdivision),"is_drum":k[0]==9,"source_message_index":si})
        tracks.append({"track":ti,"name":getattr(tr,"name","") or "","events":ev} if include_messages else
                      {"track":ti,"name":getattr(tr,"name","") or "","event_count":len(ev)})
    notes.sort(key=lambda n:(n["start_tick"],n["track"],n["pitch"]))
    max_tick=max([n["end_tick"] for n in notes]+[0]);pit=[n["pitch"] for n in notes if not n["is_drum"]]
    return {"schema":"advanced-lyricism.music-event-ir.v1","source":{"path":str(path),"type":"midi","midi_type":mid.type},
            "timing":{"ticks_per_quarter":mid.ticks_per_beat,"duration_ticks":max_tick,"duration_seconds":round(t2s(max_tick,tempo,mid.ticks_per_beat),6),
                      "analysis_subdivision":subdivision,"tempo_events":tempo,"time_signature_events":ts,"metric_segments":sg,"key_signature_events":key},
            "summary":{"notes":len(notes),"pitched_notes":len(pit),"drum_notes":sum(n["is_drum"] for n in notes),
                       "pitch_min":min(pit) if pit else None,"pitch_max":max(pit) if pit else None},
            "notes":notes,"tracks":tracks,
            "representation":{"partwise":"track/channel preserved","timewise":"notes globally sorted by start tick",
                              "limits":["note_off defines note duration; sustain-pedal sounding duration is not inferred",
                                        "metric coordinates are score/planning projections, not a claim about perceived groove"]}}
def main():
    ap=argparse.ArgumentParser(description="Convert MIDI to JSON with ticks, seconds, notes, tempo/meter maps and derived metric coordinates.")
    ap.add_argument("midi",type=Path);ap.add_argument("-o","--output",type=Path);ap.add_argument("--subdivision",type=int,default=16,choices=[4,8,12,16,24,32])
    ap.add_argument("--include-messages",action="store_true");ap.add_argument("--compact",action="store_true");a=ap.parse_args()
    if not a.midi.exists():print(json.dumps({"ok":False,"error":{"type":"input","message":"MIDI file not found"}}));return 2
    try:d=convert(a.midi,a.subdivision,a.include_messages)
    except Exception as e:print(json.dumps({"ok":False,"error":{"type":type(e).__name__,"message":str(e)}}));return 1
    s=json.dumps(d,ensure_ascii=False,indent=None if a.compact else 2)
    if a.output:a.output.write_text(s,encoding="utf-8")
    else:print(s)
    return 0
if __name__=="__main__":raise SystemExit(main())
