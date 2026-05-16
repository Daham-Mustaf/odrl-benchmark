"""Verify the new SMTs are semantic via independent perturbations."""
import z3

def smt_check(block):
    s = z3.Solver(); s.set("timeout", 3000)
    s.from_string(f"(set-logic QF_LRA)\n{block}\n(check-sat)\n")
    r = s.check()
    return "unsat" if r == z3.unsat else ("sat" if r == z3.sat else "unknown")


# Proposed new SMTs
new = {
    "ODRL610": (
        "(declare-const v Real)\n"
        "(assert (= v 600.0))\n"
        "(assert (or (< v 0.0) (> v 1200.0)))"
    ),
    "ODRL611": (
        "(declare-const v Real)\n"
        "(assert (= v 600.0))\n"
        "(assert (or (< v 0.0) (> v 1200.0)))"
    ),
    "ODRL612": (
        "(declare-const v Real)\n"
        "(assert (= v 600.0))\n"
        "(assert (or (< v 0.0) (> v 1200.0)))"
    ),
    "ODRL613": (
        "(declare-const v Real)\n"
        "(assert (= v 600.0))\n"
        "(assert (or (< v 0.0) (> v 1200.0) (= v 0.0)))"
    ),
    "ODRL615": (
        "(declare-const v Real)\n"
        "(assert (= v 600.0))\n"
        "(assert (or (< v 0.0) (> v 1200.0) (= v 1200.0)))"
    ),
}


def perturb_witness(block, new_witness):
    return block.replace("(assert (= v 600.0))",
                         f"(assert (= v {new_witness}))")


def perturb_upper(block, new_upper):
    return block.replace("1200.0", str(new_upper))


print(f"  {'ID':<10s}  {'Orig':<6s}  {'Witness=2000':<13s}  {'Upper=500':<10s}  Verdict")
print(f"  {'-'*10}  {'-'*6}  {'-'*13}  {'-'*10}  {'-'*30}")

for pid, blk in new.items():
    r0 = smt_check(blk)
    r1 = smt_check(perturb_witness(blk, "2000.0"))
    r2 = smt_check(perturb_upper(blk, "500.0"))

    if r0 == "unsat" and r1 == "sat" and r2 == "sat":
        verdict = "semantic (responds to BOTH perturbations)"
    elif r0 == "unsat" and (r1 == "sat" or r2 == "sat"):
        verdict = "partially semantic"
    elif r0 == "unsat":
        verdict = "still tautological"
    else:
        verdict = f"unexpected: orig={r0}"
    print(f"  {pid:<10s}  {r0:<6s}  {r1:<13s}  {r2:<10s}  {verdict}")
