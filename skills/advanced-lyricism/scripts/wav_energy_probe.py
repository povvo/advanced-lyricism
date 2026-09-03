#!/usr/bin/env python3
"""Map PCM WAV energy, coarse pulse and section changes."""
from __future__ import annotations

import argparse
import array
import json
import math
import statistics
import wave
from pathlib import Path


def decode(raw: bytes, width: int) -> list[int]:
    if width == 1:
        return [x - 128 for x in raw]
    if width == 2:
        values = array.array("h")
        values.frombytes(raw)
        return list(values)
    if width == 3:
        out = []
        for i in range(0, len(raw) - 2, 3):
            value = int.from_bytes(raw[i:i + 3], byteorder="little", signed=True)
            out.append(value)
        return out
    if width == 4:
        values = array.array("i")
        values.frombytes(raw)
        return list(values)
    raise ValueError("PCM sample width must be 8, 16, 24 or 32 bit")


def frame_energy(path: Path, frame_seconds: float) -> tuple[list[dict], dict]:
    with wave.open(str(path), "rb") as wav:
        channels = wav.getnchannels()
        sample_rate = wav.getframerate()
        width = wav.getsampwidth()
        total_frames = wav.getnframes()
        if wav.getcomptype() != "NONE":
            raise ValueError("compressed WAV is not supported")
        chunk_frames = max(1, int(sample_rate * frame_seconds))
        maximum = float((1 << (width * 8 - 1)) - 1)
        rows = []
        index = 0
        while True:
            raw = wav.readframes(chunk_frames)
            if not raw:
                break
            samples = decode(raw, width)
            if channels > 1:
                samples = [sum(samples[i:i + channels]) / channels for i in range(0, len(samples), channels)]
            rms = math.sqrt(sum((x / maximum) ** 2 for x in samples) / max(1, len(samples)))
            rows.append({"index": index, "start_seconds": round(index * frame_seconds, 6), "rms": round(rms, 8)})
            index += 1
    return rows, {
        "sample_rate": sample_rate,
        "channels": channels,
        "sample_width_bits": width * 8,
        "duration_seconds": round(total_frames / sample_rate, 6) if sample_rate else 0.0,
        "frame_seconds": frame_seconds,
    }


def pulse_candidate(rows: list[dict], frame_seconds: float) -> tuple[float | None, float | None]:
    energy = [x["rms"] for x in rows]
    if len(energy) < 24 or not any(energy):
        return None, None
    changes = [max(0.0, energy[i] - energy[i - 1]) for i in range(1, len(energy))]
    if not any(changes):
        return None, None
    candidates = []
    for bpm in range(60, 191):
        lag = round(60.0 / bpm / frame_seconds)
        if lag < 1 or lag >= len(changes) // 2:
            continue
        score = sum(changes[i] * changes[i - lag] for i in range(lag, len(changes)))
        candidates.append((score, bpm))
    if not candidates:
        return None, None
    candidates.sort(reverse=True)
    best_score, bpm = candidates[0]
    total = sum(x * x for x in changes) or 1.0
    return float(bpm), round(min(1.0, best_score / total), 4)


def sections(rows: list[dict], frame_seconds: float) -> list[dict]:
    values = [x["rms"] for x in rows]
    if not values:
        return []
    median = statistics.median(values)
    high = median * 1.35
    low = median * 0.65
    labels = ["high" if x >= high else "low" if x <= low else "mid" for x in values]
    for i in range(1, len(labels) - 1):
        if labels[i - 1] == labels[i + 1] != labels[i]:
            labels[i] = labels[i - 1]
    out = []
    start = 0
    for i in range(1, len(labels) + 1):
        if i == len(labels) or labels[i] != labels[start]:
            chunk = values[start:i]
            out.append({
                "start_seconds": round(start * frame_seconds, 6),
                "end_seconds": round(i * frame_seconds, 6),
                "energy_band": labels[start],
                "rms_mean": round(statistics.fmean(chunk), 8),
            })
            start = i
    return out


def analyse(path: Path, frame_seconds: float) -> dict:
    rows, audio = frame_energy(path, frame_seconds)
    bpm, pulse_support = pulse_candidate(rows, frame_seconds)
    return {
        "schema": "advanced-lyricism.wav-energy-profile.v1",
        "source": {"path": str(path)},
        "audio": audio,
        "energy_frames": rows,
        "sections": sections(rows, frame_seconds),
        "pulse": {"bpm_candidate": bpm, "autocorrelation_support": pulse_support, "half_double_time_unresolved": bpm is not None},
        "limits": [
            "energy bands are relative to this file and do not name intro, verse, hook or drop by themselves",
            "the coarse pulse candidate is a planning cue; confirm tempo and half/double-time feel by ear or DAW",
            "this operation reads uncompressed PCM WAV only and does not estimate key, harmony or instrument identity",
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Map PCM WAV energy, coarse pulse and section changes.")
    ap.add_argument("wav", type=Path)
    ap.add_argument("--frame-seconds", type=float, default=0.25)
    ap.add_argument("-o", "--output", type=Path)
    args = ap.parse_args()
    if args.frame_seconds <= 0 or not args.wav.exists():
        print(json.dumps({"ok": False, "error": {"type": "input", "message": "existing WAV and frame-seconds > 0 required"}}))
        return 2
    try:
        result = analyse(args.wav, args.frame_seconds)
    except Exception as exc:
        print(json.dumps({"ok": False, "error": {"type": type(exc).__name__, "message": str(exc)}}))
        return 1
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
