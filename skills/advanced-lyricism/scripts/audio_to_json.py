#!/usr/bin/env python3
"""Extract rhythmic and energy features from audio."""
from __future__ import annotations
import argparse,json,math
from pathlib import Path

def require():
    try:
        import numpy as np, librosa
        return np,librosa
    except Exception as e:
        raise RuntimeError(f"audio analysis requires librosa and numpy: {e}")

def scalar(x):
    try:return float(x.item())
    except Exception:return float(x)

def aggregate_by_intervals(times, values, edges, np):
    rows=[]
    for i in range(len(edges)-1):
        m=(times>=edges[i])&(times<edges[i+1])
        if np.any(m):
            vv=values[m]
            rows.append({"index":i+1,"start":round(float(edges[i]),6),"end":round(float(edges[i+1]),6),
                         "mean":round(float(np.mean(vv)),6),"max":round(float(np.max(vv)),6)})
        else:
            rows.append({"index":i+1,"start":round(float(edges[i]),6),"end":round(float(edges[i+1]),6),
                         "mean":0.0,"max":0.0})
    return rows

def convert(path:Path,sr:int|None=None,duration:float|None=None,offset:float=0.0,hop_length:int=512):
    np,librosa=require()
    y,sr2=librosa.load(str(path),sr=sr,mono=True,duration=duration,offset=offset)
    if y.size==0:raise ValueError("audio contains no samples in requested range")
    dur=len(y)/sr2
    onset_env=librosa.onset.onset_strength(y=y,sr=sr2,hop_length=hop_length)
    frame_times=librosa.times_like(onset_env,sr=sr2,hop_length=hop_length)
    tempo,beat_frames=librosa.beat.beat_track(onset_envelope=onset_env,sr=sr2,hop_length=hop_length,units="frames")
    tempo=scalar(tempo)
    beat_times=librosa.frames_to_time(beat_frames,sr=sr2,hop_length=hop_length)
    onset_frames=librosa.onset.onset_detect(onset_envelope=onset_env,sr=sr2,hop_length=hop_length,backtrack=False)
    onset_times=librosa.frames_to_time(onset_frames,sr=sr2,hop_length=hop_length)
    rms=librosa.feature.rms(y=y,hop_length=hop_length)[0]
    centroid=librosa.feature.spectral_centroid(y=y,sr=sr2,hop_length=hop_length)[0]
    # resize feature vectors defensively to onset-env frame count
    n=min(len(frame_times),len(rms),len(centroid),len(onset_env))
    ft=frame_times[:n]; rms=rms[:n]; centroid=centroid[:n]; oe=onset_env[:n]
    beats=[]
    if len(beat_times)>=2:
        for i in range(len(beat_times)-1):
            a,b=float(beat_times[i]),float(beat_times[i+1]);m=(ft>=a)&(ft<b)
            beats.append({"beat":i+1,"time":round(a,6),"duration":round(b-a,6),
                          "onset_strength_mean":round(float(np.mean(oe[m])) if np.any(m) else 0.0,6),
                          "onset_strength_max":round(float(np.max(oe[m])) if np.any(m) else 0.0,6),
                          "rms_mean":round(float(np.mean(rms[m])) if np.any(m) else 0.0,6),
                          "spectral_centroid_mean":round(float(np.mean(centroid[m])) if np.any(m) else 0.0,3)})
    # frame summaries by whole seconds keep the representation compact but inspectable
    edges=np.arange(0,max(dur,1e-9)+1.0,1.0)
    if edges[-1] < dur:edges=np.append(edges,dur)
    sec_rms=aggregate_by_intervals(ft,rms,edges,np) if len(edges)>1 else []
    return {
      "schema":"advanced-lyricism.audio-event-ir.v1",
      "source":{"path":str(path),"offset_seconds":offset,"requested_duration":duration},
      "timing":{"sample_rate":sr2,"samples":int(len(y)),"duration_seconds":round(dur,6),
                "hop_length":hop_length,"tempo_bpm_estimate":round(tempo,4),
                "beat_times_seconds":[round(float(x),6) for x in beat_times.tolist()],
                "onset_times_seconds":[round(float(x),6) for x in onset_times.tolist()]},
      "beat_features":beats,
      "second_level_rms":sec_rms,
      "summary":{"beat_count":int(len(beat_times)),"onset_count":int(len(onset_times)),
                 "rms_mean":round(float(np.mean(rms)),6),"rms_max":round(float(np.max(rms)),6),
                 "spectral_centroid_mean":round(float(np.mean(centroid)),3)},
      "representation":{"raw_audio_preserved":False,"derived_from_waveform":True,
        "limits":["beat/onset/tempo values are estimates, not score truth",
                  "half-time versus double-time interpretation is unresolved",
                  "feature changes can suggest section boundaries but do not name musical function by themselves"]}
    }

def main():
    ap=argparse.ArgumentParser(description="Convert audio to compact JSON with estimated tempo, beats, onsets and energy/timbre features.")
    ap.add_argument("audio",type=Path);ap.add_argument("-o","--output",type=Path)
    ap.add_argument("--sr",type=int,default=None);ap.add_argument("--duration",type=float,default=None);ap.add_argument("--offset",type=float,default=0.0)
    ap.add_argument("--hop-length",type=int,default=512);ap.add_argument("--compact",action="store_true")
    a=ap.parse_args()
    if not a.audio.exists():
        print(json.dumps({"ok":False,"error":{"type":"input","message":"audio file not found"}}));return 2
    if a.offset<0 or (a.duration is not None and a.duration<=0) or a.hop_length<=0:
        print(json.dumps({"ok":False,"error":{"type":"input","message":"offset >= 0, duration > 0, hop-length > 0"}}));return 2
    try:d=convert(a.audio,a.sr,a.duration,a.offset,a.hop_length)
    except Exception as e:
        print(json.dumps({"ok":False,"error":{"type":type(e).__name__,"message":str(e)}}));return 1
    s=json.dumps(d,ensure_ascii=False,indent=None if a.compact else 2)
    if a.output:a.output.write_text(s,encoding="utf-8")
    else:print(s)
    return 0
if __name__=="__main__":raise SystemExit(main())
