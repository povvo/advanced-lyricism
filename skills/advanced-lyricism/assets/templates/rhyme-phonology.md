# Rhyme and Phonology — Working Template

> Method: `references/rhyme-phonology.md`
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
- stressed vowel:
- rime:
- onset:
- coda:
- syllable count:
- stress contour:
- phrase shape:
- word boundary:
- internal position:
- landing position:
- mosaic rhyme:
- root anchor:
- assonance:
- consonance:
- accent variation:
- articulatory ease:

## Domain workspace

- anchor word / phrase:
- meaning in song:
- pronunciation as performed:
- stressed syllable:
- stressed vowel / acoustic pivot:
- coda:
- stress contour:
- intended beat position:

## Candidate families
### Close / exact
-

### Tail-varied slants
-

### Vowel-preserving
-

### Articulatory / consonant-family
-

### Consonance
-

### Mosaic / phrase
-

### Same stress contour
-

## Semantic filters
- scene:
- action:
- consequence:
- motif:
- domain-specific:
- legitimate second reading:

## Performance filter
- syllable count:
- consonant congestion:
- vowel length:
- breath:
- local pronunciation:

## Reject / demote
- predictable suffix-only:
- forced syntax:
- wrong accent:
- weak meaning:
- annotation-dependent:

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
- `phoneme_map`
- `rhyme_suggester`
- `rhyme_grid`
- `articulation_audit`
Coupled tool ids — use every one that can assist:
- `prosody_map`

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

Rhyme is heard, not spelled. Stress, accent, phrase shape, timing and delivery determine whether a relation lands.

## Rhyme unit
Track:
- stressed vowel;
- following consonants/coda;
- preceding onset where useful;
- syllable count;
- stress contour;
- word boundaries.

Useful relations:
- exact tail;
- slant;
- multisyllabic;
- mosaic;
- internal/root-anchor;
- assonant/consonant family.

These are a continuum, not a prestige ladder.

## Practitioner synthesis: vowel/stress matching
A long phrase can rhyme convincingly when it matches:
- number of syllables;
- strong/weak positions;
- vowel sequence;
- timing.

This preserves a strong UK-rap technique: match the stressed vowel and phrase shape before chasing spelling.

## Pivot families
1. start from an important anchor word;
2. extract the stressed acoustic pivot;
3. generate close matches;
4. generate tail-varied slants;
5. generate mosaics/phrase matches;
6. meter-filter;
7. remove semantically empty options.

Suffix repetition is not forbidden. It becomes weak when both the sound and semantic landing are predictable.

## Scheme architecture
Use schemes as movement:
- couplet closure;
- alternation;
- enclosure;
- sustained-family pressure;
- chain handoff;
- return after contrast;
- pivot at a semantic/flow turn.

Choose after the section's movement is known.

## Internal rhyme grid
Advanced internal architecture can track recurring positions:
- opening/entry;
- mid-bar;
- ending/landing.

Corresponding positions across bars can answer each other, creating a grid rather than end-rhyme couplets. Do not fill every slot every bar; contrast makes density legible.

## Rhyme placement
Prefer rhyme on words carrying image, action, relation, decision or consequence. A looser rhyme on a meaningful word can beat a perfect rhyme on connective tissue.

## Delayed resolution
Useful possibilities:
- imply the obvious rhyme, land elsewhere;
- delay across a bar boundary;
- answer an end rhyme internally next line;
- return an old family after a break.

Delay should change interpretation or rhythmic expectation, not exist only as trickery.

## Accent and pronunciation
Dictionaries are candidate generators, not authorities. Delivery can change stress, reduction, linking, consonants, syllabification and vowel length. Local pronunciation may create viable relations absent from a standard dictionary.

## Failure modes
Revise when:
- spelling says rhyme but the ear does not;
- rhyme forces unnatural syntax;
- internal saturation hides the image;
- key words require unintended stress;
- a family continues after its semantic purpose ends;
- the line is clever only when annotated.

Combine `scripts/craft_audit.py` pronunciation coverage and mechanical indicators with supplied pronunciation, close reading and audition when assessing freshness and speaker credibility.

Phonological similarity, rhyme placement, accent, syntax and meter must be tested together.

## Syllable structure and rhyme control

Treat a syllable as more than a count.

A practical decomposition:
- **onset** - consonants before the vowel;
- **nucleus** - vowel/diphthong;
- **coda** - consonants after the nucleus;
- **rime/rhyme** - nucleus + coda.

This supports finer slant-rhyme reasoning.

### Similarity controls
You can hold:
- nucleus constant, vary coda;
- coda family constant, move vowel nearby;
- stress contour constant across different word boundaries;
- syllable count constant while changing lexical category;
- consonant manner/place approximately constant for articulatory echo.

The closer the relation, the more obvious the sonic connection. Wider slants can create freshness when timing and stress make the relation audible.

`rhyme_suggester.py` uses phoneme-tail and stress similarity as a candidate surface, not a verdict.

---
