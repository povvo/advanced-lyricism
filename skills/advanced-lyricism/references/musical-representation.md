# Musical Representation and Beat Affordance — Deep Reference

> Working template: `assets/templates/musical-representation.md`
> Machine routes: `assets/domain-registry.json` · `assets/tool-catalog.json` · `assets/dependency-manifest.json` · runtime method `references/runtime-orchestration.md`
> This reference contains the domain method; its paired template carries the method through active lyric work.

## 1. Composition role

This layer translates MIDI, audio and beat profiles into musical coordinates the lyric system can compose against while preserving raw timing and uncertainty.

- It receives supplied audio/MIDI, tempo or meter information and section questions.
- It produces beat affordances, boundary candidates, density/energy movement and timing maps for genre, prosody, delivery and hook form.
- The paired template preserves raw timing beside derived bar/grid interpretations so later layers can revise the map without losing the source material.

## 2. Core craft model

This layer turns an instrumental, MIDI file, rhythmic grid, musical phrase or production change into writing constraints.

The central principle: **a planning grid is a coordinate system, not the ontology of rhythm**.

## 1. Raw timing and derived timing

Preserve both.

### Raw MIDI data
- absolute tick;; note-on/note-off;; pitch;; velocity;
- channel/track;; tempo messages;; time-signature messages;; key-signature messages.

### Derived coordinates
- seconds;; bar;; beat;; subdivision/slot;
- note duration;; grouped bar features.

Do not discard raw ticks after mapping to a bar grid. If the meter interpretation changes, derived coordinates can be recomputed without losing source timing.

`midi_to_json.py` emits both.

---

## 2. Partwise and timewise views

Computational music analysis benefits from two complementary arrangements.

### Partwise
Preserve track/channel/instrument identity.

Useful for:
- separating drums from pitched material;; locating kick/snare anchors;; examining one melodic layer;; identifying repeated accompaniment roles.

### Timewise
Sort events globally by onset.

Useful for:
- finding density changes;; comparing what happens simultaneously;; identifying silence/negative space;; detecting section boundaries.

The agent should not choose one representation globally. Use the view that answers the current question.

---

## 3. Meter is hierarchical and relational

A 4/4 bar can be drawn as 16 slots, but perception is not produced by equal boxes.

Listeners infer:
- stronger and weaker levels;; grouping;; recurring accents;; duration patterns;
- pitch/register boundaries;; contour turns;; repetition;; phrase endings;
- harmonic changes.

The Developing Musical Structures material is especially important here: **beat can emerge from relations among unequal durations**, and pitch/register can alter perceived grouping even when duration sequences stay the same.

Therefore:
- use slot indices as addresses;; use metric-strength weights as hypotheses;; retain events that contradict the assumed grid;; allow the ear to revise the model.

---

## 4. Grouping cues

Potential phrase/section boundaries become more plausible when several cues coincide:

- rest or long gap;; density discontinuity;; register jump;; contour reversal;
- repetition restarting;; new instrumentation;; velocity/energy change;; harmonic arrival or departure;
- drum-pattern change;; lyrical syntactic boundary;; breath or held vowel;; semantic turn.

No single cue is mandatory. `music_structure.py` deliberately returns **boundary candidates with supporting cues**, not “the phrase structure.”

### Same / different
At every return, ask:
- what is invariant?; what changed?; is the change local or structural?; does the old pattern now mean something different?

This logic links musical form directly to hook craft and callback design.

---

## 5. MIDI event interchange

`advanced-lyricism.music-event-ir.v1` is the common symbolic representation.

Use it as input to:
- `music_structure.py`;; `beat_affordance.py`;; custom agent analysis.

Important fields:
- timing maps;; notes;; metric projection;; drum flag;
- partwise track summary.

### Drum conventions
General MIDI channel 10 / zero-indexed channel 9 permits useful but imperfect kick/snare/hat identification. Treat drum-note identities as conventions, not universal production truth.

### Sustain
Note-off duration is not always sounding duration because sustain pedals and synthesis envelopes can extend sound. The converter labels this limitation.

---

## 6. Audio event interchange

When only audio is available, `audio_to_json.py` extracts estimates:
- tempo;; beat times;; onset times;; RMS energy;
- spectral centroid;; per-beat onset/energy summaries.

This can support:
- section contrast;; likely attack density;; candidate drop/return moments;; rough pacing.

It cannot reliably tell:
- half-time vs double-time intent;; exact meter in ambiguous passages;; lyric pocket;; instrument identity;
- harmony or bass function from the compact feature set.

Use the output to **focus listening**, not replace it.

---

## 7. Syncopation as controlled expectation

Syncopation matters because it changes expectation against an inferred metrical hierarchy.

Useful lyric operations:
- stress a weak subdivision;; begin before the bar;; delay a strong content word;; answer the snare rather than sit on it;
- carry syntax across a strong boundary;; leave a predicted landing empty;; place internal rhyme where the grid suggests a non-final accent.

Research on groove supports a nontrivial relationship between syncopation and embodied pleasure: maximal regularity is not automatically optimal, and maximal complexity is not automatically optimal either. The practical lyric principle is **legible expectation + selective violation**.

`music_structure.py` can expose a weak-slot occupancy proxy from MIDI, but it is not a full syncopation model.

---

## 8. Beat-affordance analysis

Do not ask “what flow does this beat require?” Ask **what does the beat make easy, salient, or risky?**

Inspect:
- pulse and metrical ambiguity;; kick/snare anchors;; hat density;; bass/808 movement;
- negative space;; melodic register;; phrase length;; energy changes;
- repetition cycle;; dropouts;; tempo and tempo changes.

Possible lyric responses:
- reinforce;; answer;; mirror;; contrast;
- leave space;; stretch over;; cut against;; deliberately ignore.

A vocal does not have to duplicate the drum pattern.

`beat_affordance.py` maps line-level syllable/stress information to candidate percussive anchors and empty slots from symbolic analysis. It is an audition aid, not an automatic flow arranger.

---

## 9. Density is relative

A syllable count becomes meaningful only against:
- BPM;; subdivision;; articulation;; pocket;
- rests;; vowel sustain;; surrounding instrumental density;; previous and following bars.

A 14-syllable line may feel spacious in one cadence and congested in another. Use:
- `prosody_map.py` for text-side density/stress;; `music_structure.py` for beat-side density/changes;
- `beat_affordance.py` to compare them.

Do not reduce density to one “maximum syllables per bar” rule.

---

## 10. Musical contour and lyrical contour

Pitch/register and energy can create structural direction even when harmony is static.

Possible couplings:
- rising melodic register -> narrow syntax then release;; falling bass slide -> held/falling vocal vowel;
- dense onset region -> simplify words for intelligibility;; sparse breakdown -> expose detail or vulnerability;
- repeated musical loop -> vary syntax or viewpoint to prevent semantic stasis;; strong production return -> hook invariant returns;
- instrumental gap -> withheld word, breath, ad-lib, or consequence.

Coupling is optional. **Counterpoint** can be stronger than mirroring.

---

## 11. Representation boundaries

Text supplies written stress, syntax, syllables and notation; direct performance or audio supplies actual millisecond pocket, sung pitch, audible breath, swing ratio and the perceived downbeat in an ambiguous recording.

MIDI supplies encoded notes, velocities, channels, durations, tempo and meter events; performance/audio supplies human articulation, final-mix masking and unencoded expressive microtiming, while the lyric supplies semantics.

Audio feature JSON supplies measured/estimated onsets, energy, tempo candidates and coarse section changes; score/MIDI, stems or direct listening resolve exact notes, instrument identity and formal function.

Use the richest available musical input and keep uncertainty visible.

## 4. Decision method

### 4.1. Frame
- Name the section function, hard constraints, and the complete set of craft objectives and questions; record them in `assets/templates/musical-representation.md`.

### 4.2. Baseline
- Describe the present behaviour before judging it; Record the decision in `assets/templates/musical-representation.md`.

### 4.3. Hinge
- Identify the full set of words, bars, events, and performance moments involved in the binding issue; Record the decision in `assets/templates/musical-representation.md`.

### 4.4. Mechanism
- Explain how the suspected variable creates the observed effect; Record the decision in `assets/templates/musical-representation.md`.

### 4.5. Isolate
- For causal comparison, hold strong dimensions fixed while varying each suspected lever separately; then combine every improvement that survives its isolated test and record the results in `assets/templates/musical-representation.md`.

### 4.6. Material and tool support
- Ground the decision in supplied creative material, direct reading or rehearsal, and every relevant representation, detector or generator; record the decision in `assets/templates/musical-representation.md`.

### 4.7. Audition
- Compare baseline and candidate in the medium that matters; Record the decision in `assets/templates/musical-representation.md`.

### 4.8. Collateral
- Check meaning, voice, rhyme, rhythm, performance, sequence, and consequence as relevant; Record the decision in `assets/templates/musical-representation.md`.

### 4.9. Commit
- Keep the most effective change set that survives audition without analytical explanation; Record the decision in `assets/templates/musical-representation.md`.

### 4.10. Handoff
- Pass observations, locked decisions, open questions, and generated candidates into every connected domain that can use them; record the handoff in `assets/templates/musical-representation.md`.

## 5. Working variables

- **Raw Tick Time** · **Seconds**
- **Tempo Map** · **Meter Map**
- **Note Event** · **Velocity**
- **Drum Event** · **Onset**
- **Beat Estimate** · **Energy**
- **Register** · **Contour**
- **Repetition** · **Boundary**
- **Negative Space** · **Half/Double-Time Ambiguity**

## 6. Template contract

- Use `assets/templates/musical-representation.md` for working state, not this reference.
- Fill every field relevant to the task; keep baseline and candidate visible together.
- Anchor the decision to exact lines, bars or timestamps; fill from supplied material, direct observation, rehearsal, or verified context, and keep genuine unknowns blank.
- Log tool id, input scope, output limit, and accepted/rejected implication; Record seed and locked dimensions for generative operations.
- Update the template whenever rehearsal or a new observation disproves the current working model.

## 7. Script routes — preflight each listed tool with `python scripts/tool_router.py --tool <id>` before execution

### Primary
- `midi_to_json` → `scripts/midi_to_json.py`
  - Contribution: converts MIDI into a timing and event representation.
  - Class: `representation`.
- `audio_to_json` → `scripts/audio_to_json.py`
  - Contribution: turns supplied audio into beat, onset and energy observations that can change the writing.
  - Class: `representation`.
- `wav_energy_probe` → `scripts/wav_energy_probe.py`
  - Contribution: maps PCM WAV energy, coarse pulse and section changes without audio-analysis packages.
  - Class: `representation`.
- Pass its section and pulse candidates into beat-fit and structure decisions; keep half/double-time unresolved until audition.
- `beat_metadata_reconcile` → `scripts/beat_metadata_reconcile.py`
  - Contribution: compares title/description BPM and key claims with fields measured by the supplied analysis.
  - Class: `detection`.
- Pass conflicts forward as open questions rather than silently selecting metadata or analysis.
- `music_structure` → `scripts/music_structure.py`
  - Contribution: bar density, boundary, repetition or drum-anchor cues from music IR.
  - Class: `detection`.
- `beat_affordance` → `scripts/beat_affordance.py`
  - Contribution: candidate lyric stress/negative-space interactions with analysed music.
  - Class: `detection`.
- `beat_profile_summary` → `scripts/beat_profile_summary.py`
  - Contribution: summarises bundled beat JSON profiles.
  - Class: `representation`.
### Secondary
- `cadence_lab` → `scripts/cadence_lab.py`
  - Contribution: alternative slot geometries for a syllable budget.
  - Class: `generation`.

### Tool-class boundaries
- Representation keeps supplied material beside labelled derived structure; detectors map concrete conditions and opportunities with locations and confidence.
- Generators and transforms create controlled candidates; evaluation combines mechanical observations with close reading, audition and comparison.
- Support checks runtime/package state, not craft quality.

## 8. Cross-file handoffs

- `references/prosody-flow.md` ↔ `assets/templates/prosody-flow.md`
- `references/performance-delivery.md` ↔ `assets/templates/performance-delivery.md`
- `references/hook-song-form.md` ↔ `assets/templates/hook-song-form.md`
- `references/genre-beat-fit.md` ↔ `assets/templates/genre-beat-fit.md`
- `references/revision-evaluation.md` once the task becomes comparative revision.

## 9. Failure modes

Repair the named craft variable, audition the result, and recheck every layer it changes.

### Derived coordinates replacing raw timing

### Tempo estimate treated as fact

### All rhythmic grouping forced to 16 slots

### Midi velocity read as guaranteed loudness

### Audio onset read as instrument identity

### Beat structure inferred from genre label alone

### Symbolic events mistaken for performed microtiming

### Music analysis not tied to a writing decision

### Counterpoint option ignored

### Uncertainty discarded from json handoff

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

- Template: `assets/templates/musical-representation.md`; Domain index: `assets/domain-registry.json`
- Tool index: `assets/tool-catalog.json`; Composition matrix: `assets/composition-matrix.md`; Validator: `scripts/validate_domain_architecture.py`; Router: `SKILL.md`
