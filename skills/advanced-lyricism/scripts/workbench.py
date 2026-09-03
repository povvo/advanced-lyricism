#!/usr/bin/env python3
"""Integrate phonology, prosody, technique, articulation, lexical, delivery and craft diagnostics."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from lyric_utils import read_text_arg,configure_pronunciation_overrides
from phoneme_map import analyse as phoneme_analyse
from prosody_map import analyse as prosody_analyse
from technique_opportunity import opportunity
from articulation_audit import analyse as articulation_analyse
from lexical_cloud import profile as lexical_profile
from delivery_notation import parse as delivery_parse
from craft_audit import analyse as craft_analyse
from beat_affordance import analyse as beat_analyse
from runtime_capabilities import snapshot

def component_state(value):
    if isinstance(value,dict) and "support_status" in value:
        es=value["support_status"]
        return {"state":es.get("state","full"),"safe_claims":es.get("safe_claims",[]),"forbidden_claims":es.get("forbidden_claims",[])}
    return {"state":"full","safe_claims":[],"forbidden_claims":[]}

def run(text,bpm=140.0,subdivision=16,structure=None,start_bar=1):
    lex,_=lexical_profile(text,top=40,stem=False)
    components={
        "phonology":phoneme_analyse(text),
        "prosody":prosody_analyse(text,bpm,subdivision),
        "technique_opportunities":opportunity(text),
        "articulation":articulation_analyse(text,bpm),
        "lexical":lex,
        "delivery":delivery_parse(text),
        "craft_audit":craft_analyse(text,bpm),
    }
    if structure is not None:
        try:components["beat_affordance"]=beat_analyse(text,structure,start_bar)
        except Exception as e:components["beat_affordance"]={"error":{"type":type(e).__name__,"message":str(e)}}
    statuses={k:component_state(v) for k,v in components.items()}
    forbidden=sorted({x for st in statuses.values() for x in st.get("forbidden_claims",[])})
    states=[st["state"] for st in statuses.values()]
    overall="blocked" if states and all(s=="blocked" for s in states) else "partial" if any(s in {"partial","unavailable","blocked"} for s in states) else "full"
    return {
        "schema":"advanced-lyricism.workbench.v2",
        "role":"late_aggregate_confirmation",
        "settings":{"bpm":bpm,"subdivision":subdivision},
        "runtime_capabilities":snapshot(),
        "support_status":{
            "state":overall,
            "component_status":statuses,
            "forbidden_claims":forbidden,
        "interpretation_rule":"A null/unavailable metric leaves that dimension unknown. Each partial component supports its declared claims and marks the remaining claims unavailable."
        },
        **components,
        "routing_rule":"Run component tools and workbench in information-dependency order, then pass every component and aggregate observation to all owning domains.",
        "selection_rule":"Map the complete supported defect and opportunity set, integrate interactions across components, and keep unavailable dimensions open for other methods and audition."
    }

def main():
    ap=argparse.ArgumentParser(description="Integrate phonology, prosody, technique, articulation, lexical, delivery and craft diagnostics.")
    g=ap.add_mutually_exclusive_group();g.add_argument("-i","--input",type=Path);g.add_argument("-t","--text")
    ap.add_argument("--bpm",type=float,default=140.0);ap.add_argument("--subdivision",type=int,default=16,choices=[4,8,12,16,24,32])
    ap.add_argument("--structure",type=Path);ap.add_argument("--start-bar",type=int,default=1)
    ap.add_argument("--pronunciation-json",type=Path);ap.add_argument("--summary",action="store_true",help="Emit compact component statuses and aggregate mechanical summaries.");ap.add_argument("-o","--output",type=Path);a=ap.parse_args()
    if a.bpm<=0:
        print(json.dumps({"ok":False,"error":{"type":"input","message":"bpm must be > 0"}}));return 2
    try:
        if a.pronunciation_json:configure_pronunciation_overrides(a.pronunciation_json)
        st=json.loads(a.structure.read_text(encoding="utf-8")) if a.structure else None
        d=run(read_text_arg(a.input,a.text),a.bpm,a.subdivision,st,a.start_bar)
    except Exception as e:
        print(json.dumps({"ok":False,"error":{"type":type(e).__name__,"message":str(e)}}));return 1
    if a.summary:
        craft=d.get("craft_audit",{})
        pros=d.get("prosody",{})
        tech=d.get("technique_opportunities",{})
        art=d.get("articulation",{})
        deli=d.get("delivery",{})
        lex=d.get("lexical",{})
        d={
          "schema":d["schema"],"role":d["role"],"settings":d["settings"],
          "support_status":d["support_status"],
          "summary":{
            "craft":{
              "lines":craft.get("lines"),"words":craft.get("words"),
              "lexical_diversity":craft.get("lexical_diversity"),
              "syllables":craft.get("syllables"),
              "pronunciation":craft.get("pronunciation"),
              "end_rhyme":craft.get("end_rhyme"),
              "internal_sound":craft.get("internal_sound"),
              "lineation":craft.get("lineation")
            },
            "prosody":pros.get("summary"),
            "technique_opportunities":tech.get("summary"),
            "articulation":{"support_status":art.get("support_status"),
                            "risk_counts":{k:sum(1 for x in art.get("lines",[]) if x.get("density_risk")==k) for k in ("low","medium","high")}},
            "lexical":{"tokens":lex.get("tokens"),"types":lex.get("types"),"top_terms":lex.get("top_terms",[])[:12]},
            "delivery":deli.get("summary")
          },
          "routing_rule":d["routing_rule"],"selection_rule":d["selection_rule"]
        }
    s=json.dumps(d,ensure_ascii=False,indent=2)
    if a.output:a.output.write_text(s,encoding="utf-8")
    else:print(s)
    return 0
if __name__=="__main__":raise SystemExit(main())
