"""
encoding/tptp.py — Hierarchy → TPTP Layer 0 axiom text.

One function.  Used by all three loaders.  Previously duplicated in
gen_layer0_geo.py, gen_layer0_kb.py, and gen_layer0_lang.py.
"""
from __future__ import annotations
from datetime import date
from itertools import combinations
from .una import build_una_lines, una_count


def generate_tptp(
    h,              # Hierarchy instance
    filename: str,
    *,
    una_mode: str = "pairwise",   # 'pairwise' | 'distinct' | 'skip'
    sibling_disjointness: bool = False,
    dag_safe: bool = True,
    skipped_pairs: list | None = None,
) -> str:
    """
    Render a Hierarchy to a TPTP Layer 0 axiom file string.

    Parameters
    ----------
    h                   : Hierarchy (paper Def. 2)
    filename            : basename used in the File header field
    una_mode            : how to encode the Unique Name Assumption —
                          'pairwise' : C(n,2) explicit ≠ axioms
                          'distinct' : $distinct groups (Sutcliffe)
                          'skip'     : omit (implicit from tree + ⊥⊥)
    sibling_disjointness: whether ⊥⊥ was derived from sibling structure
    dag_safe            : whether DAG-safe filtering was applied
    skipped_pairs       : (a, b, overlap) triples suppressed by DAG filter
    """
    cs = sorted(h.concepts)
    hs = sorted(h.edges)
    ds = h.disjoint
    st = h.stats()

    skipped_pairs = skipped_pairs or []

    una_lines, n_una, n_una_equ = build_una_lines(cs, hs, una_mode)
    n_formulae = len(cs) + len(hs) + len(ds) + n_una
    n_pred = 2 + (1 if ds else 0)
    pred_str = "concept/1; leq/2" + ("; disjoint/2" if ds else "")

    domain_rel = {
        "taxonomic":   "class subsumption (paper Def. 2, ≤ = ⊑)",
        "mereological":"part-whole containment (paper Def. 2, ≤ = ⪯)",
        "nominal":     "identity (paper Def. 2, ≤ = =)",
    }.get(h.domain, h.domain)

    una_comment = {
        "pairwise": f"C({len(cs)},2) = {n_una} pairwise ≠ axioms.",
        "distinct": f"$distinct groups (Sutcliffe); avoids clause explosion.",
        "skip":     "IMPLICIT — tree + ⊥⊥ (Implicit UNA Lemma).",
    }[una_mode]

    L = []
    A = L.append

    A("%--------------------------------------------------------------------------")
    A(f"% File     : {filename} : TPTP v0.1.0. Released v0.1.0.")
    A(f"% Domain   : {h.name}")
    A(f"% Axioms   : Full hierarchy ({h.domain})")
    A(f"% Version  : Profile: {h.profile}" if h.profile else "% Version  : Generated.")
    A(f"% English  : {h.name} encoded as TPTP Layer 0 domain KB.")
    A(f"%            UNA: {una_comment}")
    A(f"% Refs     : [MuS25] Mustafa, D. & Sutcliffe, G. (2025),")
    A(f"%            Automated Reasoning for ODRL Policy Conflict Detection")
    A(f"% Source   : {h.source}")
    A(f"% Names    : {filename}")
    A(f"% Status   : Layer 0 — Domain Knowledge Base")
    A(f"% Syntax   : Number of formulae    : {n_formulae:>5} ({n_formulae:>5} unt;   0 def)")
    A(f"%            Number of atoms       : {n_formulae:>5} ({n_una_equ:>5} equ)")
    A(f"%            Maximal formula atoms  :     1 (   1 avg)")
    A(f"%            Number of connectives  :     0 (   0   ~;   0   |;   0   &)")
    A(f"%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)")
    A(f"%            Maximal formula depth  :     1 (   1 avg)")
    A(f"%            Maximal term depth     :     1 (   1 avg)")
    A(f"%            Number of predicates   : {n_pred:>5} ({n_pred:>5} usr;   0 prp; 1-2 aty)")
    A(f"%            Number of functors     : {len(cs):>5} ({len(cs):>5} usr; {len(cs):>3} con; 0-0 aty)")
    A(f"%            Number of variables    :     0 (   0   !;   0   ?)")
    A(f"% SPC      : FOF_EPR_RFN_NEQ")
    A(f"% Comments : All formulae are ground unit clauses.")
    A(f"%          : Layer 1 provides reflexivity + transitivity of leq/2.")
    if sibling_disjointness and dag_safe and skipped_pairs:
        A(f"%          : DAG-SAFE: {len(skipped_pairs)} sibling pairs suppressed"
          f" (multi-parent overlap).")
    elif sibling_disjointness and not dag_safe:
        A(f"%          : NAIVE sibling ⊥⊥ — tree assumed; may be unsound for DAGs.")
    A(f"%          : Multi-parent: {', '.join(st['multi_parent']) or 'none'}")
    A(f"%          : Root(s): {', '.join(st['roots'])}")
    A(f"% Ontology : Predicates: {pred_str}")
    A(f"%          : Relation: leq/2 — {domain_rel}")
    A(f"% Stats    : Concepts {len(cs)}"
      f" | Edges {len(hs)}"
      f" | Disjoint {len(ds)}"
      f" | UNA {n_una}"
      f" | Total {n_formulae}")
    A(f"%          : Depth {st['max_depth']}"
      f" | Leaves {len(st['leaves'])}"
      f" | Internal {st['n_internal']}"
      f" | Branch avg {st['avg_branching']:.1f}"
      f" max {st['max_branching']}")
    A(f"% Date     : {date.today().isoformat()}")
    A(f"% Authors  : Mustafa, D. & Sutcliffe, G.")
    A(f"% Gen      : gen_layer0.py --source {h.profile or h.domain}")
    A("%--------------------------------------------------------------------------")

    # ── Section 1: Concept membership ─────────────────────────────────
    A("")
    A("% ─── Concept membership (Definition 2: C) ─────────────────────────────")
    for c in cs:
        A(f"fof(c_{c}, axiom, concept({c})).  % {h.grounding.get(c,'')}")

    # ── Section 2: Hierarchy ──────────────────────────────────────────
    A("")
    A("% ─── Hierarchy (Definition 2: ≤) ──────────────────────────────────────")
    A("% Direct edges only. Layer 1 provides reflexivity + transitivity.")
    for i, (child, parent) in enumerate(hs):
        A(f"fof(h_{i:04d}, axiom, leq({child}, {parent})).")

    # ── Section 3: Disjointness ───────────────────────────────────────
    A("")
    A("% ─── Disjointness (Definition 2: ⊥⊥) ─────────────────────────────────")
    if sibling_disjointness:
        mode_str = "DAG-safe" if dag_safe else "NAIVE (tree-assumed)"
        A(f"% {mode_str} sibling ⊥⊥. Derived ⊥⊥ via disj_downward (Layer 1).")
    if ds:
        for i, (c1, c2) in enumerate(ds):
            A(f"fof(d_{i:04d}, axiom, disjoint({c1}, {c2})).")
    else:
        A("% (none)")

    # ── Section 4: UNA ────────────────────────────────────────────────
    A("")
    A("% ─── Unique Name Assumption ───────────────────────────────────────────")
    A(f"% {una_comment}")
    for line in una_lines:
        A(line)

    # ── Footer ────────────────────────────────────────────────────────
    A("")
    A("%--------------------------------------------------------------------------")
    total = len(cs) + len(hs) + len(ds) + n_una
    A(f"% Summary: {len(cs)} concept"
      f" + {len(hs)} leq"
      f" + {len(ds)} disjoint"
      f" + {n_una} UNA"
      f" = {total} axioms")
    if skipped_pairs:
        A(f"% DAG-safe suppressed {len(skipped_pairs)} pairs:")
        for a, b, ov in skipped_pairs:
            A(f"%   {a} ⊥⊥ {b} (overlap: {', '.join(ov)})")
    A("%--------------------------------------------------------------------------")

    return "\n".join(L)
