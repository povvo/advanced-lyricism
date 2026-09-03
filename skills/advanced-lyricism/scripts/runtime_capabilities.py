#!/usr/bin/env python3
"""Runtime capability inspection for Advanced Lyricism."""
from __future__ import annotations
import importlib.util
import json
import os
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"assets"/"dependency-manifest.json"

def manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))

def disabled():
    return {x.strip().lower() for x in os.environ.get("ADVANCED_LYRICISM_DISABLE_PROVIDERS","").split(",") if x.strip()}

def provider_status(name,spec):
    dis=disabled()
    if name.lower() in dis:
        return {"name":name,"available":False,"disabled_for_test":True}
    kind=spec.get("kind")
    if kind=="bundled_asset":
        p=ROOT/spec["path"]
        return {"name":name,"available":p.exists(),"kind":kind,"path":spec["path"],"bytes":p.stat().st_size if p.exists() else None}
    if kind=="python_module":
        module=spec.get("module",name)
        ok=importlib.util.find_spec(module) is not None
        return {"name":name,"available":ok,"kind":kind,"module":module}
    return {"name":name,"available":False,"kind":kind,"error":"unknown provider kind"}

def snapshot():
    m=manifest()
    providers={name:provider_status(name,spec) for name,spec in m["providers"].items()}
    caps={}
    for name,spec in m["capabilities"].items():
        any_of=spec.get("any_of",[])
        all_of=spec.get("all_of",[])
        any_ok=any(providers.get(x,{}).get("available") for x in any_of) if any_of else True
        all_ok=all(providers.get(x,{}).get("available") for x in all_of) if all_of else True
        caps[name]={
            "available": bool(any_ok and all_ok),
            "providers_available":[x for x in any_of+all_of if providers.get(x,{}).get("available")],
            "missing":[x for x in all_of if not providers.get(x,{}).get("available")],
            "notes":spec.get("notes")
        }
    return {"schema":"advanced-lyricism.runtime-capabilities.v1","providers":providers,"capabilities":caps}

def tool_state(tool, uses=None, snap=None):
    snap=snap or snapshot()
    rt=tool.get("runtime",{})
    missing_required=[c for c in rt.get("required_capabilities",[]) if not snap["capabilities"].get(c,{}).get("available")]
    missing_preferred=[c for c in rt.get("preferred_capabilities",[]) if not snap["capabilities"].get(c,{}).get("available")]
    conditional=[]
    for use in uses or []:
        cap=(rt.get("conditional_capabilities") or {}).get(use)
        if cap and not snap["capabilities"].get(cap,{}).get("available"):
            conditional.append({"use":use,"capability":cap})
    if missing_required or conditional:
        state="blocked"
    elif missing_preferred:
        state="partial"
    else:
        state="full"
    return {
        "state":state,
        "missing_required":missing_required,
        "missing_preferred":missing_preferred,
        "missing_conditional":conditional,
        "safe_claims":rt.get("safe_claims",[]),
        "partial_forbidden_claims":rt.get("partial_forbidden_claims",[]),
        "fallback":rt.get("fallback")
    }

if __name__=="__main__":
    print(json.dumps(snapshot(),indent=2))
