# Advanced Lyricism Composition Matrix

A lyric build is a **directed composition graph**, not a one-domain lookup. Domains create intermediate craft artifacts; other domains consume, constrain, transform, perform, or evaluate them. A useful build may move through several layers and loop backward after audition.

Legend: `→` feeds · `×` compounds bidirectionally · `↺` returns revision findings · `G` means tool output has a declared support state.

## Layer matrix

| Layer | Domain pairs | Shared artifact | Feeds |
|---|---|---|---|
| 1. Context and pressure | `context-research` × `concept-architecture` × `voice-register` | grounded brief, speaker model, contradiction, stakes, exclusions | scene/meaning, music/form |
| 2. Event and meaning | `narrative-scene` × `lexical-engineering` × `rhetoric-impact` × `creative-operations` | causal scene spine, semantic fields, image system, turns, candidate mutations | sound/time, hook/form |
| 3. Sound and time | `rhyme-phonology` × `prosody-flow` × `performance-delivery` | heard rhyme network, stress grid, cadence arc, breaths, entries, emphasis | music/form, evaluation |
| 4. Music and form | `musical-representation` × `genre-beat-fit` × `hook-song-form` | beat affordances, section boundaries, return logic, contrast plan | sound/time, evaluation |
| 5. Evaluation and feedback | `revision-evaluation` | defect map, comparisons, accepted/rejected changes | `↺` any owning craft layer |
| 6. Runtime control | `runtime-orchestration` | preflight plans, support gates, execution receipts | every tool-bearing layer |

Every domain id above resolves through `assets/domain-registry.json` to its deep reference, paired template, tools, cross-links, layer and compound bundles.

## Domain × tool cross-correlation

A tool may appear in several rows because its output can strengthen several craft layers. Primary tools directly shape the row's working artifact; coupled tools pass useful output across an adjacent layer.

| Domain | Primary tools | Coupled tools |
|---|---|---|
| concept architecture | `idea_lab`, `arc_generator`, `word_rearranger` | `technique_opportunity` |
| lexical engineering | `lexical_cloud`, `semantic_field_map`, `rhyme_suggester`, `phoneme_map` | `word_rearranger` |
| rhyme and phonology | `phoneme_map`, `rhyme_suggester`, `rhyme_grid`, `articulation_audit` | `prosody_map` |
| prosody and flow | `prosody_map`, `cadence_lab`, `technique_opportunity` | `beat_affordance`, `articulation_audit` |
| musical representation | `midi_to_json`, `audio_to_json`, `wav_energy_probe`, `music_structure`, `beat_affordance`, `beat_profile_summary`, `beat_metadata_reconcile` | `cadence_lab` |
| performance and delivery | `delivery_notation`, `articulation_audit`, `prosody_map` | `beat_affordance` |
| narrative scene | `arc_generator`, `technique_opportunity` | `word_rearranger`, `scene_graph` |
| rhetoric and impact | `idea_lab`, `technique_opportunity`, `word_rearranger` | `rhyme_suggester`, `semantic_field_map` |
| voice and register | `lexical_cloud`, `phoneme_map`, `word_rearranger` | `delivery_notation`, `context_query_plan`, `preference_profile` |
| hook and song form | `arc_generator`, `cadence_lab`, `music_structure` | `lexical_cloud`, `wav_energy_probe` |
| genre and beat fit | `beat_profile_summary`, `music_structure`, `cadence_lab`, `audio_to_json`, `wav_energy_probe`, `beat_metadata_reconcile` | `beat_affordance`, `context_query_plan`, `scene_graph` |
| revision and evaluation | `craft_audit`, `workbench`, `articulation_audit`, `rhyme_grid`, `technique_opportunity`, `lexical_cloud`, `semantic_field_map`, `preference_profile` | `prosody_map`, `delivery_notation` |
| context research | `context_query_plan`, `scene_graph` | `lexical_cloud`, `preference_profile` |
| creative operations | `idea_lab`, `word_rearranger`, `arc_generator`, `cadence_lab` | `rhyme_suggester`, `lexical_cloud`, `semantic_field_map`, `preference_profile`, `workbench` |
| runtime orchestration | `tool_router`, `dependency_check` | every routed tool and downstream artifact |

## High-value cross-domain intersections

| Intersection | Compounded result |
|---|---|
| context × voice | current/local facts become speaker-credible syntax, address and pronunciation rather than pasted references |
| concept × narrative | abstract pressure becomes agency, events, reveal order and consequence |
| concept × rhetoric | contradiction becomes inversion, collision, double meaning or delayed reclassification |
| narrative × lexical | each scene demands concrete entities, actions, institutions, sensory detail and consequence vocabulary |
| voice × lexical | word choice is filtered by social relation, register, knowledge limits and the user's supplied habits |
| lexical × rhetoric | domain-accurate terms acquire second readings without losing their literal surface |
| lexical × rhyme | semantic candidates are filtered by heard vowel/stress/phrase fit instead of spelling |
| rhetoric × rhyme | the acoustic landing reinforces the semantic pivot rather than decorating it |
| rhyme × prosody | rhyme anchors constrain stress, placement, enjambment, suspension and density |
| prosody × performance | the written grid becomes breath, attack, duration, silence, pitch and texture |
| music × genre | actual beat observations correct or confirm genre priors |
| music × prosody | drum/bass/section observations anchor cadence, pickups, gaps and gear changes |
| genre × hook | lane conventions condition participation, return length, density and production contrast without dictating content |
| narrative × hook | each return inherits new listener knowledge and therefore a changed meaning |
| revision × owning domain | a measured or auditioned defect routes backward to every layer that can repair it |

## Compound bundle matrix

| Bundle / pipeline | Foundation | Meaning construction | Sound and timing | Music and form | Feedback |
|---|---|---|---|---|---|
| lyric work / `lyric_compound` | context + concept + voice | narrative + lexical + rhetoric + creative | rhyme + prosody + delivery | music + genre + hook | revision ↺ all owners |
| `narrative_drill` / `narrative_drill_compound` | context + genre + voice + concept | narrative + lexical + rhetoric + creative | rhyme + prosody + delivery | music + hook when used | revision ↺ content, register, pocket |
| `beat_locked_verse` / `beat_locked_compound` | music + genre + voice | concept + lexical + rhetoric | rhyme + prosody + delivery | section/beat constraints stay live | revision ↺ timing and diction |
| `hook_system` / `hook_compound` | concept + voice + context | lexical + rhetoric + narrative | rhyme + prosody + delivery | hook + music + genre | revision ↺ identity/contrast/return |
| `revision_feedback` / `revision_compound` | revision baseline | load every domain implicated by the defect | run all relevant detectors | retain beat/form constraints | compare, audition, loop until stable |

Bundles are starting graphs, not fixed quotas. Select them from the requested work, not from a genre word. Genre-specific material supplements the selected graph; “drill” alone does not select `narrative_drill` or exclude universal capabilities.

## Tool-chain phases

| Phase | Tools | Output consumed by later phases |
|---|---|---|
| map context | `context_query_plan`, `scene_graph`, `preference_profile` | research questions, supplied relationship topology and accepted/rejected feature associations |
| represent | `midi_to_json`, `audio_to_json`, `wav_energy_probe`, `phoneme_map` | stable music/audio/WAV-energy/phoneme representations |
| inspect structure | `music_structure`, `beat_profile_summary`, `beat_metadata_reconcile`, `beat_affordance`, `craft_audit` | section, beat, metadata and draft baselines |
| generate | `idea_lab`, `arc_generator`, `lexical_cloud`, `rhyme_suggester` | candidate concepts, arcs, word fields and sound families |
| transform | `word_rearranger`, `cadence_lab` | controlled semantic/syntactic/cadence variants |
| detect and map | `semantic_field_map`, `rhyme_grid`, `prosody_map`, `articulation_audit`, `technique_opportunity` | local observations for semantic progression, rhyme, timing, articulation and missed opportunities |
| perform | `delivery_notation` | rehearsal-ready breath, emphasis, pitch, tone and ad-lib plan |
| integrate | `workbench` | cross-detector integration after component outputs, with support states preserved |

All tool calls are `G`: preflight with `scripts/tool_router.py`, preserve full/partial/blocked state, and treat unavailable fields as unknown rather than zero.

## Execution protocol

1. Combine every named bundle whose layers can assist the task, or assemble their union as a custom graph from the layer matrix.
2. Load every domain pair in the graph and record its shared artifact in the paired template.
3. Order tools by information dependency: representation before analysis, generation before selection, targeted detectors before aggregate confirmation.
4. Pass artifacts forward explicitly; do not expect another domain or tool to reconstruct hidden state.
5. At each decision point, continue every applicable domain and tool that can assist, and record any missing input or capability that prevents execution.
6. Audition the integrated lyric against meaning, voice, beat and performance.
7. Route every detected defect backward to all owning domains, then re-run affected downstream stages.
