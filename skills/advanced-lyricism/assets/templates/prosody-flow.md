# Prosody, Flow, and Bar-Line Dynamics — Working Template

> Method: `references/prosody-flow.md`
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
- entry:
- subdivision:
- lexical stress:
- performed stress:
- musical accent:
- pocket:
- density:
- breath:
- caesura:
- enjambment:
- suspension:
- run-on syntax:

## UK drill landing profile
- clean-landing baseline:
- soft-enjambment function:
- suspension and immediate resolution:
- run-on breath/release plan:
- beat joints for turns:
- user-selected caps, if any:
- gear change:
- negative space:
- rhyme placement:
- transition:

## Domain workspace

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

---

Do not add techniques by quota. Find hinges already present.

| Location | Observed signal | Possible technique | What it could change | One local experiment | Keep / reject + reason |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

Check every applicable signal:
- grammatical dependency near a boundary -> enjambment / suspension
- repeated end closure -> scheme displacement / internal answer
- stable density -> gear change / negative space
- abrupt density jump -> transition hinge
- recurring image/token -> callback transformation
- exact cross-domain property -> collision / metaphor lock
- ambiguous word/sound -> surface-first entendre
- scene without residue -> consequence
- uniform image distance -> zoom / scale shift
- emotional declaration -> externalised physical manifestation
- local register drift -> code-switch or restore speaker syntax
- production gap -> breath / withheld word / ad-lib / impact silence

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
- `prosody_map`
- `cadence_lab`
- `technique_opportunity`
Coupled tool ids — use every one that can assist:
- `beat_affordance`
- `articulation_audit`

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

Flow is the relation among lexical stress, performed accent, syntax, rhyme position, beat location, density, breath, articulation, and timing.

## Grid
A 4/4 16th grid is a planning surface, not a prison:

`1 e & a | 2 e & a | 3 e & a | 4 e & a`

Map:
- kick/backbeat;
- subdivisions and swing;
- phrase entry/exit;
- stressed syllables;
- rhyme points;
- breaths;
- rests/held vowels.

Then decide which moments confirm or disturb the grid.

## Stress alignment
For each important word ask:
- where is lexical stress in speech?
- where is the performed accent?
- where is the musical accent?
- is mismatch expressive or accidental?

A deliberate mismatch can create urgency, drag, looseness, or ambiguity. An accidental mismatch often sounds written rather than performed.

## Cadence families
Starting geometries:
- straight subdivision;
- triplet;
- gallop;
- swing;
- half-time;
- speech-effusive/conversational;
- percussion-effusive/articulatory;
- sung/melodic.

They are resources, not genre laws. Cadence becomes personal through entry point, stress contour, vowel duration, consonant attack, density, and where syntax resolves.

## Pocket
A phrase can sit ahead, on top, behind, or across the bar. Moves include:
- pickup/anacrusis;
- delayed first stress;
- early finish;
- held vowel;
- consonant hit against kick/snare;
- internal rhyme answering percussion;
- deliberate empty subdivision after impact.

Microtiming is a performance observation; text alone does not provide millisecond precision.

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
- denser subdivisions;
- shorter syntactic units;
- more internals;
- earlier entries;
- harder consonant attack;
- reduced silence.

Shift **down** with:
- longer vowels;
- fewer syllables;
- later entry;
- simpler rhyme;
- one plain declarative line;
- more breath/negative space.

### Transition mechanics
A gear change can:
- **cut cleanly** at a section/line;
- use a **transitional bar** containing features of both pockets;
- pivot on one word whose placement belongs to the old pattern while its continuation establishes the new;
- **morph** over several beats.

Choose the transition itself as part of the expression.
