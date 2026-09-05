# Contributing

## Purpose

The goal is a source-backed contribution that preserves the explicit artifact and capability-state model and leaves a reviewable diff.

Contributions to the source graph, validators, references, templates, documentation, and route contracts are welcome when they preserve that model.

## Contribution task

Use this guide when you are changing the source graph, validators, references, templates, documentation, or route contracts. The intended result is a source-backed change that passes the local contract checks and can be reviewed from its exact diff.

## Development setup

```bash
git clone https://github.com/povvo/advanced-lyricism.git
cd advanced-lyricism
python skills/advanced-lyricism/scripts/dependency_check.py
python skills/advanced-lyricism/scripts/validate_domain_architecture.py && python skills/advanced-lyricism/scripts/validate_runtime_contracts.py
```

The final two lines are the repository's local contract checks; no package installation is required for the bundled text and MIDI paths. Read [docs/contributor-guide.md](docs/contributor-guide.md) before adding a tool, domain, pipeline, schema, reference, template, or dependency. Keep claims tied to measured outputs and include the relevant validator result in a pull request.

Validation evidence for this contribution path is source inspection plus the architecture, runtime, structural, and discovery commands shown here; no user-comprehension study is claimed.

## Verification and recovery

A contribution is ready for review when the architecture and runtime validators exit 0, `git diff --check` is clean, the tracked status contains the intended files, and the relevant discovery command returns `advanced-lyricism`. If a validator fails, keep its first error, repair the named source contract and paired resource, and rerun the command from the repository root. If discovery fails, check the skill path and host manifest before retrying; if the same failure persists, open a reproducible issue with the command, exit code, versions, and output.
