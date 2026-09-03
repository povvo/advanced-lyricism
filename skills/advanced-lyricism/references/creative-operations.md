# Agent Tooling and Controlled Creativity — Deep Reference

> Working template: `assets/templates/creative-operations.md`
> Machine routes: `assets/domain-registry.json` · `assets/tool-catalog.json` · `assets/dependency-manifest.json` · runtime method `references/runtime-orchestration.md`
> This reference contains the domain method; its paired template carries the method through active lyric work.

## 1. Composition role

This layer coordinates representation, detection, generation, transformation and evaluation around the concrete craft question.

- It receives the current graph state, supplied creative material, locked dimensions and unresolved decisions.
- It produces bounded alternatives, structural maps and local tests for the craft layers that own the decision.
- The paired template keeps generation, comparison, audition and selection distinct while tools compound rather than overwrite one another.

## 2. Core craft model

The local tools are **craft instruments**, not miniature judges. They should make hidden structure inspectable, generate bounded alternatives, or test a concrete hypothesis. The agent remains responsible for meaning, taste, voice, context, and selection.

## Four operation classes

### 1. Representation
Convert opaque material into a stable intermediate form without deciding what it means.

Examples:
- MIDI -> note/event JSON with raw ticks, seconds, track/channel identity, tempo/meter maps and derived bar/slot coordinates;
- audio -> estimated beat/onset/energy/timbre JSON;; text -> phoneme/stress/syllable JSON;
- annotated bars -> performance-event JSON.

A representation tool should preserve source material and label every derived coordinate. It should not silently quantize, normalize accent, or infer artistic intention.

### 2. Detection
Find an observable condition or **opportunity**.

Examples:
- likely enjambment/suspension hinges;; stress-grid friction;
- consonant congestion;; phrase-boundary candidates;
- repetition or register imbalance;; density jumps.

Detection returns **location + observed signal + confidence/limits + a possible operation**. It does not say “this must be fixed.” A strong craft choice can look anomalous by design.

### 3. Generation / transformation
Produce alternatives while holding explicit constraints.

Examples:
- rearrange clauses while preserving the end word;; generate rhyme candidates from phoneme tails;
- create cadence slot patterns for a syllable budget;; mutate a concept along one structural dimension;
- permute a sequence;; generate bar-level tension/density curves.

Generation should be reproducible where randomness is involved. Use `--seed`. Never confuse candidate quantity with quality.

### 4. Evaluation
Stress-test a concrete draft or plan.

Examples:
- articulation screen;; delivery/breath notation audit;
- scheme/density audit;; aggregated workbench report.

Evaluation returns dimension-specific diagnostics and comparisons that can be auditioned against the lyric.

---

## Generator vs transformer

Separate generators from transformers.

A **generator** creates new structural material from rules or distributions.  
A **transformer** takes supplied material and changes one or more parameters.

For lyrics:
- grammar scaffold = generator;; clause rearrangement = transformer;
- rhyme suggestions = candidate generator constrained by sound;; cadence variants = generator constrained by syllable count;
- “move this scene from room -> street -> institution” = transformer;; callback mutation = transformer.

Prefer a transformer when the user already has strong material. It preserves identity and exposes *which* change caused the improvement.

---

## Parameter isolation

When a passage is weak, do not randomize everything.

Hold four dimensions constant and vary one:
- wording fixed -> vary cadence;; cadence fixed -> vary rhyme landing;
- image fixed -> vary distance/scale;; scene fixed -> vary viewpoint;
- hook words fixed -> vary omission/pause;; rhyme family fixed -> vary syntax;
- meaning fixed -> vary line break;; content fixed -> vary delivery notation.

Compare the isolated variants, retain every successful change, then build controlled combination variants so compatible improvements compound across dimensions.

### Why it matters
If meaning, rhyme, cadence, viewpoint, and register all change at once, the agent cannot infer why a candidate works. Parameter isolation turns ideation into **controlled creative search**.

---

## Computational creativity primitives

Use every primitive that can assist, sequencing controlled single-variable tests before combination variants and integrated audition.

### Weighted grammar
Use for concept scaffolds, section functions, pressure sequences and hook-return forms.

Example:
`setting -> pressure -> choice -> consequence -> residue`

### Permutation
Useful when the material exists but sequence may be weak.

Permute:
- scenes;; clauses;
- reveal order;; image order;
- hook fragments;; rhyme-family entry points.

Then ask whether causality, suspense, or emphasis improved.

### Random walk
Useful for gradual parameter movement:
- emotional exposure;; image distance;
- density;; tension;
- rhyme density.

A random walk should be bounded and seeded. It is a way to escape a perfectly linear arc, not a substitute for dramatic intention.

### Mutation
Change one property:
- scale;; viewpoint;
- syntax delay;; image distance;
- payoff position;; register;
- consequence;; sonic frame;
- delivery.

Mutation is especially useful when a line is competent but unsurprising.

### Crossover
Combine **structures**, not signatures:
- pressure arc from plan A + viewpoint strategy from plan B;; rhyme movement from A + scene sequence from B;
- hook invariant from A + return mutation from B.

### Feedback
After generation, evaluate and feed only the selected property back:
1. generate;
2. test;
3. choose;
4. lock the successful dimension;
5. regenerate another dimension.

This prevents “creative drift” where every iteration becomes unrelated.

---

## Tool invocation map

### Start with representation when input is opaque
- MIDI supplied -> `midi_to_json.py`; audio supplied -> `audio_to_json.py`
- unfamiliar pronunciation/rhyme problem -> `phoneme_map.py`; delivery-marked draft -> `delivery_notation.py`

### Invoke detectors for a named problem
- “where could enjambment/suspension work?” -> `technique_opportunity.py`; “why does this stumble?” -> `articulation_audit.py`
- “where is lexical stress fighting the grid?” -> `prosody_map.py`; “where does the instrumental change?” -> `music_structure.py`
- “what space/anchors does this bar offer?” -> `beat_affordance.py`; “is the rhyme grid only end-loaded?” -> `rhyme_grid.py`
- “what vocabulary dominates/changed?” -> `lexical_cloud.py`

### Invoke generators with constraints
- “other rhyme routes” -> `rhyme_suggester.py`; “reorder this without changing vocabulary much” -> `word_rearranger.py`
- “give me structural mutations” -> `idea_lab.py`; “design a section energy contour” -> `arc_generator.py`
- “show cadence geometries for 11 syllables” -> `cadence_lab.py`

### Integrate aggregate evaluation after component passes
Use `workbench.py` after there is a real draft. It is not a prewriting oracle.

---

## Seed discipline

For any stochastic operation:
- record seed;; record mode;
- record locked constraints;; keep the source text/plan;
- compare candidates against the same evaluation criteria.

If a useful result cannot be reproduced, the tool has failed as an agent component even if the result was interesting.

---

## Selection hierarchy

When tool outputs disagree, prioritize:
1. user intention and lived or supplied creative material;
2. semantic coherence;
3. voice/register;
4. performability by the intended speaker;
5. musical fit;
6. sonic/rhetorical sophistication;
7. heuristic scores.

A 0.95 rhyme score does not justify a meaningless line. A “stress mismatch” can be the point of a flow. An unusual lexical distribution may be a motif.

---

## Anti-patterns

- **Tool soup:** running every script on every draft; **Score worship:** summing independent heuristics into fake quality.
- **Grid absolutism:** assuming 16 equal slots are the music; **Dictionary accent:** overriding the speaker because CMUdict says otherwise.
- **Randomness as creativity:** producing many arbitrary variants; **Auto-repair:** detector silently rewrites the line.
- **Feature laundering:** presenting estimated audio tempo or boundary score as ground truth.

The desired agent behaviour is: **represent -> hypothesise -> operate -> audition -> evaluate -> select**.

## 4. Decision method

### 4.1. Frame
- Name the section function, hard constraints, and the complete set of craft objectives and questions; record them in `assets/templates/creative-operations.md`.

### 4.2. Baseline
- Describe the present behaviour before judging it; Record the decision in `assets/templates/creative-operations.md`.

### 4.3. Hinge
- Identify the full set of words, bars, events, and performance moments involved in the binding issue.
- Record the decision in `assets/templates/creative-operations.md`.

### 4.4. Mechanism
- Explain how the suspected variable creates the observed effect; Record the decision in `assets/templates/creative-operations.md`.

### 4.5. Isolate
- For causal comparison, hold strong dimensions fixed while varying each suspected lever separately; then combine every improvement that survives its isolated test and record the results in `assets/templates/creative-operations.md`.

### 4.6. Material and tool support
- Ground the decision in supplied creative material, direct reading or rehearsal, and every relevant representation, detector or generator.
- Record the decision in `assets/templates/creative-operations.md`.

### 4.7. Audition
- Compare baseline and candidate in the medium that matters; Record the decision in `assets/templates/creative-operations.md`.

### 4.8. Collateral
- Check meaning, voice, rhyme, rhythm, performance, sequence, and consequence as relevant.
- Record the decision in `assets/templates/creative-operations.md`.

### 4.9. Commit
- Keep the most effective change set that survives audition without analytical explanation; Record the decision in `assets/templates/creative-operations.md`.

### 4.10. Handoff
- Pass observations, locked decisions, open questions, and generated candidates into every connected domain that can use them.
- Record the decision in `assets/templates/creative-operations.md`.

## 5. Working variables

- **Operation Class** · **Hypothesis**
- **Seed**
- **Locked Dimensions**
- **Variable Dimension**
- **Candidate Count** · **Generator**
- **Transformer** · **Mutation**
- **Permutation** · **Collision**
- **Random Walk** · **Crossover**
- **Selection Criterion**
- **Expansion / Selection Rule** · **Trace**

## 6. Template contract

- Use `assets/templates/creative-operations.md` for working state, not this reference.
- Fill every field relevant to the task; keep baseline and candidate visible together.
- Anchor the decision to exact lines, bars or timestamps; fill from supplied material, direct observation, rehearsal, or verified context, and keep genuine unknowns blank.
- Log tool id, input scope, output limit, and accepted/rejected implication; Record seed and locked dimensions for generative operations.
- Update the template whenever rehearsal or a new observation disproves the current working model.

## 7. Script routes — preflight each listed tool with `python scripts/tool_router.py --tool <id>` before execution

### Primary
- `idea_lab` → `scripts/idea_lab.py`
  - Contribution: structural grammar, mutation, collision, permutation or random-walk exploration.
  - Class: `generation_transform`.
- `word_rearranger` → `scripts/word_rearranger.py`
  - Contribution: reorders supplied words and clauses to test syntax, emphasis and landing.
  - Class: `transform`.
- `arc_generator` → `scripts/arc_generator.py`
  - Contribution: a relative section curve for density/tension/exposure/etc..
  - Class: `generation`.
- `cadence_lab` → `scripts/cadence_lab.py`
  - Contribution: alternative slot geometries for a syllable budget.
  - Class: `generation`.
### Secondary
- `semantic_field_map` → `scripts/semantic_field_map.py`
  - Contribution: exposes field collisions and unmapped repeated language before generation or mutation.
  - Class: `detection`.
- `preference_profile` → `scripts/preference_profile.py`
  - Contribution: supplies user-selected feature directions when feedback history exists.
  - Class: `detection`.
- `rhyme_suggester` → `scripts/rhyme_suggester.py`
  - Contribution: phonetic/slant rhyme candidates without committing to meaning.
  - Class: `generation`.
- `lexical_cloud` → `scripts/lexical_cloud.py`
  - Contribution: vocabulary concentration, motif frequency or revision delta.
  - Class: `detection`.
- `workbench` → `scripts/workbench.py`
  - Contribution: aggregates component outputs after the targeted detectors and generators have run.
  - Class: `evaluation_aggregate`.

### Tool-class boundaries
- Representation keeps supplied material beside labelled derived structure; detectors map concrete conditions and opportunities with locations and confidence.
- Generators and transforms create controlled candidates; evaluation combines mechanical observations with close reading, audition and comparison.
- Support checks runtime/package state, not craft quality.

## 8. Cross-file handoffs

- `references/concept-architecture.md` ↔ `assets/templates/concept-architecture.md`
- `references/revision-evaluation.md` ↔ `assets/templates/revision-evaluation.md`
- `references/rhetoric-impact.md` ↔ `assets/templates/rhetoric-impact.md`
- `references/prosody-flow.md` ↔ `assets/templates/prosody-flow.md`
- `references/revision-evaluation.md` once the task becomes comparative revision.

## 9. Failure modes

Repair the named craft variable, audition the result, and recheck every layer it changes.

### Tool invoked without decision question

### Generation and evaluation conflated

### Unseeded stochastic output compared as if reproducible

### All dimensions varied at once

### Candidate explosion

### Randomness mistaken for creativity

### Detector output auto-applied

### Mechanical tool treated as judge

### Aggregation before local diagnosis

### Successful dimensions not locked

## 10. Completion

- [ ] Question is explicit and bounded.
- [ ] User constraints remain visible.
- [ ] Observation, inference, and choice are distinct.
- [ ] Template captures every task-relevant working variable and cross-domain handoff.
- [ ] Any tool matched its catalog condition.
- [ ] Estimates and uncertainty are labelled.
- [ ] Generation and selection were separated.
- [ ] Strong existing properties were preserved.
- [ ] Cross-domain side effects were checked.
- [ ] Output survives audition without the analysis.

## 11. Topology

- Template: `assets/templates/creative-operations.md`; Domain index: `assets/domain-registry.json`
- Tool index: `assets/tool-catalog.json`; Composition matrix: `assets/composition-matrix.md`
- Validator: `scripts/validate_domain_architecture.py`; Router: `SKILL.md`
