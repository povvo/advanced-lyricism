# Context and Scene Research — Working Template

> Method: `references/context-research.md`
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
- research question:
- freshness need:
- artist property:
- scene relationship:
- producer relationship:
- locality:
- production trait:
- language trait:
- platform context:
- source date:
- source type:
- confidence:
- contradiction:
- craft implication:
- supplied creative material:
- open questions / verification scope:

## Domain workspace

## Supplied creative material
- supplied artists/tracks/lyrics:
- requested properties:
- exclusions:
- beat/audio material:

| Observation | Basis | Date | Confidence | Craft implication |
|---|---|---|---|---|
| | | | | |

## Scene relationships
- artists/producers/collectives:
- locality:
- production traits:
- language/register traits:
- uncertain features:

## Query and relationship operations
- language/query phrase:
- research intent:
- queries that can change the lyric decision:
- scene-graph focus nodes:
- relation paths that affect craft:
- supplied keep/reject history:
- preference directions with enough support:

## Translation to craft
- rhyme:
- flow:
- voice/register:
- imagery/reference:
- hook/form:

## Scope and verification
- popularity: reach/attention signal; evaluate craft separately
- autocomplete: query-pattern signal; combine with scene and language context
- one artist: one node in the wider relationship graph
- unknown slang: verify usage, function, locality and currency before use

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
- `lexical_cloud`

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

- separate observation / inference / decision
- record supplied material and direct observations before interpretation
- preserve date, confidence and uncertainty where freshness matters
- do not convert file presence, popularity, or a detector score into craft proof
- route methodology questions back to the paired deep reference
