# Advanced Lyricism

Advanced Lyricism is a skill for agents that enables much better writing, rewriting, diagnosing, beat-mapping, and performing of advanced rap and song lyrics. It connects meaning, voice, narrative, language, rhyme, prosody, music, genre, delivery, hooks, and revision through a directed composition graph, so the domains pass actual working artifacts to one another. Overall it's a passion project of mine with a lot of research as well as personal knowledge/experience from time with friends and artists. 

[![Validate skills](https://github.com/povvo/advanced-lyricism/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/povvo/advanced-lyricism/actions/workflows/validate-skills.yml)

> Release state: validated for the private GitHub source `povvo/advanced-lyricism`. Installation requires an authenticated GitHub account with access to the repository, and private repositories are not listed on skills.sh.

## What it does

- Preserves the user's subject, voice, pronunciation, register, emotional logic, supplied material, and hard constraints.
- Selects workflows from the requested work rather than from a genre label. “Drill” modifies the craft route; it does not seize the routing table.
- Composes 15 craft domains across context, meaning, sound, time, music, form, performance, and evaluation.
- Routes 27 deterministic Python tools through explicit capability checks and artifact handoffs.
- Supports text, MIDI, and audio-informed work while keeping observations, estimates, and unavailable measurements distinct.
- Sends revision findings back to every domain that owns the defect instead of promoting one score to executive producer.

The skill includes deep references, paired working templates, JSON schemas, beat profiles, a pronunciation dictionary, a bundled MIDI parser, and local tools for planning, representation, inspection, generation, transformation, mapping, delivery, and evaluation.

## Install

Inspect the discoverable skills without installing:

```bash
npx skills add povvo/advanced-lyricism --list
```

Install Advanced Lyricism into the current project:

```bash
npx skills add povvo/advanced-lyricism --skill advanced-lyricism
```

For a non-interactive Codex installation using copied files:

```bash
npx skills add povvo/advanced-lyricism --skill advanced-lyricism --agent codex --copy --yes
```

These GitHub-backed commands require authentication with access to the private repository. There is no separate npm publication step; `npx skills` installs from the repository.

## Use

Ask an agent to use the skill for work such as:

- drafting a verse while preserving a supplied voice and narrative pressure;
- building a hook whose repetitions change meaning rather than merely returning to work;
- revising rhyme, cadence, articulation, and delivery without flattening the lyric's intent;
- mapping supplied MIDI or audio observations into beat-aware writing constraints;
- diagnosing where concept, scene, sound, form, or performance stopped reinforcing the others.

The main routes are:

| Requested work | Pipeline | What it coordinates |
| --- | --- | --- |
| New lyric writing | `lyric_compound` | context, concept, voice, scene, language, rhyme, flow, form, delivery, revision |
| Causal drill scene construction | `narrative_drill_compound` | narrative pressure, drill-specific beat fit, consequence, phonology, performance |
| Writing to supplied music | `beat_locked_compound` | music representation, beat constraints, cadence, articulation, delivery |
| Hook construction | `hook_compound` | identity, return logic, contrast, lexical memory, cadence, song form |
| Coordinated revision | `revision_compound` | defect mapping, targeted alternatives, locked dimensions, downstream rechecks |

`narrative_drill_compound` is for requests where causal scene construction is central. The appearance of the word “drill” is not, by itself, an architectural event.

## How it works

The skill maintains six composition layers and passes named artifacts forward:

1. Context and pressure establish the brief, speaker, contradiction, relationships, and exclusions.
2. Event and meaning establish causal scenes, semantic fields, turns, and controlled variants.
3. Sound and time establish heard rhyme, stress, cadence, breath, and delivery constraints.
4. Music and form establish beat observations, section contrast, and return logic.
5. Evaluation maps defects back to every responsible layer.
6. Tool execution records capability state, ordered operations, and artifact handoffs.

Before a local tool runs, `scripts/tool_router.py` resolves its declared dependencies and reports whether the operation is fully available, partially available, or blocked. Missing capabilities remain unavailable or `null`; numeric zero is reserved for an observed zero, not a dependency that stayed home.

From the installed skill directory, inspect a route with:

```bash
python scripts/tool_router.py --pipeline lyric_compound
python scripts/tool_router.py --pipeline beat_locked_compound
python scripts/tool_router.py --pipeline revision_compound
```

## Repository layout

```text
.
├── README.md
├── skills/
│   └── advanced-lyricism/
│       ├── SKILL.md
│       ├── agents/
│       ├── assets/
│       ├── beats/
│       ├── references/
│       └── scripts/
└── .github/
    ├── scripts/validate-skill.mjs
    └── workflows/validate-skills.yml
```

Inside the skill:

- `SKILL.md` contains activation, constraints, workflow, and resource routing.
- `references/` contains the full craft methods for each domain.
- `assets/templates/` holds interoperable working-state templates.
- `assets/domain-registry.json` and `assets/tool-catalog.json` define the graph and executable routes.
- `assets/schemas/` defines structured interchange formats for music, delivery, context, scenes, phonology, and evaluation artifacts.
- `scripts/` contains the local toolchain and deterministic validators.
- `beats/` contains reusable beat-profile fixtures.

## Dependencies and capability states

Python is required for the local toolchain. Core text workflows use the standard library and bundled assets. Optional modules unlock additional capabilities:

| Capability | Provider |
| --- | --- |
| Pronunciation dictionary and lexical stress | bundled CMUdict or `cmudict` |
| MIDI parsing | bundled `mido` or installed `mido` |
| Audio feature analysis | `numpy` and `librosa` |
| Audio decoding | `soundfile` |
| Word-cloud image rendering | `wordcloud` |
| Porter stemming | `nltk` |

Run the dependency report before selecting tool-heavy workflows:

```bash
python skills/advanced-lyricism/scripts/dependency_check.py
```

Tool outputs assist audition and judgement; they do not prove artistic quality, perceived groove, vocal feasibility, or fit with an unheard performance. The skill treats those as decisions, not columns that became self-aware.

## Script behaviour

The project-owned scripts operate on local inputs. They print to standard output by default and write only when an explicit output path is supplied. `context_query_plan.py` prepares queries but does not execute network requests. Validation uses temporary fixtures; release packaging writes only to an explicitly selected output directory.

The bundled `mido` source retains upstream optional backend and socket utilities. Advanced Lyricism's advertised MIDI conversion route uses it to parse local Standard MIDI Files.

Review scripts and their declared capability gates before running them on valuable source material, as with any installable Agent Skill.

## Validate

From the repository root:

```bash
node .github/scripts/validate-skill.mjs skills
python skills/advanced-lyricism/scripts/validate_domain_architecture.py
python skills/advanced-lyricism/scripts/validate_runtime_contracts.py
DISABLE_TELEMETRY=1 npx --yes skills@latest add . --list
```

The included GitHub Actions workflow repeats structural validation, current-CLI discovery, and an isolated copied install on pushes to `main`, pull requests, manual dispatches, and a weekly compatibility schedule. A passing local run does not predict GitHub Actions by telepathy; the remote workflow remains a release gate after publication.

Private repositories are not eligible for ordinary skills.sh discovery. The GitHub-backed install remains available to authenticated users with repository access; the leaderboard will cope with the administrative silence.

## License

No project-level license has been granted yet for the original Advanced Lyricism material. Until one is selected, reuse and redistribution rights remain restricted by default.

Bundled third-party material retains its own terms:

- [CMU Pronouncing Dictionary license](skills/advanced-lyricism/assets/phonology/CMUDICT-LICENSE.txt)
- [Mido license](skills/advanced-lyricism/scripts/vendor/MIDO-LICENSE.txt)
