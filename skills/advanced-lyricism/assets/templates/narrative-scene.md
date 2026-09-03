# Narrative and Scene Architecture — Working Template

> Method: `references/narrative-scene.md`
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
- agent:
- want:
- opposing force:
- place:
- observable action:
- viewpoint:
- blind spot:
- image distance:
- cause:
- trigger:
- condition:
- reveal order:
- withheld information:
- state change:
- residue:
- callback:

## Domain workspace

| Unit | Viewpoint | Blind spot | Image distance | Visible / audible action | Cause relation | New information | Change / consequence | Withheld detail | Motif / callback | Sound / flow function |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | | | |
| 2 | | | | | | | | | | |
| 3 | | | | | | | | | | |
| 4 | | | | | | | | | | |

## Sequence tests
- Can units swap without changing meaning?
- What option closes or becomes irreversible?
- Is the relation cause / contrast / echo / jump / scale shift rather than just “and then”?
- Where does audience knowledge exceed speaker knowledge?
- Which cut relies on listener inference?
- Does a major event leave a body / relationship / resource / routine / belief / language trace?
- Is any line trying to show several sequential actions at once?
- Can a spoken explanation be replaced by observable action, object, or subtext?

## Anti-pattern audit
- crisis removed -> what still changes?:
- middle units that can swap:
- turn caused by character choice or imposed formula?:
- non-load-bearing person/subplot/image field:
- whose suffering is being instrumentalised?:
- costly action that proves the arc:
- opposition's independent want and method:
- exposition weaponised or merely recited?:
- narrator's blind spot / complicity / cost:
- reveal boundary and post-boundary payoff:
- literal chronology that should be compressed or reordered:

---

## Brief
- task / section / length:
- subject:
- speaker / viewpoint:
- addressee / audience:
- genre / register:
- emotional temperature:
- beat / BPM:
- hard constraints:
- supplied or established voice material:

## Pressure
- visible want / task:
- opposing force:
- contradiction worth holding:
- first irreversible change:
- consequence:

## Optional 16-bar drill scene spine
- bars 1–4 orientation / pressure:
- bars 5–8 action / procedure:
- bars 9–12 decision / reveal / cost:
- bars 13–16 residue / reframe:
- strongest actual hinge:
- reason to depart from 4/4/4/4:
- what remains unsaid:

## Technique budget
- bias: technical / content / balanced
- layer to densify:
- layer to simplify:
- planned contrast / pattern break:

## Semantic fields
- physical scene / objects:
- verbs / procedures:
- emotional pressure / value collision:
- native technical / cultural field:
- counter-field / collision partner:
- emergent third property:

## Scale / time / loop
- opening scale:
- planned zoom:
- invariant across scales:
- sequence dependency:
- delayed effect:
- reinforcing or balancing loop, if any:

## Perspective
- what speaker knows:
- blind spot:
- what listener knows first:
- alternate viewpoint that would change meaning:

## Motif
- first meaning:
- return context:
- final changed meaning:

## Sound / flow
- anchor family 1:
- anchor family 2:
- pocket / subdivision:
- landing profile:
- gear change / transition:
- breath / negative space:

## Section signposts
1.
2.
3.
4.

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
- `arc_generator`
- `technique_opportunity`
Coupled tool ids — use every one that can assist:
- `word_rearranger`

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

Use visual-narrative mechanisms—event, viewpoint, image sequence, dramatic tension and consequence—inside lyric form.

## Pressure, agency, and opposition
For narrative material define:
- agent/speaker;
- visible want or task;
- hidden fear/need when relevant;
- concrete place;
- opposing force;
- visible/audible action;
- withheld information;
- change;
- consequence;
- viewpoint.

A character who only receives events may still be a witness, but the section needs a changing relation to those events.

## Cause: trigger vs condition
Do not confuse the last visible trigger with the **underlying cause** or condition.

Ask:
1. What happened immediately before the outcome?
2. What condition made that trigger effective?
3. If the trigger vanished, would the outcome still be likely?
4. Does the attempted fix create another version of the problem?

Useful causal relations between units are equivalent to:
- therefore;
- but;
- because;
- meanwhile from a viewpoint that changes interpretation.

A run of “and then” can be valid montage, but it does not create causality by itself.

## Sequence is load-bearing
Order matters when it creates a state the next unit depends on.

Test:
- would reversing two units change interpretation?
- what becomes irreversible?
- what later reveal reclassifies an earlier detail?
- what should the audience know before the speaker?
- which event closes an option?
- which consequence has a delay?

### Information timing
Reveal the dangerous fact **early** to create dramatic irony/dread.
Reveal it **late** to create mystery/reclassification.
Repeat it **after cost** to turn information into consequence.

Do not treat reveal timing as decoration; it can change the narrative engine.

## Micro-scening
A short narrative can often use four functions:
1. orientation;
2. action/complication;
3. reversal/climax;
4. aftermath/reflection.

Do not force 4/4/4/4. The transferable rule is **change per unit**. A 2-bar scene can be complete if something enters, acts, and alters the state.

## Lyric camera: image selection, not camera cosplay
Borrow visual scale without writing screenplay directions.

- **wide:** place, crowd, weather, route, architecture, social field;
- **medium:** bodies in relation, approach/avoidance, blocking, task;
- **close:** object, hand, face, sound, screen, receipt, stain, gesture, one loaded detail.

Shift distance at meaning turns. “Cinematic” is not a virtue if the image itself is generic.

### One readable event per snapshot
The comics source warns against asking one static panel to perform two sequential actions. Lyric equivalent: when a line contains too many independent actions, the listener cannot form a stable image. Split or choose the decisive moment.

## Externalise the internal
Translate interior pressure into observable leakage:
- fear -> route checking, seating choice, scanning, body tension;
- grief -> saved messages, routines, untouched objects;
- guilt -> avoidance, ritual, over-explanation;
- anger -> clipped procedure, damaged object, narrowed attention;
- tenderness -> maintenance, memory, precise care.

Naming emotion is allowed. The test is whether the lyric also gives the listener concrete experience.
