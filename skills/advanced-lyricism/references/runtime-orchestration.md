# Runtime Orchestration — Deep Reference
> Working template: `assets/templates/runtime-orchestration.md`
> Composition map: `assets/composition-matrix.md`
> Machine routes: `assets/tool-catalog.json` · `assets/dependency-manifest.json` · `assets/domain-registry.json`
> Planner: `scripts/tool_router.py`
> Capability probe: `scripts/dependency_check.py`
> `SKILL.md` routes here whenever scripts, dependencies, multi-domain composition or feedback loops are materially involved.
## 1. Composition role
This layer turns the selected composition graph into an executable tool chain whenever scripts, dependencies or multi-domain handoffs are involved.

- It receives the selected bundle/custom graph, supplied inputs, locked constraints and required output artifacts.
- It produces a dependency-aware pipeline plan, full/partial/blocked support states, stage artifacts and feedback routes.
- The paired template records how each tool output is consumed by the next craft decision rather than treating execution as a detached script sweep.

This layer keeps tool use **operationally truthful**.

A compound tool path has six separate questions:

1. Is this the right craft question for the tool?
2. Can the current runtime support the tool?
3. If support is partial, which claims remain valid?
4. Did execution satisfy the tool’s postconditions?
5. What decision is allowed after reading the output?
6. Which domains and downstream tools consume the resulting artifact, and which earlier layers must reopen if it changes?

Never collapse these into “the script ran.”
## 2. Runtime state model
Every tool plan resolves to one of three states.
### 2.1. FULL
`full` means all required and preferred capabilities for the requested mode are available.
A FULL tool can still be wrong for the artistic decision.
FULL means every requested runtime capability is available.
### 2.2. PARTIAL
`partial` means the script can return some valid measurements or observations while a preferred capability is unavailable.
Examples:
- syllable density is available while pronunciation-backed stress is not;
- rhyme-grid token positions are available while phonological similarity is not;
- articulation density is available while phoneme-transition analysis is not;
- lexical frequencies are available while PNG rendering is not requested/available.
PARTIAL output must expose:
- supported outputs;
- unavailable outputs;
- missing preferred capability;
- null/unavailable fields where a measurement does not exist.
A PARTIAL tool contributes every supported output to the craft pass. Keep unavailable fields unknown, then combine the supported measurements with other tools, close reading and audition.
### 2.3. BLOCKED
`blocked` means a required capability for the requested mode is absent.
Resolve an available provider or follow the declared fallback, while every other applicable tool and craft layer continues.

Examples:
- audio analysis without `numpy` + `librosa`;
- MIDI conversion without a MIDI parser;
- phonetic rhyme suggestion without a pronunciation dictionary.
BLOCKED is not failure of the lyric task.
It is a routing event.
## 3. Plan tool execution
Before every direct script call:
`python scripts/tool_router.py --tool <tool_id>`
For an intended multi-step workflow:
`python scripts/tool_router.py --pipeline <pipeline_name>`

Named compound routes:
- `lyric_compound` — lyric construction across every applicable method;
- `narrative_drill_compound` — adds causal scene construction under drill-specific constraints when that narrative work is central;
- `beat_locked_compound` — keep audio/MIDI/beat constraints live across every downstream layer;
- `hook_compound` — identity, changed return meaning, memory, contrast and performance;
- `revision_compound` — baseline, every relevant detector, multi-domain repair and recheck.
For an explicit “run through the scripts/tools” request:
`python scripts/tool_router.py --pipeline script_sweep`
The planner returns:
- tool class;
- primary domain;
- deep reference;
- paired template;
- script path;
- runtime state;
- missing capabilities;
- supported outputs;
- unavailable outputs in partial mode;
- fallback;
- command skeleton.
Use the plan internally before execution. Do not announce a pause, graph selection or capability administration unless the user asks for that detail.
## 4. Select the composition graph before selecting tools
Tool routing starts with a craft objective and its interacting layers, not a filename or isolated detector.

A genre label never selects the composition graph. Choose the graph from the work requested, then add the relevant genre-specific methods. “Drill” alone does not select `narrative_drill` or replace the universal methods already applicable to lyric writing, a beat-locked verse, a hook or revision.

Correct:
`write lyrics to this supplied drill beat`
→ select the lyric-writing graph, keeping the supplied beat authoritative
→ add the drill-specific beat, register, landing and delivery methods to the applicable craft methods
→ preflight the resulting route
→ run every applicable tool and pass each artifact to its downstream consumers.

Incorrect:
`there are lots of scripts`
→ run `workbench`
→ infer weaknesses from whatever numbers appear.

If the user explicitly asks to run scripts, route every named script and every additional operation whose input is available and whose method can assist the task, then pass each output to all downstream consumers.
## 5. Dependency is not the same as capability
A Python package is a provider.
A capability is what the tool actually needs.

Examples:
- `cmudict` package and bundled CMUdict can both provide `pronunciation_dictionary`;
- `wordcloud` provides optional PNG rendering, but lexical JSON does not depend on it;
- `nltk` is needed only when stemming mode is requested;
- `numpy` + `librosa` jointly provide audio feature analysis.
Route on capabilities, not package names.

This avoids unnecessary blocking when a bundled provider can satisfy the operation.
## 6. Bundled pronunciation fallback
Core rhyme/prosody tools must not depend on a remote environment happening to have `cmudict`.

The Skill ships:
`assets/phonology/cmudict.dict.gz`
with:
`assets/phonology/CMUDICT-LICENSE.txt`
Runtime precedence is:

1. explicit user pronunciation override;
2. installed `cmudict` package;
3. bundled CMUdict;
4. heuristic syllable count only.

CMUdict is primarily General American English.

For UK rap:
- user pronunciation outranks CMUdict;
- supplied recording outranks CMUdict;
- local/accent performance may invalidate a dictionary rhyme;
- combine dictionary coverage with supplied pronunciation, recordings and direct audition.
Unknown pronunciation must remain unknown.
Never invent phonemes to keep a tool “working.”
## 7. The unknown-is-not-zero rule
This is a hard invariant.

If a measurement is unavailable:
- rhyme similarity = `null`, not `0` or `1`;
- internal echo count = `null` when no comparable phonological pairs exist;
- rhyme-family coverage = `null` when there are no known end-word pronunciations;
- stress-grid projection = unavailable when stress coverage is insufficient;
- articulation phoneme issues = unavailable when phoneme data is absent.
`0` means the tool measured a valid quantity and found zero.
`null/unavailable` means the quantity could not be measured.
The agent must never diagnose a craft deficit from an unavailable field.
## 8. Tool-class semantics
### 8.1. Representation
Representation tools transform input into a stable intermediate form.

Examples:
- MIDI → music-event JSON;
- audio → audio-event JSON;
- text → phoneme/stress map;
- annotated lyric → delivery-event map.
Representation output may contain derived coordinates.
Preserve the source and label derived values.
### 8.2. Detection
Detectors surface a location, condition, or affordance.

Examples:
- possible suspension;
- rhyme relation;
- articulation congestion;
- candidate musical boundary.
A detector reports the candidate operation with its location, cue and confidence/limits. Test it against its craft function and the integrated lyric.
### 8.3. Generation / transformation
Generators create candidates.

Examples:
- rhyme suggestions;
- cadence geometries;
- word/clause permutations;
- concept mutations.
Use seeds where stochastic.
Record locked dimensions.
Selection happens separately.
### 8.4. Evaluation
Evaluators report bounded mechanical observations.

They may compare density, repetition, coverage, lineation, or other declared proxies.

Keep independent signals in their own units with coverage and failure modes visible, so their interactions remain inspectable during revision.
### 8.5. Aggregate evaluation
`workbench` integrates component diagnostics whenever a real draft exists and a cross-detector view can assist. Feed it every available component output, route its findings through the owning component tools and craft layers, then reintegrate the results.
## 9. Support gates
Every tool invocation has a support gate.

Before using output, ask:
- What measurement is valid?
- What claim would exceed the measurement?
- What coverage threshold is reported?
- Is the result full, partial, or unavailable?
- Is the current question inside the safe-claim set?
If the tool reports unsupported claims, record them as unavailable, route around the missing measurement, and continue through every method and tool that can still assist.

## Claim boundaries and runtime independence
- User observation, current-context research, deterministic tool output, and artistic judgement are different claim classes; none may silently substitute for another.
- Text tools report written structure; audio and rehearsal expose performed microtiming, breath, pitch and articulation; supplied material carries autobiographical context; audition and artistic judgement assess emotional and overall effect.
- Syntax checks cover syntax; schema checks cover structure; fixtures cover tested behaviour; render checks cover visible output; package parity covers byte identity. Combine those results with lyric audition and judgement.
- The portable core uses local references, templates, deterministic diagnostics, and declared optional providers. It requires no live lyric scraper, external lyric corpus, or lyric-generation model.
- Low-level providers handle low-level capabilities; lyric-specific interpretation remains explicit in the owning reference and tool contract.
## 10. Pronunciation-sensitive tools
The following operations depend on pronunciation input to different degrees.
### `phoneme_map`
Without pronunciation dictionary:
- syllable heuristics remain available;
- phonemes/stress remain unknown;
- rhyme remains unknown until pronunciation or direct audition resolves it.
### `prosody_map`
Without enough stress coverage:
- syllable density remains available;
- best stress-grid projections are withheld;
- clash/lapse absence cannot be claimed.
### `articulation_audit`
Without phoneme data:
- density risk remains available;
- phoneme-transition issue list is unavailable, not empty.
### `rhyme_grid`
Without comparable tails:
- opening/mid/ending token positions remain available;
- link similarity is `null`;
- active state is `null`;
- no-rhyme conclusions are prohibited.
### `craft_audit`
Without pronunciation input:
- line/word/density/repeated-end-word measurements remain available;
- phonological family/echo metrics are unavailable.
### `rhyme_suggester`
Without pronunciation dictionary:
- tool is BLOCKED;
- do not substitute written suffix guessing.
## 11. Music dependency routes
### MIDI
Preflight:
`python scripts/tool_router.py --tool midi_to_json`
If FULL:
`midi_to_json` → `music_structure` → decision point → optional `beat_affordance`.
If BLOCKED:
- preserve supplied or already available timing information;
- do not fabricate note events;
- continue text-first if the task still permits it.
### Audio
Preflight:
`python scripts/tool_router.py --tool audio_to_json`
Audio analysis requires the declared audio capability.

If BLOCKED:
- use supplied BPM when available;
- label it as externally supplied timing;
- do not invent onsets, beats, or spectral features.
## 12. Conditional dependencies
Some features are mode-specific.
### Lexical cloud PNG
`lexical_cloud` JSON is core.
PNG rendering requires `wordcloud`.

Plan with:
`python scripts/tool_router.py --tool lexical_cloud --uses png`
### Stemming
Ordinary lexical profile is core.
Stemming mode requires `nltk`.

Plan with:
`python scripts/tool_router.py --tool lexical_cloud --uses stem`
Conditional mode failure must not block the base tool.
## 13. Revision routing
When a user asks to improve an existing draft with scripts:

1. preflight `revision_compound` or `script_sweep`;
2. run a component-preserving baseline with `craft_audit` and, when useful, `workbench`;
3. run every applicable targeted detector and keep their support states separate;
4. map every supported defect to all owning domains in the composition graph;
5. run every repair generator and transformer that can assist while locking dimensions that already work;
6. re-run every music, form, sound or performance stage invalidated by the repair;
7. audition and compare the integrated candidate against the baseline;
8. loop backward until the layers reinforce one another and the task's success condition is met.

Preflight the full catalog when the user requests “the scripts.” Run every tool that can assist the current task; record tools that cannot run because their input or capability is unavailable.
## 14. Why aggregate-first fails
Aggregate-first is risky because:
- one missing dependency can contaminate several downstream numbers;
- unavailable metrics can look like zeros;
- unrelated diagnostics can distract from a strong draft;
- a low number may distract from stronger interacting craft priorities;
- repeated analysis can create technique pile-up.
The correct order is:
`objective → composition graph → full relevant preflight → staged artifacts → all assisting operations → integrated audition → feedback to every owning layer`
## 15. Pipeline decision points
A pipeline is not a shell script.
`assets/tool-catalog.json` contains explicit decision points.
At a decision point:
- inspect the previous observations and artifacts;
- integrate the current layer's artifacts and update the graph hypothesis;
- choose every next tool that can assist and pass its contribution forward;
- continue every applicable downstream stage;
- execute the remaining graph in information-dependency order while retaining every cross-layer constraint and useful artifact.
A deterministic pipeline may transform data.
A craft pipeline must preserve decisions between operations.
## 16. Execution receipt
Use `assets/templates/runtime-orchestration.md`.

Record:
- user request;
- complete craft objectives and questions;
- selected bundle/custom graph;
- ordered layers, domain intersections and artifact contracts;
- tool ids by stage;
- planner state;
- missing required/preferred capabilities;
- supported outputs;
- unavailable outputs;
- fallback;
- exact input;
- command;
- exit code;
- output schema;
- support state;
- accepted implication;
- rejected implication;
- downstream consumers and every feedback route.
This receipt lets another agent distinguish “tool ran” from “tool supported the claim.”
## 17. Exit codes
Use exit codes as runtime signals.
- `0` — execution completed within declared mode;
- `2` — invalid user/tool input;
- `3` — dependency/capability block;
- `1` — execution/runtime error.
A non-zero exit is not a reason to guess missing output.

Record the error and route to fallback/recovery.
## 18. Fallback hierarchy
When a tool is blocked:

1. use another provider for the same capability if declared;
2. contribute every supported output from partial modes and keep unavailable fields unknown;
3. use supplied lyrics, pronunciation, audio/MIDI, references, voice and constraints;
4. use existing observations already available;
5. switch to manual/close-reading analysis;
6. leave the unsupported measurement unknown and continue the lyric work through supplied material, close reading, rehearsal, alternate representations, generators, and artistic judgement.

When pronunciation remains unavailable, label spelling similarity as a lexical clue and continue with manual pronunciation, supplied delivery, and direct audition.
## 19. Postconditions
After execution verify:
- expected JSON schema appears;
- support/status block exists when the tool can degrade;
- no `null` field is interpreted as zero;
- coverage is sufficient for the intended claim;
- output corresponds to the actual input file/version;
- seed is recorded for stochastic generation;
- source and derived data remain distinguishable.
If a postcondition fails, recover the missing capability or input, rerun the operation, or retain the valid component fields while rebuilding the invalid portion.
## 20. Transcript-derived regression cases
The first integration test exposed four failures.
### Case A — workbench selected first
Observed:
the agent announced aggregate workbench before naming a bounded hypothesis.

Correction:
`script_sweep` and `revision_targeted` preflight the catalog, execute the applicable component operations, and then integrate their outputs through workbench.
### Case B — missing pronunciation backend
Observed:
workbench reported zero dictionary coverage but the workflow continued into phonological conclusions.

Correction:
core pronunciation now has a bundled provider and every phonology-sensitive tool exposes support state.
### Case C — empty tails compared as perfect
Observed:
unknown rhyme tails were assigned perfect similarity.

Correction:
empty phoneme sequence similarity is never perfect; `rhyme_grid` emits `null` similarity for non-comparable anchors.
### Case D — unavailable measurements looked negative
Observed:
zero internal echoes / zero family coverage were read as weak rhyme glue.

Correction:
unmeasurable phonological metrics are `null/unavailable`, with those unavailable outputs carried into workbench.

These cases are release-blocking regression fixtures.
## 21. Cross-file handoffs
- `references/revision-evaluation.md` — diagnosis, candidate comparison, integration and completion checks for drafts.
- `references/rhyme-phonology.md` — pronunciation, rhyme and phonological interpretation.
- `references/prosody-flow.md` — density, stress, bar-line and cadence decisions.
- `references/musical-representation.md` — MIDI/audio representation and music structure.
- `references/performance-delivery.md` — rehearsal, breath, stress and delivery.
- `references/creative-operations.md` — seeded generation/transform selection.
Hand off the execution receipt, not a prose dump of every tool output.
## 22. Completion criteria
- [ ] A craft objective and composition graph were named before the tools.
- [ ] Every tool was planned through `tool_router.py`.
- [ ] Runtime state was FULL/PARTIAL/BLOCKED.
- [ ] Missing capabilities were handled before interpretation.
- [ ] Unknown values remained unknown.
- [ ] Partial outputs were interpreted at their reported coverage.
- [ ] The tool class was interpreted correctly.
- [ ] A pipeline integrated artifacts at decision points and continued every applicable stage.
- [ ] Workbench integrated every available component output after the component operations ran.
- [ ] Generated candidates were selected separately.
- [ ] Output schema/postconditions were checked.
- [ ] Accepted/rejected implications were recorded.
- [ ] Every stage received its explicit upstream artifacts.
- [ ] Each defect reopened every owning domain, not merely the last tool used.
