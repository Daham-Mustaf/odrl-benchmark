"""
grounding/hierarchy.py — Paper Definition 2: H_ℓ = (C, ≤, ⊥⊥, γ).

Single source of truth for the data model.  All loaders produce a
Hierarchy; all encoders consume one.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from collections import defaultdict
from itertools import combinations


@dataclass
class Hierarchy:
    """
    H_ℓ = (C, ≤, ⊥⊥, γ)  — paper Definition 2.

    concepts  : C — TPTP constant names
    edges     : direct ≤ pairs (child, parent); reflexivity + transitivity
                are supplied by Layer 1, not stored here
    disjoint  : ⊥⊥ pairs, each stored once as (a, b) with a < b
    grounding : γ — tptp_name → annotation (IRI / source code / label)
    name      : human label for TPTP Domain header field
    source    : provenance URI
    domain    : 'taxonomic' | 'mereological' | 'nominal'
    profile   : loader variant tag (e.g. 'curated', 'iso3166')
    """
    name:      str
    source:    str
    domain:    str   # 'taxonomic' | 'mereological' | 'nominal'
    profile:   str = ""

    concepts:  set[str]            = field(default_factory=set)
    edges:     list[tuple[str,str]] = field(default_factory=list)
    disjoint:  list[tuple[str,str]] = field(default_factory=list)
    grounding: dict[str,str]        = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Derived structure
    # ------------------------------------------------------------------

    def children_of(self) -> dict[str, set[str]]:
        m: dict[str, set[str]] = defaultdict(set)
        for child, parent in self.edges:
            m[parent].add(child)
        return dict(m)

    def parents_of(self) -> dict[str, set[str]]:
        m: dict[str, set[str]] = defaultdict(set)
        for child, parent in self.edges:
            m[child].add(parent)
        return dict(m)

    def downward_closure(self) -> dict[str, set[str]]:
        """↓x = {y ∈ C | y ≤ x}, x included.  Fixed-point; C is finite."""
        desc = {c: {c} for c in self.concepts}
        changed = True
        while changed:
            changed = False
            for child, parent in self.edges:
                before = len(desc[parent])
                desc[parent] |= desc[child]
                if len(desc[parent]) > before:
                    changed = True
        return desc

    def stats(self) -> dict:
        """Structural metadata used in TPTP headers and paper tables."""
        children = self.children_of()
        parents  = self.parents_of()

        roots  = sorted(c for c in self.concepts if c not in parents)
        leaves = sorted(c for c in self.concepts if c not in children)
        multi  = sorted(c for c in self.concepts if len(parents.get(c,set())) > 1)

        memo: dict[str,int] = {}
        def depth(n: str) -> int:
            if n not in memo:
                memo[n] = 0 if n not in parents else \
                          1 + max(depth(p) for p in parents[n])
            return memo[n]
        for c in self.concepts:
            depth(c)
        max_d = max(memo.values()) if memo else 0

        br = [len(children[c]) for c in self.concepts if c in children]
        return dict(
            roots        = roots,
            leaves       = leaves,
            multi_parent = multi,
            n_internal   = len(self.concepts) - len(leaves) - len(roots),
            max_depth    = max_d,
            avg_branching= sum(br)/len(br) if br else 0.0,
            max_branching= max(br) if br else 0,
        )

    # ------------------------------------------------------------------
    # Disjointness helpers
    # ------------------------------------------------------------------

    def add_sibling_disjointness(self, dag_safe: bool = True) -> list[tuple]:
        """
        Compute and merge sibling ⊥⊥ pairs into self.disjoint.

        dag_safe=True  (default): assert a ⊥⊥ b only when ↓a ∩ ↓b = ∅.
                        Prevents contradictions from multi-parent concepts.
        dag_safe=False (naive):   assert all siblings; unsound for DAGs
                        but kept for the DPV-NAIVE.ax baseline.

        Returns list of skipped (a, b, shared_descendants) triples.
        """
        children = self.children_of()
        existing = set(self.disjoint)
        skipped  = []
        closure  = self.downward_closure() if dag_safe else {}

        for siblings in children.values():
            for a, b in combinations(sorted(siblings), 2):
                pair = (a, b) if a < b else (b, a)
                if pair in existing:
                    continue
                if dag_safe:
                    overlap = closure[a] & closure[b]
                    if overlap:
                        skipped.append((a, b, sorted(overlap)))
                        continue
                existing.add(pair)
                self.disjoint.append(pair)

        self.disjoint.sort()
        return skipped

    def validate(self) -> list[str]:
        """Return list of warnings (empty = clean)."""
        w = []
        for child, parent in self.edges:
            if child not in self.concepts:
                w.append(f"Edge child not in concepts: {child}")
            if parent not in self.concepts:
                w.append(f"Edge parent not in concepts: {parent}")
            if child == parent:
                w.append(f"Self-loop: {child}")
        for a, b in self.disjoint:
            if a not in self.concepts:
                w.append(f"Disjoint concept not declared: {a}")
            if b not in self.concepts:
                w.append(f"Disjoint concept not declared: {b}")
            if a >= b:
                w.append(f"Disjoint pair not sorted: ({a},{b})")
        return w
