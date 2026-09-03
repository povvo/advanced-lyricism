#!/usr/bin/env python3
"""Build and query scene relationships from supplied rows."""
from __future__ import annotations

import argparse
import collections
import csv
import json
from pathlib import Path
from typing import Any


def load_input(path: Path) -> Any:
    text = path.read_text(encoding="utf-8-sig", errors="ignore")
    if path.suffix.lower() in {".jsonl", ".ndjson"}:
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    if path.suffix.lower() == ".json":
        return json.loads(text)
    sample = text[:4096]
    dialect = csv.Sniffer().sniff(sample) if sample.strip() else csv.excel
    return list(csv.DictReader(text.splitlines(), dialect=dialect))


def normalise(raw: Any) -> tuple[dict[str, dict], list[dict], list[str]]:
    warnings = []
    nodes: dict[str, dict] = {}
    edges: list[dict] = []
    if isinstance(raw, dict) and isinstance(raw.get("nodes"), list):
        for node in raw["nodes"]:
            node_id = str(node.get("id") or node.get("name") or "").strip()
            if node_id:
                nodes[node_id] = {"id": node_id, "type": str(node.get("type") or "unknown"), "metadata": dict(node.get("metadata") or {})}
    rows = raw.get("edges", []) if isinstance(raw, dict) else raw
    if isinstance(raw, dict) and not isinstance(rows, list):
        rows = [raw]
    if not isinstance(rows, list):
        raise ValueError("input must be a row list or an object containing nodes/edges")
    for number, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            warnings.append(f"row {number} ignored: not an object")
            continue
        source = str(row.get("source") or row.get("from") or row.get("artist") or "").strip()
        target = str(row.get("target") or row.get("to") or row.get("collaborator") or row.get("producer") or "").strip()
        if not source or not target:
            warnings.append(f"row {number} ignored: source/target missing")
            continue
        relation = str(row.get("relation") or row.get("edge_type") or row.get("type") or "related").strip()
        try:
            weight = float(row.get("weight", 1.0) or 1.0)
        except Exception:
            weight = 1.0
            warnings.append(f"row {number}: invalid weight replaced by 1.0")
        directed_raw = row.get("directed", False)
        directed = directed_raw if isinstance(directed_raw, bool) else str(directed_raw).lower() in {"1", "true", "yes"}
        meta = {k: v for k, v in row.items() if k not in {"source", "from", "artist", "target", "to", "collaborator", "producer", "relation", "edge_type", "type", "weight", "directed"} and v is not None and v != ""}
        nodes.setdefault(source, {"id": source, "type": str(row.get("source_type") or "unknown"), "metadata": {}})
        nodes.setdefault(target, {"id": target, "type": str(row.get("target_type") or "unknown"), "metadata": {}})
        edges.append({"source": source, "target": target, "relation": relation, "weight": max(0.0, weight), "directed": directed, "metadata": meta})
    return nodes, edges, warnings


def adjacency(edges: list[dict]) -> dict[str, list[tuple[str, int]]]:
    out: dict[str, list[tuple[str, int]]] = collections.defaultdict(list)
    for index, edge in enumerate(edges):
        out[edge["source"]].append((edge["target"], index))
        if not edge["directed"]:
            out[edge["target"]].append((edge["source"], index))
    return out


def neighbourhood(focus: list[str], hops: int, adj: dict[str, list[tuple[str, int]]]) -> dict[str, int]:
    distance = {node: 0 for node in focus}
    queue = collections.deque(focus)
    while queue:
        current = queue.popleft()
        if distance[current] >= hops:
            continue
        for nxt, _ in adj.get(current, []):
            if nxt not in distance:
                distance[nxt] = distance[current] + 1
                queue.append(nxt)
    return distance


def shortest_path(start: str, end: str, adj: dict[str, list[tuple[str, int]]], edges: list[dict]) -> list[dict] | None:
    queue = collections.deque([start])
    parent: dict[str, tuple[str, int] | None] = {start: None}
    while queue:
        current = queue.popleft()
        if current == end:
            break
        for nxt, edge_index in adj.get(current, []):
            if nxt not in parent:
                parent[nxt] = (current, edge_index)
                queue.append(nxt)
    if end not in parent:
        return None
    path = []
    cursor = end
    while parent[cursor] is not None:
        previous, edge_index = parent[cursor]
        edge = edges[edge_index]
        path.append({"from": previous, "to": cursor, "relation": edge["relation"], "weight": edge["weight"], "metadata": edge["metadata"]})
        cursor = previous
    return list(reversed(path))


def analyse(raw: Any, focus: list[str], hops: int, explain: tuple[str, str] | None) -> dict:
    nodes, edges, warnings = normalise(raw)
    adj = adjacency(edges)
    missing_focus = [x for x in focus if x not in nodes]
    if missing_focus:
        warnings.append("focus nodes missing: " + ", ".join(missing_focus))
    active_focus = [x for x in focus if x in nodes]
    distances = neighbourhood(active_focus, hops, adj) if active_focus else {}
    relation_counts = collections.Counter(edge["relation"] for edge in edges)
    path = shortest_path(explain[0], explain[1], adj, edges) if explain and explain[0] in nodes and explain[1] in nodes else None
    return {
        "schema": "advanced-lyricism.scene-graph.v1",
        "summary": {"nodes": len(nodes), "edges": len(edges), "relation_types": dict(relation_counts.most_common())},
        "nodes": sorted(nodes.values(), key=lambda x: x["id"].lower()),
        "edges": edges,
        "focus": {"requested": focus, "hops": hops, "distances": dict(sorted(distances.items(), key=lambda x: (x[1], x[0].lower())))},
        "connection": {"from": explain[0], "to": explain[1], "path": path} if explain else None,
        "warnings": warnings,
        "limits": [
            "relationships come only from supplied rows; absence of an edge is not absence of a real relationship",
            "graph proximity does not measure artistic quality, influence or allegiance",
            "dates and relation labels must be checked before current-scene conclusions are drawn",
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Build a local scene graph from supplied JSON, JSONL or CSV relationship rows.")
    ap.add_argument("input", type=Path)
    ap.add_argument("--focus", default="", help="Comma-separated node ids")
    ap.add_argument("--hops", type=int, default=2)
    ap.add_argument("--explain", help="Two comma-separated node ids")
    ap.add_argument("-o", "--output", type=Path)
    args = ap.parse_args()
    if args.hops < 0:
        print(json.dumps({"ok": False, "error": {"type": "input", "message": "hops must be >= 0"}}))
        return 2
    explain = None
    if args.explain:
        parts = [x.strip() for x in args.explain.split(",") if x.strip()]
        if len(parts) != 2:
            print(json.dumps({"ok": False, "error": {"type": "input", "message": "--explain requires source,target"}}))
            return 2
        explain = (parts[0], parts[1])
    try:
        result = analyse(load_input(args.input), [x.strip() for x in args.focus.split(",") if x.strip()], args.hops, explain)
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
