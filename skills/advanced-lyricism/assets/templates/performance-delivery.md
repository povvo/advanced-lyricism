# Performance and Delivery — Working Template

> Method: `references/performance-delivery.md`
> Fill every field relevant to the task. Leave genuinely unknown details blank.
> Tool outputs expose patterns for audition; they do not select edits.

## Decision
- craft objectives / questions:
- section / lines:
- user constraints to preserve:
- supplied creative material:
- uncertainty that matters:
- current hypotheses:
- success conditions:

## Working variables
- entry point:
- pocket:
- consonant attack:
- vowel duration:
- performed stress:
- breath:
- pause:
- loudness:
- pitch contour:
- sustain:
- tone:
- ad-lib:
- double vocal:
- silence after impact:
- rehearsal observations:
- studio constraint:

## Domain workspace

Use after the words are stable enough to rehearse.

## Section
- target BPM:
- base subdivision:
- base pocket:
- emotional register:
- reference performance constraints:

## Bar / line map

| Bar | Text | Entry | Primary stresses | Breath | Pause / silence | Tone | Pitch / sustain | Ad-lib | Transition |
|---|---|---|---|---|---|---|---|---|---|
| 1 |  |  |  |  |  |  |  |  |  |

Notation:
`//` breath · `CAPS` emphasis · `(ad-lib)` · `...` pause · `~` slide · `↑↓` pitch · `[tone]` · `_` sustain

## Rehearsal observations
- repeated stumble:
- involuntary breath:
- swallowed word:
- natural stress change:
- better unplanned pocket:
- line that improves without wording change:

## Decision
Keep notation only where it matches the chosen performance.

---

| Bar | Function | Entry | Strong stresses | Internal rhyme | Landing rhyme | Line ending | Density | Breath | Delivery / transition |
|---|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | | |
| 2 | | | | | | | | | |
| 3 | | | | | | | | | |
| 4 | | | | | | | | | |

Line ending: strong / soft enjambment / hard enjambment / suspension / run-on.

Working notation: `//` full breath, `/` quick breath, `_` held vowel, `>` accelerate, `<` decelerate, `^WORD` stress, `(ad-lib)`, `[rest]`.

If pocket changes, mark: clean cut / transitional bar / pivot word / morph.

Check natural vs performed stress, density contrast, breath, consonant congestion, and whether line-boundary behaviour serves meaning.

## Tool route
- planner command: `python scripts/tool_router.py --tool <id>`
- preflight state: full / partial / blocked
- available outputs:
- unavailable outputs in partial mode:
- missing capability / fallback:
- tool id:
- why this tool can change the decision:
- input:
- seed / locked variables, if generative:
- output / observations:
- limitation / uncertainty:
- accepted implication:
- rejected implication + reason:

Suggested primary tool ids:
- `delivery_notation`
- `articulation_audit`
- `prosody_map`
Coupled tool ids — use every one that can assist:
- `beat_affordance`

## Handoff
- remaining craft questions / opportunities after this pass:
- next reference/template:
- state to carry forward:
- state to preserve for later passes:

## Completion
- [ ] meaning / voice preserved
- [ ] change serves the named craft question
- [ ] tool estimates labelled as estimates
- [ ] no field filled by unsupported guess
- [ ] every connected applicable domain received the current state

## Quick operating card

> Use for execution. For rationale, edge cases, cross-domain reasoning and tool interpretation, read the paired deep reference.

Delivery is not an afterthought applied to finished words. It is one of the variables that determines rhyme, stress, timing, intelligibility, emotional distance, and impact.

## Performance parameters

Track separately:
- entry point;
- subdivision;
- pocket;
- consonant attack;
- vowel duration;
- lexical vs performed stress;
- breath;
- pause;
- loudness/emphasis;
- pitch contour;
- sustain;
- tone/texture;
- ad-lib placement;
- double/gang vocal;
- silence after impact.

A line can improve without changing one word if one of these parameters changes.

---

## Delivery notation

The package supports a lightweight notation:

- `//` or `(B)` - planned breath;
- `CAPS` - emphasis;
- `(ad-lib)` - secondary vocal;
- `...` - pause/rest;
- `~` - pitch slide;
- `↑` / `↓` - pitch direction;
- `[tone]` or `[flow]` - texture/cadence instruction;
- `_` - sustain;
- `/` - explicit syllable division when needed.

Use `delivery_notation.py` to convert a marked page into `advanced-lyricism.delivery-ir.v1`.

The notation is a **performance script**, not an acoustic measurement.

---

## Breath as rhythm

A breath occupies time. It can:
- reset flow;
- articulate a section;
- create anticipation;
- make a dense run physically possible;
- expose vulnerability;
- sound percussive;
- become part of a call/response.

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
- expressive;
- characterful;
- pronunciation-specific;
- groove-specific;
- or simply accidental.

Do not “correct” nonstandard stress that belongs to the speaker's accent or chosen delivery.

---

## Consonant attack and vowel field

Consonants help place rhythm. Vowels carry pitch, sustain and much of rhyme.

For precision:
- use plosives for hard attacks when articulation remains possible;
- watch repeated sibilant or stop sequences at speed;
- place long vowels where sustain or pitch movement has room;
- use reduced vowels/connective syllables to move between stresses;
- consider whether an end rhyme is actually audible after consonant crowding.

`articulation_audit.py` is a congestion screen. Rehearsal remains decisive.

---

## Pocket

Treat ahead/on/behind as a **relationship**, not a fixed millisecond number.

### Ahead
Can create:
- urgency;
- attack;
- anticipation.

Risks:
- rushing;
- lost final consonants;
- no room for breath.

### On
Can create:
- clarity;
- militancy;
- percussive lock.

Risks:
- stiffness;
- nursery-like predictability if every syntax/rhyme boundary also locks.

### Behind
Can create:
- ease;
- authority;
- conversational weight;
- melancholy.

Risks:
- dragging without intention;
- poor interaction with dense/jagged drums.

Actual pocket must be heard or measured from performance. Text cannot certify it.

---
