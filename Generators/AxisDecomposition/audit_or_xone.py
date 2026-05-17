"""
Audit LogicalOr (ODRL440-451) + LogicalXone (ODRL460-470).
Neither file uses COMP000 predicates -- they encode or/xone directly in FOL.
"""
import z3

Value = z3.DeclareSort("Value")
less = z3.Function("less", Value, Value, z3.BoolSort())
leq  = z3.Function("leq",  Value, Value, z3.BoolSort())
in_open   = z3.Function("in_open",   Value, Value, Value, z3.BoolSort())
in_lopen  = z3.Function("in_lopen",  Value, Value, Value, z3.BoolSort())
in_ropen  = z3.Function("in_ropen",  Value, Value, Value, z3.BoolSort())
in_closed = z3.Function("in_closed", Value, Value, Value, z3.BoolSort())

X, Y, Z, L, U = z3.Consts("X Y Z L U", Value)

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


def Vc(n): return z3.Const(n, Value)
v0 = Vc("v0"); v50 = Vc("v50"); v100 = Vc("v100"); v200 = Vc("v200")
v300 = Vc("v300"); v400 = Vc("v400"); v500 = Vc("v500"); v600 = Vc("v600")
v700 = Vc("v700"); v800 = Vc("v800"); v1000 = Vc("v1000")


def ord_chain(*vs):
    facts = []
    for i, vi in enumerate(vs):
        for vj in vs[i+1:]:
            facts.append(less(vi, vj))
            facts.append(vi != vj)
    return facts


def fol_check(extras, conj):
    s = z3.Solver(); s.set("timeout", 10000)
    for a in BASE: s.add(a)
    for e in extras: s.add(e)
    s.add(z3.Not(conj))
    r = s.check()
    return "Theorem" if r == z3.unsat else (
        "CounterSat" if r == z3.sat else "Unknown")


# ============================ LogicalOr ============================

OR_PROBLEMS = [
    {"id": "ODRL440",
     "vs": [v0, v200, v400, v600, v800],
     "conj": z3.Exists([X, Y], z3.And(
        z3.Or(in_lopen(X, v0, v400), in_lopen(Y, v0, v800)),
        z3.And(leq(v600, X), leq(v200, Y))))},
    {"id": "ODRL441",
     "vs": [v0, v100, v200, v400, v800],
     "conj": z3.ForAll([X, Y], z3.Not(z3.And(
        z3.Or(in_lopen(X, v0, v400), in_lopen(Y, v0, v100)),
        z3.And(leq(v800, X), leq(v200, Y)))))},
    {"id": "ODRL442",
     "vs": [v0, v200, v600, v800, v1000],
     "conj": z3.Exists([X, Y], z3.And(
        z3.And(in_lopen(X, v0, v800), in_lopen(Y, v0, v600)),
        z3.Or(leq(v1000, X), leq(v200, Y))))},
    {"id": "ODRL443",
     "vs": [v0, v100, v200, v400, v800],
     "conj": z3.ForAll([X, Y], z3.Not(z3.And(
        z3.And(in_lopen(X, v0, v400), in_lopen(Y, v0, v100)),
        z3.Or(leq(v800, X), leq(v200, Y)))))},
    {"id": "ODRL444",
     "vs": [v0, v300, v400, v500, v600],
     "conj": z3.Exists([X, Y], z3.And(
        z3.Or(in_lopen(X, v0, v400), in_lopen(Y, v0, v600)),
        z3.Or(leq(v300, X), leq(v500, Y))))},
    {"id": "ODRL445",
     "vs": [v0, v50, v100, v200, v400],
     "conj": z3.ForAll([X, Y, Z], z3.Not(z3.And(
        z3.Or(in_lopen(X, v0, v200), in_lopen(Y, v0, v100), in_lopen(Z, v0, v50)),
        z3.And(leq(v400, X), leq(v200, Y), leq(v100, Z)))))},
    {"id": "ODRL446",
     "vs": [v0, v100, v200, v400],
     "conj": z3.Exists([X, Y, Z], z3.And(
        z3.Or(in_lopen(X, v0, v200), in_lopen(Y, v0, v100), in_lopen(Z, v0, v200)),
        z3.And(leq(v400, X), leq(v200, Y), leq(v100, Z))))},
    {"id": "ODRL447",
     "vs": [v0, v400, v600, v800],
     "conj": z3.ForAll([X, Y], z3.Implies(
        z3.And(in_lopen(X, v0, v600), in_lopen(Y, v0, v400)),
        z3.Or(in_lopen(X, v0, v800), in_lopen(Y, v0, v600))))},
    {"id": "ODRL448",
     "vs": [v0, v400, v600, v800],
     "conj": z3.Exists([X, Y], z3.And(
        z3.Or(in_lopen(X, v0, v800), in_lopen(Y, v0, v600)),
        z3.Not(z3.And(in_lopen(X, v0, v600), in_lopen(Y, v0, v400)))))},
    {"id": "ODRL449",
     "vs": [v0, v100, v200, v300, v400, v800],
     "conj": z3.Exists([X, Y, Z], z3.And(
        z3.Or(in_lopen(X, v0, v200), in_lopen(Y, v0, v100), in_lopen(Z, v0, v800)),
        z3.Or(leq(v400, X), leq(v200, Y), leq(v300, Z))))},
    {"id": "ODRL450",
     "vs": [v0, v200, v400, v600, v800],
     "conj": z3.Exists([X, Y], z3.And(
        z3.Or(in_open(X, v0, v600), less(v200, Y)),
        z3.And(less(v400, X), in_open(Y, v0, v800))))},
    {"id": "ODRL451",
     "vs": [v0, v50, v100, v200, v400, v600, v800],
     "conj": z3.ForAll([X, Y, Z], z3.Not(z3.And(
        z3.Or(in_closed(X, v600, v600),
              in_open(Y, v0, v200),
              less(v100, Z)),
        z3.And(less(v800, X), leq(v400, Y), in_lopen(Z, v0, v50)))))},
]

# ============================ LogicalXone ============================

XONE_PROBLEMS = [
    {"id": "ODRL460",
     "vs": [v0, v400, v500, v600],
     "conj": z3.Exists([X, Y], z3.And(
        z3.Or(z3.And(in_lopen(X, v0, v600), z3.Not(in_lopen(Y, v0, v400))),
              z3.And(z3.Not(in_lopen(X, v0, v600)), in_lopen(Y, v0, v400))),
        z3.And(in_lopen(X, v0, v400), leq(v500, Y))))},
    {"id": "ODRL461",
     "vs": [v0, v200, v400, v600],
     "conj": z3.ForAll([X, Y], z3.Not(z3.And(
        z3.Or(z3.And(in_lopen(X, v0, v600), z3.Not(in_lopen(Y, v0, v400))),
              z3.And(z3.Not(in_lopen(X, v0, v600)), in_lopen(Y, v0, v400))),
        z3.And(in_lopen(X, v0, v400), in_lopen(Y, v0, v200)))))},
    {"id": "ODRL462",
     "vs": [v0, v200, v400, v600, v800],
     "conj": z3.Exists([X, Y], z3.And(
        z3.And(leq(v800, X), in_lopen(Y, v0, v200)),
        z3.Or(z3.And(in_lopen(X, v0, v600), z3.Not(in_lopen(Y, v0, v400))),
              z3.And(z3.Not(in_lopen(X, v0, v600)), in_lopen(Y, v0, v400)))))},
    {"id": "ODRL463",
     "vs": [v0, v200, v400, v600],
     "conj": z3.ForAll([X, Y], z3.Not(z3.And(
        z3.And(in_lopen(X, v0, v400), in_lopen(Y, v0, v200)),
        z3.Or(z3.And(in_lopen(X, v0, v600), z3.Not(in_lopen(Y, v0, v400))),
              z3.And(z3.Not(in_lopen(X, v0, v600)), in_lopen(Y, v0, v400))))))},
    {"id": "ODRL464",
     "vs": [v0, v300, v400, v500, v600],
     "conj": z3.Exists([X, Y], z3.And(
        z3.Or(z3.And(in_lopen(X, v0, v400), z3.Not(in_lopen(Y, v0, v300))),
              z3.And(z3.Not(in_lopen(X, v0, v400)), in_lopen(Y, v0, v300))),
        z3.Or(z3.And(in_lopen(X, v0, v600), z3.Not(in_lopen(Y, v0, v500))),
              z3.And(z3.Not(in_lopen(X, v0, v600)), in_lopen(Y, v0, v500)))))},
    {"id": "ODRL465",
     "vs": [v0, v100, v200, v400, v600],
     "conj": z3.ForAll([X, Y, Z], z3.Not(z3.And(
        z3.Or(
            z3.And(in_lopen(X, v0, v600), z3.Not(in_lopen(Y, v0, v400)), z3.Not(in_lopen(Z, v0, v200))),
            z3.And(z3.Not(in_lopen(X, v0, v600)), in_lopen(Y, v0, v400), z3.Not(in_lopen(Z, v0, v200))),
            z3.And(z3.Not(in_lopen(X, v0, v600)), z3.Not(in_lopen(Y, v0, v400)), in_lopen(Z, v0, v200))),
        z3.And(in_lopen(X, v0, v400), in_lopen(Y, v0, v200), in_lopen(Z, v0, v100)))))},
    {"id": "ODRL466",
     "vs": [v0, v200, v300, v400, v500, v600],
     "conj": z3.Exists([X, Y, Z], z3.And(
        z3.Or(
            z3.And(in_lopen(X, v0, v600), z3.Not(in_lopen(Y, v0, v400)), z3.Not(in_lopen(Z, v0, v200))),
            z3.And(z3.Not(in_lopen(X, v0, v600)), in_lopen(Y, v0, v400), z3.Not(in_lopen(Z, v0, v200))),
            z3.And(z3.Not(in_lopen(X, v0, v600)), z3.Not(in_lopen(Y, v0, v400)), in_lopen(Z, v0, v200))),
        z3.And(in_lopen(X, v0, v400), leq(v500, Y), leq(v300, Z))))},
    {"id": "ODRL467",
     "vs": [v0, v200, v400, v600, v800],
     "conj": z3.ForAll([X, Y], z3.Implies(
        z3.And(leq(v800, X), in_lopen(Y, v0, v200)),
        z3.Or(z3.And(in_lopen(X, v0, v600), z3.Not(in_lopen(Y, v0, v400))),
              z3.And(z3.Not(in_lopen(X, v0, v600)), in_lopen(Y, v0, v400)))))},
    {"id": "ODRL468",
     "vs": [v0, v200, v400, v600],
     "conj": z3.Exists([X, Y], z3.And(
        z3.And(in_lopen(X, v0, v400), in_lopen(Y, v0, v200)),
        z3.Not(z3.Or(z3.And(in_lopen(X, v0, v600), z3.Not(in_lopen(Y, v0, v400))),
                      z3.And(z3.Not(in_lopen(X, v0, v600)), in_lopen(Y, v0, v400))))))},
    {"id": "ODRL469",
     "vs": [v0, v200, v400, v600, v800],
     "conj": z3.Exists([X, Y], z3.And(
        z3.Or(z3.And(in_lopen(X, v0, v600), z3.Not(in_lopen(Y, v0, v400))),
              z3.And(z3.Not(in_lopen(X, v0, v600)), in_lopen(Y, v0, v400))),
        z3.Or(leq(v800, X), leq(v200, Y))))},
    {"id": "ODRL470",
     "vs": [v0, v100, v200, v300, v500, v600, v700, v800],
     # xone_A(X) = (X≤100 XOR X∈[500,600])
     # xone_B(X) = (X∈[200,300] XOR X∈[700,800])
     # A-support and B-support are disjoint; conjecture: no X in both
     "conj": z3.ForAll([X], z3.Not(z3.And(
        z3.Or(
            z3.And(in_lopen(X, v0, v100), z3.Not(z3.And(leq(v500, X), in_lopen(X, v0, v600)))),
            z3.And(z3.Not(in_lopen(X, v0, v100)), z3.And(leq(v500, X), in_lopen(X, v0, v600)))),
        z3.Or(
            z3.And(z3.And(leq(v200, X), in_lopen(X, v0, v300)),
                   z3.Not(z3.And(leq(v700, X), in_lopen(X, v0, v800)))),
            z3.And(z3.Not(z3.And(leq(v200, X), in_lopen(X, v0, v300))),
                   z3.And(leq(v700, X), in_lopen(X, v0, v800)))))))},
]


def run(name, problems):
    print(f"\n=== {name} ({len(problems)} problems) ===")
    pass_n = fail_n = unk_n = 0
    fails = []
    for p in problems:
        extras = ord_chain(*p["vs"])
        r = fol_check(extras, p["conj"])
        if r == "Theorem":
            pass_n += 1
            tag = "OK"
        elif r == "Unknown":
            unk_n += 1
            tag = "Z3 timeout (Vampire/E may still close)"
        else:
            fail_n += 1
            tag = "FAIL"
            fails.append(p["id"])
        print(f"  {p['id']:<10s}  {r:<12s}  {tag}")
    print(f"  >> pass={pass_n} unknown={unk_n} fail={fail_n}")
    if fails:
        print(f"  >> failures: {fails}")
    return pass_n, unk_n, fail_n, fails


print("="*78)
print("Audit LogicalOr + LogicalXone under AXIS000 v1.1 + ORD000")
print("(No COMP000 needed - problems encode or/xone directly via boolean ops)")
print("="*78)

p1, u1, f1, fails_or = run("LogicalOr",  OR_PROBLEMS)
p2, u2, f2, fails_xn = run("LogicalXone", XONE_PROBLEMS)

print()
print("="*78)
print(f"Total: pass={p1+p2} unknown={u1+u2} fail={f1+f2}")
print(f"Failures: {fails_or + fails_xn}")
print("="*78)
