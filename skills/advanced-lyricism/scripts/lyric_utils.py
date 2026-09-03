#!/usr/bin/env python3
"""Shared deterministic utilities for Advanced Lyricism CLI tools.

Pronunciation resolution order:
1. explicit user override (when configured);
2. installed cmudict package;
3. bundled compressed CMUdict fallback;
4. heuristic syllable count only.

Unknown pronunciation remains unknown; the heuristic fallback supplies syllable count only.
"""
from __future__ import annotations

import gzip
import json
import math
import os
import re
from functools import lru_cache
from pathlib import Path

WORD_RE = re.compile(r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*")
VOWEL_RE = re.compile(r"^([A-Z]+)([012])$")
FUNCTION_WORDS = {
    "a","an","the","and","or","but","nor","for","so","yet","to","of","in","on","at","by",
    "from","with","without","into","onto","over","under","through","across","after","before",
    "if","when","while","because","although","though","unless","than","that","which","who",
    "whose","whom","as","is","am","are","was","were","be","been","being","do","does","did",
    "have","has","had","can","could","will","would","shall","should","may","might","must",
    "i","you","he","she","it","we","they","me","him","her","us","them","my","your","his",
    "its","our","their","this","these","those","there","here"
}
CONTENT_STOP = FUNCTION_WORDS | {"yeah","uh","um","like","just","really","very","got","get","gonna","wanna","ain't"}
ARPABET_VOWELS = {"AA","AE","AH","AO","AW","AY","EH","ER","EY","IH","IY","OW","OY","UH","UW"}
VOWEL_FEATURES = {
    "IY":("high","front","unrounded"), "IH":("high","front","unrounded"),
    "EH":("mid","front","unrounded"), "AE":("low","front","unrounded"),
    "AA":("low","back","unrounded"), "AH":("mid","central","unrounded"),
    "AO":("mid","back","rounded"), "UH":("high","back","rounded"), "UW":("high","back","rounded"),
    "ER":("mid","central","rhotic"), "EY":("diphthong","front","unrounded"),
    "AY":("diphthong","front-back","unrounded"), "OW":("diphthong","back","rounded"),
    "AW":("diphthong","front-back","unrounded"), "OY":("diphthong","back-front","rounded"),
}
CONS_FEATURES = {
    "P":("stop","bilabial","voiceless"), "B":("stop","bilabial","voiced"),
    "T":("stop","alveolar","voiceless"), "D":("stop","alveolar","voiced"),
    "K":("stop","velar","voiceless"), "G":("stop","velar","voiced"),
    "CH":("affricate","postalveolar","voiceless"), "JH":("affricate","postalveolar","voiced"),
    "F":("fricative","labiodental","voiceless"), "V":("fricative","labiodental","voiced"),
    "TH":("fricative","dental","voiceless"), "DH":("fricative","dental","voiced"),
    "S":("fricative","alveolar","voiceless"), "Z":("fricative","alveolar","voiced"),
    "SH":("fricative","postalveolar","voiceless"), "ZH":("fricative","postalveolar","voiced"),
    "HH":("fricative","glottal","voiceless"),
    "M":("nasal","bilabial","voiced"), "N":("nasal","alveolar","voiced"), "NG":("nasal","velar","voiced"),
    "L":("approximant","alveolar","voiced"), "R":("approximant","postalveolar","voiced"),
    "W":("approximant","labial-velar","voiced"), "Y":("approximant","palatal","voiced")
}
SIBILANTS={"S","Z","SH","ZH","CH","JH"}

ROOT = Path(__file__).resolve().parents[1]
BUNDLED_CMU = ROOT / "assets" / "phonology" / "cmudict.dict.gz"
_DISABLE = {x.strip().lower() for x in os.environ.get("ADVANCED_LYRICISM_DISABLE_PROVIDERS","").split(",") if x.strip()}
_OVERRIDES: dict[str, list[list[str]]] = {}

def words(text:str): return WORD_RE.findall(text)
def norm_word(w:str)->str: return w.lower().replace("’","'")

def configure_pronunciation_overrides(path: Path | str | None) -> int:
    """Load optional ARPABET overrides: {"word": ["F","OW1"], "word2": [["..."],["..."]]}."""
    global _OVERRIDES
    if not path:
        _OVERRIDES = {}
        return 0
    p = Path(path)
    raw = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("pronunciation override JSON must be an object")
    out={}
    for k,v in raw.items():
        if isinstance(v, list) and v and all(isinstance(x,str) for x in v):
            vals=[v]
        elif isinstance(v, list) and all(isinstance(x,list) and all(isinstance(y,str) for y in x) for x in v):
            vals=v
        else:
            raise ValueError(f"invalid pronunciation override for {k}")
        out[norm_word(str(k))]=[[str(x).upper() for x in row] for row in vals]
    _OVERRIDES=out
    return len(out)

def _parse_bundled() -> dict[str,list[list[str]]]:
    d={}
    if not BUNDLED_CMU.exists() or "bundled_cmudict" in _DISABLE:
        return d
    with gzip.open(BUNDLED_CMU,"rt",encoding="utf-8",errors="replace") as f:
        for raw in f:
            line=raw.strip()
            if not line or line.startswith(";;;"):
                continue
            parts=line.split()
            if len(parts)<2:
                continue
            word=parts[0]
            word=re.sub(r"\(\d+\)$","",word)
            d.setdefault(norm_word(word),[]).append(parts[1:])
    return d

@lru_cache(maxsize=1)
def _installed_cmu():
    if "cmudict" in _DISABLE:
        return {}
    try:
        import cmudict
        return cmudict.dict()
    except Exception:
        return {}

@lru_cache(maxsize=1)
def _bundled_cmu():
    return _parse_bundled()

def cmu():
    """Return the best available full pronunciation dictionary."""
    d=_installed_cmu()
    if d:
        return d
    return _bundled_cmu()

def pronunciation_backend():
    if _OVERRIDES:
        override_count=len(_OVERRIDES)
    else:
        override_count=0
    installed=_installed_cmu()
    bundled=_bundled_cmu() if not installed else {}
    if installed:
        provider="cmudict-package"
        entries=len(installed)
    elif bundled:
        provider="bundled-cmudict"
        entries=len(bundled)
    else:
        provider=None
        entries=0
    return {
        "available": bool(provider),
        "provider": provider,
        "entries": entries,
        "override_entries": override_count,
        "accent_note": "CMUdict is primarily General American English; supplied/local pronunciation outranks it."
    }

def pronunciations(word:str):
    w=norm_word(word)
    if w in _OVERRIDES:
        return _OVERRIDES[w]
    d=cmu()
    out=d.get(w,[])
    if out:
        return out
    for c in (re.sub(r"'s$","",w), re.sub(r"n't$","",w)):
        if c and c!=w and c in _OVERRIDES:
            return _OVERRIDES[c]
        if c and c!=w and c in d:
            return d[c]
    return []

def split_phoneme(ph:str):
    m=VOWEL_RE.match(ph)
    return (m.group(1),int(m.group(2))) if m else (ph,None)

def stress_pattern(pron):
    return "".join(str(st) for ph in pron for _,st in [split_phoneme(ph)] if st is not None)

def syllable_count_pron(pron):
    return sum(1 for ph in pron if split_phoneme(ph)[1] is not None)

def heuristic_syllables(word:str)->int:
    w=re.sub(r"[^a-z]","",norm_word(word))
    if not w:return 0
    c=len(re.findall(r"[aeiouy]+",w))
    if w.endswith("e") and not w.endswith(("le","ye")) and c>1:c-=1
    if w.endswith("ed") and c>1 and not re.search(r"[td]ed$",w):c-=1
    return max(1,c)

def rhyme_tail(pron):
    vs=[]; stressed=[]
    for i,ph in enumerate(pron):
        _,st=split_phoneme(ph)
        if st is not None:
            vs.append(i)
            if st in (1,2):stressed.append(i)
    if not vs:return []
    return list(pron[stressed[-1] if stressed else vs[-1]:])

def syllable_units(pron):
    units=[]; onset=[]; cur=None
    for ph in pron:
        b,st=split_phoneme(ph)
        if b in ARPABET_VOWELS:
            if cur is not None:units.append(cur)
            cur={"onset":onset,"nucleus":b,"stress":st,"coda":[]}; onset=[]
        elif cur is None:onset.append(b)
        else:cur["coda"].append(b)
    if cur is not None:units.append(cur)
    return units

def analyze_word(word:str):
    ps=pronunciations(word)
    if ps:
        p=ps[0]
        source="override" if norm_word(word) in _OVERRIDES else (pronunciation_backend()["provider"] or "dictionary")
        return {"word":word,"normalized":norm_word(word),"source":source,"phonemes":p,
                "stress":stress_pattern(p),"syllables":syllable_count_pron(p),
                "rhyme_tail":rhyme_tail(p),"syllable_units":syllable_units(p)}
    return {"word":word,"normalized":norm_word(word),"source":"heuristic","phonemes":[],
            "stress":"","syllables":heuristic_syllables(word),"rhyme_tail":[],"syllable_units":[]}

def line_syllables(line:str)->int:
    return sum(analyze_word(w)["syllables"] for w in words(line))

def line_stress(line:str):
    seq=[]
    for w in words(line):
        a=analyze_word(w)
        seq.extend([int(x) for x in a["stress"]] if a["stress"] else [None]*a["syllables"])
    return seq

def stress_coverage(seq):
    return sum(x is not None for x in seq)/len(seq) if seq else 0.0

def support_state(coverage: float, full_threshold: float=.85):
    if coverage <= 0:
        return "unavailable"
    if coverage >= full_threshold:
        return "full"
    return "partial"

def evidence_state(coverage: float, full_threshold: float=.85):
    """Backward-compatible v7 name for support_state()."""
    return support_state(coverage, full_threshold)

def terminal_word(line:str):
    ws=words(line); return ws[-1] if ws else ""

def rhyme_signature(word:str):
    a=analyze_word(word)
    return {"tail":[split_phoneme(x)[0] for x in a["rhyme_tail"]],"stress":a["stress"],
            "syllables":a["syllables"],"source":a["source"]}

def normalized_entropy(counts):
    vals=[v for v in counts.values() if v>0]
    if len(vals)<=1:return 0.0
    t=sum(vals); h=-sum((v/t)*math.log(v/t,2) for v in vals)
    return h/math.log(len(vals),2)

def read_text_arg(path=None,text=None):
    if text is not None:return text
    if path:return Path(path).read_text(encoding="utf-8",errors="ignore")
    import sys; return sys.stdin.read()

def phoneme_similarity(a,b):
    aa,_=split_phoneme(a); bb,_=split_phoneme(b)
    if aa==bb:return 1.0
    if aa in ARPABET_VOWELS and bb in ARPABET_VOWELS:
        fa=VOWEL_FEATURES.get(aa);fb=VOWEL_FEATURES.get(bb)
    else:
        fa=CONS_FEATURES.get(aa);fb=CONS_FEATURES.get(bb)
    return sum(x==y for x,y in zip(fa,fb))/3 if fa and fb else 0.0

def sequence_similarity(a,b):
    """Similarity for known phoneme sequences. Empty/empty is UNKNOWN, not perfect."""
    a=[split_phoneme(x)[0] for x in a]; b=[split_phoneme(x)[0] for x in b]
    if not a or not b:
        return 0.0
    gap=-.35; dp=[[0.0]*(len(b)+1) for _ in range(len(a)+1)]
    for i in range(1,len(a)+1):dp[i][0]=i*gap
    for j in range(1,len(b)+1):dp[0][j]=j*gap
    for i in range(1,len(a)+1):
        for j in range(1,len(b)+1):
            s=phoneme_similarity(a[i-1],b[j-1])*1.2-.2
            dp[i][j]=max(dp[i-1][j-1]+s,dp[i-1][j]+gap,dp[i][j-1]+gap)
    return max(0,min(1,dp[-1][-1]/max(len(a),len(b))))
