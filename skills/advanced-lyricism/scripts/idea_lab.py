#!/usr/bin/env python3
"""Generate controlled concept mutations, collisions and permutations."""
from __future__ import annotations
import argparse,json,random,itertools
from pathlib import Path
from lyric_utils import read_text_arg

GRAM={
"pressure-scene":[["concrete setting","pressure enters","speaker choice","immediate consequence","residue/callback"],
                  ["mundane routine","small disturbance","blind spot","irreversible action","aftermath detail"]],
"collision":[["domain A exact property","domain B exact property","shared relation","emergent third meaning","second-order implication"],
             ["ordinary object","technical operation","human pressure","literal bridge","surface-first payoff"]],
"argument":[["claim","concrete support","resistant detail","qualification","changed claim"],
            ["assumption","inversion","constraint that makes inversion true","cost","image that proves it"]],
"hook-return":[["hook invariant","verse changes one condition","hook returns with altered referent","new consequence"],
               ["phrase","omission/gap","verse fills context","same phrase becomes reclassified"]],
"performance":[["base pocket","contrast pocket","transition hinge","impact silence","return"],
               ["low density","acceleration","peak","deceleration","landing"]],
"scene-envelope":[["state before","attack/trigger","development","maintained pressure","release","residue"],
                  ["observable event","state change","counteraction","new constraint","remaining trace"]]
}

MUT=[
("scale-shift","move one invariant across body -> room -> street -> institution/system"),
("time-scale","translate pressure across second -> night -> year -> generation"),
("perspective-shift","restate from chronicler, witness, confessor, counterparty or institutional viewpoint"),
("syntax-delay","delay a grammatical complement across the bar line; audition enjambment before suspension"),
("payoff-displacement","move the expected rhyme/payoff away from the line ending, then return later"),
("image-distance","replace summary with one physical event, or pull back from object to system"),
("contradiction-hold","make both sides of a tension concrete"),
("register-switch","change pronoun/word-order/discourse system with audience or emotional context"),
("caesura","remove words and let breath/rest/ad-lib carry part of the transition"),
("metaphor-lock","choose a domain operation first and constrain rhyme to genuine properties"),
("consequence","add a trace that remains after the event"),
("callback-transform","repeat a prior token/image but change function, referent or moral weight"),
("sonic-reframe","preserve stressed vowel/stress contour while changing spelling, boundary or tail"),
("delivery-reframe","hold words constant; change emphasis, pocket, breath, pitch contour or sustain"),
("parameter-isolation","hold meaning/rhyme fixed and vary cadence; then hold cadence fixed and vary wording"),
("grouping-reframe","keep event durations/words but shift grouping cue through pause, register, contour or restart"),
("same-different","preserve one invariant and change exactly one property on return")
]

def grammar(cs,n,seed):
    r=random.Random(seed);keys=list(GRAM);out=[]
    for i in range(n):
        k=r.choice(keys);form=r.choice(GRAM[k]);rot=cs[i%len(cs):]+cs[:i%len(cs)] if cs else []
        out.append({"id":i+1,"family":k,"sequence":form,
                    "seed_bindings":{slot:(rot[j%len(rot)] if rot and j<len(rot) else None) for j,slot in enumerate(form)}})
    return out

def mutate(text,n,seed):
    r=random.Random(seed);pool=MUT[:];r.shuffle(pool);ls=[x for x in text.splitlines() if x.strip()]
    # cycle only after every mutation has been seen
    rows=[]
    for i in range(n):
        name,op=pool[i%len(pool)]
        rows.append({"id":i+1,"technique":name,"target_line":i%len(ls)+1 if ls else None,"operation":op})
        if i and i%len(pool)==len(pool)-1:r.shuffle(pool)
    return rows

def collide(cs,n,seed):
    r=random.Random(seed);pairs=list({tuple(sorted(p)) for p in itertools.combinations(cs,2)});r.shuffle(pairs)
    return [{"id":i+1,"domains":list(p),
             "questions":[f"What exact operation/property does {p[0]} have?",f"What exact operation/property does {p[1]} have?",
                          "Where is structural overlap?","What third meaning emerges?","What second-order consequence follows?"]}
            for i,p in enumerate(pairs[:n])]

def permute(cs,n,seed):
    r=random.Random(seed)
    if len(cs)<2:return []
    out=[];seen=set()
    # exact permutations for small lists, seeded samples otherwise
    if len(cs)<=7:
        pool=list(itertools.permutations(cs));r.shuffle(pool)
        for p in pool[:n]:
            out.append({"id":len(out)+1,"sequence":list(p),"operation":"test whether reveal/causality/emphasis improves under this order"})
    else:
        for _ in range(n*10):
            p=cs[:];r.shuffle(p);k=tuple(p)
            if k not in seen:
                seen.add(k);out.append({"id":len(out)+1,"sequence":p,"operation":"test whether reveal/causality/emphasis improves under this order"})
                if len(out)>=n:break
    return out

def walk(cs,n,seed):
    """Random walk through structural mutation states; only one dimension changes per step."""
    r=random.Random(seed)
    dims=["scale","viewpoint","syntax","image_distance","register","delivery","density","rhyme_position","consequence","grouping"]
    state={d:0 for d in dims};rows=[]
    for i in range(n):
        d=r.choice(dims);step=r.choice([-1,1]);state[d]=max(-2,min(2,state[d]+step))
        rows.append({"step":i+1,"changed_dimension":d,"direction":step,"state":dict(state),
                     "concept":cs[i%len(cs)] if cs else None})
    return rows

def main():
    ap=argparse.ArgumentParser(description="Generate reproducible structural ideation scaffolds and controlled transformations without drafting finished lyrics.")
    ap.add_argument("--mode",choices=["grammar","mutate","collide","permute","walk"],default="grammar")
    ap.add_argument("--concepts",default="",help="Comma-separated concepts/events/domains.")
    g=ap.add_mutually_exclusive_group();g.add_argument("-i","--input",type=Path);g.add_argument("-t","--text")
    ap.add_argument("-n","--count",type=int,default=8);ap.add_argument("--seed",type=int,default=0);ap.add_argument("-o","--output",type=Path);a=ap.parse_args()
    if not 1<=a.count<=100:
        print(json.dumps({"ok":False,"error":{"type":"input","message":"count must be 1..100"}}));return 2
    cs=[x.strip() for x in a.concepts.split(",") if x.strip()]
    txt=read_text_arg(a.input,a.text) if a.input or a.text is not None else ""
    if a.mode in {"collide","permute"} and len(cs)<2:
        print(json.dumps({"ok":False,"error":{"type":"input","message":f"{a.mode} mode requires at least two comma-separated concepts"}}));return 2
    items={"grammar":lambda:grammar(cs,a.count,a.seed),"mutate":lambda:mutate(txt,a.count,a.seed),
           "collide":lambda:collide(cs,a.count,a.seed),"permute":lambda:permute(cs,a.count,a.seed),
           "walk":lambda:walk(cs,a.count,a.seed)}[a.mode]()
    d={"schema":"advanced-lyricism.idea-lab.v2","mode":a.mode,"seed":a.seed,"concepts":cs,"items":items,
       "method":"generate/transform first; evaluate meaning, sound, voice, sequence and performance afterward",
       "limits":["structural creativity aid, not automatic authorship","random operations are seeded and bounded"]}
    s=json.dumps(d,ensure_ascii=False,indent=2)
    if a.output:a.output.write_text(s,encoding="utf-8")
    else:print(s)
    return 0
if __name__=="__main__":raise SystemExit(main())
