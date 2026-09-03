#!/usr/bin/env python3
"""Report runtime providers/capabilities and optionally enforce selected capabilities."""
from __future__ import annotations
import argparse,json
from runtime_capabilities import snapshot

def main():
    ap=argparse.ArgumentParser(description="Check Advanced Lyricism runtime capabilities.")
    ap.add_argument("--required",default="",help="Comma-separated capability ids that must be available.")
    ap.add_argument("--providers",default="",help="Comma-separated provider ids to report prominently.")
    a=ap.parse_args()
    d=snapshot()
    req=[x.strip() for x in a.required.split(",") if x.strip()]
    bad=[x for x in req if not d["capabilities"].get(x,{}).get("available")]
    d["required"]=req
    d["required_missing"]=bad
    if a.providers:
        names=[x.strip() for x in a.providers.split(",") if x.strip()]
        d["selected_providers"]={x:d["providers"].get(x,{"available":False,"unknown":True}) for x in names}
    print(json.dumps(d,indent=2))
    return 3 if bad else 0

if __name__=="__main__":
    raise SystemExit(main())
