"""
Audit BoxContainment: SUBS000-0.ax + the 8 problem dicts.

Key question: is axis_subsumes/4 actually defined?  If not, problems that
need to DERIVE axis_subsumes facts (ODRL650, ODRL651) cannot close.
"""
import z3

# ---------------------------------------------------------------------
# Sorts
# ---------------------------------------------------------------------
Value = z3.DeclareSort("Value")
Verdict = z3.DeclareSort("Verdict")
Presence = z3.DeclareSort("Presence")

# ORD000
less = z3.Function("less", Value, Value, z3.BoolSort())
leq  = z3.Function("leq",  Value, Value, z3.BoolSort())

# SUBS000 predicates
axis_subsumes = z3.Function(
    "axis_subsumes", Value, Value, Value, Value, z3.BoolSort())
subs_verdict = z3.Function(
    "subs_verdict",
    Value, Value, Presence, Value, Value, Presence, Verdict)
box_subs = z3.Function("box_subs", Verdict, Verdict, Verdict)

is_presence = z3.Function("is_presence", Presence, z3.BoolSort())
is_verdict  = z3.Function("is_verdict",  Verdict,  z3.BoolSort())

present, absent = z3.Consts("present absent", Presence)
compatible, conflict, unknown = z3.Consts(
    "compatible conflict unknown", Verdict)


# ---------------------------------------------------------------------
# ORD000 base
# ---------------------------------------------------------------------
X, Y, Z = z3.Consts("X Y Z", Value)
L1, U1, L2, U2 = z3.Consts("L1 U1 L2 U2", Value)
V1, V2 = z3.Consts("V1 V2", Verdict)
P1, P2 = z3.Consts("P1 P2", Presence)
A, B   = z3.Consts("A B", Value)

ORD000 = [
    z3.ForAll([X], z3.Not(less(X, X))),
    z3.ForAll([X, Y, Z], z3.Implies(z3.And(less(X, Y), less(Y, Z)),
                                     less(X, Z))),
    z3.ForAll([X, Y], z3.Implies(less(X, Y), z3.Not(less(Y, X)))),
    z3.ForAll([X, Y], leq(X, Y) == z3.Or(less(X, Y), X == Y)),
]

# AXIS000 (just verdict distinctness, which is what we actually need)
AXIS000 = [
    compatible != conflict,
    compatible != unknown,
    conflict   != unknown,
    z3.ForAll([V1], is_verdict(V1) ==
              z3.Or(V1 == compatible, V1 == conflict, V1 == unknown)),
    is_verdict(compatible),
    is_verdict(conflict),
    is_verdict(unknown),
]

# SUBS000 v1.0 — CURRENT (no axis_subsumes definition)
SUBS000_v1 = [
    present != absent,
    z3.ForAll([P1], is_presence(P1) ==
              z3.Or(P1 == present, P1 == absent)),
    is_presence(present),
    is_presence(absent),
    z3.ForAll([L1, U1, L2, U2],
              subs_verdict(L1, U1, absent, L2, U2, present) == unknown),
    z3.ForAll([L1, U1, L2, U2],
              subs_verdict(L1, U1, present, L2, U2, absent) == unknown),
    z3.ForAll([L1, U1, L2, U2],
              subs_verdict(L1, U1, absent, L2, U2, absent) == unknown),
    z3.ForAll([L1, U1, L2, U2],
              z3.Implies(axis_subsumes(L1, U1, L2, U2),
                         subs_verdict(L1, U1, present, L2, U2, present)
                         == compatible)),
    z3.ForAll([L1, U1, L2, U2],
              z3.Implies(z3.Not(axis_subsumes(L1, U1, L2, U2)),
                         subs_verdict(L1, U1, present, L2, U2, present)
                         == conflict)),
    z3.ForAll([V1, V2], z3.Implies(
        z3.And(is_verdict(V1), is_verdict(V2),
               V1 == compatible, V2 == compatible),
        box_subs(V1, V2) == compatible)),
    z3.ForAll([V1, V2], z3.Implies(
        z3.And(is_verdict(V1), is_verdict(V2),
               z3.Or(V1 == conflict, V2 == conflict)),
        box_subs(V1, V2) == conflict)),
    z3.ForAll([V1, V2], z3.Implies(
        z3.And(is_verdict(V1), is_verdict(V2),
               z3.Not(z3.And(V1 == compatible, V2 == compatible)),
               V1 != conflict, V2 != conflict),
        box_subs(V1, V2) == unknown)),
]

# SUBS000 v1.1 — proposed, with axis_subsumes biconditional added
SUBS000_v2 = SUBS000_v1 + [
    z3.ForAll([L1, U1, L2, U2],
              axis_subsumes(L1, U1, L2, U2) ==
              z3.And(leq(L2, L1), leq(U1, U2))),
]


def Vc(n): return z3.Const(n, Value)


def fol_check(axioms, extras, conj):
    s = z3.Solver()
    s.set("timeout", 15000)
    for ax in axioms: s.add(ax)
    for e in extras:  s.add(e)
    s.add(z3.Not(conj))
    r = s.check()
    return "Theorem" if r == z3.unsat else (
        "CounterSat" if r == z3.sat else "Unknown")


# ---------------------------------------------------------------------
# Problem definitions
# ---------------------------------------------------------------------
v0 = Vc("v0"); v16 = Vc("v16"); v32 = Vc("v32"); v150 = Vc("v150")
v300 = Vc("v300"); v400 = Vc("v400"); v600 = Vc("v600"); v800 = Vc("v800")

ord_chain_650 = [
    less(v0, v600), less(v0, v800), less(v600, v800),
    v0 != v600, v0 != v800, v600 != v800,
]

ord_chain_652 = [
    less(v0, v16), less(v0, v32), less(v0, v150), less(v0, v300),
    less(v0, v400), less(v0, v600), less(v0, v800),
    less(v16, v32), less(v16, v150), less(v16, v300), less(v16, v400),
    less(v16, v600), less(v16, v800),
    less(v32, v150), less(v32, v300), less(v32, v400), less(v32, v600),
    less(v32, v800),
    less(v150, v300), less(v150, v400), less(v150, v600), less(v150, v800),
    less(v300, v400), less(v300, v600), less(v300, v800),
    less(v400, v600), less(v400, v800),
    less(v600, v800),
    v0 != v16, v0 != v32, v0 != v150, v0 != v300, v0 != v400,
    v0 != v600, v0 != v800,
    v16 != v32, v16 != v150, v16 != v300, v16 != v400,
    v16 != v600, v16 != v800,
    v32 != v150, v32 != v300, v32 != v400, v32 != v600, v32 != v800,
    v150 != v300, v150 != v400, v150 != v600, v150 != v800,
    v300 != v400, v300 != v600, v300 != v800,
    v400 != v600, v400 != v800,
    v600 != v800,
]

PROBLEMS = [
    {
        "id": "ODRL650",
        "extras": ord_chain_650,
        "conj":   subs_verdict(v0, v600, present, v0, v800, present) == compatible,
        "expected": "Theorem",
    },
    {
        "id": "ODRL651",
        "extras": ord_chain_650,
        "conj":   subs_verdict(v0, v800, present, v0, v600, present) == conflict,
        "expected": "Theorem",
    },
    {
        "id": "ODRL652",
        # has explicit hints for 4 axis_subsumes facts
        "extras": ord_chain_652 + [
            axis_subsumes(v0, v600, v0, v800),
            axis_subsumes(v0, v400, v0, v800),
            axis_subsumes(v0, v16,  v0, v32),
            axis_subsumes(v0, v150, v0, v300),
        ],
        "conj":   box_subs(
                    box_subs(
                      box_subs(
                        subs_verdict(v0, v600, present, v0, v800, present),
                        subs_verdict(v0, v400, present, v0, v800, present)),
                      subs_verdict(v0, v16, present, v0, v32, present)),
                    subs_verdict(v0, v150, present, v0, v300, present)
                  ) == compatible,
        "expected": "Theorem",
    },
    {
        "id": "ODRL653",
        # has explicit hint for ~axis_subsumes(v0, v800, v0, v600)
        "extras": ord_chain_650 + [
            z3.Not(axis_subsumes(v0, v800, v0, v600)),
        ],
        "conj":   subs_verdict(v0, v800, present, v0, v600, present) == conflict,
        "expected": "Theorem",
    },
    {
        "id": "ODRL654",
        "extras": ord_chain_650,
        "conj":   subs_verdict(v0, v600, absent, v0, v800, present) == unknown,
        "expected": "Theorem",
    },
    {
        "id": "ODRL655",
        "extras": ord_chain_650,
        "conj":   subs_verdict(v0, v600, present, v0, v800, absent) == unknown,
        "expected": "Theorem",
    },
    {
        "id": "ODRL656",
        "extras": ord_chain_650,
        "conj":   subs_verdict(v0, v600, absent, v0, v800, absent) == unknown,
        "expected": "Theorem",
    },
    {
        "id": "ODRL657",
        "extras": ord_chain_652 + [
            axis_subsumes(v0, v400, v0, v800),
            axis_subsumes(v0, v16,  v0, v32),
            axis_subsumes(v0, v150, v0, v300),
        ],
        "conj":   box_subs(
                    box_subs(
                      box_subs(
                        subs_verdict(v0, v800, absent,  v0, v800, present),
                        subs_verdict(v0, v400, present, v0, v800, present)),
                      subs_verdict(v0, v16, present, v0, v32, present)),
                    subs_verdict(v0, v150, present, v0, v300, present)
                  ) == unknown,
        "expected": "Theorem",
    },
]

# ---------------------------------------------------------------------
# Run audits
# ---------------------------------------------------------------------
v1_axioms = ORD000 + AXIS000 + SUBS000_v1
v2_axioms = ORD000 + AXIS000 + SUBS000_v2

print(f"{'='*78}")
print(f"FOL audit: BoxContainment / SUBS000")
print(f"{'='*78}")
print(f"\nColumn 1: closure under CURRENT SUBS000 (no axis_subsumes def)")
print(f"Column 2: closure under PROPOSED SUBS000 v1.1 (axis_subsumes biconditional added)")
print()
print(f"  {'ID':<10s}  {'current':<14s}  {'proposed v1.1':<14s}  Notes")
print(f"  {'-'*10}  {'-'*14}  {'-'*14}  {'-'*40}")
for p in PROBLEMS:
    a = fol_check(v1_axioms, p["extras"], p["conj"])
    b = fol_check(v2_axioms, p["extras"], p["conj"])
    a_ok = (a == p["expected"])
    b_ok = (b == p["expected"])
    if a_ok and b_ok:
        note = "OK in both"
    elif b_ok and not a_ok:
        note = "FIXED by biconditional"
    elif a_ok and not b_ok:
        note = "REGRESSED -- biconditional breaks it"
    else:
        note = "broken in both"
    print(f"  {p['id']:<10s}  {a:<14s}  {b:<14s}  {note}")
