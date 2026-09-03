# Prosody, Flow, and Bar-Line Dynamics — Deep Reference

> Working template: `assets/templates/prosody-flow.md`
> Machine routes: `assets/domain-registry.json` · `assets/tool-catalog.json` · `assets/dependency-manifest.json` · runtime method `references/runtime-orchestration.md`
> This reference contains the domain method; its paired template carries the method through active lyric work.

## 1. Composition role

This layer designs the relation among lexical stress, performed accent, syntax, beat location, density, breath, rhyme placement and timing.

- It receives candidate lines, phonological structure, beat affordances, genre fit and delivery constraints.
- It produces cadence grids, pocket/entry choices, bar-line behaviour, density curves and suspension/release patterns.
- The paired template keeps written stress, performed accent and musical position visible together while variants are auditioned.

## 2. Core craft model

Flow is the relation among lexical stress, performed accent, syntax, rhyme position, beat location, density, breath, articulation, and timing.

## Grid
A 4/4 16th grid is a planning surface, not a prison:

`1 e & a | 2 e & a | 3 e & a | 4 e & a`

Map:
- kick/backbeat;; subdivisions and swing;; phrase entry/exit;; stressed syllables;
- rhyme points;; breaths;; rests/held vowels.

Then decide which moments confirm or disturb the grid.

## Stress alignment
For each important word ask:
- where is lexical stress in speech?; where is the performed accent?; where is the musical accent?; is mismatch expressive or accidental?

A deliberate mismatch can create urgency, drag, looseness, or ambiguity. An accidental mismatch often sounds written rather than performed.

## Cadence families
Starting geometries:
- straight subdivision;; triplet;; gallop;; swing;
- half-time;; speech-effusive/conversational;; percussion-effusive/articulatory;; sung/melodic.

They are resources, not genre laws. Cadence becomes personal through entry point, stress contour, vowel duration, consonant attack, density, and where syntax resolves.

## Pocket
A phrase can sit ahead, on top, behind, or across the bar. Moves include:
- pickup/anacrusis;; delayed first stress;; early finish;; held vowel;
- consonant hit against kick/snare;; internal rhyme answering percussion;; deliberate empty subdivision after impact.

Microtiming comes from performance; do not claim millisecond precision from text alone.

## Bar-line behaviour
Different line endings create different cognition:

- **strong landing** — syntax/rhyme resolve at or near the boundary; closure, authority, punch;
- **soft enjambment** — sentence crosses but the local phrase remains stable; continuity without full destabilisation;
- **hard enjambment** — a syntactic dependency is stranded; forward pull and instability;
- **suspension** — an expected word/resolution is withheld; tension comes from incompleteness;
- **run-on** — syntax spills through several boundaries; acceleration, panic, insistence, or conversational momentum.

Do not rank these universally. Establish a landing profile, then break it for function. A break is strongest when the listener first learns the baseline.

## Rhyme placement vs syntax
End rhyme does not automatically create closure. If syntax continues strongly across the boundary, the rhyme can feel medial. Conversely, an internal rhyme can feel like a landing if syntax, accent, and space all converge there.

This is one reason scheme diagrams alone are insufficient.

## Gear changes
Shift **up** with:
- denser subdivisions;; shorter syntactic units;; more internals;; earlier entries;
- harder consonant attack;; reduced silence.

Shift **down** with:
- longer vowels;; fewer syllables;; later entry;; simpler rhyme;
- one plain declarative line;; more breath/negative space.

### Transition mechanics
A gear change can:
- **cut cleanly** at a section/line;; use a **transitional bar** containing features of both pockets;
- pivot on one word whose placement belongs to the old pattern while its continuation establishes the new;
- **morph** over several beats.

Choose the transition itself as part of the expression.

## Density as drama
High density reduces processing time; sparse language creates weight and inference space. Oscillate rather than living at one ceiling.

Density can mark:
- pursuit/action;; explanation;; panic;; climax;
- aftermath;; hook contrast.

Relative change matters more than a global syllable target.

## Beat interaction
When audio exists inspect:
- kick;; snare/backbeat;; hi-hat subdivision/swing;; bass/808;
- harmonic rhythm;; section energy/drop;; melodic contour;; frequency space.

Avoid accidentally shadowing every bass movement with the vocal. Counterpoint and silence can create pocket.

## Genre priors
- **UK drill:** syncopation/sliding-bass space, pickups, clipped or conversational entries, gallop-derived cells, 2-bar phrase logic.
- **Grime:** fast perceived pulse, percussive articulation, sharp pivots, agile straight/skippy subdivision.
- **Trap:** triplet/half-time flexibility, repeated rhythmic cells, elastic phrase length.
- **Boom bap:** swing/backbeat, conversational behind-beat placement, strong pocket conversation.
- **Melodic rap:** vowel sustain, pitch contour, breath and consonant economy may outrank rhyme saturation.

Read `references/genre-beat-fit.md`; actual beat and speaker override priors.

## Breath and delivery notation
Use notation only when it reduces ambiguity:
- `//` full breath;; `/` quick breath;; `_` held vowel;; `>` accelerate;
- `<` decelerate;; `^WORD` primary stress/emphasis;; `(ad-lib)` secondary vocal;; `[rest]` intentional gap.

Mark **mandatory** breaths caused by phrase design separately from optional expressive breaths. If delivery only works by hiding emergency breaths, rewrite.

## Performance loop
At target tempo:
1. tap/clap the backbeat or play the beat;
2. perform three times;
3. mark repeated stumbles;
4. mark involuntary breaths;
5. locate unintended stress;
6. note consonant congestion and swallowed key words;
7. revise every unit whose change is required to fix the repeated failure;
8. perform again.

## Audio-tool synthesis
The original audio/MIDI/BPM/key/bounce utilities contributed the craft-relevant outputs:
- tempo/pulse hypotheses;; subdivision;; section energy;; drop placement;
- melodic contour;; note/rhythm cells;; density opportunities;; metadata conflicts.

The heavy pipelines are intentionally not runtime dependencies. For bundled beat JSON use `scripts/beat_profile_summary.py`.

## Timing and meter principle
Treat rhyme placement, accented syllables, syntax, measure boundaries, expressive timing, and metric ambiguity as interacting parameters. Enjambment can weaken apparent bar-end closure, and syllable count alone cannot describe flow.

## Advanced line-boundary control

The bar line is a **negotiation point** between musical cycle and linguistic continuation.

### End-stopped convergence
Syntax, rhyme and metric boundary resolve together.

Use for:
- declarative authority;; hook clarity;; a deliberately blunt landing;; contrast before a later spill.

Failure mode: if every bar resolves the same way, the listener can predict both language and rhyme shape before hearing the words.

### Soft enjambment
The bar completes a local sonic unit but syntax continues.

It creates forward pull when:
- you want forward pull without obscuring meaning;; the end rhyme should register but not close the thought;
- a prepositional/complement phrase can cross naturally.

### Hard enjambment
The boundary splits a stronger grammatical dependency.

Use for:
- urgency;; destabilisation;; conversational spill;; a delayed semantic landing.

The stronger the dependency, the stronger the pull. Test aloud: the continuation should feel demanded, not merely awkward.

### Suspension
Place the break where the grammar predicts a missing complement:
- article before noun;; preposition before object;; conjunction before clause;; auxiliary before lexical verb;
- unfinished comparison.

The empty time becomes active because a required linguistic element is absent.

Do not use suspension mechanically. A function word at the end of a line is only useful if:
1. the listener can feel what is missing;
2. the gap has enough temporal weight to matter;
3. the resolution earns the delay.

Use `technique_opportunity.py` to locate candidate hinges.

### Run-on
Several bar boundaries pass without strong syntactic closure.

Effects can include:
- breathlessness;; obsession;; argument momentum;; panic;
- conversational authority;; deliberate difficulty of bar-counting.

A run-on needs planned breathing and a later release point. Continuous density with no contrast becomes blur.

### UK drill landing and deviation design

On a sparse half-time drill beat, audition a clean-landing version first, then earn each deviation by function:

- tension or connected motion → soft enjambment;
- a withheld object, actor or consequence → one suspension followed by a decisive landing;
- panic, pursuit or spiralling insistence → bounded run-on with marked breaths and a release bar;
- punch setup → local pattern stability before a turn at the beat's strongest joint.

Strong endings are a profile, not a moral rule. Record the intended landing ratio and exception functions in the template; do not impose fixed per-song caps unless the user has selected that exact discipline.

---

## Cadence architecture in more detail

A useful grid family includes:

- **straight 16ths** - evenly distributed articulatory motion;; **8ths / half-time** - space, weight, clearer content;
- **triplet field** - ternary subdivision against binary meter;; **gallop** - selective omission within the four-part subdivision;
- **swing** - uneven subdivision timing;; **syncopated cell** - strong accents displaced from primary beats;
- **pickup/anacrusis** - phrase begins before the notated bar;; **late entry** - silence makes the first stress heavier;
- **early exit** - bar remainder becomes negative space.

These are geometries, not identities. `cadence_lab.py` generates slot patterns for audition; it cannot infer the performer's groove.

### Stress distribution
Do not count syllables alone. Track:
- content-word stresses;; weak function syllables;; adjacent stress clashes;; long lapses;
- vowel length;; consonant attack.

An 11-syllable line with five heavy stresses can feel denser than a 14-syllable line with connective reductions.

`prosody_map.py` exposes lexical-stress candidates and multiple grid projections rather than choosing one “correct” alignment.

---

## Density as an arc

Density can move through a section:

- low -> medium -> high -> release;; alternating dense / sparse;; steady base with one burst;; high opening then sudden decompression;
- slow accumulation via internal rhyme rather than syllable count.

Contrast is relational. Fast feels faster after space; space feels heavier after compression.

Use `arc_generator.py` to plan relative curves. Do not force density, rhyme density, emotional exposure and tension to peak simultaneously unless that convergence is the intended effect.

---

## Transition design

A gear change needs a hinge.

Possible hinges:
- a pause;; a breath;; held vowel;; ad-lib;
- pivot word;; syntactic completion;; semantic reversal;; rhyme-family change;
- pickup into the new cell;; production boundary.

A smooth morph can change one parameter over 2-4 bars while preserving another:
- same rhyme / new cadence;; same cadence / rising density;; same syntax / shifted accent;; same words / altered delivery.

This is parameter isolation in performance form.

---

## Physicality and articulation

Flow is embodied. At speed, clusters compete for the same articulators.

Watch:
- repeated sibilants;; rapid stop-to-stop place changes;; tongue-tip congestion;; consonant clusters at breath edges;
- important words buried after a dense run;; stressed vowels too short to carry intended rhyme.

`articulation_audit.py` flags coarse phonemic congestion; the out-loud test remains decisive.

## 4. Decision method

### 4.1. Frame
- Name the section function, hard constraints, and the complete set of craft objectives and questions; record them in `assets/templates/prosody-flow.md`.

### 4.2. Baseline
- Describe the present behaviour before judging it; Record the decision in `assets/templates/prosody-flow.md`.

### 4.3. Hinge
- Identify the full set of words, bars, events, and performance moments involved in the binding issue; Record the decision in `assets/templates/prosody-flow.md`.

### 4.4. Mechanism
- Explain how the suspected variable creates the observed effect; Record the decision in `assets/templates/prosody-flow.md`.

### 4.5. Isolate
- For causal comparison, hold strong dimensions fixed while varying each suspected lever separately; then combine every improvement that survives its isolated test and record the results in `assets/templates/prosody-flow.md`.

### 4.6. Material and tool support
- Ground the decision in supplied creative material, direct reading or rehearsal, and every relevant representation, detector or generator; record the decision in `assets/templates/prosody-flow.md`.

### 4.7. Audition
- Compare baseline and candidate in the medium that matters; Record the decision in `assets/templates/prosody-flow.md`.

### 4.8. Collateral
- Check meaning, voice, rhyme, rhythm, performance, sequence, and consequence as relevant; Record the decision in `assets/templates/prosody-flow.md`.

### 4.9. Commit
- Keep the most effective change set that survives audition without analytical explanation; Record the decision in `assets/templates/prosody-flow.md`.

### 4.10. Handoff
- Pass observations, locked decisions, open questions, and prosody outputs into every connected domain that can use them; record the handoff in `assets/templates/prosody-flow.md`.

## 5. Working variables

- **Entry** · **Subdivision**
- **Lexical Stress** · **Performed Stress**
- **Musical Accent** · **Pocket**
- **Density** · **Breath**
- **Caesura** · **Enjambment**
- **Suspension** · **Run-On Syntax**
- **Gear Change** · **Negative Space**
- **Rhyme Placement** · **Transition**

## 6. Template contract

- Use `assets/templates/prosody-flow.md` for working state; fill every field relevant to the task.
- Keep baseline and candidate visible together; anchor the decision to exact lines, bars or timestamps instead of vague adjectives.
- Fill from supplied material, direct observation, rehearsal, or verified context; keep genuine unknowns blank; log tool id, input scope, output limit, and accepted/rejected implication.
- Record seed and locked dimensions for generative operations; update the template whenever rehearsal or a new observation disproves the current working model.

## 7. Script routes — preflight each listed tool with `python scripts/tool_router.py --tool <id>` before execution

### Primary
- `prosody_map` → `scripts/prosody_map.py`
  - Contribution: maps syllable density, lexical stress and candidate grid fit.
  - Class: `detection`.
- `cadence_lab` → `scripts/cadence_lab.py`
  - Contribution: alternative slot geometries for a syllable budget.
  - Class: `generation`.
- `technique_opportunity` → `scripts/technique_opportunity.py`
  - Contribution: plausible enjambment, suspension, caesura, gear-change, scheme or callback opportunities.
  - Class: `detection`.
### Secondary
- `beat_affordance` → `scripts/beat_affordance.py`
  - Contribution: candidate lyric stress/negative-space interactions with analysed music.
  - Class: `detection`.
- `articulation_audit` → `scripts/articulation_audit.py`
  - Contribution: maps consonant density and physically awkward transitions.
  - Class: `detection`.

### Tool-class boundaries
- Representation keeps supplied material beside labelled derived structure; detectors map concrete conditions and opportunities with locations and confidence.
- Generators and transforms create controlled candidates; evaluation combines mechanical observations with close reading, audition and comparison.
- Support checks runtime/package state, not craft quality.

## 8. Cross-file handoffs

- `references/musical-representation.md` ↔ `assets/templates/musical-representation.md`
- `references/performance-delivery.md` ↔ `assets/templates/performance-delivery.md`
- `references/rhyme-phonology.md` ↔ `assets/templates/rhyme-phonology.md`
- `references/hook-song-form.md` ↔ `assets/templates/hook-song-form.md`
- `references/revision-evaluation.md` ↔ `assets/templates/revision-evaluation.md`
- `references/revision-evaluation.md` once the task becomes comparative revision.

## 9. Failure modes

Repair the named craft variable, audition the result, and recheck every layer it changes.

### Grid treated as ontology

### Every bar end-stopped

### Function-word suspension by accident

### Density held flat

### Gear change without transition

### Stress mismatch mistaken for automatic error

### Breath ignored until recording

### Flow chosen from genre stereotype

### Bar count confused with sentence structure

### Quantized analysis hiding groove

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

- Template: `assets/templates/prosody-flow.md`; Domain index: `assets/domain-registry.json`; Tool index: `assets/tool-catalog.json`; Composition matrix: `assets/composition-matrix.md`
- Validator: `scripts/validate_domain_architecture.py`; Router: `SKILL.md`
