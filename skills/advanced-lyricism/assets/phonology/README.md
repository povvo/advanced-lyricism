# Bundled pronunciation fallback

This package includes a gzip-compressed copy of the CMU Pronouncing Dictionary as a local fallback.
Its purpose is runtime robustness when the `cmudict` Python package is absent.
CMUdict mainly covers General American English. Supplied pronunciation and accent-specific material take priority.
See `CMUDICT-LICENSE.txt` for redistribution terms.
