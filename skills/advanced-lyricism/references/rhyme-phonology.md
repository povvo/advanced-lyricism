# Rhyme and Phonology — Deep Reference

> Working template: `assets/templates/rhyme-phonology.md`
> Machine routes: `assets/domain-registry.json` · `assets/tool-catalog.json` · `assets/dependency-manifest.json` · runtime method `references/runtime-orchestration.md`
> This reference contains the domain method; its paired template carries the method through active lyric work.

## 1. Composition role

This layer models rhyme as heard structure: stress, vowel/rime, phrase shape, syllable structure, accent, timing and delivery rather than spelling.

- It receives candidate language, intended pronunciation, voice/register and cadence/delivery constraints.
- It produces rhyme families, multisyllabic anchors, sound-law transformations and phrase-shape options for lexical, prosodic and performance layers.
- The paired template keeps dictionary suggestions subordinate to the supplied or intended performance.

## 2. Core craft model

Rhyme is heard, not spelled. Stress, accent, phrase shape, timing and delivery determine whether a relation lands.

## Rhyme unit
Track:
- stressed vowel;; following consonants/coda;
- preceding onset where useful;; syllable count;
- stress contour;; word boundaries.

Useful relations:
- exact tail;; slant;
- multisyllabic;; mosaic;
- internal/root-anchor;; assonant/consonant family.

These are a continuum, not a prestige ladder.

## Practitioner synthesis: vowel/stress matching
A long phrase can rhyme convincingly when it matches:
- number of syllables;; strong/weak positions;
- vowel sequence;; timing.

This preserves one of the strongest UK-rap practitioner insights.

## Pivot families
1. start from an important anchor word;
2. extract the stressed acoustic pivot;
3. generate close matches;
4. generate tail-varied slants;
5. generate mosaics/phrase matches;
6. meter-filter;
7. remove semantically empty options.

Suffix repetition is not forbidden. It becomes weak when both the sound and semantic landing are predictable.

## Scheme architecture
Use schemes as movement:
- couplet closure;; alternation;
- enclosure;; sustained-family pressure;
- chain handoff;; return after contrast;
- pivot at a semantic/flow turn.

Choose after the section's movement is known.

## Internal rhyme grid
Advanced internal architecture can track recurring positions:
- opening/entry;; mid-bar;
- ending/landing.

Corresponding positions across bars can answer each other, creating a grid rather than end-rhyme couplets. Do not fill every slot every bar; contrast makes density legible.

## Rhyme placement
Prefer rhyme on words carrying image, action, relation, decision or consequence. A looser rhyme on a meaningful word can beat a perfect rhyme on connective tissue.

## Delayed resolution
Useful possibilities:
- imply the obvious rhyme, land elsewhere;; delay across a bar boundary;
- answer an end rhyme internally next line;; return an old family after a break.

Delay should change interpretation or rhythmic expectation, not exist only as trickery.

## Accent and pronunciation
Dictionaries are candidate generators, not authorities. Delivery can change stress, reduction, linking, consonants, syllabification and vowel length. Local pronunciation may create viable relations absent from a standard dictionary.

## Failure modes
Revise when:
- spelling says rhyme but the ear does not;; rhyme forces unnatural syntax;
- internal saturation hides the image;; key words require unintended stress;
- a family continues after its semantic purpose ends;; the line is clever only when annotated.

Combine `scripts/craft_audit.py` pronunciation coverage and mechanical indicators with supplied pronunciation, close reading and audition when assessing freshness and speaker credibility.

Rhyme must be evaluated phonologically and in interaction with accent, syntax, meter, timing, and performed phrase shape.

## Syllable structure and rhyme control

Treat a syllable as more than a count.

A practical decomposition:
- **onset** - consonants before the vowel;; **nucleus** - vowel/diphthong;
- **coda** - consonants after the nucleus;; **rime/rhyme** - nucleus + coda.

This supports finer slant-rhyme reasoning.

### Similarity controls
You can hold:
- nucleus constant, vary coda;; coda family constant, move vowel nearby;
- stress contour constant across different word boundaries;; syllable count constant while changing lexical category;
- consonant manner/place approximately constant for articulatory echo.

The closer the relation, the more obvious the sonic connection. Wider slants can create freshness when timing and stress make the relation audible.

`rhyme_suggester.py` uses phoneme-tail and stress similarity as a candidate surface, not a verdict.

---

## Syllable weight and line design

Phonology distinguishes heavier and lighter syllable structures. For lyric craft, the exact linguistic theory should not be over-generalised across accents, but the practical insight survives:

- long vowels/diphthongs and closed syllables often carry more acoustic weight;; stressed heavy syllables can make strong anchors;
- clusters can slow articulation;; reduced vowels can act as connective tissue.

Therefore a “12-syllable line” is not one fixed rhythmic load.

---

## Stress as hierarchy

Stress is relational, not a binary paint layer.

Track:
- primary stress;; secondary stress;
- weak syllables;; adjacent strong syllables (potential clash);
- stretches of weak syllables (potential lapse).

Rap performance can deliberately override lexical defaults, but the override needs to sound owned.

`phoneme_map.py` and `prosody_map.py` expose stress patterns; supplied pronunciation wins.

---

## Phonotactics and articulation

A rhyme can be excellent on paper yet unperformable in context.

Check:
- transition into the rhyme word;; coda of previous word -> onset of target;
- repeated place/manner sequences;; sibilant pile-ups;
- whether a pickup compresses consonants before the beat;; whether final consonants disappear when the next line begins early.

This is why rhyme families should be filtered *after* phrase construction, not only before it.

---

## The three-position rhyme grid

For high-density writing, track recurring sound roles across:
1. opening/entry;
2. mid-line/mid-bar;
3. ending/landing.

The point is not to fill every cell. It is to create **correspondence**:
- opening answers opening;; mid position can carry the denser multisyllabic relation;
- ending can relax while internals continue;; one position can disappear to create contrast.

`rhyme_grid.py` provides a coarse token-position diagnostic. If beat-level timing is available, override token proportion with performed locations.

---

## Scheme break as event

A scheme change is strongest when aligned with another change:
- new scene;; new speaker;
- emotional pivot;; beat change;
- argument reversal;; tempo/density shift;
- reveal.

Then sound participates in form.

Random scheme changes read as abandoned technique. Deliberate displacement can create tension:
- expected end rhyme appears internally;; family vanishes for a bar then returns;
- rhyme is implied but withheld;; phrase rhyme crosses the line boundary.

## 3A. Extended phonological guidance

### Syllable structure
- Treat onset, nucleus and coda as separate sound channels; the stressed nucleus usually carries more perceptual weight than spelling.
- Coda similarity can tighten a family without requiring identical words; Onset variation prevents a chain from sounding like suffix substitution.
- Multiword mosaics may preserve stress and vowel shape across word boundaries.
- Do not call a relation “multisyllabic” if only the final syllable is doing the work.

### Stress hierarchy
- Record lexical stress before performed stress; Record performed stress before deciding musical alignment.
- A phrase may rhyme through matched prominence even when segmental tails differ.
- A dictionary stress pattern is a prior; supplied pronunciation or performance can override it.
- Unknown words should keep uncertainty rather than receive invented phonemes.

### Slant-rhyme search
1. Start with the stressed vowel or rime.
2. Preserve syllable count when phrase shape matters.
3. Search close tails before widening consonant tolerance.
4. Check whether the candidate survives the intended accent.
5. Check whether the candidate belongs in the semantic field.
6. Demote any candidate that forces syntax or meaning merely to land.

### Three-position architecture
- Opening, mid-bar, and landing rhyme are distinct positions; A strong grid can mirror all three across bars.
- Position changes can create movement without changing the rhyme family.
- Internal rhyme can carry continuity while end-rhyme placement breaks expectation.
- Use `rhyme_grid` to expose positions, then decide whether the pattern is musically useful.

## 4. Decision method

### 4.1. Frame
- Name the section function, hard constraints, and the complete set of craft objectives and questions; record them in `assets/templates/rhyme-phonology.md`.

### 4.2. Baseline
- Describe the present behaviour before judging it; Record the decision in `assets/templates/rhyme-phonology.md`.

### 4.3. Hinge
- Identify the full set of words, bars, events, and performance moments involved in the binding issue.
- Record the decision in `assets/templates/rhyme-phonology.md`.

### 4.4. Mechanism
- Explain how the suspected variable creates the observed effect; Record the decision in `assets/templates/rhyme-phonology.md`.

### 4.5. Isolate
- For causal comparison, hold strong dimensions fixed while varying each suspected lever separately; then combine every improvement that survives its isolated test and record the results in `assets/templates/rhyme-phonology.md`.

### 4.6. Material and tool support
- Ground the decision in supplied creative material, direct reading or rehearsal, and every relevant representation, detector or generator.
- Record the decision in `assets/templates/rhyme-phonology.md`.

### 4.7. Audition
- Compare baseline and candidate in the medium that matters; Record the decision in `assets/templates/rhyme-phonology.md`.

### 4.8. Collateral
- Check meaning, voice, rhyme, rhythm, performance, sequence, and consequence as relevant.
- Record the decision in `assets/templates/rhyme-phonology.md`.

### 4.9. Commit
- Keep the most effective change set that survives audition without analytical explanation; Record the decision in `assets/templates/rhyme-phonology.md`.

### 4.10. Handoff
- Pass observations, locked decisions, open questions, and generated candidates into every connected domain that can use them.
- Record the decision in `assets/templates/rhyme-phonology.md`.

## 5. Working variables

- **Stressed Vowel** · **Rime**
- **Onset** · **Coda**
- **Syllable Count** · **Stress Contour**
- **Phrase Shape** · **Word Boundary**
- **Internal Position**
- **Landing Position** · **Mosaic Rhyme**
- **Root Anchor** · **Assonance**
- **Consonance** · **Accent Variation**
- **Articulatory Ease**

## 6. Template contract

- Use `assets/templates/rhyme-phonology.md` for working state, not this reference.
- Fill every field relevant to the task; keep baseline and candidate visible together.
- Anchor the decision to exact lines, bars or timestamps; fill from supplied material, direct observation, rehearsal, or verified context, and keep genuine unknowns blank.
- Log tool id, input scope, output limit, and accepted/rejected implication; Record seed and locked dimensions for generative operations.
- Update the template whenever rehearsal or a new observation disproves the current working model.

## 7. Script routes — preflight each listed tool with `python scripts/tool_router.py --tool <id>` before execution

### Primary
- `phoneme_map` → `scripts/phoneme_map.py`
  - Contribution: maps pronunciation, stress, syllable structure and rhyme material.
  - Class: `representation`.
- `rhyme_suggester` → `scripts/rhyme_suggester.py`
  - Contribution: phonetic/slant rhyme candidates without committing to meaning.
  - Class: `generation`.
- `rhyme_grid` → `scripts/rhyme_grid.py`
  - Contribution: maps opening/mid/end rhyme positions and supported links.
  - Class: `detection`.
- `articulation_audit` → `scripts/articulation_audit.py`
  - Contribution: maps consonant density and physically awkward transitions.
  - Class: `detection`.
### Secondary
- `prosody_map` → `scripts/prosody_map.py`
  - Contribution: maps syllable density, lexical stress and candidate grid fit.
  - Class: `detection`.

### Tool-class boundaries
- Representation keeps supplied material beside labelled derived structure; detectors map concrete conditions and opportunities with locations and confidence.
- Generators and transforms create controlled candidates; evaluation combines mechanical observations with close reading, audition and comparison.
- Support checks runtime/package state, not craft quality.

## 8. Cross-file handoffs

- `references/lexical-engineering.md` ↔ `assets/templates/lexical-engineering.md`
- `references/prosody-flow.md` ↔ `assets/templates/prosody-flow.md`
- `references/performance-delivery.md` ↔ `assets/templates/performance-delivery.md`
- `references/voice-register.md` ↔ `assets/templates/voice-register.md`
- `references/revision-evaluation.md` ↔ `assets/templates/revision-evaluation.md`
- `references/revision-evaluation.md` once the task becomes comparative revision.

## 9. Failure modes

Repair the named craft variable, audition the result, and recheck every layer it changes.

### Spelling rhyme

### Suffix-only chains

### Dictionary accent treated as authority

### Slant rhyme without audible anchor

### Forced syntax for end rhyme

### Technical density with no semantic return

### Rhyme annotation required to hear relation

### Identical placement fatigue

### Articulation congestion

### Phoneme confidence hidden from user

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

- Template: `assets/templates/rhyme-phonology.md`; Domain index: `assets/domain-registry.json`
- Tool index: `assets/tool-catalog.json`; Composition matrix: `assets/composition-matrix.md`
- Validator: `scripts/validate_domain_architecture.py`; Router: `SKILL.md`
