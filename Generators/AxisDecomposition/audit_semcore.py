"""
Audit SemanticCore: 14 problems (ODRL500-513) from gen_semantic_core.py.

Reuses BASE_AXIOMS structure from audit_box2d_3d.py.
"""
import z3

Value = z3.DeclareSort("Value")
Verdict = z3.DeclareSort("Verdict")

less = z3.Function("less", Value, Value, z3.BoolSort())
leq  = z3.Function("leq",  Value, Value, z3.BoolSort())

in_open   = z3.Function("in_open",   Value, Value, Value, z3.BoolSort())
in_lopen  = z3.Function("in_lopen",  Value, Value, Value, z3.BoolSort())
in_ropen  = z3.Function("in_ropen",  Value, Value, Value, z3.BoolSort())
in_closed = z3.Function("in_closed", Value, Value, Value, z3.BoolSort())

X, Y, Z = z3.Consts("X Y Z", Value)
L, U = z3.Consts("L U", Value)

BASE = [
    z3.ForAll([X], z3.Not(less(X, X))),
    z3.ForAll([X, Y, Z], z3.Implies(z3.And(less(X, Y), less(Y, Z)), less(X, Z))),
    z3.ForAll([X, Y], z3.Implies(less(X, Y), z3.Not(less(Y, X)))),
    z3.ForAll([X, Y], leq(X, Y) == z3.Or(less(X, Y), X == Y)),
    z3.ForAll([X, L, U], in_open(X, L, U) == z3.And(less(L, X), less(X, U))),
    z3.ForAll([X, L, U], in_lopen(X, L, U) == z3.And(less(L, X), leq(X, U))),
    z3.ForAll([X, L, U], in_ropen(X, L, U) == z3.And(leq(L, X), less(X, U))),
    z3.ForAll([X, L, U], in_closed(X, L, U) == z3.And(leq(L, X), leq(X, U))),
]

ORD001 = [
    z3.ForAll([X, Y], z3.Implies(less(X, Y),
        z3.Exists([Z], z3.And(less(X, Z), less(Z, Y))))),
]


def Vc(n): return z3.Const(n, Value)
v0 = Vc("v0"); v200 = Vc("v200"); v400 = Vc("v400"); v600 = Vc("v600")


DECLS_2 = [
    less(v0, v200), less(v0, v600), less(v200, v600),
    v0 != v200, v0 != v600, v200 != v600,
]

DECLS_3 = [
    less(v0, v200), less(v0, v400), less(v0, v600),
    less(v200, v400), less(v200, v600), less(v400, v600),
    v0 != v200, v0 != v400, v0 != v600,
    v200 != v400, v200 != v600, v400 != v600,
]

DECLS_v0_v600 = [less(v0, v600), v0 != v600]


def fol_check(extras, conj, needs_density=False):
    s = z3.Solver(); s.set("timeout", 10000)
    for a in BASE: s.add(a)
    if needs_density:
        for a in ORD001: s.add(a)
    for e in extras: s.add(e)
    s.add(z3.Not(conj))
    r = s.check()
    return "Theorem" if r == z3.unsat else (
        "CounterSat" if r == z3.sat else "Unknown")


PROBLEMS = [
    {"id": "ODRL500", "decls": DECLS_2, "needs_density": False,
     "conj": z3.Exists([X], in_lopen(X, v0, v600))},
    {"id": "ODRL501", "decls": DECLS_2, "needs_density": False,
     "conj": z3.Exists([X], leq(v200, X))},
    {"id": "ODRL502", "decls": DECLS_2, "needs_density": False,
     "conj": z3.Exists([X], in_open(X, v0, v600))},
    {"id": "ODRL503", "decls": DECLS_2, "needs_density": False,
     "conj": z3.Exists([X], less(v200, X))},
    {"id": "ODRL504", "decls": DECLS_2, "needs_density": False,
     "conj": z3.Exists([X], in_closed(X, v200, v200))},
    {"id": "ODRL505", "decls": DECLS_3, "needs_density": False,
     "conj": z3.Exists([X],
        z3.And(in_lopen(X, v0, v400), in_lopen(X, v0, v600)))},
    {"id": "ODRL506", "decls": DECLS_3, "needs_density": False,
     "conj": z3.ForAll([X],
        z3.Not(z3.And(in_lopen(X, v0, v200), leq(v400, X))))},
    {"id": "ODRL507", "decls": DECLS_3, "needs_density": False,
     # P => P where P = (in_lopen(X, v0, v600) & in_lopen(Y, v0, v400))
     "conj": z3.ForAll([X, Y], z3.Implies(
        z3.And(in_lopen(X, v0, v600), in_lopen(Y, v0, v400)),
        z3.And(in_lopen(X, v0, v600), in_lopen(Y, v0, v400))))},
    {"id": "ODRL508", "decls": DECLS_3, "needs_density": False,
     "conj": z3.Exists([X],
        z3.And(leq(v200, X), in_lopen(X, v0, v400)))},
    {"id": "ODRL509", "decls": DECLS_3, "needs_density": False,
     "conj": z3.Exists([X],
        z3.And(less(v200, X), in_lopen(X, v0, v400)))},
    {"id": "ODRL510", "decls": DECLS_3, "needs_density": False,
     "conj": z3.Exists([X],
        z3.And(leq(v200, X), in_open(X, v0, v400)))},
    {"id": "ODRL511", "decls": DECLS_3, "needs_density": True,
     "conj": z3.Exists([X],
        z3.And(less(v200, X), in_open(X, v0, v400)))},
    {"id": "ODRL512", "decls": DECLS_2, "needs_density": False,
     "conj": z3.ForAll([X], z3.Not(in_open(X, v0, v0)))},
    {"id": "ODRL513", "decls": DECLS_v0_v600, "needs_density": False,
     "conj": z3.ForAll([X],
        z3.Not(z3.And(less(v600, X), in_lopen(X, v0, v600))))},
]

print("="*78)
print("SemanticCore audit (14 problems)")
print("="*78)
print()
for p in PROBLEMS:
    r = fol_check(p["decls"], p["conj"], p["needs_density"])
    nd = " [density]" if p["needs_density"] else ""
    print(f"  {p['id']}{nd:<10s}  {r}")

# --- Tautology check on SMTs ---
print()
print("="*78)
print("SMT tautology audit (perturbation test)")
print("="*78)
print()


def smt(block):
    s = z3.Solver(); s.set("timeout", 3000)
    s.from_string(f"(set-logic QF_LRA)\n{block}\n(check-sat)\n")
    r = s.check()
    return "unsat" if r == z3.unsat else ("sat" if r == z3.sat else "unknown")


# Key SMTs to verify
SMTS = {
    "ODRL500": ("(declare-const x Real)\n"
                "(assert (> x 0.0))\n(assert (<= x 600.0))",
                "sat — semantic existence"),
    "ODRL506": ("(declare-const x Real)\n"
                "(assert (> x 0.0))\n(assert (<= x 200.0))\n(assert (>= x 400.0))",
                "unsat — 200 < 400, empty interval"),
    "ODRL507": ("(declare-const x Real)\n(declare-const y Real)\n"
                "(assert (> x 0.0))\n(assert (<= x 600.0))\n"
                "(assert (> y 0.0))\n(assert (<= y 400.0))\n"
                "(assert (not (and (<= x 600.0) (<= y 400.0))))",
                "unsat — but trivially: (<= x 600) is already asserted; "
                "negating its conjunction with another asserted clause "
                "is propositionally contradictory.  TAUTOLOGY."),
    "ODRL512": ("(declare-const x Real)\n"
                "(assert (> x 0.0))\n(assert (< x 0.0))",
                "unsat — P AND NOT P at value 0 (irreflexivity-at-a-point, "
                "same disposition as ODRL614/637/762: accepted)"),
    "ODRL513": ("(declare-const x Real)\n"
                "(assert (> x 600.0))\n(assert (<= x 600.0))",
                "unsat — P AND NOT P at value 600 (same pattern)"),
}

for pid, (block, note) in SMTS.items():
    r0 = smt(block)
    print(f"  {pid}: {r0}")
    print(f"    {note}")
    print()

# Perturbation test on ODRL507 specifically
print("ODRL507 perturbation test (replace second '600' with '100'):")
mod507 = ("(declare-const x Real)\n(declare-const y Real)\n"
          "(assert (> x 0.0))\n(assert (<= x 600.0))\n"
          "(assert (> y 0.0))\n(assert (<= y 400.0))\n"
          "(assert (not (and (<= x 100.0) (<= y 400.0))))")
print(f"  Original: {smt(SMTS['ODRL507'][0])}")
print(f"  Modified: {smt(mod507)}")
print(f"  -> If 'sat', SMT is semantic. If 'unsat', tautological.")
