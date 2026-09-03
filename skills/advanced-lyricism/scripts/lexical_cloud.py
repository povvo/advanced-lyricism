#!/usr/bin/env python3
"""Map vocabulary concentration, motifs and lexical changes."""
from __future__ import annotations
import argparse,collections,json
from pathlib import Path
from lyric_utils import words,norm_word,CONTENT_STOP,read_text_arg,normalized_entropy
def stemmer():
    try:
        from nltk.stem import PorterStemmer
        p=PorterStemmer();return p.stem
    except Exception:return lambda x:x
def profile(text,top=80,stem=False):
    st=stemmer();t=[norm_word(w) for w in words(text)];t=[st(w) if stem else w for w in t if len(w)>1 and w not in CONTENT_STOP and not w.isdigit()]
    c=collections.Counter(t);b=collections.Counter(zip(t,t[1:]))
    return {"tokens":len(t),"types":len(c),"type_token_ratio":round(len(c)/len(t),4) if t else 0,"normalized_frequency_entropy":round(normalized_entropy(c),4),
            "top_terms":[{"term":w,"count":n,"share":round(n/max(1,len(t)),4)} for w,n in c.most_common(top)],
            "top_bigrams":[{"terms":[a,b],"count":n} for (a,b),n in b.most_common(min(top,30))]},c
def compare(a,b,top=60):
    ta=sum(a.values()) or 1;tb=sum(b.values()) or 1;rows=[]
    for w in set(a)|set(b):
        pa=a[w]/ta;pb=b[w]/tb;rows.append({"term":w,"share_a":round(pa,5),"share_b":round(pb,5),"delta":round(pa-pb,5)})
    return sorted(rows,key=lambda x:(-abs(x["delta"]),x["term"]))[:top]
def png(c,path,w=1600,h=900):
    from wordcloud import WordCloud
    wc=WordCloud(width=w,height=h,background_color="black",color_func=lambda *a,**k:"white",prefer_horizontal=.86,collocations=False,margin=4,relative_scaling=.5)
    wc.generate_from_frequencies(dict(c));wc.to_file(str(path))
def main():
    ap=argparse.ArgumentParser(description="Emit lexical frequency/collocation JSON and optionally a monochrome word-cloud PNG.");ap.add_argument("-i","--input",type=Path);ap.add_argument("-t","--text");ap.add_argument("--compare",type=Path);ap.add_argument("--stem",action="store_true");ap.add_argument("--top",type=int,default=80);ap.add_argument("--png",type=Path);ap.add_argument("-o","--output",type=Path);a=ap.parse_args()
    d,c=profile(read_text_arg(a.input,a.text),a.top,a.stem);doc={"schema":"advanced-lyricism.lexical-cloud.v1","profile":d}
    if a.compare:
        q,cc=profile(a.compare.read_text(errors="ignore"),a.top,a.stem);doc["comparison_profile"]=q;doc["delta_terms"]=compare(c,cc,a.top)
    if a.png:
        try:png(c,a.png);doc["png"]=str(a.png)
        except Exception as e:doc["png_error"]=str(e)
    doc["limits"]=["frequency highlights repetition/field concentration; it does not identify thematic importance by itself"]
    s=json.dumps(doc,ensure_ascii=False,indent=2)
    if a.output:a.output.write_text(s,encoding="utf-8")
    else:print(s)
    return 0
if __name__=="__main__":raise SystemExit(main())
