#!/usr/bin/env python3
"""Summarise bundled beat-grid JSON."""
from __future__ import annotations

import argparse
import json
import statistics
from collections import Counter
from pathlib import Path

def summarise(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    meta = data.get("meta", {})
    grid = data.get("grid", [])
    events = [ev for m in grid for ev in m.get("events", [])]
    types = Counter(ev.get("type","unknown") for ev in events)
    capacities = Counter(ev.get("capacity","unknown") for ev in events)
    anchors = sum(1 for ev in events if ev.get("is_anchor"))
    per_measure = [len(m.get("events", [])) for m in grid]
    bpm = float(meta.get("bpm", 0) or 0)
    swing = meta.get("swing_ratio")
    result = {
        "profile": path.name,
        "title": meta.get("title"),
        "bpm": bpm or None,
        "swing_ratio": swing,
        "duration_seconds": meta.get("duration"),
        "measures": len(grid),
        "events": len(events),
        "anchors": anchors,
        "anchor_ratio": round(anchors/len(events), 3) if events else 0.0,
        "event_types": dict(types.most_common()),
        "capacity": dict(capacities.most_common()),
        "events_per_measure": {
            "mean": round(statistics.mean(per_measure), 2) if per_measure else 0,
            "median": round(statistics.median(per_measure), 2) if per_measure else 0,
            "min": min(per_measure) if per_measure else 0,
            "max": max(per_measure) if per_measure else 0,
        },
        "guidance": data.get("guidance", {}),
    }
    if bpm:
        result["four_four_bar_seconds"] = round(240.0/bpm, 3)
    return result

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("profile", help="path to beat JSON")
    ap.add_argument("--markdown", action="store_true")
    args = ap.parse_args()
    d = summarise(Path(args.profile))
    if args.markdown:
        print(f"# {d.get('title') or d['profile']}")
        print(f"- BPM: {d['bpm']} | swing ratio: {d['swing_ratio']} | measures: {d['measures']}")
        print(f"- Events: {d['events']} | anchors: {d['anchors']} ({d['anchor_ratio']})")
        print(f"- Event types: {d['event_types']}")
        print(f"- Capacity: {d['capacity']}")
        print(f"- Events/measure: {d['events_per_measure']}")
        if d.get("guidance"):
            print(f"- Original guidance: {d['guidance']}")
    else:
        print(json.dumps(d, indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
