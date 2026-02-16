#!/usr/bin/env python3
"""
gen_layer0_lang.py — Generate TPTP Layer 0 axiom file for BCP47 language tags.

Curated hierarchy of BCP47 language tags relevant to European dataspaces.
Structure: base language → regional variant (language-region)

Usage:
    uv run python gen_layer0_lang.py \
        --output Problems/ODRL/Axioms/Layer0-DomainKB/LANG000-0.ax \
        --sibling-disjointness \
        --base-disjointness \
        --no-una

Source: RFC 5646 / BCP47, ISO 639-1, ISO 3166-1
"""
import argparse
import sys
from collections import defaultdict
from datetime import date
from itertools import combinations
from pathlib import Path

LANG_HIERARCHY = [
    ("en","English",None),("en-US","English (United States)","en"),
    ("en-GB","English (United Kingdom)","en"),("en-AU","English (Australia)","en"),
    ("en-IE","English (Ireland)","en"),("en-CA","English (Canada)","en"),
    ("de","German",None),("de-DE","German (Germany)","de"),
    ("de-AT","German (Austria)","de"),("de-CH","German (Switzerland)","de"),
    ("de-LU","German (Luxembourg)","de"),
    ("nl","Dutch",None),("nl-NL","Dutch (Netherlands)","nl"),("nl-BE","Dutch (Belgium)","nl"),
    ("sv","Swedish",None),("sv-SE","Swedish (Sweden)","sv"),("sv-FI","Swedish (Finland)","sv"),
    ("da","Danish",None),("da-DK","Danish (Denmark)","da"),
    ("nb","Norwegian Bokmål",None),("nb-NO","Norwegian Bokmål (Norway)","nb"),
    ("fr","French",None),("fr-FR","French (France)","fr"),("fr-BE","French (Belgium)","fr"),
    ("fr-CH","French (Switzerland)","fr"),("fr-LU","French (Luxembourg)","fr"),
    ("fr-CA","French (Canada)","fr"),
    ("es","Spanish",None),("es-ES","Spanish (Spain)","es"),("es-MX","Spanish (Mexico)","es"),
    ("es-AR","Spanish (Argentina)","es"),
    ("it","Italian",None),("it-IT","Italian (Italy)","it"),("it-CH","Italian (Switzerland)","it"),
    ("pt","Portuguese",None),("pt-PT","Portuguese (Portugal)","pt"),("pt-BR","Portuguese (Brazil)","pt"),
    ("ro","Romanian",None),("ro-RO","Romanian (Romania)","ro"),
    ("pl","Polish",None),("pl-PL","Polish (Poland)","pl"),
    ("cs","Czech",None),("cs-CZ","Czech (Czechia)","cs"),
    ("sk","Slovak",None),("sk-SK","Slovak (Slovakia)","sk"),
    ("bg","Bulgarian",None),("bg-BG","Bulgarian (Bulgaria)","bg"),
    ("hr","Croatian",None),("hr-HR","Croatian (Croatia)","hr"),
    ("sl","Slovenian",None),("sl-SI","Slovenian (Slovenia)","sl"),
    ("el","Greek",None),("el-GR","Greek (Greece)","el"),("el-CY","Greek (Cyprus)","el"),
    ("fi","Finnish",None),("fi-FI","Finnish (Finland)","fi"),
    ("et","Estonian",None),("et-EE","Estonian (Estonia)","et"),
    ("lv","Latvian",None),("lv-LV","Latvian (Latvia)","lv"),
    ("lt","Lithuanian",None),("lt-LT","Lithuanian (Lithuania)","lt"),
    ("hu","Hungarian",None),("hu-HU","Hungarian (Hungary)","hu"),
    ("mt","Maltese",None),("mt-MT","Maltese (Malta)","mt"),
    ("ga","Irish",None),("ga-IE","Irish (Ireland)","ga"),
]

def tag_to_tptp(tag):
    parts = tag.split("-")
    if len(parts) == 1: return parts[0].lower()
    result = parts[0].lower()
    for p in parts[1:]: result += p[0].upper() + p[1:].lower()
    return result

def compute_sibling_disjointness(concepts, edges):
    children_map = defaultdict(set)
    for c,p in edges: children_map[p].add(c)
    seen = set(); pairs = []
    for parent, children in children_map.items():
        for c1,c2 in combinations(sorted(children),2):
            if (c1,c2) not in seen: seen.add((c1,c2)); pairs.append((c1,c2))
    return sorted(pairs)

def compute_base_disjointness(concepts, edges):
    all_children = {c for c,_ in edges}
    top = sorted(concepts - all_children)
    return sorted(list(combinations(top,2)))

def generate_tptp(concepts, edges, disjointness, tag_map,
                  filename, sibling_disj=False, skip_una=False):
    cs = sorted(concepts); hs = sorted(edges)
    n_una = 0 if skip_una else len(cs)*(len(cs)-1)//2
    n_formulae = len(cs)+len(hs)+len(disjointness)+n_una

    children_map = defaultdict(set); parents_map = defaultdict(set)
    for c,p in hs: children_map[p].add(c); parents_map[c].add(p)
    leaves = sorted([c for c in cs if not children_map[c]])
    roots = sorted([c for c in cs if not parents_map[c]])
    br = [len(children_map[c]) for c in cs if children_map[c]]
    avg_b = sum(br)/len(br) if br else 0; max_b = max(br) if br else 0
    max_d = 0
    for c in cs:
        d=0; cur=c
        while parents_map.get(cur): d+=1; cur=next(iter(parents_map[cur]))
        max_d=max(max_d,d)

    n_pred = 2 if not disjointness else 3
    pred_str = "concept/1; leq/2" + ("; disjoint/2" if disjointness else "")

    L = []
    L.append("%--------------------------------------------------------------------------")
    L.append(f"% File     : {filename} : TPTP v0.1.0. Released v0.1.0.")
    L.append(f"% Domain   : BCP47 Language Tags — European Dataspace Languages")
    L.append(f"% Axioms   : Language tag hierarchy (taxonomic)")
    L.append(f"% Version  : Curated from RFC 5646 / ISO 639-1 / ISO 3166-1.")
    L.append(f"% English  : BCP47 language tag hierarchy for ODRL policy reasoning.")
    L.append(f"%            leq/2 represents language specialization (is-variant-of).")
    if skip_una:
        L.append(f"%            UNA is implicit from tree + sibling/base disjointness.")
    L.append(f"% Refs     : [MuS25] Mustafa, D. & Sutcliffe, G. (2025),")
    L.append(f"%            Automated Reasoning for ODRL Policy Conflict Detection")
    L.append(f"% Source   : https://www.rfc-editor.org/rfc/rfc5646 (BCP47)")
    L.append(f"% Names    : {filename}")
    L.append(f"% Status   : Layer 0 — Domain Knowledge Base")
    L.append(f"% Syntax   : Number of formulae    : {n_formulae:>5} ({n_formulae:>5} unt;   0 def)")
    L.append(f"%            Number of atoms       : {n_formulae:>5} ({n_una:>5} equ)")
    L.append(f"%            Maximal formula atoms  :     1 (   1 avg)")
    L.append(f"%            Number of connectives  :     0 (   0   ~;   0   |;   0   &)")
    L.append(f"%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)")
    L.append(f"%            Maximal formula depth  :     1 (   1 avg)")
    L.append(f"%            Maximal term depth     :     1 (   1 avg)")
    L.append(f"%            Number of predicates   : {n_pred:>5} ({n_pred:>5} usr;   0 prp; 1-2 aty)")
    L.append(f"%            Number of functors     : {len(cs):>5} ({len(cs):>5} usr; {len(cs):>3} con; 0-0 aty)")
    L.append(f"%            Number of variables    :     0 (   0   !;   0   ?)")
    L.append(f"% SPC      : FOF_EPR_RFN_NEQ")
    L.append(f"% Comments : All formulae are ground unit clauses.")
    L.append(f"%          : Layer 1 provides reflexivity + transitivity of leq/2.")
    if skip_una:
        L.append(f"%          : UNA: IMPLICIT — tree + disjointness (Implicit UNA Lemma).")
    L.append(f"%          : Root(s): {len(roots)} base languages (no single root)")
    L.append(f"% Ontology : Predicates: {pred_str}")
    L.append(f"%          : Relation: leq/2 — language specialization (paper Def. 2)")
    L.append(f"% Stats    : Concepts {len(cs)} | Edges {len(hs)} | Disjoint {len(disjointness)} | UNA {n_una} | Total {n_formulae}")
    L.append(f"%          : Depth {max_d} | Leaves {len(leaves)} | Base langs {len(roots)} | Branch avg {avg_b:.1f} max {max_b}")
    L.append(f"% Date     : {date.today().isoformat()}")
    L.append(f"% Authors  : Mustafa, D. & Sutcliffe, G.")
    L.append(f"% Gen      : gen_layer0_lang.py (curated BCP47 subset)")
    L.append("%--------------------------------------------------------------------------")

    L.append("")
    L.append("% ─── Concept membership (Definition 2: C) ─────────────────────────────")
    for c in cs: L.append(f"fof(c_{c}, axiom, concept({c})).  % {tag_map.get(c,'')}")

    L.append("")
    L.append("% ─── Hierarchy (Definition 2: ≤ = language specialization) ─────────────")
    L.append("% leq(enUs, en) means: en-US is a regional variant of en.")
    for i,(ch,pa) in enumerate(hs): L.append(f"fof(h_{i:04d}, axiom, leq({ch}, {pa})).")

    L.append("")
    L.append("% ─── Disjointness (Definition 2: ⊥⊥) ─────────────────────────────────")
    if sibling_disj:
        L.append("% Sibling + base language disjointness.")
        L.append("% Derived disjointness follows from disj_downward (Layer 1).")
    if disjointness:
        for i,(c1,c2) in enumerate(disjointness): L.append(f"fof(d_{i:04d}, axiom, disjoint({c1}, {c2})).")
    else:
        L.append("% (none)")

    L.append("")
    una_count = 0
    if skip_una:
        L.append("% ─── Unique Name Assumption ───────────────────────────────────────────")
        L.append("% SKIPPED (--no-una): UNA is implicit from tree structure + sibling")
        L.append("% and base language disjointness. All constants provably distinct via:")
        L.append("%   - leq antisymmetry + disj_downward + disj_irrefl")
    else:
        L.append("% ─── Unique Name Assumption ───────────────────────────────────────────")
        L.append(f"% C({len(cs)},2) = {n_una} pairwise distinctness axioms.")
        for c1,c2 in combinations(cs,2):
            L.append(f"fof(una_{una_count:04d}, axiom, {c1} != {c2})."); una_count+=1

    L.append("")
    L.append("%--------------------------------------------------------------------------")
    total = len(cs)+len(hs)+len(disjointness)+una_count
    L.append(f"% Summary: {len(cs)} concept + {len(hs)} leq + {len(disjointness)} disjoint + {una_count} UNA = {total} axioms")
    L.append("%--------------------------------------------------------------------------")
    return "\n".join(L)

def main():
    ap = argparse.ArgumentParser(description="Generate TPTP Layer 0 for BCP47 languages.")
    ap.add_argument("-o","--output", required=True)
    ap.add_argument("--sibling-disjointness", action="store_true")
    ap.add_argument("--base-disjointness", action="store_true")
    ap.add_argument("--no-una", action="store_true",
        help="Skip UNA axioms (implicit from tree + disjointness)")
    args = ap.parse_args()

    concepts = set(); edges = []; tag_map = {}; t2t = {}
    for tag,label,parent in LANG_HIERARCHY:
        t = tag_to_tptp(tag); t2t[tag]=t; concepts.add(t)
        tag_map[t] = f"BCP47:{tag} — {label}"
    for tag,label,parent in LANG_HIERARCHY:
        if parent and parent in t2t: edges.append((t2t[tag], t2t[parent]))

    print(f"{len(concepts)} concepts, {len(edges)} edges", file=sys.stderr)

    disjointness = []
    if args.sibling_disjointness:
        sp = compute_sibling_disjointness(concepts, edges)
        disjointness.extend(sp)
        print(f"  {len(sp)} sibling disjointness pairs", file=sys.stderr)
    if args.base_disjointness:
        bp = compute_base_disjointness(concepts, edges)
        existing = set(disjointness)
        for p in bp:
            if p not in existing: disjointness.append(p); existing.add(p)
        print(f"  {len(bp)} base language disjointness pairs", file=sys.stderr)
    disjointness.sort()

    filename = Path(args.output).name
    tptp = generate_tptp(concepts, edges, disjointness, tag_map, filename,
                         sibling_disj=(args.sibling_disjointness or args.base_disjointness),
                         skip_una=args.no_una)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f: f.write(tptp + "\n")

    una_count = 0 if args.no_una else len(concepts)*(len(concepts)-1)//2
    total = len(concepts)+len(edges)+len(disjointness)+una_count
    saved = len(concepts)*(len(concepts)-1)//2 if args.no_una else 0
    print(f"\nWritten: {args.output}", file=sys.stderr)
    print(f"  {len(concepts)} concepts, {len(edges)} leq, "
          f"{len(disjointness)} disjoint, {una_count} UNA = {total} axioms", file=sys.stderr)
    if saved: print(f"  (--no-una saved {saved} axioms)", file=sys.stderr)

if __name__ == "__main__":
    main()
