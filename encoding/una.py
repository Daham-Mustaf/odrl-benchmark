"""
encoding/una.py — Unique Name Assumption variants.

Three modes, all previously scattered across three files.
"""
from __future__ import annotations
from collections import defaultdict
from itertools import combinations


def build_una_lines(
    concepts: list[str],
    edges: list[tuple[str,str]],
    mode: str,               # 'pairwise' | 'distinct' | 'skip'
) -> tuple[list[str], int, int]:
    """
    Build UNA axiom lines for the given mode.

    Returns (lines, n_una_axioms, n_equality_atoms).
    n_equality_atoms is used in the TPTP Syntax header.
    """
    if mode == "skip":
        return (
            ["% SKIPPED — implicit from tree structure + ⊥⊥ (Implicit UNA Lemma)."],
            0, 0,
        )

    if mode == "pairwise":
        lines = []
        for i, (c1, c2) in enumerate(combinations(concepts, 2)):
            lines.append(f"fof(una_{i:04d}, axiom, {c1} != {c2}).")
        n = len(lines)
        return lines, n, n

    if mode == "distinct":
        groups = _distinct_groups(concepts, edges)
        lines  = []
        for gname, members in groups:
            if len(", ".join(members)) <= 70:
                lines.append(f"fof({gname}, axiom, $distinct({', '.join(members)})).")
            else:
                lines.append(f"fof({gname}, axiom,")
                lines.append(f"    $distinct(")
                chunks = [members[i:i+8] for i in range(0, len(members), 8)]
                for j, chunk in enumerate(chunks):
                    suffix = "," if j < len(chunks) - 1 else ""
                    lines.append(f"        {', '.join(chunk)}{suffix}")
                lines.append("    )).")
            lines.append("")
        return lines, len(groups), 0   # $distinct ≠ equality atoms

    raise ValueError(f"Unknown UNA mode: {mode!r}")


def una_count(concepts: list[str], edges: list[tuple], mode: str) -> int:
    """Quick count without generating lines — used for header stats."""
    if mode == "skip":     return 0
    if mode == "pairwise": return len(concepts) * (len(concepts) - 1) // 2
    if mode == "distinct": return len(_distinct_groups(concepts, edges))
    raise ValueError(mode)


def _distinct_groups(
    concepts: list[str],
    edges: list[tuple[str,str]],
) -> list[tuple[str, list[str]]]:
    """
    Group concepts by parent for $distinct.

    - One group for all roots (no parent).
    - One group per parent for its direct children.
    """
    children: dict[str, list[str]] = defaultdict(list)
    has_parent: set[str] = set()
    for child, parent in edges:
        children[parent].append(child)
        has_parent.add(child)

    groups = []
    roots = sorted(c for c in concepts if c not in has_parent)
    if len(roots) > 1:
        groups.append(("una_distinct_roots", roots))

    for parent in sorted(children):
        siblings = sorted(children[parent])
        if len(siblings) > 1:
            groups.append((f"una_distinct_{parent}", siblings))

    return groups
