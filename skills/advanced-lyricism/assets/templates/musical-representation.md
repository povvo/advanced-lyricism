# Musical Representation and Beat Affordance — Working Template

> Method: `references/musical-representation.md`
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
- raw tick time:
- seconds:
- tempo map:
- meter map:
- note event:
- velocity:
- drum event:
- onset:
- beat estimate:
- energy:
- register:
- contour:
- repetition:
- boundary:
- negative space:
- half/double-time ambiguity:

## WAV and metadata reconciliation
- PCM WAV energy sections:
- coarse pulse candidate + support:
- metadata BPM/key claims:
- same/half/double-time alignment:
- unresolved conflict:
- downstream beat/form decision:

## Domain workspace

## Source
- type: MIDI / audio / beat profile / listening notes
- file:
- tempo:
- meter hypothesis:
- half/double-time ambiguity:
- section/time range:

## Raw musical input
- kick/snare/hats:
- bass / 808:
- melodic register / contour:
- recurring cycle:
- dropouts / rests:
- energy changes:
- phrase-boundary cues:
- harmonic/tonal changes:
- unusual timing:

## Lyric affordances
- candidate stress anchors:
- candidate negative space:
- pickup opportunities:
- places to sustain:
- places to simplify diction:
- places to increase density:
- places where syntax could cross the boundary:
- hook return / contrast opportunity:

## Counterpoint option
What happens if the vocal **does not** mirror the instrumental?

## Verification
Which observations came from:
- symbolic data:
- audio estimates:
- listening:
- user instruction:

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
- `midi_to_json`
- `audio_to_json`
- `music_structure`
- `beat_affordance`
- `beat_profile_summary`
Coupled tool ids — use every one that can assist:
- `cadence_lab`

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

Use when the lyric must respond to an actual instrumental, MIDI file, rhythmic grid, musical phrase, or production change.

The central principle: **a planning grid is a coordinate system, not the ontology of rhythm**.

## 1. Raw timing and derived timing

Preserve both.

### Raw MIDI events
- absolute tick;
- note-on/note-off;
- pitch;
- velocity;
- channel/track;
- tempo messages;
- time-signature messages;
- key-signature messages.

### Derived coordinates
- seconds;
- bar;
- beat;
- subdivision/slot;
- note duration;
- grouped bar features.

Keep raw ticks after mapping to a bar grid so derived coordinates can be recomputed when the meter interpretation changes.

`midi_to_json.py` emits both.

---

## 2. Partwise and timewise views

Computational music analysis benefits from two complementary arrangements.

### Partwise
Preserve track/channel/instrument identity.

Useful for:
- separating drums from pitched material;
- locating kick/snare anchors;
- examining one melodic layer;
- identifying repeated accompaniment roles.

### Timewise
Sort events globally by onset.

Useful for:
- finding density changes;
- comparing what happens simultaneously;
- identifying silence/negative space;
- detecting section boundaries.

The agent should not choose one representation globally. Use the view that answers the current question.

---

## 3. Meter is hierarchical and relational

A 4/4 bar can be drawn as 16 slots, but perception is not produced by equal boxes.

Listeners infer:
- stronger and weaker levels;
- grouping;
- recurring accents;
- duration patterns;
- pitch/register boundaries;
- contour turns;
- repetition;
- phrase endings;
- harmonic changes.

The Developing Musical Structures material is especially important here: **beat can emerge from relations among unequal durations**, and pitch/register can alter perceived grouping even when duration sequences stay the same.

Therefore:
- use slot indices as addresses;
- use metric-strength weights as hypotheses;
- retain events that contradict the assumed grid;
- allow the ear to revise the model.

---

## 4. Grouping cues

Potential phrase/section boundaries become more plausible when several cues coincide:

- rest or long gap;
- density discontinuity;
- register jump;
- contour reversal;
- repetition restarting;
- new instrumentation;
- velocity/energy change;
- harmonic arrival or departure;
- drum-pattern change;
- lyrical syntactic boundary;
- breath or held vowel;
- semantic turn.

No single cue is mandatory. `music_structure.py` deliberately returns **boundary candidates with supporting cues**, not “the phrase structure.”

### Same / different
At every return, ask:
- what is invariant?
- what changed?
- is the change local or structural?
- does the old pattern now mean something different?

This logic links musical form directly to hook craft and callback design.

---

## 5. MIDI event interchange

`advanced-lyricism.music-event-ir.v1` is the common symbolic representation.

Use it as input to:
- `music_structure.py`;
- `beat_affordance.py`;
- custom agent analysis.

Important fields:
- timing maps;
- notes;
- metric projection;
- drum flag;
- partwise track summary.

### Drum conventions
General MIDI channel 10 / zero-indexed channel 9 permits useful but imperfect kick/snare/hat identification. Treat drum-note identities as conventions, not universal production truth.

### Sustain
Note-off duration is not always sounding duration because sustain pedals and synthesis envelopes can extend sound. The converter labels this limitation.

---
