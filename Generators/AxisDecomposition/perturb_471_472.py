"""Perturbation test for new Composition SMTs."""
import z3


def smt(block):
    s = z3.Solver(); s.set("timeout", 3000)
    s.from_string(f"(set-logic QF_LRA)\n{block}\n(check-sat)\n")
    r = s.check()
    return "unsat" if r == z3.unsat else ("sat" if r == z3.sat else "unknown")


# ODRL471 original
SMT_471 = "(assert (not (= (ite (<= 0.0 2.0) 2.0 0.0) 2.0)))"

# ODRL472 original
SMT_472 = (
    "(assert (not (=\n"
    "  (ite (and (= 2.0 2.0) (= 0.0 0.0)) 2.0\n"
    "    (ite (and (= 2.0 0.0) (= 0.0 0.0)) 0.0\n"
    "      1.0))\n"
    "  2.0)))"
)

print(f"ODRL471 original:           {smt(SMT_471)}")
# Perturbation 1: change second 2.0 to -1.0 -> max(0, -1) = 0, not 2
PERT_471_a = "(assert (not (= (ite (<= 0.0 (- 0.0 1.0)) (- 0.0 1.0) 0.0) 2.0)))"
print(f"ODRL471 perturbation a:     {smt(PERT_471_a)}")
# This tests max(0, -1).  In ite encoding: (<= 0.0 -1.0) is FALSE -> picks 0.0. 0.0 != 2.0 -> negation TRUE -> sat.

# Better perturbation: change the equality target
PERT_471_b = "(assert (not (= (ite (<= 0.0 2.0) 2.0 0.0) 0.0)))"
print(f"ODRL471 perturbation b (target=0): {smt(PERT_471_b)}")
# ite (<=0 2) -> 2.0.  2.0 != 0.0 -> negation TRUE -> sat.  Confirms target matters.

print()
print(f"ODRL472 original:           {smt(SMT_472)}")
# Perturbation: change VM from 2.0 to 0.0 in the first branch test
PERT_472_a = (
    "(assert (not (=\n"
    "  (ite (and (= 0.0 2.0) (= 0.0 0.0)) 2.0\n"  # changed first 2.0 -> 0.0
    "    (ite (and (= 0.0 0.0) (= 0.0 0.0)) 0.0\n"
    "      1.0))\n"
    "  2.0)))"
)
print(f"ODRL472 perturbation (VM=conflict): {smt(PERT_472_a)}")
# First branch: VM=0.0=2.0? FALSE. Skip.
# Second branch: VM=0.0=0.0? TRUE.  VR=0.0=0.0? TRUE.  Picks 0.0.
# 0.0 != 2.0 -> negation TRUE -> sat.  Confirms value-dependent.
