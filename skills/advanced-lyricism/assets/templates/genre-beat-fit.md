# Genre and Beat Fit — Working Template

> Method: `references/genre-beat-fit.md`
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
- tempo:
- counting convention:
- backbeat:
- kick pattern:
- hi-hat subdivision:
- bass behaviour:
- swing:
- density range:
- pocket prior:
- entry prior:
- phrase loop:
- ad-lib space:
- vocal register:
- production density:
- counterpoint:
- genre ambiguity:

## UK drill lane controls
- pressure balance: technical / content / balanced
- foreground system:
- simplified system:
- landing profile:
- deviation functions:
- four-bar joints / actual beat hinges:
- optional 16-bar movement:
- deadpan / melodic / mixed delivery relation:
- content called for by the brief:

## Domain workspace

## Source
- type: MIDI / audio / beat profile / listening notes
- file:
- tempo:
- meter hypothesis:
- half/double-time ambiguity:
- section/time range:

## Actual beat observations
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
- `beat_profile_summary`
- `music_structure`
- `cadence_lab`
- `audio_to_json`
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

Profiles are priors, not laws. Start with the user's beat, voice and brief.

## UK drill
Affordances:
- syncopation/sliding bass;
- pickups;
- clipped/conversational entries;
- gallop/triplet-derived cells;
- 2-bar phrase logic;
- abrupt cadence turns.

UK rap/drill craft can include:
- multisyllabic vowel/stress matching;
- internal chains;
- precise line landings;
- understated/deadpan delivery;
- mundane/high-stakes collision;
- local/institutional specificity;
- controlled register switches.

These are tools. Violence and MLE markers are not mandatory because a beat is drill.

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
