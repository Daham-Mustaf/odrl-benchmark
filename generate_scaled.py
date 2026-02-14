#!/usr/bin/env python3
"""
ODRL Benchmark Scalability Generator (v2 — Fixed)
==================================================

Key fix: Added sibling non-subsumption axioms. Without these,
open-world semantics allows provers to find models where siblings
have unexpected subsumption, producing CounterSatisfiable on
problems that should be Theorem.

This is the SAME phenomenon as the xone finding in the core suite.

Usage:
    python generate_scaled.py              # Default sizes
    python generate_scaled.py --all        # Larger sizes
"""

import os
import sys
from pathlib import Path

TPTP_OUT = "Problems/ODRL/KBGrounding/Scaled"
SMT_OUT = "SMT/ODRL/KBGrounding/Scaled"


def tptp_header(pid, desc, status, category, n_concepts):
    spc = "THM" if status == "Theorem" else "CSA"
    return f"""%--------------------------------------------------------------------------
% File     : {pid} : TPTP v9.0.0. Released v9.1.0.
% Domain   : Policy (ODRL)
% Problem  : {desc}
% Version  : [Mus26] axioms : Scaled.
% English  : Scaled benchmark with {n_concepts} concepts.
% Refs     : [Mus26] Mustafa, D. (2026), Grounding ODRL Constraints.
% Source   : [Mus26]
% Names    : {pid} [Mus26]
%
% Status   : {status}
% Rating   : ? v9.1.0
% SPC      : FOF_{spc}_EPR
%
% Comments : Scaled benchmark. Category: {category}
%--------------------------------------------------------------------------
"""


def flat_kb_tptp(n, prefix="c", root="root"):
    """Flat taxonomy: n concepts under root, with full negative axioms."""
    lines = []
    names = [f"{prefix}{i}" for i in range(n)]
    all_names = names + [root]

    for name in all_names:
        lines.append(f"fof({name}_concept, axiom, concept({name})).")
    for name in names:
        lines.append(f"fof({name}_sub, axiom, subclass({name}, {root})).")

    lines.append("fof(refl, axiom, ![X]: (concept(X) => subclass(X, X))).")
    lines.append("fof(trans, axiom, ![X,Y,Z]: ((subclass(X,Y) & subclass(Y,Z)) => subclass(X,Z))).")

    # UNA + sibling non-subsumption
    for i, a in enumerate(all_names):
        for b in all_names[i+1:]:
            lines.append(f"fof(una_{a}_{b}, axiom, {a} != {b}).")
    for i, a in enumerate(names):
        for b in names[i+1:]:
            lines.append(f"fof(nosub_{a}_{b}, axiom, ~subclass({a}, {b})).")
            lines.append(f"fof(nosub_{b}_{a}, axiom, ~subclass({b}, {a})).")
    for name in names:
        lines.append(f"fof(nosub_{root}_{name}, axiom, ~subclass({root}, {name})).")

    closure = " | ".join([f"X = {n}" for n in all_names])
    lines.append(f"fof(closure, axiom, ![X]: (concept(X) => ({closure}))).")

    return lines, names


def chain_kb_tptp(depth, prefix="c"):
    """Chain: c0 < c1 < ... < c_{depth-1}."""
    lines = []
    names = [f"{prefix}{i}" for i in range(depth)]

    for name in names:
        lines.append(f"fof({name}_concept, axiom, concept({name})).")
    for i in range(depth - 1):
        lines.append(f"fof(chain_{i}, axiom, subclass({names[i]}, {names[i+1]})).")

    lines.append("fof(refl, axiom, ![X]: (concept(X) => subclass(X, X))).")
    lines.append("fof(trans, axiom, ![X,Y,Z]: ((subclass(X,Y) & subclass(Y,Z)) => subclass(X,Z))).")

    for i, a in enumerate(names):
        for b in names[i+1:]:
            lines.append(f"fof(una_{a}_{b}, axiom, {a} != {b}).")
    # No backward subsumption
    for i in range(depth):
        for j in range(i):
            lines.append(f"fof(nosub_{names[i]}_{names[j]}, axiom, ~subclass({names[i]}, {names[j]})).")

    closure = " | ".join([f"X = {n}" for n in names])
    lines.append(f"fof(closure, axiom, ![X]: (concept(X) => ({closure}))).")

    return lines, names


def gen_wide(n, pid_base):
    problems = []
    kb_lines, names = flat_kb_tptp(n)
    kb = "\n".join(kb_lines)
    half = n // 2

    pid_a = f"ODRL{pid_base:03d}-1"
    exclude = " | ".join([f"subclass(X, {names[i]})" for i in range(half)])
    target = names[half]
    conj_a = f"""
fof(den1, axiom, ![X]: (inDen1(X) <=> (concept(X) & ~({exclude})))).
fof(den2, axiom, ![X]: (inDen2(X) <=> (X = {target}))).
fof(conjecture, conjecture, ?[X]: (inDen1(X) & inDen2(X))).
"""
    problems.append({"pid": pid_a, "desc": f"Wide-{n}: isNoneOf(half) vs eq → Compat",
                      "status": "Theorem", "category": "Scaled", "n": n,
                      "content": tptp_header(pid_a, f"Wide-{n} compatible", "Theorem", "Scaled/Wide", n) + "\n" + kb + conj_a})

    pid_b = f"ODRL{pid_base+1:03d}-1"
    exclude_all = " | ".join([f"subclass(X, {nm})" for nm in names])
    conj_b = f"""
fof(den1, axiom, ![X]: (inDen1(X) <=> (concept(X) & ~({exclude_all}) & X != root))).
fof(den2, axiom, ![X]: (inDen2(X) <=> (concept(X) & subclass(X, root)))).
fof(conjecture, conjecture, ~?[X]: (inDen1(X) & inDen2(X))).
"""
    problems.append({"pid": pid_b, "desc": f"Wide-{n}: isNoneOf(all) vs isA → Conflict",
                      "status": "Theorem", "category": "Scaled", "n": n,
                      "content": tptp_header(pid_b, f"Wide-{n} conflict", "Theorem", "Scaled/Wide", n) + "\n" + kb + conj_b})
    return problems


def gen_deep(depth, pid_base):
    problems = []
    kb_lines, names = chain_kb_tptp(depth)
    kb = "\n".join(kb_lines)
    top, mid, bot = names[-1], names[depth//2], names[0]

    pid_a = f"ODRL{pid_base:03d}-1"
    conj_a = f"""
fof(den1, axiom, ![X]: (inDen1(X) <=> (concept(X) & subclass(X, {top})))).
fof(den2, axiom, ![X]: (inDen2(X) <=> (concept(X) & subclass(X, {mid})))).
fof(conjecture, conjecture, ?[X]: (inDen1(X) & inDen2(X))).
"""
    problems.append({"pid": pid_a, "desc": f"Chain-{depth}: isA(top) vs isA(mid) → Compat",
                      "status": "Theorem", "category": "Scaled", "n": depth,
                      "content": tptp_header(pid_a, f"Chain-{depth} compatible", "Theorem", "Scaled/Deep", depth) + "\n" + kb + conj_a})

    pid_b = f"ODRL{pid_base+1:03d}-1"
    conj_b = f"""
fof(den1, axiom, ![X]: (inDen1(X) <=> (concept(X) & subclass(X, {mid})))).
fof(den2, axiom, ![X]: (inDen2(X) <=> (concept(X) & ~subclass(X, {mid})))).
fof(conjecture, conjecture, ~?[X]: (inDen1(X) & inDen2(X))).
"""
    problems.append({"pid": pid_b, "desc": f"Chain-{depth}: isA(mid) vs NOT isA(mid) → Conflict",
                      "status": "Theorem", "category": "Scaled", "n": depth,
                      "content": tptp_header(pid_b, f"Chain-{depth} conflict", "Theorem", "Scaled/Deep", depth) + "\n" + kb + conj_b})
    return problems


def gen_valueset(n, pid_base):
    problems = []
    kb_lines, names = flat_kb_tptp(n)
    kb = "\n".join(kb_lines)
    half = n // 2

    pid_a = f"ODRL{pid_base:03d}-1"
    set_a = " | ".join([f"X = {names[i]}" for i in range(half)])
    set_b = " | ".join([f"X = {names[i]}" for i in range(half, n)])
    conj_a = f"""
fof(den1, axiom, ![X]: (inDen1(X) <=> (concept(X) & ({set_a})))).
fof(den2, axiom, ![X]: (inDen2(X) <=> (concept(X) & ({set_b})))).
fof(conjecture, conjecture, ~?[X]: (inDen1(X) & inDen2(X))).
"""
    problems.append({"pid": pid_a, "desc": f"ValueSet-{n}: disjoint isAnyOf → Conflict",
                      "status": "Theorem", "category": "Scaled", "n": n,
                      "content": tptp_header(pid_a, f"ValueSet-{n} conflict", "Theorem", "Scaled/ValueSet", n) + "\n" + kb + conj_a})

    pid_b = f"ODRL{pid_base+1:03d}-1"
    conj_b = f"""
fof(den1, axiom, ![X]: (inDen1(X) <=> (concept(X) & ({set_a} | {set_b})))).
fof(den2, axiom, ![X]: (inDen2(X) <=> (concept(X) & ~({set_a})))).
fof(conjecture, conjecture, ?[X]: (inDen1(X) & inDen2(X))).
"""
    problems.append({"pid": pid_b, "desc": f"ValueSet-{n}: isAnyOf(all) vs isNoneOf(half) → Compat",
                      "status": "Theorem", "category": "Scaled", "n": n,
                      "content": tptp_header(pid_b, f"ValueSet-{n} compatible", "Theorem", "Scaled/ValueSet", n) + "\n" + kb + conj_b})
    return problems


def gen_composition(n_dims, pid_base):
    problems = []
    kb_lines = []
    for d in range(n_dims):
        for c in ["a", "b", "root"]:
            kb_lines.append(f"fof(d{d}_{c}, axiom, concept_d{d}(d{d}_{c})).")
        kb_lines.append(f"fof(d{d}_a_sub, axiom, sub_d{d}(d{d}_a, d{d}_root)).")
        kb_lines.append(f"fof(d{d}_b_sub, axiom, sub_d{d}(d{d}_b, d{d}_root)).")
        kb_lines.append(f"fof(d{d}_refl, axiom, ![X]: (concept_d{d}(X) => sub_d{d}(X, X))).")
        kb_lines.append(f"fof(d{d}_una_ab, axiom, d{d}_a != d{d}_b).")
        kb_lines.append(f"fof(d{d}_una_ar, axiom, d{d}_a != d{d}_root).")
        kb_lines.append(f"fof(d{d}_una_br, axiom, d{d}_b != d{d}_root).")
        kb_lines.append(f"fof(d{d}_nosub_ab, axiom, ~sub_d{d}(d{d}_a, d{d}_b)).")
        kb_lines.append(f"fof(d{d}_nosub_ba, axiom, ~sub_d{d}(d{d}_b, d{d}_a)).")
    kb = "\n".join(kb_lines)

    pid_a = f"ODRL{pid_base:03d}-1"
    clauses = " & ".join([f"?[X{d}]: (sub_d{d}(X{d}, d{d}_root) & sub_d{d}(X{d}, d{d}_root))" for d in range(n_dims)])
    conj_a = f"\nfof(conjecture, conjecture, ({clauses})).\n"
    problems.append({"pid": pid_a, "desc": f"AND({n_dims}): all compatible",
                      "status": "Theorem", "category": "Scaled", "n": n_dims,
                      "content": tptp_header(pid_a, f"AND-{n_dims} compatible", "Theorem", "Scaled/Comp", n_dims*3) + "\n" + kb + conj_a})

    pid_b = f"ODRL{pid_base+1:03d}-1"
    compat = " & ".join([f"?[X{d}]: (sub_d{d}(X{d}, d{d}_root))" for d in range(n_dims-1)])
    last = n_dims - 1
    conflict = f"?[X{last}]: (X{last} = d{last}_a & X{last} = d{last}_b)"
    conj_b = f"\nfof(conjecture, conjecture, ~({compat} & {conflict})).\n"
    problems.append({"pid": pid_b, "desc": f"AND({n_dims}): last conflicts",
                      "status": "Theorem", "category": "Scaled", "n": n_dims,
                      "content": tptp_header(pid_b, f"AND-{n_dims} conflict", "Theorem", "Scaled/Comp", n_dims*3) + "\n" + kb + conj_b})
    return problems


def main():
    kb_sizes = [20, 50, 100]
    depths = [10, 20, 50]
    vset_sizes = [10, 30, 50]
    comp_dims = [5, 10, 20]

    if "--all" in sys.argv:
        kb_sizes = [20, 50, 100, 200, 500]
        depths = [10, 20, 50, 100]
        vset_sizes = [10, 30, 50, 100]
        comp_dims = [5, 10, 20, 50]

    pid = 300
    all_probs = []

    print("Generating scaled benchmarks (v2 — with non-subsumption axioms)...")

    for n in kb_sizes:
        all_probs.extend(gen_wide(n, pid)); pid += 2
    for d in depths:
        all_probs.extend(gen_deep(d, pid)); pid += 2
    for n in vset_sizes:
        all_probs.extend(gen_valueset(n, pid)); pid += 2
    for n in comp_dims:
        all_probs.extend(gen_composition(n, pid)); pid += 2

    os.makedirs(TPTP_OUT, exist_ok=True)
    for p in all_probs:
        with open(os.path.join(TPTP_OUT, f"{p['pid']}.p"), 'w') as f:
            f.write(p["content"])

    print(f"\nGenerated {len(all_probs)} problems in {TPTP_OUT}/")
    print(f"\nAxiom counts (indicator of difficulty):")
    for p in all_probs:
        n_ax = p["content"].count("fof(")
        print(f"  {p['pid']:<14} {p['n']:>4} concepts  {n_ax:>6} axioms  {p['status']:<20} {p['desc'][:45]}")

    print(f"\nv2 fix: sibling non-subsumption axioms → O(n²) for Wide-n")
    print(f"Wide-100 will have ~10,000 axioms — this is the scalability test.")


if __name__ == "__main__":
    main()