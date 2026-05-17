"""
Audit COMP000-0.ax against paper §7 (def:or-verdict, def:xone-verdict).

Two questions:
1. Does the axiom file correctly encode the paper's case analysis?
2. Do the predicate signatures match what LogicalOr / LogicalXone /
   Composition problems will actually use?

For (1) we check each case from def:or-verdict and def:xone-verdict.
For (2) we'll need the problem files, but flagging concerns from the
axiom file alone first.
"""
import z3

Value = z3.DeclareSort("Value")
Verdict = z3.DeclareSort("Verdict")

is_verdict = z3.Function("is_verdict", Verdict, z3.BoolSort())
or_verdict   = z3.Function("or_verdict",   Verdict, Verdict, Verdict)
xone_verdict = z3.Function("xone_verdict", Verdict, Verdict, Verdict)

compatible, conflict_v, unknown = z3.Consts(
    "compatible conflict_v unknown", Verdict)

V1, V2 = z3.Consts("V1 V2", Verdict)

# AXIS000 verdict facts (assumed present from earlier audit)
VERDICTS = [
    compatible != conflict_v, compatible != unknown, conflict_v != unknown,
    z3.ForAll([V1], is_verdict(V1) == z3.Or(V1 == compatible,
                                             V1 == conflict_v,
                                             V1 == unknown)),
    is_verdict(compatible), is_verdict(conflict_v), is_verdict(unknown),
]

# COMP000 v1.0
COMP000 = [
    # or_verdict cases
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
    z3.ForAll([V1, V2], z3.Implies(
        z3.And(is_verdict(V1), is_verdict(V2)),
        z3.Or(or_verdict(V1, V2) == compatible,
              or_verdict(V1, V2) == conflict_v,
              or_verdict(V1, V2) == unknown))),
    # xone_verdict cases
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
               z3.Not(z3.And(V1 == conflict_v, V2 == conflict_v))),
        xone_verdict(V1, V2) == unknown)),
    z3.ForAll([V1, V2], z3.Implies(
        z3.And(is_verdict(V1), is_verdict(V2)),
        z3.Or(xone_verdict(V1, V2) == compatible,
              xone_verdict(V1, V2) == conflict_v,
              xone_verdict(V1, V2) == unknown))),
]


def check(conj, label):
    s = z3.Solver(); s.set("timeout", 5000)
    for a in VERDICTS: s.add(a)
    for a in COMP000:  s.add(a)
    s.add(z3.Not(conj))
    r = s.check()
    status = "Theorem" if r == z3.unsat else (
        "CounterSat" if r == z3.sat else "Unknown")
    return status


# ---------------------------------------------------------------------
# Audit 1: or_verdict full truth table (9 cases for 3x3 inputs)
# ---------------------------------------------------------------------
print("="*78)
print("or_verdict truth table (paper def:or-verdict)")
print("="*78)
print()
print("  Paper says:")
print("    Compatible if any branch pair compatible")
print("    Conflict   if all branch pairs conflict")
print("    Unknown    otherwise")
print()
print(f"  {'V1':<12s} {'V2':<12s} {'Expected':<12s} {'Got':<12s} {'?'}")
print(f"  {'-'*12} {'-'*12} {'-'*12} {'-'*12} {'-'}")

OR_EXPECTED = {
    (compatible, compatible): compatible,
    (compatible, conflict_v): compatible,
    (compatible, unknown):    compatible,
    (conflict_v, compatible): compatible,
    (conflict_v, conflict_v): conflict_v,
    (conflict_v, unknown):    unknown,    # paper: "otherwise" -> Unknown
    (unknown,    compatible): compatible,
    (unknown,    conflict_v): unknown,    # paper: "otherwise" -> Unknown
    (unknown,    unknown):    unknown,
}

for (v1, v2), expected in OR_EXPECTED.items():
    got = None
    for cand in (compatible, conflict_v, unknown):
        if check(or_verdict(v1, v2) == cand, f"or({v1},{v2})={cand}") == "Theorem":
            got = cand
            break
    label1 = str(v1).replace("conflict_v", "conflict")
    label2 = str(v2).replace("conflict_v", "conflict")
    exp_label = str(expected).replace("conflict_v", "conflict")
    got_label = str(got).replace("conflict_v", "conflict") if got is not None else "??"
    ok = "ok" if got is not None and got.eq(expected) else "MISMATCH"
    print(f"  {label1:<12s} {label2:<12s} {exp_label:<12s} {got_label:<12s} {ok}")

# ---------------------------------------------------------------------
# Audit 2: xone_verdict cases
# ---------------------------------------------------------------------
print()
print("="*78)
print("xone_verdict truth table (paper def:xone-verdict)")
print("="*78)
print()
print("  Paper says:")
print("    Compatible if exactly one branch pair compatible AND rest conflict")
print("    Conflict   if all branch pairs conflict")
print("    Unknown    otherwise")
print()
print("  NOTE: this is the binary reduction xone_verdict(VM, VR).")
print("    VM = 'match' verdict (verdict of one specific branch pair)")
print("    VR = 'remainder' aggregate verdict (over the other branch pairs)")
print("    These are NOT both branch-pair verdicts on equal footing!")
print()
print(f"  {'VM':<12s} {'VR':<12s} {'Expected':<12s} {'Got':<12s} {'?'}")
print(f"  {'-'*12} {'-'*12} {'-'*12} {'-'*12} {'-'}")

# Under the conservative reduction in the axiom file:
#   xone(compat, conflict) = compatible    (one match, rest conflict)
#   xone(conflict, conflict) = conflict    (no match, all conflict)
#   everything else          = unknown     (conservative)
XONE_EXPECTED = {
    (compatible, compatible): unknown,     # two compatibles -> not "exactly one"
    (compatible, conflict_v): compatible,  # exactly one match
    (compatible, unknown):    unknown,
    (conflict_v, compatible): unknown,     # second is unmodeled; conservative
    (conflict_v, conflict_v): conflict_v,  # no match, all conflict
    (conflict_v, unknown):    unknown,
    (unknown,    compatible): unknown,
    (unknown,    conflict_v): unknown,
    (unknown,    unknown):    unknown,
}

for (v1, v2), expected in XONE_EXPECTED.items():
    got = None
    for cand in (compatible, conflict_v, unknown):
        if check(xone_verdict(v1, v2) == cand, "") == "Theorem":
            got = cand
            break
    label1 = str(v1).replace("conflict_v", "conflict")
    label2 = str(v2).replace("conflict_v", "conflict")
    exp_label = str(expected).replace("conflict_v", "conflict")
    got_label = str(got).replace("conflict_v", "conflict") if got is not None else "??"
    ok = "ok" if got is not None and got.eq(expected) else "MISMATCH"
    print(f"  {label1:<12s} {label2:<12s} {exp_label:<12s} {got_label:<12s} {ok}")

# ---------------------------------------------------------------------
# Audit 3: are there any dead predicates / undefined symbols?
# ---------------------------------------------------------------------
print()
print("="*78)
print("Predicate inventory: what does COMP000 define?")
print("="*78)
print()
print("  Defined predicates:")
print("    or_verdict/2   : (Verdict, Verdict) -> Verdict")
print("    xone_verdict/2 : (Verdict, Verdict) -> Verdict")
print()
print("  Predicates used by COMP000 (must be defined elsewhere):")
print("    is_verdict/1   : Verdict -> Bool          (AXIS000 Section B)")
print("    compatible, conflict, unknown : Verdict   (AXIS000 Section B)")
print()
print("  COMP000 itself is closed: it doesn't reference predicates that")
print("  aren't either defined here or in AXIS000.  Good.")
print()
print("  But the problem files MAY use other predicates like:")
print("    branch_verdict/4  -- per-branch-pair verdict")
print("    or_verdict_n/N    -- N-ary versions")
print("    xone_aggregate/N  -- aggregated branch verdicts")
print()
print("  Need to see the problem files to check for that mismatch.")
