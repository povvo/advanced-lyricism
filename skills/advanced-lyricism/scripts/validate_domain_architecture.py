#!/usr/bin/env python3
"""Validate domain, tool, reference and template architecture."""
from pathlib import Path
import json, sys

ROOT=Path(__file__).resolve().parents[1]
errors=[];warnings=[]

reg_path=ROOT/"assets/domain-registry.json"
cat_path=ROOT/"assets/tool-catalog.json"
dep_path=ROOT/"assets/dependency-manifest.json"
matrix_path=ROOT/"assets/composition-matrix.md"

reg=json.loads(reg_path.read_text()) if reg_path.exists() else {"domains":[]}
cat=json.loads(cat_path.read_text()) if cat_path.exists() else {"tools":[]}
dep=json.loads(dep_path.read_text()) if dep_path.exists() else {"providers":{},"capabilities":{}}

if not reg_path.exists():errors.append("missing assets/domain-registry.json")
if not cat_path.exists():errors.append("missing assets/tool-catalog.json")
if not dep_path.exists():errors.append("missing assets/dependency-manifest.json")
if not matrix_path.exists():errors.append("missing assets/composition-matrix.md")
pair_index_path=ROOT/"assets/reference-template-index.md"
if not pair_index_path.exists():errors.append("missing assets/reference-template-index.md")

domain_ids={d.get("id") for d in reg.get("domains",[])}
tool_ids={t.get("id") for t in cat.get("tools",[])}
pipeline_ids={p.get("name") for p in cat.get("pipelines",[])}

if len(domain_ids)!=len(reg.get("domains",[])):errors.append("duplicate domain ids")
if len(tool_ids)!=len(cat.get("tools",[])):errors.append("duplicate tool ids")
if len(pipeline_ids)!=len(cat.get("pipelines",[])):errors.append("duplicate pipeline ids")
if len(domain_ids)!=15:errors.append(f"expected 15 domains, found {len(domain_ids)}")
if "runtime-orchestration" not in domain_ids:errors.append("missing runtime-orchestration domain")
if "tool_router" not in tool_ids:errors.append("missing tool_router operation")
if "evidence-provenance" in domain_ids:errors.append("deleted provenance domain must not return to runtime")
if reg.get("schema")!="advanced-lyricism.domain-registry.v2":errors.append("domain registry must use composition schema v2")

# Composition graph must cover every domain and resolve every layer, edge and bundle.
composition=reg.get("composition",{})
if composition.get("matrix")!="assets/composition-matrix.md":errors.append("composition graph does not route to assets/composition-matrix.md")
layers=composition.get("layers",[])
layer_ids={x.get("id") for x in layers}
if len(layer_ids)!=len(layers):errors.append("duplicate composition layer ids")
layer_domain_ids=[]
for layer in layers:
    for did in layer.get("domains",[]):
        layer_domain_ids.append(did)
        if did not in domain_ids:errors.append(f"composition layer {layer.get('id')}: unknown domain {did}")
    for target in layer.get("feeds",[]):
        if target not in layer_ids:errors.append(f"composition layer {layer.get('id')}: unknown feed layer {target}")
if set(layer_domain_ids)!=domain_ids:
    errors.append(f"composition layers do not cover all domains: missing={sorted(domain_ids-set(layer_domain_ids))} extra={sorted(set(layer_domain_ids)-domain_ids)}")
if len(layer_domain_ids)!=len(set(layer_domain_ids)):errors.append("a domain appears in more than one primary composition layer")

edges=composition.get("edges",[])
for i,edge in enumerate(edges):
    if edge.get("from") not in domain_ids:errors.append(f"composition edge {i}: unknown from domain {edge.get('from')}")
    if edge.get("to") not in domain_ids:errors.append(f"composition edge {i}: unknown to domain {edge.get('to')}")
    if edge.get("from")==edge.get("to"):errors.append(f"composition edge {i}: self edge")
    if not edge.get("relation") or not edge.get("artifact"):errors.append(f"composition edge {i}: missing relation/artifact")

bundles=composition.get("bundles",[])
bundle_ids={b.get("id") for b in bundles}
if len(bundle_ids)!=len(bundles):errors.append("duplicate composition bundle ids")
for bundle in bundles:
    if bundle.get("pipeline") not in pipeline_ids:errors.append(f"bundle {bundle.get('id')}: unknown pipeline {bundle.get('pipeline')}")
    flattened=[did for stage in bundle.get("stages",[]) for did in stage]
    for did in flattened:
        if did not in domain_ids:errors.append(f"bundle {bundle.get('id')}: unknown domain {did}")
    if not flattened:errors.append(f"bundle {bundle.get('id')}: no staged domains")

for forbidden in (ROOT/"references/evidence-provenance.md", ROOT/"assets/templates/evidence-provenance.md"):
    if forbidden.exists():errors.append(f"build-only provenance file present in runtime: {forbidden.relative_to(ROOT)}")

for d in reg.get("domains",[]):
    did=d["id"];rp=ROOT/d["reference"];tp=ROOT/d["template"]
    if not rp.exists():errors.append(f"{did}: missing reference {d['reference']}")
    if not tp.exists():errors.append(f"{did}: missing template {d['template']}")
    if rp.exists():
        txt=rp.read_text(errors="replace");size=len(txt.encode());lines=len(txt.splitlines())
        if size<8000:errors.append(f"{did}: reference lacks a deep method body ({size} bytes)")
        if lines<200:errors.append(f"{did}: reference lacks enough structured method detail ({lines} lines)")
        required_sections=["## 1. Composition role"]
        if did!="runtime-orchestration":
            required_sections += ["## 2. Core craft model","## 5. Working variables","## 6. Template contract","## 7. Script routes","## 8. Cross-file handoffs","## 9. Failure modes","Topology"]
        for section in required_sections:
            if section not in txt:errors.append(f"{did}: missing method section {section}")
        if d["template"] not in txt:errors.append(f"{did}: reference does not link paired template")
        if "assets/tool-catalog.json" not in txt:errors.append(f"{did}: reference does not link tool catalog")
        if "assets/composition-matrix.md" not in txt:errors.append(f"{did}: reference does not link composition matrix")
    if tp.exists():
        template_text=tp.read_text(errors="replace")
        if d["reference"] not in template_text:errors.append(f"{did}: template does not link paired reference")
        if did!="runtime-orchestration" and "## Quick operating card" not in template_text:
            errors.append(f"{did}: v7 operating craft card is missing")
    for tid in d.get("primary_tools",[])+d.get("secondary_tools",[]):
        if tid not in tool_ids:errors.append(f"{did}: unknown tool {tid}")

# Preservation floor: these are v7 craft mechanisms, not source/provenance
# bookkeeping. Current references may expand them, but may not silently lose them.
craft_floor={
    "concept-architecture":["pressure before topic","technique budget","semantic fields before rhyme fields","collision: two domains","contradiction holding","feedback loops and delay","path dependence","candidate selection and continued development"],
    "lexical-engineering":["escape the orthographic trap","articulatory families","metrical filtering","mosaic / phrase rhyme","word archaeology","semantic-change mechanisms","sound-law tests","morphology and formation history","derivation-chain discipline"],
    "rhyme-phonology":["rhyme unit","vowel/stress matching","rhyme grid","internal rhyme grid","delayed resolution","accent and pronunciation","syllable structure","three-position rhyme grid"],
    "prosody-flow":["stress alignment","cadence families","bar-line behaviour","rhyme placement vs syntax","gear changes","breath and delivery notation","advanced line-boundary control","soft enjambment","suspension","run-on","uk drill landing and deviation"],
    "musical-representation":["raw midi data","derived coordinates","partwise and timewise views","meter is hierarchical","grouping cues","same / different","sustain","counterpoint"],
    "performance-delivery":["performance parameters","delivery notation","breath as rhythm","lexical, performed, musical","consonant attack and vowel field","ahead","behind","gear changes","ad-libs","pitch contour","emotional delivery"],
    "narrative-scene":["pressure, agency, and opposition","trigger vs condition","sequence is load-bearing","information timing","micro-scening","lyric camera","externalise the internal","perspective mapping","violence and transgression","action as argument","impact stack","event, state, and transition"],
    "rhetoric-impact":["surface-first entendre","triangulated meaning","punchline architecture","collision and re-signification","uk drill collision palette","metaphor-locked rhyme","incongruity","deadpan","inversion","contradiction","callback","understatement","dramatic irony","impact ladder"],
    "voice-register":["voice as system","preserve supplied voice","containment","psychological positions","sublimation","emotional externalisation","integrative complexity","blind spots","mle / london registers","code-switching","euphemistic irony","social computation","mle-specific controls","uk drill delivery positions"],
    "hook-song-form":["hook function","archetypes","genre-conditioned hook modes","compression","repetition legitimises","repetition-with-difference","the gap","drop / return placement","verse-hook contrast","signposts","serial logic","motif return","pattern break","negative space"],
    "genre-beat-fit":["uk drill lane controls","uk drill landing and section profile","grime","ny drill","dark trap","melodic rap/trap","boom bap","spoken/free meter","beat interaction","line-ending profile","technique budgets","uk drill affordances","separate tempo from feel","counterpoint"],
    "revision-evaluation":["eight passes","uk drill compound pass","out-loud protocol","meaning test","predictability test","filler test","anti-pattern library","polishing symptoms before upstream cause","simplification cascade","candidate selection","user preference update","close-reading revision","mechanical indicators","executable opportunity pass","rewrite thresholds"],
    "context-research":["separate input types","artist reference -> properties","input priority","scene graph","triangulate","mle query translation","audio/metadata reconciliation","taste learning","runtime boundary"],
    "creative-operations":["four operation classes","generator vs transformer","parameter isolation","computational creativity primitives","weighted grammar","permutation","random walk","mutation","crossover","feedback","tool invocation map","seed discipline","selection hierarchy"],
    "runtime-orchestration":["preflight","runtime state model","unknown-is-not-zero","tool-class semantics","claim boundaries","pronunciation-sensitive tools","music dependency routes","conditional dependencies","decision points","exit codes","fallback","postconditions","regression cases"],
}
template_card_floor={
    "concept-architecture":["i want x, but y makes wanting it dangerous","rapid cadence vs image complexity","the same image means one thing before the turn"],
    "lexical-engineering":["preserve the vowel, relax coda","audible stressed anchors","comparable phrase duration"],
    "rhyme-phonology":["answer an end rhyme internally next line","return an old family after a break","the line is clever only when annotated"],
    "prosody-flow":["where is the musical accent","internal rhyme answering percussion","one plain declarative line"],
    "musical-representation":["retain events that contradict the assumed grid","allow the ear to revise the model","does the old pattern now mean something different"],
    "performance-delivery":["make a dense run physically possible","secondary vocal","long vowels where sustain or pitch movement has room"],
    "narrative-scene":["what later reveal reclassifies an earlier detail","wide:","grief -> saved messages"],
    "rhetoric-impact":["setup constraint","property-based comparison revealed late","mistaken identity/reclassification"],
    "voice-register":["low overt editorialising","emotion visible through behaviour/detail","vulnerability -> exact physical/relational detail"],
    "hook-song-form":["changing one word while keeping cadence","changing pronoun/addressee","disclose to listener before speaker"],
    "genre-beat-fit":["profiles are priors, not laws","uk rap/drill craft can include"],
    "revision-evaluation":["repeated orthographic suffix","maintaining genre costume","explaining a reference the line failed to make legible"],
    "context-research":["separate observation / inference / decision","preserve date, confidence and uncertainty","detector score into craft proof"],
    "creative-operations":["wording fixed -> vary cadence","scene fixed -> vary viewpoint","content fixed -> vary delivery notation"],
}
for did,markers in craft_floor.items():
    domain=next((d for d in reg.get("domains",[]) if d.get("id")==did),None)
    if not domain:continue
    pair_text="\n".join((ROOT/domain[key]).read_text(errors="replace") for key in ("reference","template")).lower()
    for marker in markers:
        if marker not in pair_text:errors.append(f"{did}: v7 craft floor missing {marker!r}")
for did,markers in template_card_floor.items():
    domain=next((d for d in reg.get("domains",[]) if d.get("id")==did),None)
    if not domain:continue
    template_text=(ROOT/domain["template"]).read_text(errors="replace").lower()
    for marker in markers:
        if marker not in template_text:errors.append(f"{did}: restored operating card missing {marker!r}")

for t in cat.get("tools",[]):
    tid=t["id"]
    if t.get("primary_domain") not in domain_ids:
        errors.append(f"tool {tid}: unknown primary_domain {t.get('primary_domain')}")
    for key in ("primary_reference","primary_template","script","runtime","cli"):
        if key not in t:errors.append(f"tool {tid}: missing {key}")
    for key in ("primary_reference","primary_template","script"):
        path=t.get(key)
        if path and not (ROOT/path).exists():errors.append(f"tool {tid}: path missing {path}")
    rt=t.get("runtime",{})
    for cap in rt.get("required_capabilities",[])+rt.get("preferred_capabilities",[])+list((rt.get("conditional_capabilities") or {}).values()):
        if cap not in dep.get("capabilities",{}):errors.append(f"tool {tid}: unknown capability {cap}")
    if not rt.get("safe_claims"):warnings.append(f"tool {tid}: no safe_claims declared")

def step_tool_ids(step):
    if isinstance(step,str):
        if step.startswith("tool_router:"):return [step.split(":",1)[1]]
        return [step] if step in tool_ids else []
    if not isinstance(step,dict):return []
    ids=[]
    if step.get("tool") and step.get("tool")!="tool_router":ids.append(step["tool"])
    for key in ("tools","choices","conditional_tools"):ids.extend(step.get(key,[]))
    return ids

for pipe in cat.get("pipelines",[]):
    pname=pipe.get("name")
    for did in pipe.get("domains",[]):
        if did not in domain_ids:errors.append(f"pipeline {pname}: unknown domain {did}")
    for step in pipe.get("steps",[]):
        if isinstance(step,dict):
            for did in step.get("domains",[]):
                if did not in domain_ids:errors.append(f"pipeline {pname}: stage unknown domain {did}")
        for tid in step_tool_ids(step):
            if tid not in tool_ids:errors.append(f"pipeline {pname}: unknown tool {tid}")

# Dependency providers referenced by capabilities must exist.
for cid,spec in dep.get("capabilities",{}).items():
    for provider in spec.get("any_of",[])+spec.get("all_of",[]):
        if provider not in dep.get("providers",{}):
            errors.append(f"capability {cid}: unknown provider {provider}")

# Router remains thin but must expose every domain pair and orchestration invariant.
skill=(ROOT/"SKILL.md").read_text(errors="replace")
skill_lines=len(skill.splitlines())
if skill_lines>160:warnings.append(f"SKILL router is thick ({skill_lines} lines)")
for d in reg.get("domains",[]):
    if d["reference"] not in skill or d["template"] not in skill:
        errors.append(f"router missing pair {d['id']}")
for needle in ("scripts/tool_router.py","assets/dependency-manifest.json","assets/composition-matrix.md",
               "assets/reference-template-index.md",
               "lyric_compound","narrative_drill_compound","beat_locked_compound",
               "hook_compound","revision_compound","Unavailable measurements MUST remain unknown/null"):
    if needle not in skill:errors.append(f"router missing runtime invariant: {needle}")
if "including work developed with artists, MUST remain first-class craft knowledge" not in skill:
    errors.append("router missing user and artist-developed craft preservation invariant")

runtime_text="\n".join(
    p.read_text(errors="replace")
    for base in (ROOT/"references", ROOT/"assets/templates")
    for p in base.glob("*.md")
)
runtime_prompt_text="\n".join([
    skill,
    runtime_text,
    *[(ROOT/path).read_text(errors="replace") for path in (
        "agents/openai.yaml", "assets/domain-registry.json", "assets/tool-catalog.json",
        "assets/composition-matrix.md", "assets/reference-template-index.md",
    )],
    *[p.read_text(errors="replace") for p in (ROOT/"scripts").glob("*.py")
      if p.name != "validate_domain_architecture.py"],
]).lower()
agent_facing_text="\n".join([
    skill,
    runtime_text,
    *[(ROOT/path).read_text(errors="replace") for path in (
        "agents/openai.yaml", "assets/composition-matrix.md",
        "assets/reference-template-index.md",
    )],
]).lower()
for marker in (
    "imitation presets", "clone a living artist", "living artist to a preset",
    "copyrighted surface style", "permission to imitate", "artist corpus leakage",
    "recognizable artist phrasing", "never infer violence or gunshot vocabulary",
    "when the brief licenses a hard-content", "content explicitly licensed by the brief",
    "ethical and aesthetic decision", "morality or slang density",
    "use this file when the domain can materially change", "smallest domain bundle",
    "smallest operation", "smallest script", "smallest relevant input",
    "only one or two next tools", "why that tool is smaller", "full-stack lyric",
    "complete lyric", "full lyric", "fill only fields that can change",
    "stop when another domain becomes the bottleneck", "secondary only when needed",
    "next domain routed only if still necessary", "host-agnostic",
    "without inventing a universal", "not a universal numeric",
    "if the answer would not change a craft decision, stop",
    "record only decision-changing observations", "execute only queries that can change",
    "template contains only decision-relevant state", "state to discard",
    "stop if the question is answered", "abandon the unsupported claim",
    "candidate stop rule", "stop once one candidate", "stop when one option",
    "skip png or stemming", "excluded domain and concrete non-applicability",
    "excluded tools and concrete non-applicability", "deep_lyric_compound",
    "do not complete every pass at equal depth", "fix the lowest important dimension first",
    "revise only the repeated failures", "mandatory full-catalog",
    "full-catalog applicability/preflight", "not the first command in an open-ended script sweep",
    "late aggregator", "not total lyric quality", "universal lyric-quality score",
):
    if marker in runtime_prompt_text:
        errors.append(f"rejected governance or narrow-routing language returned to runtime: {marker}")
for marker in ("evidence", "provenance", "safe claims", "forbidden claims"):
    if marker in agent_facing_text:
        errors.append(f"rejected accounting/governance label returned to agent-facing craft material: {marker}")
for stale in (
    "evidence-provenance.md", "genre-profiles.md", "concept-engine.md", "agent-tooling.md",
    "assets/templates/bar-grid.md", "assets/templates/context-brief.md",
    "assets/templates/hook-variation-map.md", "assets/templates/revision-scorecard.md",
    "assets/templates/scene-sequence-board.md", "assets/templates/sound-cloud.md",
    "assets/templates/word-archaeology.md",
):
    if stale in runtime_text:errors.append(f"stale or provenance-shaped runtime route: {stale}")

for marker in (
    "## Key Sources", "Evidence Quality Assessment", "Recommended Deep Reading List",
    "## Practitioner corpus", "## Academic anchors", "## Archive accounting",
):
    if marker in runtime_text:errors.append(f"source/provenance section present in runtime: {marker}")

result={"ok":not errors,"errors":errors,"warnings":warnings,
        "metrics":{"skill_lines":skill_lines,"domains":len(domain_ids),"tools":len(tool_ids),
                   "layers":len(layers),"edges":len(edges),"bundles":len(bundles),"pipelines":len(pipeline_ids),
                   "reference_files":len(list((ROOT/"references").glob("*.md"))),
                   "template_files":len(list((ROOT/"assets/templates").glob("*.md"))),
                   "scripts":len(list((ROOT/"scripts").glob("*.py"))) }}
print(json.dumps(result,indent=2))
sys.exit(0 if not errors else 1)
