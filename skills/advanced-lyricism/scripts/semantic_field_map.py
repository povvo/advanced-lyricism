#!/usr/bin/env python3
"""Map lyrics across semantic fields and cross-field collisions."""
from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path

from lyric_utils import CONTENT_STOP, read_text_arg

WORD_RE = re.compile(r"[A-Za-z0-9]+(?:['’][A-Za-z0-9]+)?")

PRESETS = {
    "universal": {
        "body_sense": ["body", "blood", "breath", "bone", "chest", "eye", "face", "hand", "head", "heart", "mouth", "skin", "smell", "taste", "touch", "voice"],
        "movement": ["arrive", "back", "carry", "cross", "drive", "fall", "follow", "leave", "move", "return", "ride", "run", "step", "turn", "walk"],
        "place": ["block", "bridge", "city", "door", "ends", "estate", "flat", "home", "house", "road", "room", "street", "town", "yard"],
        "institution": ["bail", "bank", "court", "hospital", "judge", "office", "police", "prison", "school", "state", "work"],
        "material_money": ["bag", "bread", "cash", "chain", "clothes", "cost", "gold", "money", "price", "rent", "ring", "watch"],
        "relation": ["bro", "child", "enemy", "family", "friend", "lover", "mother", "opp", "partner", "sister", "stranger", "they", "we", "you"],
        "conflict_pressure": ["attack", "fight", "force", "harm", "pressure", "risk", "scar", "threat", "trap", "war", "weapon", "wound"],
        "grief_absence": ["alone", "dead", "empty", "gone", "grief", "loss", "memory", "miss", "mourning", "remember", "silence"],
        "time_change": ["after", "again", "before", "day", "future", "late", "moment", "night", "now", "old", "past", "still", "time", "young"],
        "status_display": ["brand", "crown", "famous", "flex", "image", "king", "luxury", "name", "power", "rank", "status"],
        "music_media": ["album", "bar", "beat", "camera", "film", "flow", "hook", "mic", "music", "record", "screen", "song", "stage", "verse"],
    },
    "uk-drill": {
        "territory": ["bits", "block", "ends", "estate", "gates", "manor", "opp block", "postcode", "road", "strip", "yard"],
        "movement": ["back out", "dip", "glide", "hop out", "link", "move", "pattern", "slide", "spin", "step", "touch road"],
        "institution": ["bail", "bird", "court", "fed", "feds", "hmp", "injunction", "probation", "recall", "remand", "sentence"],
        "economy": ["bag", "bando", "bands", "bread", "brick", "food", "line", "paper", "plug", "ps", "trap", "work"],
        "relation_loyalty": ["bredrin", "bro", "day one", "family", "gang", "mandem", "opp", "opps", "paigon", "snake", "trust", "yute"],
        "grief_residue": ["angel", "gone", "lost", "memory", "miss", "rest", "rip", "sentence", "visiting", "wake"],
        "conflict": ["attack", "bore", "bun", "chef", "corn", "dip", "kweng", "shank", "shoot", "splash", "stab", "wap", "wet", "wound"],
        "status_display": ["bands", "drip", "ice", "name", "off-white", "power", "reputation", "roley", "status"],
        "music_performance": ["bar", "beat", "cold", "flow", "freestyle", "hook", "mic", "studio", "track", "verse", "video"],
    },
}


def tokens(text: str) -> list[str]:
    return [x.lower().replace("’", "'") for x in WORD_RE.findall(text)]


def load_fields(preset: str, custom: Path | None) -> dict[str, list[str]]:
    fields = {k: list(v) for k, v in PRESETS[preset].items()}
    if custom:
        raw = json.loads(custom.read_text(encoding="utf-8"))
        if not isinstance(raw, dict) or not all(isinstance(v, list) for v in raw.values()):
            raise ValueError("custom fields must be a JSON object of field -> term list")
        for name, terms in raw.items():
            fields[str(name)] = [str(x).lower() for x in terms if str(x).strip()]
    return fields


def term_pattern(term: str) -> re.Pattern[str]:
    bits = [re.escape(x) for x in term.lower().split()]
    return re.compile(r"(?<![\w'])" + r"\s+".join(bits) + r"(?![\w'])", re.IGNORECASE)


def analyse(text: str, fields: dict[str, list[str]], preset: str) -> dict:
    lines = [x.rstrip() for x in text.splitlines() if x.strip()]
    compiled = {name: [(term, term_pattern(term)) for term in terms] for name, terms in fields.items()}
    totals: collections.Counter[str] = collections.Counter()
    matched_terms: dict[str, collections.Counter[str]] = {name: collections.Counter() for name in fields}
    progression = []
    co = collections.Counter()

    for number, line in enumerate(lines, 1):
        line_fields = []
        line_hits = {}
        for name, pats in compiled.items():
            hits = []
            for term, pattern in pats:
                n = len(pattern.findall(line))
                if n:
                    hits.extend([term] * n)
                    totals[name] += n
                    matched_terms[name][term] += n
            if hits:
                line_fields.append(name)
                line_hits[name] = sorted(set(hits))
        for i, left in enumerate(sorted(set(line_fields))):
            for right in sorted(set(line_fields))[i + 1:]:
                co[(left, right)] += 1
        progression.append({"line": number, "text": line, "fields": line_hits})

    all_tokens = tokens(text)
    salient = collections.Counter(x for x in all_tokens if len(x) > 2 and x not in CONTENT_STOP and not x.isdigit())
    covered_singletons = {term for terms in fields.values() for term in terms if " " not in term}
    unmatched = [{"term": term, "count": count} for term, count in salient.most_common() if term not in covered_singletons][:30]
    field_rows = []
    for name in fields:
        count = totals[name]
        field_rows.append({
            "field": name,
            "matches": count,
            "line_coverage": sum(1 for row in progression if name in row["fields"]),
            "terms": [{"term": term, "count": n} for term, n in matched_terms[name].most_common()],
        })
    field_rows.sort(key=lambda x: (-x["matches"], x["field"]))
    collisions = [{"fields": [a, b], "shared_lines": n} for (a, b), n in co.most_common()]
    return {
        "schema": "advanced-lyricism.semantic-field-map.v1",
        "preset": preset,
        "summary": {"lines": len(lines), "tokens": len(all_tokens), "active_fields": sum(x["matches"] > 0 for x in field_rows)},
        "fields": field_rows,
        "line_progression": progression,
        "field_collisions": collisions,
        "unmapped_salient_terms": unmatched,
        "limits": [
            "field matches expose lexical distribution; they do not determine a lyric's theme or quality",
            "the UK-drill preset is opt-in and descriptive; it does not require violence, MLE markers or any content quota",
            "polysemous terms require context and supplied pronunciation/register before interpretation",
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Map lyrics across semantic fields and cross-field collisions.")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("-i", "--input", type=Path)
    src.add_argument("-t", "--text")
    ap.add_argument("--preset", choices=sorted(PRESETS), default="universal")
    ap.add_argument("--fields", type=Path, help="JSON object of additional/replacement field term lists")
    ap.add_argument("-o", "--output", type=Path)
    args = ap.parse_args()
    try:
        result = analyse(read_text_arg(args.input, args.text), load_fields(args.preset, args.fields), args.preset)
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
