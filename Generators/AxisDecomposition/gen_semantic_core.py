"""
gen_semantic_core.py
====================
SemanticCore tier (14 problems, ODRL500-513).

Covers paper formal results not in other tiers:
  lem:totality      -- direct non-emptiness of each operator denotation (5)
  lem:normalisation -- same-axis constraint intersection (2)
  thm:projection    -- Cartesian product membership (1)
  thm:aabb          -- all 4 bounded interval shapes (4)
  def:profile       -- well-formedness violation rejection (2)

Output: Problems/ODRL/AxisDecomposition/SemanticCore/
"""
import argparse
import os
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

from header import problem_header

AXIS_INCLUDE    = "include('Axioms/ORD000-0.ax').\ninclude('Axioms/AXIS000-0.ax').\n"
DENSITY_INCLUDE = "include('Axioms/ORD000-0.ax').\ninclude('Axioms/ORD001-0.ax').\ninclude('Axioms/AXIS000-0.ax').\n"

DECLS_2 = """\
fof(val_v0,        axiom, val(v0)).
fof(val_v200,      axiom, val(v200)).
fof(val_v600,      axiom, val(v600)).
fof(ord_v0_v200,   axiom, less(v0,   v200)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(distinct,      axiom, $distinct(v0, v200, v600)).
"""

DECLS_3 = """\
fof(val_v0,        axiom, val(v0)).
fof(val_v200,      axiom, val(v200)).
fof(val_v400,      axiom, val(v400)).
fof(val_v600,      axiom, val(v600)).
fof(ord_v0_v200,   axiom, less(v0,   v200)).
fof(ord_v0_v400,   axiom, less(v0,   v400)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct,      axiom, $distinct(v0, v200, v400, v600)).
"""

TTL_TEMPLATE = """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator {op} ;
      odrl:rightOperand "{val}"^^xsd:decimal ] ] ."""


PROBLEMS = [
    # ── lem:totality (5) ───────────────────────────────────────────
    {"id": "ODRL500", "relation": "conflict",
     "name": "lem:totality — lteq denotation is non-empty",
     "verdict": "Compatible", "density": False, "decls": DECLS_2,
     "conjecture": "?[X]: in_lopen(X, v0, v600)",
     "smt_vars": "(declare-const x Real)",
     "smt": "(assert (> x 0.0))\n(assert (<= x 600.0))", "smt_sat": "sat",
     "ttl": TTL_TEMPLATE.format(op="odrl:lteq", val="600")},
    {"id": "ODRL501", "relation": "conflict",
     "name": "lem:totality — gteq denotation is non-empty",
     "verdict": "Compatible", "density": False, "decls": DECLS_2,
     "conjecture": "?[X]: leq(v200, X)",
     "smt_vars": "(declare-const x Real)",
     "smt": "(assert (>= x 200.0))", "smt_sat": "sat",
     "ttl": TTL_TEMPLATE.format(op="odrl:gteq", val="200")},
    {"id": "ODRL502", "relation": "conflict",
     "name": "lem:totality — lt denotation is non-empty",
     "verdict": "Compatible", "density": False, "decls": DECLS_2,
     "conjecture": "?[X]: in_open(X, v0, v600)",
     "smt_vars": "(declare-const x Real)",
     "smt": "(assert (> x 0.0))\n(assert (< x 600.0))", "smt_sat": "sat",
     "ttl": TTL_TEMPLATE.format(op="odrl:lt", val="600")},
    {"id": "ODRL503", "relation": "conflict",
     "name": "lem:totality — gt denotation is non-empty",
     "verdict": "Compatible", "density": False, "decls": DECLS_2,
     "conjecture": "?[X]: less(v200, X)",
     "smt_vars": "(declare-const x Real)",
     "smt": "(assert (> x 200.0))", "smt_sat": "sat",
     "ttl": TTL_TEMPLATE.format(op="odrl:gt", val="200")},
    {"id": "ODRL504", "relation": "conflict",
     "name": "lem:totality — eq denotation is non-empty",
     "verdict": "Compatible", "density": False, "decls": DECLS_2,
     "conjecture": "?[X]: in_closed(X, v200, v200)",
     "smt_vars": "(declare-const x Real)",
     "smt": "(assert (= x 200.0))", "smt_sat": "sat",
     "ttl": TTL_TEMPLATE.format(op="odrl:eq", val="200")},

    # ── lem:normalisation (2) ──────────────────────────────────────
    {"id": "ODRL505", "relation": "conflict",
     "name": "lem:normalisation — same-axis lteq intersection reduces to tighter bound",
     "verdict": "Compatible", "density": False, "decls": DECLS_3,
     "conjecture": "?[X]: (in_lopen(X, v0, v400) & in_lopen(X, v0, v600))",
     "smt_vars": "(declare-const x Real)",
     "smt": "(assert (> x 0.0))\n(assert (<= x 400.0))\n(assert (<= x 600.0))", "smt_sat": "sat",
     "ttl": TTL_TEMPLATE.format(op="odrl:lteq", val="400")},
    {"id": "ODRL506", "relation": "conflict",
     "name": "lem:normalisation — conflicting same-axis constraints yield empty denotation",
     "verdict": "Conflict", "density": False, "decls": DECLS_3,
     "conjecture": "![X]: ~(in_lopen(X, v0, v200) & leq(v400, X))",
     "smt_vars": "(declare-const x Real)",
     "smt": "(assert (> x 0.0))\n(assert (<= x 200.0))\n(assert (>= x 400.0))", "smt_sat": "unsat",
     "ttl": TTL_TEMPLATE.format(op="odrl:lteq", val="200")},

    # ── thm:projection (1) ─────────────────────────────────────────
    {"id": "ODRL507", "relation": "verdict_algebra",
     "name": "thm:projection — 2D box membership iff per-axis membership holds",
     "verdict": "Compatible", "density": False, "decls": DECLS_3,
     "conjecture": "![X,Y]: ((in_lopen(X, v0, v600) & in_lopen(Y, v0, v400)) => (in_lopen(X, v0, v600) & in_lopen(Y, v0, v400)))",
     "smt_vars": "(declare-const x Real)\n(declare-const y Real)",
     "smt": "(assert (> x 0.0))\n(assert (<= x 600.0))\n(assert (> y 0.0))\n(assert (<= y 400.0))\n(assert (not (and (<= x 600.0) (<= y 400.0))))",
     "smt_sat": "unsat",
     "ttl": TTL_TEMPLATE.format(op="odrl:lteq", val="600")},

    # ── thm:aabb 4 cases ───────────────────────────────────────────
    {"id": "ODRL508", "relation": "conflict",
     "name": "thm:aabb — closed bounded interval is non-empty",
     "verdict": "Compatible", "density": False, "decls": DECLS_3,
     "conjecture": "?[X]: (leq(v200, X) & in_lopen(X, v0, v400))",
     "smt_vars": "(declare-const x Real)",
     "smt": "(assert (>= x 200.0))\n(assert (<= x 400.0))", "smt_sat": "sat",
     "ttl": TTL_TEMPLATE.format(op="odrl:gteq", val="200")},
    {"id": "ODRL509", "relation": "conflict",
     "name": "thm:aabb — half-open right-closed (l,u] is non-empty",
     "verdict": "Compatible", "density": False, "decls": DECLS_3,
     "conjecture": "?[X]: (less(v200, X) & in_lopen(X, v0, v400))",
     "smt_vars": "(declare-const x Real)",
     "smt": "(assert (> x 200.0))\n(assert (<= x 400.0))", "smt_sat": "sat",
     "ttl": TTL_TEMPLATE.format(op="odrl:gt", val="200")},
    {"id": "ODRL510", "relation": "conflict",
     "name": "thm:aabb — half-open left-closed [l,u) is non-empty",
     "verdict": "Compatible", "density": False, "decls": DECLS_3,
     "conjecture": "?[X]: (leq(v200, X) & in_open(X, v0, v400))",
     "smt_vars": "(declare-const x Real)",
     "smt": "(assert (>= x 200.0))\n(assert (< x 400.0))", "smt_sat": "sat",
     "ttl": TTL_TEMPLATE.format(op="odrl:gteq", val="200")},
    {"id": "ODRL511", "relation": "conflict",
     "name": "thm:aabb — open bounded interval is non-empty (density)",
     "verdict": "Compatible", "density": True, "decls": DECLS_3,
     "conjecture": "?[X]: (less(v200, X) & in_open(X, v0, v400))",
     "smt_vars": "(declare-const x Real)",
     "smt": "(assert (> x 200.0))\n(assert (< x 400.0))", "smt_sat": "sat",
     "ttl": TTL_TEMPLATE.format(op="odrl:gt", val="200")},

    # ── def:profile (2) ─────────────────────────────────────────────
    {"id": "ODRL512", "relation": "verdict_algebra",
     "name": "def:profile (ii) — lt at domain lower bound yields empty denotation",
     "verdict": "Conflict", "density": False, "decls": DECLS_2,
     "conjecture": "![X]: ~in_open(X, v0, v0)",
     "smt_vars": "(declare-const x Real)",
     "smt": "(assert (> x 0.0))\n(assert (< x 0.0))", "smt_sat": "unsat",
     "ttl": TTL_TEMPLATE.format(op="odrl:lt", val="0")},
    {"id": "ODRL513", "relation": "verdict_algebra",
     "name": "def:profile (iii) — gt at effective upper bound yields empty denotation",
     "verdict": "Conflict", "density": False,
     "decls": ("fof(val_v0,      axiom, val(v0)).\n"
               "fof(val_v600,    axiom, val(v600)).\n"
               "fof(ord_v0_v600, axiom, less(v0, v600)).\n"
               "fof(distinct,    axiom, $distinct(v0, v600)).\n"),
     "conjecture": "![X]: ~(less(v600, X) & in_lopen(X, v0, v600))",
     "smt_vars": "(declare-const x Real)",
     "smt": "(assert (> x 600.0))\n(assert (<= x 600.0))", "smt_sat": "unsat",
     "ttl": TTL_TEMPLATE.format(op="odrl:gt", val="600")},
]


for p in PROBLEMS:
    p["status_fof"] = "Theorem"


def write_fof(p, out_dir):
    inc = DENSITY_INCLUDE if p["density"] else AXIS_INCLUDE
    hdr = problem_header(p, "axis")
    body = (
        hdr + inc
        + "% ─── Named constants and ordering "
        + "─" * 37 + "\n"
        + p["decls"]
        + "% ─── Conjecture "
        + "─" * 52 + "\n"
        + f"fof({p['id'].lower()}, conjecture,\n    {p['conjecture']}).\n"
        + "%--------------------------------------------------------------------------\n"
    )
    path = out_dir / f"{p['id']}-1.p"
    path.write_text(body)


def write_smt2(p, out_dir):
    lines = [
        f"; {p['id']} — {p['name']}",
        "(set-logic QF_LRA)",
        p["smt_vars"], p["smt"], "(check-sat)",
    ]
    (out_dir / f"{p['id']}-1.smt2").write_text("\n".join(lines) + "\n")


def write_ttl(p, policies_dir):
    (policies_dir / f"{p['id']}-policy.ttl").write_text(p["ttl"].strip() + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[2])
    ap.add_argument("--out-dir", default="Problems/ODRL/AxisDecomposition")
    args = ap.parse_args()

    out_root = Path(args.out_dir).resolve()
    semcore_dir = out_root / "SemanticCore"
    policies_dir = out_root / "Policies"

    semcore_dir.mkdir(parents=True, exist_ok=True)
    policies_dir.mkdir(parents=True, exist_ok=True)

    print(f"── SemanticCore ({len(PROBLEMS)} problems) ──", file=sys.stderr)
    for p in PROBLEMS:
        tag = " [density]" if p["density"] else ""
        print(f"  {p['id']}  {p['verdict']:<12}{tag}", file=sys.stderr)
        write_fof(p, semcore_dir)
        write_smt2(p, semcore_dir)
        write_ttl(p, policies_dir)

    print(f"\nWritten: {len(PROBLEMS)} .p  |  {len(PROBLEMS)} .smt2  |  "
          f"{len(PROBLEMS)} .ttl", file=sys.stderr)
    print(f"Output: {semcore_dir}", file=sys.stderr)


if __name__ == "__main__":
    main()
