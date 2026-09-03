#!/usr/bin/env python3
"""Resolve lyric tool and pipeline routes, capability states, paired methods,
working templates, command inputs, and output contracts before execution.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
from runtime_capabilities import snapshot, tool_state

ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/"assets"/"tool-catalog.json"
DOMAINS=ROOT/"assets"/"domain-registry.json"

def load():
    cat=json.loads(CATALOG.read_text(encoding="utf-8"))
    dom=json.loads(DOMAINS.read_text(encoding="utf-8"))
    return cat,dom

def plan_tool(tool_id,uses=None,snap=None):
    cat,_=load()
    found=next((t for t in cat["tools"] if t["id"]==tool_id),None)
    if found is None:
        return {"ok":False,"error":{"type":"unknown_tool","message":tool_id}}
    snap=snap or snapshot()
    state=tool_state(found,uses or [],snap)
    return {
        "ok":True,
        "schema":"advanced-lyricism.tool-plan.v1",
        "tool":tool_id,
        "class":found["class"],
        "script":found["script"],
        "when":found["when"],
        "primary_domain":found.get("primary_domain"),
        "reference":found.get("primary_reference"),
        "template":found.get("primary_template"),
        "input":found.get("input",[]),
        "output":found.get("output"),
        "runtime":state,
        "command_template":f"python {found['script']} <tool arguments>",
        "execution_rule":"Blocked plans report the missing input or capability for recovery. Partial plans ground interpretation in safe_claims and leave partial_forbidden_claims unavailable.",
        "cli":found.get("cli",{}),
        "agent_io":found.get("agent_io",{}),
        "postcondition":"Inspect the tool's support/status fields before drawing craft conclusions."
    }

def _tool_ids_in_step(step):
    if isinstance(step,str):
        if step.startswith("tool_router:"):
            return [step.split(":",1)[1]]
        return [step] if step not in {"decision_point","evaluate_separately","arc_generator_or_word_rearranger"} else []
    if isinstance(step,dict):
        ids=[]
        if step.get("tool") and step["tool"]!="tool_router":
            ids.append(step["tool"])
        for key in ("tools","choices","conditional_tools"):
            ids += list(step.get(key,[]))
        return ids
    return []

def plan_pipeline(name,snap=None):
    cat,dom=load(); snap=snap or snapshot()
    pipe=next((p for p in cat.get("pipelines",[]) if p["name"]==name),None)
    if pipe is None:
        return {"ok":False,"error":{"type":"unknown_pipeline","message":name}}
    tool_plans={}
    tool_order=[]
    for step in pipe.get("steps",[]):
        for tid in _tool_ids_in_step(step):
            if tid in {t["id"] for t in cat["tools"]}:
                tool_plans[tid]=plan_tool(tid,snap=snap)
                if tid not in tool_order:
                    tool_order.append(tid)
    domain_index={d["id"]:d for d in dom.get("domains",[])}
    domain_bundle=[]
    for did in pipe.get("domains",[]):
        if did in domain_index:
            d=domain_index[did]
            domain_bundle.append({
                "id":did,
                "reference":d.get("reference"),
                "template":d.get("template"),
                "purpose":d.get("purpose")
            })
    compound=next((b for b in dom.get("composition",{}).get("bundles",[])
                   if b.get("pipeline")==name),None)
    return {
        "ok":True,
        "schema":"advanced-lyricism.pipeline-plan.v1",
        "pipeline":name,
        "purpose":pipe.get("purpose"),
        "composition_bundle":compound.get("id") if compound else None,
        "domains":domain_bundle,
        "steps":pipe.get("steps",[]),
        "tool_order":tool_order,
        "tool_plans":tool_plans,
        "stage_artifacts":[
            {"stage":s.get("name"),"produces":s.get("produces")}
            for s in pipe.get("steps",[]) if isinstance(s,dict) and s.get("produces")
        ],
        "rule":"Integrate artifacts at every decision point, then continue every applicable stage and tool that can assist. Pass each output to its downstream consumers before the next decision point."
    }

def list_tools():
    cat,_=load(); snap=snapshot()
    rows=[]
    for t in cat["tools"]:
        st=tool_state(t,[],snap)
        rows.append({"id":t["id"],"class":t["class"],"domain":t.get("primary_domain"),"state":st["state"],"missing_required":st["missing_required"],"missing_preferred":st["missing_preferred"]})
    return {"schema":"advanced-lyricism.tool-list.v1","tools":rows}

def main():
    ap=argparse.ArgumentParser(description="Preflight and route Advanced Lyricism tools/pipelines.")
    g=ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--tool")
    g.add_argument("--pipeline")
    g.add_argument("--list",action="store_true")
    ap.add_argument("--uses",default="",help="Comma-separated conditional modes such as png,stem.")
    a=ap.parse_args()
    if a.list:
        d=list_tools()
    elif a.pipeline:
        d=plan_pipeline(a.pipeline)
    else:
        uses=[x.strip() for x in a.uses.split(",") if x.strip()]
        d=plan_tool(a.tool,uses=uses)
    print(json.dumps(d,indent=2,ensure_ascii=False))
    if not d.get("ok",True):
        return 2
    if a.tool and d.get("runtime",{}).get("state")=="blocked":
        return 3
    return 0

if __name__=="__main__":
    raise SystemExit(main())
