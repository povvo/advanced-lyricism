# Advanced Lyricism contributor guide

## Reader outcome

Use this guide to add or maintain a domain, tool, pipeline, schema, reference, template, beat profile, validator, or dependency without breaking the composition graph or overstating what the runtime can measure.

## Repository contracts

The repository has one source of truth for each contract:

| Contract | File or directory | Update it when |
| --- | --- | --- |
| Agent activation, constraints, examples, resource routing | `skills/advanced-lyricism/SKILL.md` | The user-facing skill behaviour or route names change |
| Machine-readable domains, edges, bundles | `skills/advanced-lyricism/assets/domain-registry.json` | A domain, edge, bundle, reference, template, or primary tool changes |
| Tool inputs, outputs, capabilities, fallbacks, CLI | `skills/advanced-lyricism/assets/tool-catalog.json` | A tool or safe-claim boundary changes |
| Providers, capability states, unknown rule | `skills/advanced-lyricism/assets/dependency-manifest.json` | A dependency, bundled fallback, or capability gate changes |
| Human-readable reference/template/tool pairs | `skills/advanced-lyricism/assets/reference-template-index.md` | A pair is added, renamed, or removed |
| Directed cross-correlation and compound chains | `skills/advanced-lyricism/assets/composition-matrix.md` | Layer order, intersections, or feedback edges change |
| Interchange schemas | `skills/advanced-lyricism/assets/schemas/` | An output contract changes |
| Deep craft methods | `skills/advanced-lyricism/references/` | The method or evidence boundary changes |
| Working state | `skills/advanced-lyricism/assets/templates/` | The corresponding method needs new fields |
| Executable implementation | `skills/advanced-lyricism/scripts/` | A declared tool changes |
| Beat fixtures | `skills/advanced-lyricism/beats/` | A reusable profile or metadata fixture is added |

Do not add a script in isolation. The graph needs a reason for the tool, an input/output contract, capability state, safe claims, fallback, reference, template, and downstream consumers.

## Add a tool

1. State the craft question the tool answers and the input representation it requires.
2. Implement the public script under `skills/advanced-lyricism/scripts/` with a stable CLI, explicit output path behaviour, and clear errors.
3. Keep generation, transformation, detection, and evaluation separate. A generated candidate is not an evaluation result.
4. Add the tool to `assets/tool-catalog.json` with its class, script, input, output, deterministic status, primary domain/reference/template, required and preferred capabilities, safe claims, forbidden partial claims, fallback, and first/full CLI forms.
5. Add providers and capability logic to `assets/dependency-manifest.json`. A missing optional dependency must remain `partial` or `blocked`, never a negative measurement.
6. Add the tool to its domain's `primary_tools` or `secondary_tools` and to every pipeline that can actually consume it. Update `SKILL.md` route tables and phase descriptions when the agent-facing contract changes.
7. Add or update the reference/template pair, schema, and runtime contract tests needed to make the output interoperable.
8. Run the architecture, runtime, skill, and CLI validators before asking for review.

## Add a domain

1. Define the domain's purpose in terms of an actual craft decision.
2. Create the deep reference and paired working template.
3. Register the domain, primary/secondary tools, cross-links, and graph edges in `domain-registry.json`.
4. Add the pair to `reference-template-index.md` and the relevant layer/correlation in `composition-matrix.md`.
5. Add the domain to the applicable compound pipeline stages and describe what artifact it passes forward.
6. Add a feedback edge if revision findings can belong to the domain.
7. Update the user-facing route and contributor docs with the new decision boundary and limitations.

## Add or change a pipeline

Define the pipeline by requested work and artifact dependencies, not by a genre label. Every pipeline should state:

- the purpose and applicable inputs;
- the preflight operation;
- ordered representation, foundation, detection, generation, transformation, evaluation, and audition stages as applicable;
- each tool's inputs and outputs;
- the decision point where evidence is integrated;
- the owner domains for defects and the downstream checks invalidated by a repair;
- a fallback when a capability is unavailable.

Register the pipeline in `assets/tool-catalog.json`, mirror the name and selection rule in `SKILL.md`, document it in the README/user guide, then run a real preflight and representative route execution. Keep exit codes and blocked states in the evidence record.

## Change a dependency or fallback

1. Update the provider and capability declaration in `dependency-manifest.json`.
2. Update the tool catalog's required/preferred capabilities, safe claims, partial forbidden claims, and fallback.
3. Run the full dependency report and a required-capability check that exercises the expected exit path.
4. Run the route through `tool_router.py` and execute the tool in both available and unavailable conditions when practical.
5. Update README/user-guide limitations so a reader can choose a useful fallback without inferring unsupported analysis.

For audio, keep the distinction between `audio_to_json`'s estimated tempo/beat/onset/energy route and `wav_energy_probe`'s coarse PCM WAV energy/pulse route. Neither route permits claims about key, harmony, instrument identity, or performed feel without separate evidence.

## Validate locally

From the repository root:

```bash
node .github/scripts/validate-skill.mjs skills
python skills/advanced-lyricism/scripts/validate_skill.py skills/advanced-lyricism
python skills/advanced-lyricism/scripts/validate_domain_architecture.py
python skills/advanced-lyricism/scripts/validate_runtime_contracts.py
DISABLE_TELEMETRY=1 npx --yes skills@latest add . --list
git diff --check
```

Use `PYTHONDONTWRITEBYTECODE=1` for repeated Python checks when you want to avoid new ignored bytecode. Inspect the exact tracked diff and status; an ignored cache warning from the Node validator is not a substitute for a clean source review.

## Recovery and escalation

When a change does not validate, keep the failing output and repair the source contract before retrying.

| Failure | First check | Recovery |
| --- | --- | --- |
| Architecture validator rejects a domain, edge, bundle, or pair | Read the first path and compare the registry with `reference-template-index.md` and `composition-matrix.md` | Update the source registry and every paired resource, then rerun `validate_domain_architecture.py`; success is a zero exit with the expected domain/tool counts. |
| Runtime validator rejects a capability or output contract | Inspect `dependency-manifest.json`, the tool catalog safe claims, and the relevant schema | Keep unavailable providers `partial` or `blocked`, repair the contract/fallback, and rerun `validate_runtime_contracts.py`; do not turn unknown into numeric zero. |
| Discovery or copied install fails | Confirm the skill path and `advanced-lyricism` identifier, then rerun the CLI from the repository root | Fix the host manifest or source layout, rerun the structural validator and `npx --yes skills@latest add . --list`, and record the exact exit/output. |
| A route change alters downstream meaning, timing, or delivery | Compare the changed artifact with its consumers and owning domains | Rerun the invalidated downstream tools and audition the result; if the defect remains, revert only the pending change after preserving the evidence record. |

If a failure persists after the applicable repair and rerun, stop the change and escalate with the exact command, exit code, source path, input representation, Python/Node version, and captured output. A passing preflight is not a successful lyric or installation.

## Review checklist

- The change preserves user-supplied voice, pronunciation, text, audio, and hard constraints.
- Source observations, derived coordinates, interpretations, generated candidates, and human decisions remain distinguishable.
- Unknown or blocked measurements remain unknown/null; zero means an observed zero.
- Every new script call is routed through `tool_router.py`.
- Every output has a readable path, schema or documented shape, and a consumer.
- References and templates are paired and linked from the registries.
- Revision findings route backward to every owning domain and trigger downstream rechecks.
- CLI exits are documented and tested, including the expected blocked path for missing optional capabilities.
- README and user documentation describe the actual setup, limitations, examples, and recovery path.
- Third-party files retain their licenses; update the attribution if a bundled asset changes.

## Release hygiene

Keep repository metadata and workflow claims separate from local validation. A passing local command proves the command in the current checkout. CI status, repository topics/description, remote commit identity, and copied-install readback are separate release evidence and should be checked explicitly during release review. Never turn a preflight, fixture run, or generated cache into a claim that a remote workflow or native host accepted the change.
