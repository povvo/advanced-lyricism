#!/usr/bin/env python3
"""Run fast regression tests for runtime routes and support states."""
from __future__ import annotations
import json, math, os, struct, sys, tempfile, wave
from contextlib import contextmanager
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))

import lyric_utils as lu
import runtime_capabilities as rc
import tool_router
import phoneme_map
import rhyme_grid
import craft_audit
import prosody_map
import articulation_audit
import workbench
import rhyme_suggester
import midi_to_json
import beat_metadata_reconcile
import context_query_plan
import preference_profile
import scene_graph
import semantic_field_map
import technique_opportunity
import wav_energy_probe
from vendor import mido as vendored_mido

@contextmanager
def providers_disabled(names):
    old=os.environ.get("ADVANCED_LYRICISM_DISABLE_PROVIDERS")
    os.environ["ADVANCED_LYRICISM_DISABLE_PROVIDERS"]=",".join(names)
    old_disable=set(lu._DISABLE)
    lu._DISABLE={x.lower() for x in names}
    lu._installed_cmu.cache_clear()
    lu._bundled_cmu.cache_clear()
    lu.configure_pronunciation_overrides(None)
    try:
        yield
    finally:
        if old is None: os.environ.pop("ADVANCED_LYRICISM_DISABLE_PROVIDERS",None)
        else: os.environ["ADVANCED_LYRICISM_DISABLE_PROVIDERS"]=old
        lu._DISABLE=old_disable
        lu._installed_cmu.cache_clear()
        lu._bundled_cmu.cache_clear()
        lu.configure_pronunciation_overrides(None)

def assert_true(cond,msg):
    if not cond: raise AssertionError(msg)

def validate_value(value,schema,path="$"):
    expected=schema.get("type")
    if expected:
        names=expected if isinstance(expected,list) else [expected]
        checks={
            "object":lambda x:isinstance(x,dict),
            "array":lambda x:isinstance(x,list),
            "string":lambda x:isinstance(x,str),
            "number":lambda x:isinstance(x,(int,float)) and not isinstance(x,bool),
            "integer":lambda x:isinstance(x,int) and not isinstance(x,bool),
            "boolean":lambda x:isinstance(x,bool),
            "null":lambda x:x is None,
        }
        assert_true(any(checks[name](value) for name in names),f"{path}: expected {names}, got {type(value).__name__}")
    if "const" in schema:
        assert_true(value==schema["const"],f"{path}: expected constant {schema['const']!r}, got {value!r}")
    if isinstance(value,dict):
        missing=[name for name in schema.get("required",[]) if name not in value]
        assert_true(not missing,f"{path}: missing {missing}")
        for name,child in schema.get("properties",{}).items():
            if name in value: validate_value(value[name],child,f"{path}.{name}")
    if isinstance(value,list) and isinstance(schema.get("items"),dict):
        for index,item in enumerate(value): validate_value(item,schema["items"],f"{path}[{index}]")

def validate_contract(filename,value):
    schema=json.loads((ROOT/"assets"/"schemas"/filename).read_text(encoding="utf-8"))
    validate_value(value,schema)
    return value

def unknown_text():
    return "glorptastic blenqzor\nsnarphotic trenzvul"

def main():
    tests=[]
    def record(name,fn):
        try:
            detail=fn() or {}
            tests.append({"name":name,"passed":True,"detail":detail})
        except Exception as e:
            tests.append({"name":name,"passed":False,"error":f"{type(e).__name__}: {e}"})

    record("empty_phoneme_sequences_are_not_perfect",test_empty_similarity)
    record("v7_support_state_api_remains_callable",test_v7_support_state_alias)
    record("bundled_cmudict_keeps_phonology_full_without_installed_package",test_bundled_cmudict)
    record("rhyme_grid_unknown_unknown_is_null_not_perfect",test_unknown_rhyme)
    record("craft_audit_unknown_phonology_is_null_not_zero",test_unknown_craft)
    record("prosody_with_unknown_stress_withholds_best_projection",test_unknown_prosody)
    record("articulation_without_phonemes_is_unavailable_not_clean",test_unknown_articulation)
    record("workbench_propagates_partial_support",test_partial_workbench)
    record("rhyme_suggester_blocks_without_pronunciation_capability",test_blocked_rhyme_suggester)
    record("script_sweep_preflights_full_catalog_before_decision",test_script_sweep)
    record("lyric_compound_pipeline_routes_all_domain_and_tool_layers",test_lyric_compound_pipeline)
    record("bundled_mido_converts_when_installed_mido_is_disabled",test_bundled_mido)
    record("adapted_text_and_context_tools_compose",test_adapted_text_context_tools)
    record("adapted_beat_tools_preserve_tempo_ambiguity",test_adapted_beat_tools)
    record("technique_opportunities_expose_signals",test_technique_signals)
    record("high_volume_tools_expose_summary_mode",test_summary_modes)

    passed=sum(t["passed"] for t in tests)
    result={"schema":"advanced-lyricism.runtime-regression.v1","passed":passed,"total":len(tests),
            "ok":passed==len(tests),"tests":tests}
    print(json.dumps(result,indent=2))
    return 0 if result["ok"] else 1

def test_empty_similarity():
    v=lu.sequence_similarity([],[])
    assert_true(v==0.0,v)
    return {"similarity":v}

def test_v7_support_state_alias():
    values=[0.0,0.5,0.85,1.0]
    current=[lu.support_state(value) for value in values]
    legacy=[lu.evidence_state(value) for value in values]
    assert_true(legacy==current,(legacy,current))
    return {"states":legacy,"alias":"evidence_state -> support_state"}

def test_bundled_cmudict():
    with providers_disabled(["cmudict"]):
        plan=tool_router.plan_tool("rhyme_grid")
        d=validate_contract("phoneme-map.schema.json",phoneme_map.analyse("light signs time mine"))
    assert_true(plan["runtime"]["state"]=="full",plan["runtime"])
    assert_true(d["support_status"]["dictionary_coverage"]>0.9,d["support_status"])
    assert_true(d["support_status"]["backend"]["provider"]=="bundled-cmudict",d["support_status"]["backend"])
    return {"router_state":"full","backend":"bundled-cmudict",
            "coverage":d["support_status"]["dictionary_coverage"]}

def test_unknown_rhyme():
    with providers_disabled(["cmudict","bundled_cmudict"]):
        d=rhyme_grid.analyse(unknown_text())
    assert_true(d["support_status"]["state"]=="unavailable",d["support_status"])
    assert_true(d["summary"]["unknown_links"]>0,d["summary"])
    assert_true(all(x["similarity"] is None and x["active"] is None for x in d["adjacent_position_links"]),
                d["adjacent_position_links"])
    return {"state":"unavailable","unknown_links":d["summary"]["unknown_links"]}

def test_unknown_craft():
    with providers_disabled(["cmudict","bundled_cmudict"]):
        d=craft_audit.analyse(unknown_text())
    assert_true(d["support_status"]["state"]=="unavailable",d["support_status"])
    assert_true(d["end_rhyme"]["family_coverage_of_known_endwords"] is None,d["end_rhyme"])
    assert_true(d["internal_sound"]["total_echo_pairs"] is None,d["internal_sound"])
    return {"state":"unavailable","family_coverage":None,"internal_echoes":None}

def test_unknown_prosody():
    with providers_disabled(["cmudict","bundled_cmudict"]):
        d=prosody_map.analyse(unknown_text())
    assert_true(d["support_status"]["state"]=="unavailable",d["support_status"])
    assert_true(all(x["projection_status"]=="unavailable_or_insufficient_coverage" for x in d["lines"]),d["lines"])
    return {"state":"unavailable","stress_coverage":d["support_status"]["stress_coverage"]}

def test_unknown_articulation():
    with providers_disabled(["cmudict","bundled_cmudict"]):
        d=articulation_audit.analyse(unknown_text())
    assert_true(d["support_status"]["state"]=="unavailable",d["support_status"])
    assert_true(all(x["issues"] is None for x in d["lines"]),d["lines"])
    return {"state":"unavailable","issues":None}

def test_partial_workbench():
    with providers_disabled(["cmudict","bundled_cmudict"]):
        d=workbench.run(unknown_text(),92.29,16)
    assert_true(d["support_status"]["state"]=="partial",d["support_status"])
    forbidden=" ".join(d["support_status"]["forbidden_claims"]).lower()
    assert_true("rhyme" in forbidden or "phonolog" in forbidden,forbidden)
    return {"state":"partial","forbidden_claims":len(d["support_status"]["forbidden_claims"])}

def test_blocked_rhyme_suggester():
    with providers_disabled(["cmudict","bundled_cmudict"]):
        plan=tool_router.plan_tool("rhyme_suggester")
        d=rhyme_suggester.suggest("light",5)
    assert_true(plan["runtime"]["state"]=="blocked",plan["runtime"])
    assert_true(d["support_status"]["state"]=="blocked",d)
    return {"router_state":"blocked","tool_state":"blocked"}

def test_script_sweep():
    d=tool_router.plan_pipeline("script_sweep")
    steps=d["steps"]
    catalog_i=next(i for i,x in enumerate(steps) if isinstance(x,dict) and x.get("type")=="catalog")
    decision_i=next(i for i,x in enumerate(steps) if isinstance(x,dict) and x.get("type")=="decision_point")
    catalog=json.loads((ROOT/"assets"/"tool-catalog.json").read_text(encoding="utf-8"))
    expected={x["id"] for x in catalog["tools"]}
    listed=set(steps[catalog_i]["tools"])
    assert_true(catalog_i<decision_i,(catalog_i,decision_i))
    assert_true(listed==expected,(listed,expected))
    assert_true(set(d["tool_plans"])==expected,set(d["tool_plans"]))
    assert_true("every applicable stage" in d["rule"].lower(),d["rule"])
    return {"catalog_step":catalog_i+1,"decision_step":decision_i+1,"preflighted_tools":len(expected)}

def test_lyric_compound_pipeline():
    d=tool_router.plan_pipeline("lyric_compound")
    expected={
        "midi_to_json","audio_to_json","phoneme_map","idea_lab","arc_generator",
        "lexical_cloud","word_rearranger","technique_opportunity","rhyme_suggester",
        "rhyme_grid","prosody_map","cadence_lab","articulation_audit",
        "delivery_notation","music_structure","beat_profile_summary","beat_affordance",
        "craft_audit","workbench","wav_energy_probe","beat_metadata_reconcile",
        "semantic_field_map","context_query_plan","scene_graph","preference_profile"
    }
    assert_true(len(d["domains"])==15,d["domains"])
    assert_true(set(d["tool_plans"])==expected,set(d["tool_plans"]))
    assert_true(set(d["tool_order"])==expected,d["tool_order"])
    assert_true(len(d["stage_artifacts"])>=6,d["stage_artifacts"])
    return {"pipeline":d["pipeline"],"domains":len(d["domains"]),
            "preflighted_tools":len(d["tool_plans"]),"stage_artifacts":len(d["stage_artifacts"])}

def test_bundled_mido():
    with tempfile.TemporaryDirectory() as td:
        midi=Path(td)/"fixture.mid"
        m=vendored_mido.MidiFile()
        t=vendored_mido.MidiTrack();m.tracks.append(t)
        t.append(vendored_mido.MetaMessage("set_tempo",tempo=vendored_mido.bpm2tempo(92),time=0))
        t.append(vendored_mido.MetaMessage("time_signature",numerator=4,denominator=4,time=0))
        t.append(vendored_mido.Message("note_on",note=60,velocity=90,time=0))
        t.append(vendored_mido.Message("note_off",note=60,velocity=0,time=480))
        m.save(midi)
        with providers_disabled(["mido"]):
            plan=tool_router.plan_tool("midi_to_json")
            d=midi_to_json.convert(midi)
    assert_true(plan["runtime"]["state"]=="full",plan["runtime"])
    assert_true(d["summary"]["notes"]==1,d["summary"])
    return {"router_state":"full","notes":1,"fallback_provider":"bundled_mido"}

def test_adapted_text_context_tools():
    fields=semantic_field_map.load_fields("uk-drill",None)
    mapped=validate_contract("semantic-field-map.schema.json",semantic_field_map.analyse("Court on the block, bread for the rent\nStill miss bro when the gates shut",fields,"uk-drill"))
    assert_true(mapped["summary"]["active_fields"]>=3,mapped["summary"])
    assert_true(mapped["field_collisions"],mapped)
    queries=validate_contract("context-query-plan.schema.json",context_query_plan.build_queries("peak in the ends",["usage","scene"],["primary","web","community"],"London","2026"))
    assert_true({x["term"] for x in queries["recognized_terms"]}>={"peak","ends"},queries["recognized_terms"])
    assert_true(queries["queries"],queries)
    graph=validate_contract("scene-graph.schema.json",scene_graph.analyse([
        {"source":"artist-a","target":"producer-b","relation":"worked-with"},
        {"source":"producer-b","target":"artist-c","relation":"produced-for"},
    ],["artist-a"],2,("artist-a","artist-c")))
    assert_true(len(graph["connection"]["path"])==2,graph["connection"])
    profile=validate_contract("preference-profile.schema.json",preference_profile.analyse([
        {"accepted":True,"features":{"deadpan":.9,"density":.4},"reason":"dry landing"},
        {"accepted":True,"features":{"deadpan":.8,"density":.5}},
        {"accepted":False,"features":{"deadpan":.1,"density":.9},"reason":"overpacked"},
        {"accepted":False,"features":{"deadpan":.2,"density":.8}},
    ]))
    directions={x["feature"]:x["preferred_direction"] for x in profile["feature_associations"]}
    assert_true(directions=={"deadpan":"higher","density":"lower"},directions)
    return {"semantic_fields":mapped["summary"]["active_fields"],"queries":len(queries["queries"]),"graph_path":2,"preferences":directions}

def test_adapted_beat_tools():
    metadata=validate_contract("beat-metadata-reconcile.schema.json",beat_metadata_reconcile.analyse({"schema":"fixture","pulse":{"bpm_candidate":140}},"70 BPM F# minor",2.0))
    best=metadata["comparison"]["tempo"]["best"]
    assert_true(metadata["comparison"]["tempo"]["state"]=="aligned",metadata)
    assert_true(best["relation"]=="metadata_half_of_measurement",best)
    with tempfile.TemporaryDirectory() as td:
        path=Path(td)/"pulse.wav"
        rate=8000
        with wave.open(str(path),"wb") as wav:
            wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(rate)
            samples=[]
            for i in range(rate*3):
                beat=(i%(rate//2))<400
                value=int((.75 if beat else .08)*32767*math.sin(2*math.pi*110*i/rate))
                samples.append(struct.pack("<h",value))
            wav.writeframes(b"".join(samples))
        profile=validate_contract("wav-energy-profile.schema.json",wav_energy_probe.analyse(path,.05))
    assert_true(profile["audio"]["duration_seconds"]==3.0,profile["audio"])
    assert_true(profile["energy_frames"] and profile["sections"],profile)
    assert_true(profile["pulse"]["half_double_time_unresolved"] is True,profile["pulse"])
    return {"metadata_relation":best["relation"],"wav_frames":len(profile["energy_frames"]),"pulse_candidate":profile["pulse"]["bpm_candidate"]}

def test_technique_signals():
    d=validate_contract("technique-opportunities.schema.json",technique_opportunity.opportunity("I left the key in\nthe door, then paused\nSame name in the rain\nSame name came again"))
    assert_true(d["opportunities"],d)
    assert_true(all("signals" in x and "evidence" not in x for x in d["opportunities"]),d["opportunities"])
    return {"opportunities":len(d["opportunities"]),"field":"signals"}

def test_summary_modes():
    files=["phoneme_map.py","rhyme_grid.py","prosody_map.py","articulation_audit.py","workbench.py"]
    missing=[]
    for name in files:
        text=(ROOT/"scripts"/name).read_text(encoding="utf-8")
        if "--summary" not in text: missing.append(name)
    assert_true(not missing,missing)
    return {"tools":files,"all_have_summary_flag":True}

if __name__=="__main__":
    raise SystemExit(main())
