#!/usr/bin/env python3
"""Compare beat metadata with measured tempo and key fields."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

BPM_RE = re.compile(r"(?<!\d)(\d{2,3}(?:\.\d+)?)\s*bpm\b", re.IGNORECASE)
KEY_RE = re.compile(r"\b([A-Ga-g](?:#|b)?\s*(?:minor|major|min|maj|m))\b")


def get_path(data: dict, paths: list[tuple[str, ...]]) -> Any:
    for path in paths:
        value: Any = data
        for key in path:
            if not isinstance(value, dict) or key not in value:
                value = None
                break
            value = value[key]
        if value is not None and value != "":
            return value
    return None


def measured_fields(data: dict) -> tuple[float | None, str | None, str | None]:
    raw_bpm = get_path(data, [
        ("timing", "tempo_bpm_estimate"),
        ("pulse", "bpm_candidate"),
        ("bpm",),
        ("estimated_bpm",),
        ("audio_bpm",),
    ])
    try:
        bpm = float(raw_bpm) if raw_bpm is not None else None
    except Exception:
        bpm = None
    key = get_path(data, [("analysis", "key"), ("key",), ("audio_key",), ("key_detected",)])
    return bpm, str(key) if key is not None and key != "" else None, data.get("schema")


def bpm_alignment(measured: float | None, claims: list[float], tolerance: float) -> dict:
    if measured is None or not claims:
        return {"state": "unavailable", "best": None}
    rows = []
    for claim in claims:
        for relation, candidate in (("same", measured), ("metadata_half_of_measurement", measured / 2), ("metadata_double_measurement", measured * 2)):
            rows.append({"metadata_bpm": claim, "relation": relation, "difference": round(abs(claim - candidate), 4)})
    best = min(rows, key=lambda x: x["difference"])
    return {"state": "aligned" if best["difference"] <= tolerance else "conflict", "best": best, "tolerance_bpm": tolerance}


def analyse(analysis_data: dict, metadata_text: str, tolerance: float) -> dict:
    bpm, key, source_schema = measured_fields(analysis_data)
    bpm_claims = sorted({float(x) for x in BPM_RE.findall(metadata_text)})
    key_claims = sorted({re.sub(r"\s+", " ", x).strip() for x in KEY_RE.findall(metadata_text)}, key=str.lower)
    alignment = bpm_alignment(bpm, bpm_claims, tolerance)
    if key is None or not key_claims:
        key_state = "unavailable"
    else:
        key_state = "aligned" if any(key.lower().replace(" ", "") == x.lower().replace(" ", "") for x in key_claims) else "conflict"
    issues = []
    if bpm is not None and not bpm_claims:
        issues.append("metadata_bpm_missing")
    if alignment["state"] == "conflict":
        issues.append("metadata_bpm_conflict")
    if key is not None and not key_claims:
        issues.append("metadata_key_missing")
    if key_state == "conflict":
        issues.append("metadata_key_conflict")
    return {
        "schema": "advanced-lyricism.beat-metadata-reconcile.v1",
        "source_schema": source_schema,
        "measured": {"tempo_bpm": bpm, "key": key},
        "metadata_claims": {"tempo_bpm": bpm_claims, "key": key_claims},
        "comparison": {"tempo": alignment, "key": {"state": key_state}},
        "issues": issues,
        "limits": [
            "metadata claims and measured estimates remain separate",
            "half-time and double-time equivalence is tested before calling a tempo conflict",
            "no key comparison is made when the analysis input contains no measured key",
            "title or description mood words do not establish the beat's emotional effect",
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Compare beat metadata with measured tempo and key fields.")
    ap.add_argument("analysis", type=Path, help="JSON from audio, WAV, MIDI or beat analysis")
    meta = ap.add_mutually_exclusive_group(required=True)
    meta.add_argument("--metadata", type=Path)
    meta.add_argument("--text")
    ap.add_argument("--tolerance", type=float, default=2.0)
    ap.add_argument("-o", "--output", type=Path)
    args = ap.parse_args()
    if args.tolerance < 0:
        print(json.dumps({"ok": False, "error": {"type": "input", "message": "tolerance must be >= 0"}}))
        return 2
    try:
        analysis_data = json.loads(args.analysis.read_text(encoding="utf-8"))
        metadata_text = args.text if args.text is not None else args.metadata.read_text(encoding="utf-8", errors="ignore")
        result = analyse(analysis_data, metadata_text, args.tolerance)
    except Exception as exc:
        print(json.dumps({"ok": False, "error": {"type": type(exc).__name__, "message": str(exc)}}))
        return 2
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
