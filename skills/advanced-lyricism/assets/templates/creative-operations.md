# Agent Tooling and Controlled Creativity — Working Template

> Method: `references/creative-operations.md`
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
- operation class:
- hypothesis:
- seed:
- locked dimensions:
- variable dimension:
- candidate count:
- generator:
- transformer:
- mutation:
- permutation:
- collision:
- random walk:
- crossover:
- selection criterion:
- expansion / selection rule:
- trace:

## Domain workspace

Start from one strong source line/scene/plan. Test each relevant dimension separately, then build combination variants from every compatible improvement.

| Variant | Meaning | Rhyme | Cadence | Syntax | Viewpoint | Scale | Image distance | Register | Delivery | Result |
|---|---|---|---|---|---|---|---|---|---|---|
| Source | lock | lock | lock | lock | lock | lock | lock | lock | lock | baseline |
| A | lock | lock | **vary** | lock | lock | lock | lock | lock | lock |  |
| B | lock | **vary** | lock | lock | lock | lock | lock | lock | lock |  |
| C | lock | lock | lock | **vary** | lock | lock | lock | lock | lock |  |

Useful mutations:
scale · time scale · viewpoint · syntax delay · payoff displacement · image distance · contradiction · register · caesura · metaphor lock · consequence · callback · sonic frame · delivery

Record seed when a script generates candidates.

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
- `idea_lab`
- `word_rearranger`
- `arc_generator`
- `cadence_lab`
Coupled tool ids — use every one that can assist:
- `rhyme_suggester`
- `lexical_cloud`
- `workbench`

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

The local tools are **craft instruments**, not miniature judges. They should make hidden structure inspectable, generate bounded alternatives, or test a concrete hypothesis. The agent remains responsible for meaning, taste, voice, context, and selection.

## Four operation classes

### 1. Representation
Convert opaque material into a stable intermediate form without deciding what it means.

Examples:
- MIDI -> note/event JSON with raw ticks, seconds, track/channel identity, tempo/meter maps and derived bar/slot coordinates;
- audio -> estimated beat/onset/energy/timbre JSON;
- text -> phoneme/stress/syllable JSON;
- annotated bars -> performance-event JSON.

A representation tool should preserve raw input and label every derived coordinate. It should not silently quantize, normalize accent, or infer artistic intention.

### 2. Detection
Find a concrete signal of a condition or **opportunity**.

Examples:
- likely enjambment/suspension hinges;
- stress-grid friction;
- consonant congestion;
- phrase-boundary candidates;
- repetition or register imbalance;
- density jumps.

Detection returns **location + signal + confidence/limits + a possible operation**. It does not say “this must be fixed.” A strong craft choice can look anomalous by design.

### 3. Generation / transformation
Produce alternatives while holding explicit constraints.

Examples:
- rearrange clauses while preserving the end word;
- generate rhyme candidates from phoneme tails;
- create cadence slot patterns for a syllable budget;
- mutate a concept along one structural dimension;
- permute a sequence;
- generate bar-level tension/density curves.

Generation should be reproducible where randomness is involved. Use `--seed`. Never confuse candidate quantity with quality.

### 4. Evaluation
Stress-test a concrete draft or plan.

Examples:
- articulation screen;
- delivery/breath notation audit;
- scheme/density audit;
- aggregated workbench report.

Evaluation returns dimension-specific diagnostics and comparisons that can be auditioned against the lyric.

---

## Generator vs transformer

Generation and transformation are different operations.

A **generator** creates new structural material from rules or distributions.  
A **transformer** takes supplied material and changes one or more parameters.

For lyrics:
- grammar scaffold = generator;
- clause rearrangement = transformer;
- rhyme suggestions = candidate generator constrained by sound;
- cadence variants = generator constrained by syllable count;
- “move this scene from room -> street -> institution” = transformer;
- callback mutation = transformer.

Prefer a transformer when the user already has strong material. It preserves identity and exposes *which* change caused the improvement.

---

## Parameter isolation

When a passage is weak, do not randomize everything.

Hold four dimensions constant and vary one:
- wording fixed -> vary cadence;
- cadence fixed -> vary rhyme landing;
- image fixed -> vary distance/scale;
- scene fixed -> vary viewpoint;
- hook words fixed -> vary omission/pause;
- rhyme family fixed -> vary syntax;
- meaning fixed -> vary line break;
- content fixed -> vary delivery notation.

Then compare. This is the lyric equivalent of changing one synthesis parameter while retaining the rest of the model.

### Why it matters
If meaning, rhyme, cadence, viewpoint, and register all change at once, the agent cannot infer why a candidate works. Parameter isolation turns ideation into **controlled creative search**.

---
