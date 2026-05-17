"""Verify ODRL471 and ODRL472 close under AXIS000 + COMP000."""
import z3

Verdict = z3.DeclareSort("Verdict")
is_verdict = z3.Function("is_verdict", Verdict, z3.BoolSort())
or_verdict   = z3.Function("or_verdict",   Verdict, Verdict, Verdict)
xone_verdict = z3.Function("xone_verdict", Verdict, Verdict, Verdict)

compatible, conflict_v, unknown = z3.Consts(
    "compatible conflict unknown", Verdict)
V1, V2 = z3.Consts("V1 V2", Verdict)

AXIOMS = [
    # AXIS000 verdict facts
    compatible != conflict_v, compatible != unknown, conflict_v != unknown,
    z3.ForAll([V1], is_verdict(V1) == z3.Or(V1 == compatible,
                                             V1 == conflict_v,
                                             V1 == unknown)),
    is_verdict(compatible), is_verdict(conflict_v), is_verdict(unknown),
    # COMP000 or_verdict
    z3.ForAll([V1, V2], z3.Implies(
        z3.And(is_verdict(V1), is_verdict(V2),
               z3.Or(V1 == compatible, V2 == compatible)),
        or_verdict(V1, V2) == compatible)),
    z3.ForAll([V1, V2], z3.Implies(
        z3.And(is_verdict(V1), is_verdict(V2),
               V1 == conflict_v, V2 == conflict_v),
        or_verdict(V1, V2) == conflict_v)),
    z3.ForAll([V1, V2], z3.Implies(
        z3.And(is_verdict(V1), is_verdict(V2),
               V1 != compatible, V2 != compatible,
               z3.Not(z3.And(V1 == conflict_v, V2 == conflict_v))),
        or_verdict(V1, V2) == unknown)),
    # COMP000 xone_verdict
    z3.ForAll([V1, V2], z3.Implies(
        z3.And(is_verdict(V1), is_verdict(V2),
               V1 == compatible, V2 == conflict_v),
        xone_verdict(V1, V2) == compatible)),
    z3.ForAll([V1, V2], z3.Implies(
        z3.And(is_verdict(V1), is_verdict(V2),
               V1 == conflict_v, V2 == conflict_v),
        xone_verdict(V1, V2) == conflict_v)),
    z3.ForAll([V1, V2], z3.Implies(
        z3.And(is_verdict(V1), is_verdict(V2),
               z3.Not(z3.And(V1 == compatible, V2 == conflict_v)),
               z3.Not(z3.And(V1 == conflict_v,  V2 == conflict_v))),
        xone_verdict(V1, V2) == unknown)),
]


def check(label, conj):
    s = z3.Solver(); s.set("timeout", 5000)
    for a in AXIOMS: s.add(a)
    s.add(z3.Not(conj))
    r = s.check()
    status = "Theorem" if r == z3.unsat else (
        "CounterSat" if r == z3.sat else "Unknown")
    print(f"  {label}: {status}")


# ODRL471: or_verdict(conflict, compatible) = compatible
check("ODRL471: or_verdict(conflict, compatible) = compatible",
      or_verdict(conflict_v, compatible) == compatible)

# Soundness: wrong claim should NOT close
check("  soundness: or_verdict(conflict, compatible) = conflict (should CounterSat)",
      or_verdict(conflict_v, compatible) == conflict_v)

# ODRL472: xone_verdict(compatible, conflict) = compatible
check("ODRL472: xone_verdict(compatible, conflict) = compatible",
      xone_verdict(compatible, conflict_v) == compatible)

# Soundness
check("  soundness: xone_verdict(compatible, conflict) = conflict (should CounterSat)",
      xone_verdict(compatible, conflict_v) == conflict_v)

# Also test the conflict-conflict cases (def:or-verdict Rule 2, def:xone-verdict)
check("Bonus: or_verdict(conflict, conflict) = conflict",
      or_verdict(conflict_v, conflict_v) == conflict_v)
check("Bonus: xone_verdict(conflict, conflict) = conflict",
      xone_verdict(conflict_v, conflict_v) == conflict_v)
