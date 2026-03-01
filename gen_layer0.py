#!/usr/bin/env python3
"""
gen_layer0.py — Generate TPTP Layer 0 axiom files.

Replaces gen_layer0_geo.py, gen_layer0_kb.py, gen_layer0_lang.py.

Usage examples
--------------
# Curated geo KB (primary test KB)
uv run python gen_layer0.py geo curated \
    -o Problems/ODRL/Axioms/Layer0-DomainKB/GEO000-0.ax \
    --sibling-disjointness --una distinct

# ISO 3166 alignment target + bridge axioms
uv run python gen_layer0.py geo iso3166 \
    -o Problems/ODRL/Axioms/Layer0-DomainKB/ISO3166-0.ax \
    --una distinct \
    --emit-alignment Problems/ODRL/Axioms/Alignment/ALIGN-GEO-ISO.ax

# BCP47 language KB
uv run python gen_layer0.py lang \
    -o Problems/ODRL/Axioms/Layer0-DomainKB/LANG000-0.ax \
    --sibling-disjointness --base-disjointness --una distinct

# DPV Purpose KB from OWL file
uv run python gen_layer0.py owl \
    -i data/dpv/dpv-owl.ttl \
    -o Problems/ODRL/Axioms/Layer0-DomainKB/DPV000-0.ax \
    --namespace "https://w3id.org/dpv#" \
    --root-class Purpose \
    --domain taxonomic \
    --sibling-disjointness --una skip

# DPV naive baseline (for benchmark comparison)
uv run python gen_layer0.py owl \
    -i data/dpv/dpv-owl.ttl \
    -o Problems/ODRL/Axioms/Layer0-DomainKB/DPV-NAIVE.ax \
    --namespace "https://w3id.org/dpv#" \
    --root-class Purpose \
    --domain taxonomic \
    --sibling-disjointness --naive --una skip
"""
import argparse
import sys
from pathlib import Path

from grounding.geo  import load_curated, load_iso3166, load_m49, CURATED_TO_ISO3166
from grounding.lang import load_lang
from grounding.owl  import load_owl
from encoding.tptp  import generate_tptp


# ── Alignment file generation ─────────────────────────────────────────────────

def _emit_alignment(mapping: dict, filename: str, output_path: str):
    from datetime import date
    n = len(mapping)
    L = []
    A = L.append
    A("%--------------------------------------------------------------------------")
    A(f"% File     : {filename} : TPTP v0.1.0.")
    A(f"% Domain   : KB Alignment — Curated GEO to ISO 3166-1")
    A(f"% Axioms   : Order-preserving alignment (paper Definition 8)")
    A(f"% Version  : Partial alignment (countries + root only)")
    A(f"% English  : Maps curated GEO (GEO000-0.ax) to ISO 3166 (ISO3166-0.ax).")
    A(f"%            Tests Proposition 2: verdict preservation under alignment.")
    A(f"% Refs     : [MuS25] Mustafa, D. & Sutcliffe, G. (2025), §4.3")
    A(f"% Status   : Layer 0+ — Alignment Bridge")
    A(f"% Syntax   : Number of formulae    : {n:>5} ({n:>5} unt;   0 def)")
    A(f"% Ontology : Predicate: align/2 — alignment function α: C_A → C_B")
    A(f"% Date     : {date.today().isoformat()}")
    A(f"% Authors  : Mustafa, D. & Sutcliffe, G.")
    A("%--------------------------------------------------------------------------")
    A("")
    A("% ─── Alignment Axioms (Definition 8: α: C_A → C_B) ────────────────────")
    for i, (src, tgt) in enumerate(sorted(mapping.items())):
        A(f"fof(align_{i:04d}, axiom, align({src}, {tgt})).")
    A("")
    A("%--------------------------------------------------------------------------")
    A(f"% Summary: {n} alignment axioms (partial mapping)")
    A("%--------------------------------------------------------------------------")
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"Alignment: {output_path} ({n} pairs)", file=sys.stderr)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(
        description="Generate TPTP Layer 0 domain KB axiom files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = ap.add_subparsers(dest="source", required=True)

    # ── geo ──────────────────────────────────────────────────────────────────
    p_geo = sub.add_parser("geo", help="Geographic KB (curated/iso3166/m49-*)")
    p_geo.add_argument("profile",
        choices=["curated","iso3166","m49-europe","m49-full"])
    p_geo.add_argument("--emit-alignment",
        help="Also write alignment axioms to this path (curated→ISO only)")

    # ── lang ─────────────────────────────────────────────────────────────────
    p_lang = sub.add_parser("lang", help="BCP47 language KB")
    p_lang.add_argument("--base-disjointness", action="store_true",
        help="Also assert pairwise ⊥⊥ between all base language roots")

    # ── owl ──────────────────────────────────────────────────────────────────
    p_owl = sub.add_parser("owl", help="Extract KB from OWL/TTL ontology")
    p_owl.add_argument("-i","--input", required=True)
    p_owl.add_argument("--namespace",  "-n", required=True)
    p_owl.add_argument("--root-class", "-r", required=True)
    p_owl.add_argument("--domain", "-d", default="taxonomic",
        choices=["taxonomic","mereological","nominal"])
    p_owl.add_argument("--name",   default="OWL Ontology")
    p_owl.add_argument("--owl-source", default="")
    p_owl.add_argument("--format", default=None)
    p_owl.add_argument("--naive", action="store_true",
        help="Naive (tree-assumed) sibling ⊥⊥ instead of DAG-safe")

    # ── shared ───────────────────────────────────────────────────────────────
    for p in (p_geo, p_lang, p_owl):
        p.add_argument("-o", "--output", required=True, help="Output .ax file path")
        p.add_argument("--sibling-disjointness", action="store_true")
        p.add_argument("--una", default="pairwise",
            choices=["pairwise","distinct","skip"],
            help="UNA encoding (default: pairwise)")

    args = ap.parse_args()

    # ── Load hierarchy ────────────────────────────────────────────────────────
    skipped = []
    dag_safe = True

    if args.source == "geo":
        if args.profile == "curated":      h = load_curated()
        elif args.profile == "iso3166":    h = load_iso3166()
        elif args.profile == "m49-europe": h = load_m49("europe")
        else:                              h = load_m49("full")

    elif args.source == "lang":
        h = load_lang()

    elif args.source == "owl":
        h = load_owl(
            path       = args.input,
            namespace  = args.namespace,
            root_class = args.root_class,
            name       = args.name,
            source     = args.owl_source,
            domain     = args.domain,
            fmt        = args.format,
        )
        dag_safe = not args.naive

    # ── Disjointness ─────────────────────────────────────────────────────────
    if args.sibling_disjointness:
        skipped = h.add_sibling_disjointness(dag_safe=dag_safe)
        print(f"  ⊥⊥: {len(h.disjoint)} pairs"
              + (f" ({len(skipped)} skipped — DAG-safe)" if skipped else ""),
              file=sys.stderr)

    if args.source == "lang" and getattr(args, "base_disjointness", False):
        from itertools import combinations as _comb
        parents_set = {child for child, _ in h.edges}
        roots = sorted(c for c in h.concepts if c not in parents_set)
        existing = set(h.disjoint)
        added = 0
        for a, b in _comb(roots, 2):
            pair = (min(a,b), max(a,b))
            if pair not in existing:
                h.disjoint.append(pair)
                existing.add(pair)
                added += 1
        h.disjoint.sort()
        print(f"  base ⊥⊥: +{added} pairs (roots)", file=sys.stderr)

    # ── Validate ──────────────────────────────────────────────────────────────
    warnings = h.validate()
    for w in warnings:
        print(f"WARNING: {w}", file=sys.stderr)

    # ── Generate ──────────────────────────────────────────────────────────────
    filename = Path(args.output).name
    text = generate_tptp(
        h, filename,
        una_mode             = args.una,
        sibling_disjointness = args.sibling_disjointness,
        dag_safe             = dag_safe,
        skipped_pairs        = skipped,
    )
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(text + "\n", encoding="utf-8")

    # ── Summary ───────────────────────────────────────────────────────────────
    from encoding.una import una_count
    cs = list(h.concepts)
    n_una = una_count(sorted(cs), sorted(h.edges), args.una)
    total = len(cs) + len(h.edges) + len(h.disjoint) + n_una
    print(f"Written: {args.output}", file=sys.stderr)
    print(f"  {len(cs)} concepts, {len(h.edges)} leq, "
          f"{len(h.disjoint)} ⊥⊥, {n_una} UNA = {total} axioms", file=sys.stderr)

    # ── Alignment (geo only) ──────────────────────────────────────────────────
    if args.source == "geo" and getattr(args, "emit_alignment", None):
        if args.profile != "curated":
            print("WARNING: --emit-alignment only implemented for curated profile",
                  file=sys.stderr)
        else:
            align_filename = Path(args.emit_alignment).name
            _emit_alignment(CURATED_TO_ISO3166, align_filename, args.emit_alignment)


if __name__ == "__main__":
    main()