# Advanced Lyricism user guide

## Reader outcome

Use this guide to turn a lyric request and its supplied material into a traceable working session. You will choose a route, establish a brief, preflight capabilities, preserve the right representation, carry artifacts through the composition graph, audition the result, and recover when a measurement or dependency is unavailable.

## 1. Establish the brief before touching a generator

Write a small working brief before selecting a pipeline. Include:

- the speaker, viewpoint, subject, contradiction, stakes, and causal scene;
- the intended section, audience, delivery, pronunciation, accent, register, and emotional distance;
- supplied lyrics, MIDI, audio, beat metadata, relationships, keep/reject history, or references;
- locked dimensions such as a phrase, event order, bar length, BPM, hook return, or spelling;
- exclusions and failure conditions;
- what the next decision must establish.

The skill treats the user's supplied voice, pronunciation, text, audio, and constraints as first-class craft knowledge. Genre and dictionary priors can add methods; they cannot silently replace the brief.

## 2. Select the work route

Choose the route from the requested job:

| Job | First route | Add when |
| --- | --- | --- |
| New or rewritten lyric | `lyric_compound` | Add `beat_locked_compound` when supplied music is authoritative |
| Causal drill scene | `narrative_drill_compound` | Keep universal lyric capabilities; drill is a method layer |
| Hook identity and changed returns | `hook_compound` | Add beat representation when a beat controls participation or contrast |
| Full revision | `revision_compound` | Use `revision_targeted` when the defect boundary is genuinely narrow |
| MIDI timing | `midi_to_verse` | Add the larger compound route for meaning, voice, and form |
| Audio timing | `audio_to_verse` | Check `audio_analysis`; fall back explicitly when blocked |
| Controlled alternatives | `controlled_ideation` | Keep generation separate from selection |
| Full script inventory | `script_sweep` | Use only when the user explicitly asks for a catalog sweep |

Preflight the plan:

```bash
python skills/advanced-lyricism/scripts/tool_router.py --pipeline lyric_compound
```

For a pipeline that contains optional audio, inspect the returned capability state before writing any sentence that depends on tempo, onset, or energy estimates.

## 3. Build the six-layer working state

### Context and pressure

Use `context_query_plan.py`, `scene_graph.py`, and `preference_profile.py` when current context, relationships, or prior keep/reject decisions matter. The output is a grounded brief and a speaker model, not a replacement for the artist's intent.

### Event and meaning

Use `idea_lab.py`, `arc_generator.py`, `semantic_field_map.py`, `technique_opportunity.py`, `word_rearranger.py`, and the lexical tools to establish causal events, semantic fields, turns, and controlled variants. A candidate line is still a candidate until it survives meaning, voice, sound, timing, and delivery checks.

### Sound and time

Use `phoneme_map.py`, `rhyme_suggester.py`, `rhyme_grid.py`, `prosody_map.py`, `cadence_lab.py`, and `articulation_audit.py` to inspect heard rhyme, stress, density, phrase shape, mouth-feel, and slot geometry. Dictionary coverage determines which phonological claims are safe. A spelling match is not a heard-rhyme verdict.

### Music and form

Represent the supplied beat first. Use `midi_to_json.py` for MIDI, `audio_to_json.py` only when its audio capability is available, `wav_energy_probe.py` for supported PCM WAV energy cues, or `beat_profile_summary.py` for bundled profiles. Then use `music_structure.py`, `beat_metadata_reconcile.py`, and `beat_affordance.py` to derive structure cues and candidate stress/space relationships. Keep raw timing beside derived coordinates.

### Evaluation feedback

Start with `craft_audit.py` for a component-preserving baseline. Add targeted detectors or use `workbench.py` when several observations need aggregate comparison. Route a supported defect back to all owning domains. Re-run every invalidated downstream layer after a change; a repaired rhyme can alter cadence, articulation, delivery, and hook return.

### Runtime orchestration

Every Skill-local call is planned through `tool_router.py`. `dependency_check.py` reports providers, while `runtime_capabilities.py` resolves bundled assets and importable modules. Treat `full`, `partial`, and `blocked` as operational states. A blocked measurement is unknown, not a score of zero.

## 4. Representation-specific procedures

### Text-only draft

```bash
python skills/advanced-lyricism/scripts/tool_router.py --pipeline lyric_compound
python skills/advanced-lyricism/scripts/phoneme_map.py -i lyrics.txt --summary
python skills/advanced-lyricism/scripts/prosody_map.py -i lyrics.txt --bpm 140 -o build/prosody.json
python skills/advanced-lyricism/scripts/rhyme_grid.py -i lyrics.txt -o build/rhyme.json
python skills/advanced-lyricism/scripts/delivery_notation.py -i annotated-lyrics.txt -o build/delivery.json
```

Use a pronunciation override when the speaker's pronunciation differs from the bundled dictionary. Keep the brief, tool outputs, selected changes, rejected variants, and audition notes together so a later revision can distinguish source material from derived observations.

### MIDI

```bash
python skills/advanced-lyricism/scripts/tool_router.py --pipeline midi_to_verse
python skills/advanced-lyricism/scripts/midi_to_json.py beat.mid -o build/music.json
python skills/advanced-lyricism/scripts/music_structure.py build/music.json -o build/structure.json
python skills/advanced-lyricism/scripts/beat_affordance.py build/structure.json -i lyrics.txt -o build/affordances.json
```

`midi_to_json.py` retains event timing and derives seconds/metric coordinates from tempo and meter events. It does not tell you whether a pocket feels right when performed.

### Audio and PCM WAV

First inspect the route:

```bash
python skills/advanced-lyricism/scripts/tool_router.py --pipeline audio_to_verse
python skills/advanced-lyricism/scripts/dependency_check.py --required audio_analysis
```

When `audio_analysis` is full, `audio_to_json.py` may estimate tempo, beats, onsets, and energy. If the required `numpy`/`librosa` capability is blocked, use supplied BPM/section timing or:

```bash
python skills/advanced-lyricism/scripts/tool_router.py --tool wav_energy_probe
python skills/advanced-lyricism/scripts/wav_energy_probe.py beat.wav -o build/wav-energy.json
```

The WAV route provides coarse energy and pulse cues only. Neither route establishes key, harmony, instrument identity, vocal intelligibility, half-time versus double-time, or artistic fit without further evidence and audition.

## 5. Audition and revision decisions

At each decision point, ask:

1. Does the line still mean what the brief requires?
2. Does the speaker still sound like the supplied voice and register?
3. Are the heard vowel/consonant relationships intentional?
4. Does the stress, density, breath, and bar-line behaviour work at the intended delivery?
5. Does the supplied beat or section form remain authoritative where it was locked?
6. Does the hook return with changed information or pressure when that is the design?
7. Which domain owns the remaining defect, and which downstream artifacts must be rerun?

Use the tools to expose alternatives and interactions. Keep the final decision with the writer's audition and judgement. If a tool was blocked, write that into the session record and state what was retained or deferred.

## 6. Recovery paths

| Situation | Recovery |
| --- | --- |
| `audio_to_json` is blocked | Keep supplied BPM/sections, use `wav_energy_probe` for supported PCM WAV cues, or defer audio-derived claims |
| Pronunciation is uncovered or dialect-specific | Supply an explicit pronunciation JSON override and label dictionary coverage as partial |
| MIDI parsing is unavailable | Use supplied beat metadata/timing and preserve the missing parser capability as blocked |
| PNG lexical cloud or stemming is unavailable | Continue with lexical JSON and text reports |
| A route returns a partial state | Use only its safe claims and identify which downstream decisions remain unsupported |
| A generated candidate harms voice or meaning | Reject it, retain locked dimensions, and regenerate from the owning domain |
| A repair changes a downstream dimension | Re-run the invalidated sound, beat, form, or delivery checks before accepting it |

## 7. Verification checklist

Before delivering a lyric or revision, verify the dimensions relevant to the task: meaning and pressure, voice/register fidelity, pronunciation, heard rhyme, timing and breath, beat fit, section movement, and performance feasibility. Before delivering a repository change, run the validators in the README and inspect `git diff --check` and the tracked status.
