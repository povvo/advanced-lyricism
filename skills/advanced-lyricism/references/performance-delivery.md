# Performance and Delivery — Deep Reference

> Working template: `assets/templates/performance-delivery.md`
> Machine routes: `assets/domain-registry.json` · `assets/tool-catalog.json` · `assets/dependency-manifest.json` · runtime method `references/runtime-orchestration.md`
> This reference contains the domain method; its paired template carries the method through active lyric work.

## 1. Composition role

This layer treats breath, emphasis, entry, pocket, consonant attack, vowel duration, silence, pitch and texture as compositional variables.

- It receives the words, heard-rhyme plan, cadence map, beat affordances, voice and section function.
- It produces a rehearsable delivery plan whose discoveries can revise wording, rhyme, prosody and form upstream.
- The paired template records performance choices and rehearsal discoveries without pretending text alone determines execution.

## 2. Core craft model

Delivery is not an afterthought applied to finished words. It is one of the variables that determines rhyme, stress, timing, intelligibility, emotional distance, and impact.

## Performance parameters

Track separately:
- entry point;; subdivision;; pocket;; consonant attack;
- vowel duration;; lexical vs performed stress;; breath;; pause;
- loudness/emphasis;; pitch contour;; sustain;; tone/texture;
- ad-lib placement;; double/gang vocal;; silence after impact.

A line can improve without changing one word if one of these parameters changes.

---

## Delivery notation

The package supports a lightweight notation:

- `//` or `(B)` - planned breath;; `CAPS` - emphasis;; `(ad-lib)` - secondary vocal;; `...` - pause/rest;
- `~` - pitch slide;; `↑` / `↓` - pitch direction;; `[tone]` or `[flow]` - texture/cadence instruction;; `_` - sustain;
- `/` - explicit syllable division when needed.

Use `delivery_notation.py` to convert a marked page into `advanced-lyricism.delivery-ir.v1`.

The notation is a **performance script**, not an acoustic measurement.

---

## Breath as rhythm

A breath occupies time. It can:
- reset flow;; articulate a section;; create anticipation;; make a dense run physically possible;
- expose vulnerability;; sound percussive;; become part of a call/response.

Do not insert breath only after a line is already overfilled.

### Breath audit
Mark:
1. planned breaths;
2. involuntary breaths during rehearsal;
3. words swallowed before/after breath;
4. repeated stumble points;
5. whether a breath falls at meaningful syntax or fights it.

A dense four-bar run with no breath can be valid only if the performer can actually execute it or if recording construction is deliberately part of the effect.

---

## Stress: lexical, performed, musical

Three stresses can align or diverge:

**Lexical stress** - default speech prominence inside the word.  
**Performed stress** - what the rapper/singer actually accents.  
**Musical stress** - strength inferred from beat/meter/accompaniment.

Strong craft asks whether divergence is:
- expressive;; characterful;; pronunciation-specific;; groove-specific;
- or simply accidental.

Do not “correct” nonstandard stress that belongs to the speaker's accent or chosen delivery.

---

## Consonant attack and vowel field

Consonants help place rhythm. Vowels carry pitch, sustain and much of rhyme.

For precision:
- use plosives for hard attacks when articulation remains possible;; watch repeated sibilant or stop sequences at speed;
- place long vowels where sustain or pitch movement has room;; use reduced vowels/connective syllables to move between stresses;
- consider whether an end rhyme is actually audible after consonant crowding.

`articulation_audit.py` is a congestion screen. Rehearsal remains decisive.

---

## Pocket

Treat ahead/on/behind as a **relationship**, not a fixed millisecond number.

### Ahead
Can create:
- urgency;; attack;; anticipation.

Risks:
- rushing;; lost final consonants;; no room for breath.

### On
Can create:
- clarity;; militancy;; percussive lock.

Risks:
- stiffness;; nursery-like predictability if every syntax/rhyme boundary also locks.

### Behind
Can create:
- ease;; authority;; conversational weight;; melancholy.

Risks:
- dragging without intention;; poor interaction with dense/jagged drums.

Actual pocket must be heard or measured from performance. Text cannot certify it.

---

## Gear changes

A flow switch works best when the listener can hear both:
1. an established base;
2. the changed parameter.

Possible transitions:
- pause/reset;; sustained vowel;; pickup;; pivot word whose stress supports both patterns;
- gradual morph;; density ramp;; syntactic turn;; emotional turn.

A switch every bar can erase the baseline needed to perceive contrast.

Use `cadence_lab.py` for candidate geometries and `arc_generator.py` for section-level contrast planning.

---

## Silence and negative space

Silence can function as:
- withheld syntax;; post-punchline amplification;; breath;; beat reveal;
- emotional refusal;; hook participation slot;; boundary marker.

The question is not “is there empty space?” but **what expectation occupies it?**

Suspension is powerful because the listener supplies the missing continuation. This is distinct from simply having a short line.

---

## Ad-libs as structural layer

Ad-libs can:
- fill deliberately unused pockets;; answer the main voice;; mark social stance;; reinforce a drum/bass gesture;
- hide a breath;; create a second viewpoint;; carry a recurring sonic motif.

Avoid a fixed “every N bars” rule. Frequency depends on beat space, genre, persona and section function.

---

## Pitch contour

Even predominantly rapped delivery can use:
- phrase-final fall;; questioning rise;; local pitch lift at climax;; vowel slide;
- monotone contrast against moving bass;; repeated melodic cell.

Pitch can change grouping. A register jump may make a boundary audible even if rhythm stays identical.

When MIDI or audio exists, inspect production contour before deciding whether vocal contour should mirror or counter it.

---

## Emotional delivery

Emotion need not mean larger volume.

Possible mappings:
- containment -> reduced overt pitch/volume movement, precise detail;; panic -> breath pressure, syntax spill, accelerating attacks;
- grief -> space, sustain, unstable or lowered contour;; anger -> clipped consonants, narrowed pitch, silence;
- intimacy -> closer speech rhythm, less rhetorical projection;; dissociation -> controlled monotone against disturbing content.

These are options, not universal psychological laws. The supplied or established voice outranks defaults.

---

## Studio vs page

The page can encode intention but cannot prove performance.

Final sequence:
1. mark intended delivery;
2. perform;
3. note what changed naturally;
4. decide whether natural change is better;
5. update the page;
6. perform again.

The aim is not to force the body to obey notation. The notation should become a reliable map of the chosen performance.

## 3A. Extended delivery guidance

### Three stress layers
- Lexical stress belongs to the word as spoken; Performed stress is what the rapper chooses to foreground.
- Musical stress comes from beat hierarchy and production; Alignment produces lock and clarity.
- Deliberate disagreement can create drag, urgency, irony, or instability; Accidental disagreement usually feels like a stumble.

### Breath as time
- A breath occupies real rhythmic space; Dense writing must reserve that space instead of adding it after composition.
- Mark repeated involuntary breaths before planned breaths; if the body chooses the same breath twice, treat that as a structural constraint.
- Do not hide emergency gasps inside function words.

### Notation semantics
- `//` marks a full breath or clear reset; `/` can mark a quick breath when the phrase remains continuous.
- `CAPS` marks chosen emphasis, not every stressed syllable; `(ad-lib)` occupies secondary-vocal space and should not mask the main line.
- `...` marks silence whose duration must be auditioned; `~`, `↑`, and `↓` describe contour, not exact pitch.
- `_` marks sustain and therefore changes available syllabic time; `[tone]` records texture only when it affects the performance decision.

### Studio test
1. Perform once without notation.
2. Mark what the body naturally changes.
3. Compare natural and planned stress.
4. Keep notation only where it improves repeatability or intention.
5. Re-test after doubles, ad-libs, and production fills are added.

## 4. Decision method

### 4.1. Frame
- Name the section function, hard constraints, and the complete set of craft objectives and questions; record them in `assets/templates/performance-delivery.md`.

### 4.2. Baseline
- Describe the present behaviour before judging it; Record the decision in `assets/templates/performance-delivery.md`.

### 4.3. Hinge
- Identify the full set of words, bars, events, and performance moments involved in the binding issue; Record the decision in `assets/templates/performance-delivery.md`.

### 4.4. Mechanism
- Explain how the suspected variable creates the observed effect; Record the decision in `assets/templates/performance-delivery.md`.

### 4.5. Isolate
- For causal comparison, hold strong dimensions fixed while varying each suspected lever separately; then combine every improvement that survives its isolated test and record the results in `assets/templates/performance-delivery.md`.

### 4.6. Material and tool support
- Ground the decision in supplied creative material, direct reading or rehearsal, and every relevant representation, detector or generator; record the decision in `assets/templates/performance-delivery.md`.

### 4.7. Audition
- Compare baseline and candidate in the medium that matters; Record the decision in `assets/templates/performance-delivery.md`.

### 4.8. Collateral
- Check meaning, voice, rhyme, rhythm, performance, sequence, and consequence as relevant; Record the decision in `assets/templates/performance-delivery.md`.

### 4.9. Commit
- Keep the most effective change set that survives audition without analytical explanation; Record the decision in `assets/templates/performance-delivery.md`.

### 4.10. Handoff
- Pass observations, locked decisions, open questions, and generated candidates into every connected domain that can use them; record the handoff in `assets/templates/performance-delivery.md`.

## 5. Working variables

- **Entry Point** · **Pocket**
- **Consonant Attack** · **Vowel Duration**
- **Performed Stress** · **Breath**
- **Pause** · **Loudness**
- **Pitch Contour** · **Sustain**
- **Tone** · **Ad-Lib**
- **Double Vocal** · **Silence After Impact**
- **Rehearsal observation** · **Studio constraint**

## 6. Template contract

- Use `assets/templates/performance-delivery.md` for working state, not this reference.
- Fill every field relevant to the task; keep baseline and candidate visible together.
- Anchor the decision to exact lines, bars or timestamps; fill from supplied material, direct observation, rehearsal, or verified context, and keep genuine unknowns blank.
- Log tool id, input scope, output limit, and accepted/rejected implication; Record seed and locked dimensions for generative operations.
- Update the template whenever rehearsal or a new observation disproves the current working model.

## 7. Script routes — preflight each listed tool with `python scripts/tool_router.py --tool <id>` before execution

### Primary
- `delivery_notation` → `scripts/delivery_notation.py`
  - Contribution: turns breath, emphasis, ad-lib, pitch and tone annotations into a delivery map.
  - Class: `representation`.
- `articulation_audit` → `scripts/articulation_audit.py`
  - Contribution: maps consonant density and physically awkward transitions.
  - Class: `detection`.
- `prosody_map` → `scripts/prosody_map.py`
  - Contribution: maps syllable density, lexical stress and candidate grid fit.
  - Class: `detection`.
### Secondary
- `beat_affordance` → `scripts/beat_affordance.py`
  - Contribution: candidate lyric stress/negative-space interactions with analysed music.
  - Class: `detection`.

### Tool-class boundaries
- Representation keeps supplied material beside labelled derived structure; detectors map concrete conditions and opportunities with locations and confidence.
- Generators and transforms create controlled candidates; evaluation combines mechanical observations with close reading, audition and comparison.
- Support checks runtime/package state, not craft quality.

## 8. Cross-file handoffs

- `references/prosody-flow.md` ↔ `assets/templates/prosody-flow.md`
- `references/musical-representation.md` ↔ `assets/templates/musical-representation.md`
- `references/voice-register.md` ↔ `assets/templates/voice-register.md`
- `references/rhyme-phonology.md` ↔ `assets/templates/rhyme-phonology.md`
- `references/revision-evaluation.md` ↔ `assets/templates/revision-evaluation.md`
- `references/revision-evaluation.md` once the task becomes comparative revision.

## 9. Failure modes

Repair the named craft variable, audition the result, and recheck every layer it changes.

### Notation applied before words stabilise

### Every emphasis capitalised

### Ad-libs filling every gap

### Breath marks divorced from performance

### Tone labels replacing acting choices

### Pitch arrows treated as exact notation

### Delivery used to rescue weak meaning

### Natural stress overridden unintentionally

### No space reserved for secondary vocals

### Page map never tested aloud

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

- Template: `assets/templates/performance-delivery.md`; Domain index: `assets/domain-registry.json`
- Tool index: `assets/tool-catalog.json`; Composition matrix: `assets/composition-matrix.md`; Validator: `scripts/validate_domain_architecture.py`; Router: `SKILL.md`
