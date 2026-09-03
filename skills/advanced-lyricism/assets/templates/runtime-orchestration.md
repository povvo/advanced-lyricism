# Runtime Orchestration — Working Template

> Method: `references/runtime-orchestration.md`
> Planner: `scripts/tool_router.py`
> Capability probe: `scripts/dependency_check.py`
> Fill every field relevant to the task. Record the composition graph, routed scripts, support states and passed-forward artifacts; leave genuinely unknown details blank.

## Request

- user request:
- supplied inputs:
- target section:
- craft objectives / questions:
- primary craft domain(s):
- why each selected tool can assist this decision:
- selected composition bundle or custom graph:
- why these layers must compound:

## Composition graph

| Stage | Domains / paired templates | Input artifact | Output artifact | Feeds stage | Feedback owner |
|---|---|---|---|---|---|
| | | | | | |

- high-value domain intersections:
- locked facts / dimensions shared across every stage:
- optional stage and activation condition:
- domain awaiting missing input or capability, plus recovery route:
- feedback edges that may reopen an earlier stage:

## Preflight receipt

- pipeline id:
- planner command:

| Tool | Stage | Runtime state | Supported outputs used | Unavailable outputs | Missing capability / input | Recovery or next availability |
|---|---|---|---|---|---|---|
| | | full / partial / blocked | | | | |

- tool / pipeline ids:
- aggregate runtime state: full / partial / blocked
- required capabilities:
- missing required:
- preferred capabilities:
- missing preferred:
- conditional modes:
- supported outputs:
- unavailable outputs in partial mode:
- fallback:
- paired deep references:
- paired working templates:

## Execution

| Tool | Exact input | Command | Seed | Exit | Schema / support state | Output artifact consumed by |
|---|---|---|---|---|---|---|
| | | | | | | |

- exact input file / text ranges:
- pronunciation override file, if any:
- seeds, if stochastic:
- locked dimensions:
- commands and exit codes:
- output schemas:
- output artifacts:
- component support states:
- coverage:
- raw representations preserved separately from derived interpretations:
- null/unavailable fields:

## Interpretation

- observations actually supported:
- measurements explicitly unavailable:
- candidate implication:
- accepted / rejected:
- reason:
- direct audition / supplied performance or input:
- conflict between tool and audition:
- resolution:

## Decision point

- status of every current craft objective / question:
- are the current stage artifacts internally consistent?:
- new or remaining defects / opportunities:
- every owning domain to reopen:
- every downstream stage invalidated by the change:
- all next tools that can assist and what each contributes:
- next domains and tools in execution order:
- tools awaiting missing input or capability, plus recovery routes:

## Workbench inputs

Run workbench when:
- [ ] a real draft exists
- [ ] targeted diagnosis already occurred, or aggregate confirmation is explicitly needed
- [ ] component support states will be inspected
- [ ] unavailable metrics will not be treated as zero

## Completion

- [ ] tool planned before execution
- [ ] runtime state respected
- [ ] unavailable tools used their recovery or fallback route
- [ ] partial outputs were interpreted at their reported coverage
- [ ] unknown remained null/unavailable
- [ ] output schema checked
- [ ] original input kept alongside derived representations
- [ ] stochastic seed recorded
- [ ] decision recorded separately from raw output
- [ ] next route continues every applicable connected domain and tool
- [ ] every stage passed an explicit artifact to the next
- [ ] revision feedback reopened every owning domain, not merely the last tool used
