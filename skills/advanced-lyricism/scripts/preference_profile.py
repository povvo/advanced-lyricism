#!/usr/bin/env python3
"""Summarise patterns in accepted and rejected lyric choices."""
from __future__ import annotations

import argparse
import collections
import csv
import json
import statistics
from pathlib import Path
from typing import Any


def load_rows(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8-sig", errors="ignore")
    if path.suffix.lower() in {".jsonl", ".ndjson"}:
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    if path.suffix.lower() == ".json":
        raw = json.loads(text)
        if isinstance(raw, dict):
            raw = raw.get("choices") or raw.get("rows") or raw.get("history") or [raw]
        if not isinstance(raw, list):
            raise ValueError("JSON must contain a list of feedback rows")
        return [dict(x) for x in raw]
    sample = text[:4096]
    dialect = csv.Sniffer().sniff(sample) if sample.strip() else csv.excel
    return [dict(x) for x in csv.DictReader(text.splitlines(), dialect=dialect)]


def as_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if value is None or value == "":
        return None
    lower = str(value).strip().lower()
    if lower in {"1", "true", "yes", "keep", "accepted", "like"}:
        return True
    if lower in {"0", "false", "no", "reject", "rejected", "dislike"}:
        return False
    return None


def rating(row: dict) -> float | None:
    accepted = as_bool(row.get("accepted", row.get("keep")))
    if accepted is not None:
        return 5.0 if accepted else 1.0
    raw = row.get("rating", row.get("score"))
    try:
        value = float(raw)
    except Exception:
        return None
    if 0 <= value <= 1:
        return 1 + value * 4
    return max(1.0, min(5.0, value))


def features(row: dict) -> dict[str, float]:
    raw = row.get("features", {})
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except Exception:
            raw = {}
    if not isinstance(raw, dict):
        return {}
    out = {}
    for name, value in raw.items():
        try:
            number = float(value)
        except Exception:
            continue
        if 0 <= number <= 1:
            out[str(name)] = number
    return out


def mean(values: list[float]) -> float | None:
    return round(statistics.fmean(values), 4) if values else None


def analyse(rows: list[dict]) -> dict:
    usable = []
    skipped = []
    for index, row in enumerate(rows, 1):
        r = rating(row)
        f = features(row)
        if r is None:
            skipped.append({"row": index, "reason": "rating/accepted value missing"})
            continue
        usable.append({"rating": r, "features": f, "reason": str(row.get("reason") or row.get("note") or "").strip(), "cluster": str(row.get("cluster") or row.get("lane") or "").strip()})

    liked = [x for x in usable if x["rating"] >= 4]
    disliked = [x for x in usable if x["rating"] <= 2]
    feature_names = sorted({name for row in usable for name in row["features"]})
    associations = []
    for name in feature_names:
        liked_values = [x["features"][name] for x in liked if name in x["features"]]
        disliked_values = [x["features"][name] for x in disliked if name in x["features"]]
        lm, dm = mean(liked_values), mean(disliked_values)
        delta = round(lm - dm, 4) if lm is not None and dm is not None else None
        if delta is None or abs(delta) < 0.12:
            direction = "unclear"
        else:
            direction = "higher" if delta > 0 else "lower"
        paired_n = min(len(liked_values), len(disliked_values))
        associations.append({
            "feature": name,
            "liked_mean": lm,
            "disliked_mean": dm,
            "difference": delta,
            "preferred_direction": direction,
            "support": {"liked": len(liked_values), "disliked": len(disliked_values), "confidence": round(min(1.0, paired_n / 5), 3)},
        })
    associations.sort(key=lambda x: (x["difference"] is None, -abs(x["difference"] or 0), x["feature"]))
    cluster_rows = []
    clusters = collections.defaultdict(list)
    for row in usable:
        if row["cluster"]:
            clusters[row["cluster"]].append(row["rating"])
    for name, values in clusters.items():
        cluster_rows.append({"cluster": name, "mean_rating": mean(values), "observations": len(values)})
    return {
        "schema": "advanced-lyricism.preference-profile.v1",
        "summary": {"rows": len(rows), "usable": len(usable), "liked": len(liked), "disliked": len(disliked), "neutral": len(usable) - len(liked) - len(disliked)},
        "feature_associations": associations,
        "cluster_associations": sorted(cluster_rows, key=lambda x: (-x["mean_rating"], x["cluster"])),
        "accepted_reasons": [x["reason"] for x in liked if x["reason"]],
        "rejected_reasons": [x["reason"] for x in disliked if x["reason"]],
        "skipped": skipped,
        "limits": [
            "associations describe supplied feedback history; they are not stable personality traits",
            "small or one-sided samples remain unclear rather than being converted into false confidence",
            "explicit instructions in the current request outrank historical associations",
            "no feedback is persisted unless the caller explicitly saves the output",
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Summarise patterns in accepted and rejected lyric choices.")
    ap.add_argument("input", type=Path)
    ap.add_argument("-o", "--output", type=Path)
    args = ap.parse_args()
    try:
        result = analyse(load_rows(args.input))
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
