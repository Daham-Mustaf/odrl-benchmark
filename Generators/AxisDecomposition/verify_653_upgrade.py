"""Verify the upgraded ODRL653 conjecture (4-axis chain) closes."""
import z3

# (same setup as audit_subs.py - reusing the same predicate signatures)
Value = z3.DeclareSort("Value")
Verdict = z3.DeclareSort("Verdict")
Presence = z3.DeclareSort("Presence")

less = z3.Function("less", Value, Value, z3.BoolSort())
leq  = z3.Function("leq",  Value, Value, z3.BoolSort())

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

X, Y, Z = z3.Consts("X Y Z", Value)
L1, U1, L2, U2 = z3.Consts("L1 U1 L2 U2", Value)
V1, V2 = z3.Consts("V1 V2", Verdict)
P1, P2 = z3.Consts("P1 P2", Presence)

BASE = [
    # ORD000
    z3.ForAll([X], z3.Not(less(X, X))),
    z3.ForAll([X, Y, Z], z3.Implies(z3.And(less(X, Y), less(Y, Z)),
                                     less(X, Z))),
    z3.ForAll([X, Y], z3.Implies(less(X, Y), z3.Not(less(Y, X)))),
    z3.ForAll([X, Y], leq(X, Y) == z3.Or(less(X, Y), X == Y)),

    # AXIS000 (verdict distinctness)
    compatible != conflict, compatible != unknown, conflict != unknown,
    z3.ForAll([V1], is_verdict(V1) ==
              z3.Or(V1 == compatible, V1 == conflict, V1 == unknown)),
    is_verdict(compatible), is_verdict(conflict), is_verdict(unknown),

    # SUBS000 v1.1
    z3.ForAll([L1, U1, L2, U2],
              axis_subsumes(L1, U1, L2, U2) ==
              z3.And(leq(L2, L1), leq(U1, U2))),  # the new biconditional

    present != absent,
    z3.ForAll([P1], is_presence(P1) ==
              z3.Or(P1 == present, P1 == absent)),
    is_presence(present), is_presence(absent),
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


def Vc(n): return z3.Const(n, Value)
v0 = Vc("v0"); v16 = Vc("v16"); v32 = Vc("v32"); v150 = Vc("v150")
v300 = Vc("v300"); v400 = Vc("v400"); v600 = Vc("v600"); v800 = Vc("v800")

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


def fol_check(extras, conj):
    s = z3.Solver(); s.set("timeout", 15000)
    for a in BASE: s.add(a)
    for e in extras: s.add(e)
    s.add(z3.Not(conj))
    r = s.check()
    return "Theorem" if r == z3.unsat else (
        "CounterSatisfiable" if r == z3.sat else "Unknown")


# Test the proposed new ODRL653 conjecture: 4-axis chain with width=Conflict
new_653_conj = box_subs(
    box_subs(
        box_subs(
            subs_verdict(v0, v800, present, v0, v600, present),  # width: Conflict
            subs_verdict(v0, v400, present, v0, v800, present)), # height: Compatible
        subs_verdict(v0, v16, present, v0, v32, present)),       # depth: Compatible
    subs_verdict(v0, v150, present, v0, v300, present)           # alt: Compatible
) == conflict

result = fol_check(ord_chain_652, new_653_conj)
print(f"Proposed ODRL653 (4-axis chain, width Conflict): {result}")

# Also test that NEGATIVE conjectures (different expected verdicts) fail
print("\nSoundness check: do wrong-verdict conjectures correctly fail?")
for wrong_verdict, label in [(compatible, "compatible"), (unknown, "unknown")]:
    wrong_conj = box_subs(
        box_subs(
            box_subs(
                subs_verdict(v0, v800, present, v0, v600, present),
                subs_verdict(v0, v400, present, v0, v800, present)),
            subs_verdict(v0, v16, present, v0, v32, present)),
        subs_verdict(v0, v150, present, v0, v300, present)
    ) == wrong_verdict
    r = fol_check(ord_chain_652, wrong_conj)
    expected = "CounterSatisfiable"
    ok = "OK" if r == expected else "FAIL"
    print(f"  ODRL653 with verdict={label}: {r}  [{ok}]")
