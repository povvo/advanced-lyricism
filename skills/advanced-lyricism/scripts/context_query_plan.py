#!/usr/bin/env python3
"""Build current-context research queries from lyric language."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


MLE_GLOSSES = {
    "back out": ["produce or draw an object"],
    "bando": ["abandoned property", "dealing location in some rap contexts"],
    "bare": ["much or very"],
    "block": ["immediate estate or territory"],
    "bun": ["smoke", "reject", "shoot in some contexts"],
    "dip": ["leave quickly", "stab in some contexts"],
    "ends": ["local area"],
    "food": ["ordinary food", "drug product in some contexts"],
    "hold": ["possess", "receive or endure"],
    "innit": ["discourse tag"],
    "link": ["meet"],
    "man": ["first-person or generic-person reference depending on syntax"],
    "mandem": ["peer collective"],
    "opp": ["opponent or rival"],
    "paigon": ["false or disloyal person"],
    "pattern": ["sort out or handle"],
    "peak": ["adverse or unfortunate"],
    "road": ["street activity or life outside, depending on phrase"],
    "spin": ["move through or revisit an area"],
    "still": ["emphasis or persistence marker"],
    "ting": ["person", "object", "weapon", "general placeholder"],
    "touch road": ["leave custody or return outside"],
    "wet": ["stabbed or injured", "unimpressive"],
    "work": ["ordinary labour", "drug product in some contexts"],
    "yard": ["home"],
    "yute": ["young person"],
}

PLATFORMS = {"primary", "web", "youtube", "community", "scholarly"}
INTENTS = {"usage", "artist", "scene", "production", "reference"}


def find_terms(phrase: str) -> list[dict]:
    lower = phrase.lower()
    rows = []
    for term in sorted(MLE_GLOSSES, key=len, reverse=True):
        if re.search(r"(?<![\w'])" + re.escape(term) + r"(?![\w'])", lower):
            rows.append({"term": term, "working_senses": MLE_GLOSSES[term], "ambiguous": len(MLE_GLOSSES[term]) > 1})
    return rows


def compact(parts: list[str | None]) -> str:
    return re.sub(r"\s+", " ", " ".join(x for x in parts if x)).strip()


def build_queries(phrase: str, intents: list[str], platforms: list[str], area: str | None, year: str | None) -> dict:
    found = find_terms(phrase)
    focus_terms = [x["term"] for x in found] or [phrase]
    rows = []

    def add(platform: str, query: str, purpose: str, priority: int) -> None:
        if platform in platforms and query:
            rows.append({"platform": platform, "query": query, "purpose": purpose, "source_priority": priority})

    for intent in intents:
        if intent == "usage":
            for term in focus_terms:
                add("primary", compact([f'"{term}"', area, year, "interview OR transcript OR lyrics"]), "observe the term in speaker-controlled context", 1)
                add("scholarly", compact([f'"{term}"', "Multicultural London English OR sociolinguistics"]), "check durable meaning, syntax and social function", 3)
                add("community", compact([f'"{term}"', area, "usage meaning"]), "discover current contested or local senses; verify elsewhere", 5)
        elif intent == "artist":
            add("primary", compact([f'"{phrase}"', "official interview OR live performance", year]), "translate the reference into observable craft properties", 1)
            add("youtube", compact([f'"{phrase}"', "live OR freestyle OR interview", year]), "inspect delivery, pronunciation and section behaviour", 2)
        elif intent == "scene":
            add("web", compact([f'"{phrase}"', area, year, "scene collaboration release"]), "map current relationships and releases", 2)
            add("community", compact([f'"{phrase}"', area, year]), "discover candidate relationships or terms; do not treat popularity as quality", 5)
        elif intent == "production":
            add("youtube", compact([f'"{phrase}"', area, year, "instrumental OR producer"]), "locate current audible production examples", 2)
            add("web", compact([f'"{phrase}"', "producer interview BPM arrangement", year]), "check production and arrangement claims", 2)
        elif intent == "reference":
            add("primary", compact([f'"{phrase}"', "official source"]), "establish the literal property before building a lyrical collision", 1)
            add("web", compact([f'"{phrase}"', "meaning history context"]), "check ambiguity, currency and likely listener knowledge", 3)

    seen = set()
    unique = []
    for row in sorted(rows, key=lambda x: (x["source_priority"], x["platform"], x["query"])):
        key = (row["platform"], row["query"])
        if key not in seen:
            seen.add(key)
            unique.append(row)
    return {
        "schema": "advanced-lyricism.context-query-plan.v1",
        "phrase": phrase,
        "scope": {"area": area, "year_or_period": year, "intents": intents, "platforms": platforms},
        "recognized_terms": found,
        "queries": unique,
        "execution": "Run the queries that can change the lyric decision with available research tools.",
        "limits": [
            "this tool generates queries but does not execute network requests",
            "autocomplete and community results are discovery signals, not definitions or measures of craft quality",
            "recognized senses are working hypotheses; current local usage and supplied speaker material can override them",
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Build current-context research queries from lyric language.")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("phrase", nargs="?")
    src.add_argument("-i", "--input", type=Path)
    ap.add_argument("--intent", default="usage,scene", help="Comma-separated: usage,artist,scene,production,reference")
    ap.add_argument("--platforms", default="primary,web,youtube,community,scholarly")
    ap.add_argument("--area")
    ap.add_argument("--year")
    ap.add_argument("-o", "--output", type=Path)
    args = ap.parse_args()
    phrase = args.phrase if args.phrase is not None else args.input.read_text(encoding="utf-8", errors="ignore")
    intents = [x.strip() for x in args.intent.split(",") if x.strip()]
    platforms = [x.strip() for x in args.platforms.split(",") if x.strip()]
    bad_intents = sorted(set(intents) - INTENTS)
    bad_platforms = sorted(set(platforms) - PLATFORMS)
    if not phrase.strip() or bad_intents or bad_platforms:
        print(json.dumps({"ok": False, "error": {"type": "input", "message": f"empty phrase or unsupported values: intents={bad_intents}, platforms={bad_platforms}"}}))
        return 2
    result = build_queries(phrase.strip(), intents, platforms, args.area, args.year)
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
