# Genre and Beat Fit — Deep Reference

> Working template: `assets/templates/genre-beat-fit.md`
> Machine routes: `assets/domain-registry.json` · `assets/tool-catalog.json` · `assets/dependency-manifest.json` · runtime method `references/runtime-orchestration.md`
> This reference contains the domain method; its paired template carries the method through active lyric work.

## 1. Composition role

This layer connects genre priors to the actual beat, supplied material and intended performance without turning convention into law.

- It receives the beat/profile, voice, section function and relevant scene conventions.
- It produces beat-fit hypotheses, lane-specific options and production-aware constraints for prosody, delivery, rhyme and hook form.
- The paired template keeps actual beat observations separate from genre expectation so either can correct the other.

## 2. Core craft model

Profiles are additions to the general lyric method, not replacement routes. Start with the user's beat, voice and brief; apply the relevant genre details without dropping any universal craft capability needed by the task.

Genre is a listener contract about timing, energy, texture, density and return—not a command to reproduce stock content. A hybrid can combine two or three grammars, but name the primary rhythmic/section grammar so competing conventions do not blur every choice. Satisfy enough of that grammar for recognition, then locate one deliberate point of counterpoint or subversion.

## UK drill
Affordances:
- syncopation/sliding bass;
- pickups;
- clipped/conversational entries;
- gallop/triplet-derived cells;
- 2-bar phrase logic;
- abrupt cadence turns.

Practitioner-derived UK rap/drill craft can include:
- multisyllabic vowel/stress matching;
- internal chains;
- precise line landings;
- understated/deadpan delivery;
- mundane/high-stakes collision;
- local/institutional specificity;
- controlled register switches.

These are tools. Violence and MLE markers are not mandatory because a beat is drill.

### UK drill lane controls

Choose the pressure balance before drafting, then let the other layers correct it:

| Lane | Foreground | Simplify to make room |
|---|---|---|
| technical-pressure | multisyllabic networks, internal saturation, pivots, cadence turns | fewer simultaneous scene changes and fewer layered interpretations per landing |
| content-pressure | causal scene, consequence, sensory/local specificity, emotional residue | cleaner rhyme geometry and more stable cadence cells |
| balanced | one main sound system and one main consequence system | secondary ornaments that do not reinforce either system |

The trade-off is attentional, not a fixed inverse percentage. A lyric may sustain high technical and narrative complexity when the same words carry both, but independent layers compete for breath, listener processing and bar space.

### UK drill landing and section profile

- Hard or clean landings are a useful baseline when the beat has sparse half-time weight.
- Soft enjambment can connect a pursuit, procedure or thought across one boundary.
- Suspension can withhold the decisive noun/verb for a reveal.
- A run-on can embody panic, insistence or acceleration, but it needs a planned breath and visible release.
- Four-bar joints and bars 4/8/12/16 are strong candidate turn points; move the turn when the actual beat or story creates a better hinge.
- A 16-bar verse can rise through setup → pressure/action → decisive turn → residue, but the song does not owe this geometry.

Set frequencies from the brief, beat and speaker. Do not convert one reference style's deviation caps into a universal drill law.

## Grime
Fast perceived pulse, percussive articulation, compact images, sharp bar turns, call/response energy, agile straight/skippy subdivision.

## NY drill
Retain drill rhythmic affordances while preserving local pronunciation, syntax and scene references. Do not import London vocabulary as costume.

## Dark trap
Half-time feel, triplet cells, elastic phrase length, repeated motifs, sparse contrast.

## Melodic rap/trap
Vowel sustain, pitch contour, breath, lower consonant congestion, strong hook/verse melodic contrast.

## Boom bap
Swing/backbeat, behind-beat conversation, internal rhyme density, line-boundary variation, audible scheme development.

## Spoken/free meter
Create pulse through stress recurrence, syntax, phrase length, breath, sound recurrence and deliberate breaks.

## Beat interaction
Inspect tempo, backbeat, kick, hats, bass/808, harmony, sections and negative space. Bundled `beats/*.json` are timing references, not universal genre definitions.

## Line-ending profile
Choose rather than assume:
- hard-landing bias;
- mixed closure;
- high enjambment;
- melodic suspension.

## Technique budgets
Genre changes likely trade-offs, not fixed percentages: dense rhyme may require simpler imagery; complex narrative may use simpler end schemes; melodic hooks need vowel/breath space; fast cadence rewards compact syntax.

For current slang/scene/artist-lane questions use `context-research.md`.

## Beat-mechanics matrix

Use these as starting priors only.

| Feature | Boom bap | Trap | UK drill | Grime |
|---|---|---|---|---|
| common tempo region | ~85-95 BPM | ~130-150 / half-time perception | ~140-145 | ~140 |
| common pulse feel | backbeat + swing | half-time | half-time | more full-time/percussive |
| hats | swung 8ths/16ths | rolling 16ths/32nds/triplets | 16ths + rolls | skippy 8ths/16ths |
| bass | sample/bassline varies | sustained 808 | sliding/melodic 808 common | often more staccato/electronic |
| likely vocal space | conversational internals | triplet/melodic flexibility | sparse/negative-space responsive | denser/percussive |
| pocket prior | behind/conversational | on/behind | on/ahead or floating pickups | on/ahead |

The actual instrumental outranks the matrix.

### UK drill affordances
Inspect:
- pickup before bar 1;
- sparse kick;
- half-time snare;
- hi-hat rolls;
- 808 slide direction;
- two-bar repetition;
- cut-outs.

Possible responses:
- let stressed words reinforce kick/snare;
- use pickup to enter already in motion;
- leave bass slide exposed;
- mirror a slide with vowel/pitch;
- stay deadpan while bass moves;
- use ad-lib as structural fill;
- change cadence against a repeated two-bar loop.

### Grime
At the same nominal BPM, denser or more percussive vocal activity can make the music feel faster. Derive perceived speed from tempo, subdivisions, drum activity, vocal density, articulation and pocket together.

### Trap
Triplet vocabulary can interact with a binary grid without filling every subdivision. The most useful contrast may be slow vocal cells against busy hats.

### Boom bap
Swing is a timing relation, not “old-school vocabulary.” Straightly quantised syllables can fight a swung drum feel even if syllable count is correct.

Use the actual MIDI/audio representation when available.

## 3A. Extended beat-fit guidance

### Separate tempo from feel
- The same nominal BPM can support different counting conventions.
- Drill and grime can share a tempo while producing different vocal density and attack.
- Trap may be counted at full or half tempo.
- Boom-bap swing changes off-beat placement even when BPM is stable.

### Beat observations to inspect
- backbeat location;
- kick density and displacement;
- hi-hat subdivision and roll behaviour;
- bass/808 sustain or glide;
- harmonic/melodic density;
- recurring loop length;
- dropouts and negative space;
- swing or microtiming;
- phrase-level production changes.

### UK drill prior
- Expect half-time weight, sparse space, pickups, and sliding-bass interaction as possibilities.
- Gallop-derived cells are options, not mandatory signatures.
- Deadpan or understated delivery may counter the production's motion.
- Draw subject matter, MLE density and ad-lib use from the supplied concept, speaker, section and available beat space.

### Grime prior
- Expect more full-time attack and higher syllabic occupancy than drill.
- Treat jagged drums and staccato bass as rhythmic surfaces to attack or counter.
- Do not collapse grime into “fast drill.”

### Trap prior
- Triplet families, half-time space, and hi-hat contrast are common affordances.
- A vocal can match, contrast, or answer dense hats.
- Double-time is a relative percept, not merely “more syllables.”

### Boom-bap prior
- Swing and behind-the-beat placement often matter more than subdivision count.
- Straight quantised vocals can fight the groove.
- Conversational density should still respond to sample density and snare placement.

### Counterpoint test
For every beat-fit plan, audition one option that does not mirror the instrumental.
If contrast creates clearer authority, tension, or space, the counterpoint may be stronger than synchrony.

## 4. Decision method

### 4.1. Frame
- Name the section function, hard constraints, and the complete set of craft objectives and questions.
- Record the decision in `assets/templates/genre-beat-fit.md`.

### 4.2. Baseline
- Describe the present behaviour before judging it.
- Record the decision in `assets/templates/genre-beat-fit.md`.

### 4.3. Hinge
- Identify the full set of words, bars, events, and performance moments involved in the binding issue.
- Record the decision in `assets/templates/genre-beat-fit.md`.

### 4.4. Mechanism
- Explain how the suspected variable creates the observed effect.
- Record the decision in `assets/templates/genre-beat-fit.md`.

### 4.5. Isolate
- For causal comparison, hold strong dimensions fixed while varying each suspected lever separately; then combine every improvement that survives its isolated test.
- Record the decision in `assets/templates/genre-beat-fit.md`.

### 4.6. Material and tool support
- Ground the decision in supplied creative material, direct reading or rehearsal, and every relevant representation, detector or generator.
- Record the decision in `assets/templates/genre-beat-fit.md`.

### 4.7. Audition
- Compare baseline and candidate in the medium that matters.
- Record the decision in `assets/templates/genre-beat-fit.md`.

### 4.8. Collateral
- Check meaning, voice, rhyme, rhythm, performance, sequence, and consequence as relevant.
- Record the decision in `assets/templates/genre-beat-fit.md`.

### 4.9. Commit
- Keep the most effective change set that survives audition without analytical explanation.
- Record the decision in `assets/templates/genre-beat-fit.md`.

### 4.10. Handoff
- Pass observations, locked decisions, open questions, and beat-fit outputs into every connected domain that can use them.
- Record the decision in `assets/templates/genre-beat-fit.md`.

## 5. Working variables

- **Tempo**
- **Counting Convention**
- **Backbeat**
- **Kick Pattern**
- **Hi-Hat Subdivision**
- **Bass Behaviour**
- **Swing**
- **Density Range**
- **Pocket Prior**
- **Entry Prior**
- **Phrase Loop**
- **Ad-Lib Space**
- **Vocal Register**
- **Production Density**
- **Counterpoint**
- **Genre Ambiguity**

## 6. Template contract

- Use `assets/templates/genre-beat-fit.md` for working state, not this reference.
- Fill every field relevant to the task.
- Keep baseline and candidate visible together.
- Anchor the decision to exact lines, bars or timestamps instead of vague adjectives.
- Fill from supplied material, direct observation, or verified context, and keep genuine unknowns blank.
- Log tool id, input scope, output limit, and accepted/rejected implication.
- Record seed and locked dimensions for generative operations.
- Update the template whenever rehearsal or a new observation disproves the current working model.

## 7. Script routes — preflight each listed tool with `python scripts/tool_router.py --tool <id>` before execution

### Primary
- `beat_profile_summary` → `scripts/beat_profile_summary.py`
  - Contribution: summarises bundled beat JSON profiles.
  - Class: `representation`.
- `music_structure` → `scripts/music_structure.py`
  - Contribution: bar density, boundary, repetition or drum-anchor cues from music IR.
  - Class: `detection`.
- `cadence_lab` → `scripts/cadence_lab.py`
  - Contribution: alternative slot geometries for a syllable budget.
  - Class: `generation`.
- `audio_to_json` → `scripts/audio_to_json.py`
  - Contribution: turns supplied audio into beat, onset and energy observations that can change the writing.
  - Class: `representation`.
### Secondary
- `beat_affordance` → `scripts/beat_affordance.py`
  - Contribution: candidate lyric stress/negative-space interactions with analysed music.
  - Class: `detection`.

### Tool-class boundaries
- Representation keeps supplied material beside labelled derived structure.
- Detection maps concrete conditions and opportunities with locations and confidence.
- Generation and transformation create controlled candidates.
- Evaluation combines mechanical observations with close reading, audition and comparison.
- Support checks runtime/package state, not craft quality.

## 8. Cross-file handoffs

- `references/musical-representation.md` ↔ `assets/templates/musical-representation.md`
- `references/prosody-flow.md` ↔ `assets/templates/prosody-flow.md`
- `references/performance-delivery.md` ↔ `assets/templates/performance-delivery.md`
- `references/voice-register.md` ↔ `assets/templates/voice-register.md`
- `references/context-research.md` ↔ `assets/templates/context-research.md`
- `references/revision-evaluation.md` once the task becomes comparative revision.

## 9. Failure modes

Repair the named craft variable, audition the result, and recheck every layer it changes.

### Genre label treated as law

### Violence or slang inferred from drill beat

### Same bpm assumed to imply same feel

### Grime and drill collapsed

### Straight flow forced onto swung drums

### Dense vocal masks dense instrumental

### Genre profile overrides user voice

### Producer-specific trait generalized to scene

### Half-time convention ignored

### Ad-lib convention used as quota

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

- Template: `assets/templates/genre-beat-fit.md`
- Domain index: `assets/domain-registry.json`
- Tool index: `assets/tool-catalog.json`
- Composition matrix: `assets/composition-matrix.md`
- Validator: `scripts/validate_domain_architecture.py`
- Router: `SKILL.md`
