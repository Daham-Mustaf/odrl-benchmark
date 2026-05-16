"""
Audit Projection: PROJ000-0.ax + 10 problem dicts.

Critical mismatch: PROJ000 currently defines box_member/6 and box_member3/9,
but problems use in_box2/6, in_box3/9, box2_compatible/8, box2_conflict/8.
Four predicates the problems USE are not DEFINED anywhere.
"""
import z3

# ---------------------------------------------------------------------
# Sorts and signatures
# ---------------------------------------------------------------------
Value = z3.DeclareSort("Value")

less = z3.Function("less", Value, Value, z3.BoolSort())
leq  = z3.Function("leq",  Value, Value, z3.BoolSort())
val  = z3.Function("val",  Value, z3.BoolSort())

in_closed = z3.Function("in_closed", Value, Value, Value, z3.BoolSort())
in_lopen  = z3.Function("in_lopen",  Value, Value, Value, z3.BoolSort())
in_ropen  = z3.Function("in_ropen",  Value, Value, Value, z3.BoolSort())
in_open   = z3.Function("in_open",   Value, Value, Value, z3.BoolSort())

in_box2 = z3.Function("in_box2",
                      Value, Value, Value, Value, Value, Value,
                      z3.BoolSort())
in_box3 = z3.Function("in_box3",
                      Value, Value, Value, Value, Value, Value, Value, Value, Value,
                      z3.BoolSort())
box2_compatible = z3.Function("box2_compatible",
                              Value, Value, Value, Value,
                              Value, Value, Value, Value,
                              z3.BoolSort())
box2_conflict   = z3.Function("box2_conflict",
                              Value, Value, Value, Value,
                              Value, Value, Value, Value,
                              z3.BoolSort())

X, Y, Z, W = z3.Consts("X Y Z W", Value)
L1, U1, L2, U2, L3, U3 = z3.Consts("L1 U1 L2 U2 L3 U3", Value)
L1B, U1B, L2B, U2B = z3.Consts("L1B U1B L2B U2B", Value)


# ORD000
ORD000 = [
    z3.ForAll([X], z3.Not(less(X, X))),
    z3.ForAll([X, Y, Z], z3.Implies(z3.And(less(X, Y), less(Y, Z)),
                                     less(X, Z))),
    z3.ForAll([X, Y], z3.Implies(less(X, Y), z3.Not(less(Y, X)))),
    z3.ForAll([X, Y], leq(X, Y) == z3.Or(less(X, Y), X == Y)),
]

# Density (ORD001) -- ONLY for ODRL628
ORD001 = [
    z3.ForAll([X, Y], z3.Implies(less(X, Y),
        z3.Exists([Z], z3.And(less(X, Z), less(Z, Y))))),
]

# AXIS000 -- assumed interval predicates
AXIS000 = [
    z3.ForAll([X, L1, U1],
              in_closed(X, L1, U1) == z3.And(leq(L1, X), leq(X, U1))),
    z3.ForAll([X, L1, U1],
              in_lopen(X, L1, U1) == z3.And(less(L1, X), leq(X, U1))),
    z3.ForAll([X, L1, U1],
              in_ropen(X, L1, U1) == z3.And(leq(L1, X), less(X, U1))),
    z3.ForAll([X, L1, U1],
              in_open(X, L1, U1) == z3.And(less(L1, X), less(X, U1))),
]

# PROJ000 v1.0 -- CURRENT (uses box_member, not in_box2)
PROJ000_v1 = [
    # box_member is defined but NO problem uses it!
]

# PROJ000 v1.1 -- PROPOSED: in_box2/3, box2_compatible, box2_conflict biconditionals
PROJ000_v2 = [
    z3.ForAll([X, Y, L1, U1, L2, U2],
              in_box2(X, Y, L1, U1, L2, U2) ==
              z3.And(in_closed(X, L1, U1), in_closed(Y, L2, U2))),
    z3.ForAll([X, Y, Z, L1, U1, L2, U2, L3, U3],
              in_box3(X, Y, Z, L1, U1, L2, U2, L3, U3) ==
              z3.And(in_closed(X, L1, U1),
                     in_closed(Y, L2, U2),
                     in_closed(Z, L3, U3))),
    # box2_compatible: two 2D boxes overlap iff per-axis intersections non-empty
    # For closed-closed: max(L_A, L_B) <= min(U_A, U_B) per axis
    # = (L_A <= U_B) AND (L_B <= U_A)
    z3.ForAll([L1, U1, L2, U2, L1B, U1B, L2B, U2B],
              box2_compatible(L1, U1, L2, U2, L1B, U1B, L2B, U2B) ==
              z3.And(leq(L1, U1B), leq(L1B, U1),
                     leq(L2, U2B), leq(L2B, U2))),
    # box2_conflict: any axis has disjoint intervals (per Conflict Criterion)
    z3.ForAll([L1, U1, L2, U2, L1B, U1B, L2B, U2B],
              box2_conflict(L1, U1, L2, U2, L1B, U1B, L2B, U2B) ==
              z3.Or(less(U1, L1B), less(U1B, L1),
                    less(U2, L2B), less(U2B, L2))),
]


def Vc(n): return z3.Const(n, Value)
v0 = Vc("v0"); v200 = Vc("v200"); v300 = Vc("v300"); v400 = Vc("v400")
v600 = Vc("v600"); v800 = Vc("v800"); v1200 = Vc("v1200")


def fol_check(axioms, extras, conj, needs_density=False):
    s = z3.Solver(); s.set("timeout", 15000)
    for ax in axioms: s.add(ax)
    if needs_density:
        for ax in ORD001: s.add(ax)
    for e in extras: s.add(e)
    s.add(z3.Not(conj))
    r = s.check()
    return "Theorem" if r == z3.unsat else (
        "CounterSat" if r == z3.sat else "Unknown")


# Problem catalogue
PROBLEMS = [
    {
        "id": "ODRL620",
        "extras": [
            less(v0, v300), less(v0, v400), less(v300, v600), less(v400, v600),
            v0 != v300, v0 != v400, v0 != v600,
            v300 != v400, v300 != v600, v400 != v600,
        ],
        "conj": in_box2(v300, v400, v0, v600, v0, v600),
        "expected": "Theorem", "needs_density": False,
    },
    {
        "id": "ODRL621",
        "extras": [
            less(v0, v400), less(v0, v600), less(v400, v600), less(v600, v800),
            v0 != v400, v0 != v600, v0 != v800,
            v400 != v600, v400 != v800, v600 != v800,
        ],
        "conj": z3.Not(in_box2(v800, v400, v0, v600, v0, v600)),
        "expected": "Theorem", "needs_density": False,
    },
    {
        "id": "ODRL622",
        "extras": [
            less(v0, v200), less(v0, v300), less(v0, v400),
            less(v200, v600), less(v300, v600), less(v400, v600),
            v0 != v200, v0 != v300, v0 != v400, v0 != v600,
            v200 != v300, v200 != v400, v200 != v600,
            v300 != v400, v300 != v600, v400 != v600,
        ],
        "conj": in_box3(v300, v400, v200, v0, v600, v0, v600, v0, v600),
        "expected": "Theorem", "needs_density": False,
    },
    {
        "id": "ODRL623",
        "extras": [
            less(v0, v200), less(v0, v300), less(v0, v600),
            less(v200, v600), less(v300, v600), less(v600, v800),
            v0 != v200, v0 != v300, v0 != v600, v0 != v800,
            v200 != v300, v200 != v600, v200 != v800,
            v300 != v600, v300 != v800, v600 != v800,
        ],
        "conj": z3.Not(in_box3(v300, v800, v200, v0, v600, v0, v600, v0, v600)),
        "expected": "Theorem", "needs_density": False,
    },
    {
        "id": "ODRL624",
        "extras": [
            less(v0, v400), less(v0, v600), less(v400, v600),
            less(v400, v800), less(v600, v800),
            v0 != v400, v0 != v600, v0 != v800,
            v400 != v600, v400 != v800, v600 != v800,
        ],
        "conj": box2_compatible(v0, v600, v0, v600, v400, v800, v400, v800),
        "expected": "Theorem", "needs_density": False,
    },
    {
        "id": "ODRL625",
        "extras": [
            less(v0, v400), less(v0, v600), less(v400, v600),
            less(v400, v800), less(v600, v800),
            v0 != v400, v0 != v600, v0 != v800,
            v400 != v600, v400 != v800, v600 != v800,
        ],
        "conj": box2_conflict(v0, v400, v0, v600, v600, v800, v0, v600),
        "expected": "Theorem", "needs_density": False,
    },
    {
        "id": "ODRL626",
        "extras": [
            less(v400, v600),
            v400 != v600,
        ],
        "conj": z3.And(in_closed(v600, v600, v600),
                       z3.Not(in_closed(v400, v600, v600))),
        "expected": "Theorem", "needs_density": False,
    },
    {
        "id": "ODRL627",
        "extras": [
            less(v0, v400), less(v400, v600),
            v0 != v400, v0 != v600, v400 != v600,
        ],
        "conj": z3.And(in_ropen(v400, v0, v600),
                       z3.Not(in_ropen(v600, v0, v600))),
        "expected": "Theorem", "needs_density": False,
    },
    {
        "id": "ODRL628",
        "extras": [
            less(v400, v600),
            v400 != v600,
        ],
        "conj": z3.Exists([X], in_open(X, v400, v600)),
        "expected": "Theorem", "needs_density": True,
    },
    {
        "id": "ODRL629",
        "extras": [
            less(v0, v600), less(v600, v1200),
            v0 != v600, v0 != v1200, v600 != v1200,
        ],
        "conj": z3.ForAll([X], z3.Implies(z3.And(leq(v0, X), leq(X, v1200)),
                                          in_closed(X, v0, v1200))),
        "expected": "Theorem", "needs_density": False,
    },
]

# Run the audit
v1_axioms = ORD000 + AXIS000 + PROJ000_v1
v2_axioms = ORD000 + AXIS000 + PROJ000_v2

print(f"{'='*78}")
print(f"FOL audit: Projection / PROJ000")
print(f"{'='*78}")
print(f"\nColumn 1: closure under CURRENT PROJ000 (defines box_member, no problem uses it)")
print(f"Column 2: closure under PROPOSED PROJ000 v1.1 (in_box2/3/box2_compatible/box2_conflict)")
print()
print(f"  {'ID':<10s}  {'current':<12s}  {'proposed':<12s}  Notes")
print(f"  {'-'*10}  {'-'*12}  {'-'*12}  {'-'*40}")
for p in PROBLEMS:
    a = fol_check(v1_axioms, p["extras"], p["conj"], p["needs_density"])
    b = fol_check(v2_axioms, p["extras"], p["conj"], p["needs_density"])
    a_ok = (a == p["expected"])
    b_ok = (b == p["expected"])
    if a_ok and b_ok:
        note = "OK in both (uses only AXIS000)"
    elif b_ok and not a_ok:
        note = "FIXED by new PROJ000"
    elif a_ok and not b_ok:
        note = "REGRESSED"
    else:
        note = "broken in both"
    print(f"  {p['id']:<10s}  {a:<12s}  {b:<12s}  {note}")


# SMT audit -- spot check a few key ones for tautology
print(f"\n{'='*78}")
print(f"SMT spot-check (tautology test on ODRL626)")
print(f"{'='*78}\n")

import re

def smt(block):
    s = z3.Solver(); s.set("timeout", 3000)
    s.from_string(f"(set-logic QF_LRA)\n{block}\n(check-sat)\n")
    r = s.check()
    return "unsat" if r == z3.unsat else ("sat" if r == z3.sat else "unknown")


# ODRL626 current SMT
sm_626_current = (
    "(declare-const x Real)\n"
    "(assert (= x 600.0))\n"
    "(assert (not (= x 600.0)))"
)
# Substitution test: only the EQUALITY in second assertion
sm_626_pert = (
    "(declare-const x Real)\n"
    "(assert (= x 600.0))\n"
    "(assert (not (= x 100.0)))"
)
print(f"ODRL626 current:  {smt(sm_626_current)} (P AND NOT P at value 600)")
print(f"ODRL626 perturbed (change second 600 -> 100): {smt(sm_626_pert)}")
print(f"  -> result flips? {'yes (semantic-enough)' if smt(sm_626_current) != smt(sm_626_pert) else 'no (purely tautological)'}")

# Proposed semantic ODRL626 SMT
sm_626_new = (
    "(declare-const x Real)\n"
    "(assert (= x 400.0))\n"
    "(assert (and (>= x 600.0) (<= x 600.0)))"
)
print(f"\nProposed ODRL626 (semantic): pin witness v400, assert in_closed at [600,600]")
print(f"  Result: {smt(sm_626_new)} (unsat because 400 not in {{600}})")
sm_626_new_pert = (
    "(declare-const x Real)\n"
    "(assert (= x 600.0))\n"
    "(assert (and (>= x 600.0) (<= x 600.0)))"
)
print(f"  Perturbed (witness=600): {smt(sm_626_new_pert)}")
