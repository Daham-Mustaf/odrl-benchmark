"""
problem_data.py
===============
SingleAxis benchmark problems: ODRL300-314 (15 problems).

Category A: Single-axis interval conflict / compatible / subsumption.
Tests all five ODRL operators (eq, lt, lteq, gt, gteq) and both
discrete (no density) and continuous (density) domains.

Verdict algebra (paper: def:verdict-algebra, def:box-containment):
  Three verdicts only: Conflict / Compatible / Unknown

  relation = "conflict"     — tests interval intersection
    Conflict    ~?[X]: (A(X) & B(X))        Theorem  / unsat
    Compatible   ?[X]: (A(X) & B(X))        Theorem  / sat

  relation = "subsumption"  — tests interval containment
    Compatible  ![X]: (A(X) => B(X))        Theorem  / unsat
    Conflict     ?[X]: (A(X) & ~B(X))       Theorem  / sat

  Unknown — axis unconstrained by one policy; not submitted to prover.

TTL prefix: drk: <http://w3id.org/drk/ontology/>

Include pattern:
  Discrete domain : include('Axioms/AXIS000-0.ax').
  Continuous      : include('Axioms/ORD001-0.ax').
                    include('Axioms/AXIS000-0.ax').
"""

PROBLEMS = [

    # ------------------------------------------------------------------
    # ODRL300 — lteq vs gteq: disjoint → Conflict
    # ------------------------------------------------------------------
    {
        "id":            "ODRL300",
        "subdir":        "SingleAxis",
        "name":          "width ≤ 600 vs width ≥ 800: disjoint intervals",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "width lteq 600 → (0, 600]\n"
            "width gteq 800 → [800, ∞)\n"
            "(0, 600] ∩ [800, ∞) = ∅ → Conflict"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .

drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ;
      odrl:rightOperand "800"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,        axiom, val(v0)).
fof(val_v600,      axiom, val(v600)).
fof(val_v800,      axiom, val(v800)).
fof(ord_v0_v600,   axiom, less(v0, v600)).
fof(ord_v0_v800,   axiom, less(v0, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct,      axiom, $distinct(v0, v600, v800)).
""",
        "fof_conjecture": "~?[X]: (in_lopen(X, v0, v600) & leq(v800, X))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 600.0))
(assert (>= x 800.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL301 — eq vs eq: distinct points → Conflict
    # ------------------------------------------------------------------
    {
        "id":            "ODRL301",
        "subdir":        "SingleAxis",
        "name":          "width = 600 vs width = 800: distinct points",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "width eq 600 → {600}\n"
            "width eq 800 → {800}\n"
            "{600} ∩ {800} = ∅ → Conflict"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .

drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ;
      odrl:rightOperand "800"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,        axiom, val(v0)).
fof(val_v600,      axiom, val(v600)).
fof(val_v800,      axiom, val(v800)).
fof(ord_v0_v600,   axiom, less(v0, v600)).
fof(ord_v0_v800,   axiom, less(v0, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct,      axiom, $distinct(v0, v600, v800)).
""",
        "fof_conjecture": "~?[X]: (in_closed(X, v600, v600) & in_closed(X, v800, v800))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (= x 600.0))
(assert (= x 800.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL302 — lt vs gteq: open/closed boundary → Conflict (density)
    # ------------------------------------------------------------------
    {
        "id":            "ODRL302",
        "subdir":        "SingleAxis",
        "name":          "width < 600 vs width ≥ 600: open/closed boundary",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": True,
        "description": (
            "width lt 600   → (0, 600)\n"
            "width gteq 600 → [600, ∞)\n"
            "(0, 600) ∩ [600, ∞) = ∅ → Conflict\n"
            "Requires density: open interval (0,600) is non-empty."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lt ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .

drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,      axiom, val(v0)).
fof(val_v600,    axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct,    axiom, $distinct(v0, v600)).
""",
        "fof_conjecture": "~?[X]: (in_ropen(X, v0, v600) & leq(v600, X))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (< x 600.0))
(assert (>= x 600.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL303 — gt vs lteq: mirror boundary → Conflict (density)
    # ------------------------------------------------------------------
    {
        "id":            "ODRL303",
        "subdir":        "SingleAxis",
        "name":          "width > 600 vs width ≤ 600: mirror boundary",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": True,
        "description": (
            "width gt 600   → (600, ∞)\n"
            "width lteq 600 → (0, 600]\n"
            "(600, ∞) ∩ (0, 600] = ∅ → Conflict\n"
            "Symmetric to ODRL302. Requires density."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gt ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .

drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,      axiom, val(v0)).
fof(val_v600,    axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct,    axiom, $distinct(v0, v600)).
""",
        "fof_conjecture": "~?[X]: (less(v600, X) & in_lopen(X, v0, v600))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (> x 600.0))
(assert (<= x 600.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL304 — lteq vs gteq: overlapping → Compatible
    # ------------------------------------------------------------------
    {
        "id":            "ODRL304",
        "subdir":        "SingleAxis",
        "name":          "width ≤ 600 vs width ≥ 200: overlapping intervals",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "width lteq 600 → (0, 600]\n"
            "width gteq 200 → [200, ∞)\n"
            "(0, 600] ∩ [200, ∞) ≠ ∅ → Compatible\n"
            "Witness: X = 400."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .

drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ;
      odrl:rightOperand "200"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,        axiom, val(v0)).
fof(val_v200,      axiom, val(v200)).
fof(val_v600,      axiom, val(v600)).
fof(ord_v0_v200,   axiom, less(v0, v200)).
fof(ord_v0_v600,   axiom, less(v0, v600)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(distinct,      axiom, $distinct(v0, v200, v600)).
""",
        "fof_conjecture": "?[X]: (in_lopen(X, v0, v600) & leq(v200, X))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 600.0))
(assert (>= x 200.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL305 — lteq touch gteq: touching at boundary → Compatible
    # ------------------------------------------------------------------
    {
        "id":            "ODRL305",
        "subdir":        "SingleAxis",
        "name":          "width ≤ 600 vs width ≥ 600: touching at 600",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "width lteq 600 → (0, 600]\n"
            "width gteq 600 → [600, ∞)\n"
            "(0, 600] ∩ [600, ∞) = {600} ≠ ∅ → Compatible\n"
            "Witness: X = 600. Tests closed-closed boundary touch."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .

drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,      axiom, val(v0)).
fof(val_v600,    axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct,    axiom, $distinct(v0, v600)).
""",
        "fof_conjecture": "?[X]: (in_lopen(X, v0, v600) & leq(v600, X))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 600.0))
(assert (>= x 600.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL306 — eq vs eq same point → Compatible
    # ------------------------------------------------------------------
    {
        "id":            "ODRL306",
        "subdir":        "SingleAxis",
        "name":          "width = 600 vs width = 600: identical points",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "width eq 600 → {600}\n"
            "width eq 600 → {600}\n"
            "{600} ∩ {600} = {600} ≠ ∅ → Compatible"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .

drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,      axiom, val(v0)).
fof(val_v600,    axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct,    axiom, $distinct(v0, v600)).
""",
        "fof_conjecture": "?[X]: (in_closed(X, v600, v600) & in_closed(X, v600, v600))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (= x 600.0))
(assert (= x 600.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL307 — eq vs lteq: point inside interval → Compatible
    # ------------------------------------------------------------------
    {
        "id":            "ODRL307",
        "subdir":        "SingleAxis",
        "name":          "width = 400 vs width ≤ 600: point inside interval",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "width eq 400   → {400}\n"
            "width lteq 600 → (0, 600]\n"
            "{400} ∩ (0, 600] = {400} ≠ ∅ → Compatible"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ;
      odrl:rightOperand "400"^^xsd:decimal ] ] .

drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,        axiom, val(v0)).
fof(val_v400,      axiom, val(v400)).
fof(val_v600,      axiom, val(v600)).
fof(ord_v0_v400,   axiom, less(v0, v400)).
fof(ord_v0_v600,   axiom, less(v0, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct,      axiom, $distinct(v0, v400, v600)).
""",
        "fof_conjecture": "?[X]: (in_closed(X, v400, v400) & in_lopen(X, v0, v600))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (= x 400.0))
(assert (<= x 600.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL308 — gt vs lt: open overlap → Compatible (density)
    # ------------------------------------------------------------------
    {
        "id":            "ODRL308",
        "subdir":        "SingleAxis",
        "name":          "width > 200 vs width < 800: open overlap",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "needs_density": True,
        "description": (
            "width gt 200 → (200, ∞)\n"
            "width lt 800 → (0, 800)\n"
            "(200, ∞) ∩ (0, 800) = (200, 800) ≠ ∅ → Compatible\n"
            "Requires density: witness lies in open interval."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gt ;
      odrl:rightOperand "200"^^xsd:decimal ] ] .

drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lt ;
      odrl:rightOperand "800"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,        axiom, val(v0)).
fof(val_v200,      axiom, val(v200)).
fof(val_v800,      axiom, val(v800)).
fof(ord_v0_v200,   axiom, less(v0, v200)).
fof(ord_v0_v800,   axiom, less(v0, v800)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(distinct,      axiom, $distinct(v0, v200, v800)).
""",
        "fof_conjecture": "?[X]: (less(v200, X) & in_open(X, v0, v800))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (> x 200.0))
(assert (< x 800.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL309 — lteq ⊆ lteq: tighter bound subsumes wider → Compatible
    # ------------------------------------------------------------------
    {
        "id":            "ODRL309",
        "subdir":        "SingleAxis",
        "name":          "(0,600] ⊆ (0,1200]: tighter bound subsumes wider",
        "relation":      "subsumption",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "width lteq 600  → (0, 600]\n"
            "width lteq 1200 → (0, 1200]\n"
            "(0, 600] ⊆ (0, 1200] → Compatible (subsumption)\n"
            "SMT: ∄ x ∈ A s.t. x ∉ B → unsat."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .

drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "1200"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,         axiom, val(v0)).
fof(val_v600,       axiom, val(v600)).
fof(val_v1200,      axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v0_v1200,   axiom, less(v0, v1200)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct,       axiom, $distinct(v0, v600, v1200)).
""",
        "fof_conjecture": "![X]: (in_lopen(X, v0, v600) => in_lopen(X, v0, v1200))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 600.0))
(assert (not (<= x 1200.0)))""",
    },

    # ------------------------------------------------------------------
    # ODRL310 — lteq ⊄ lteq: wider does not subsume → Conflict
    # ------------------------------------------------------------------
    {
        "id":            "ODRL310",
        "subdir":        "SingleAxis",
        "name":          "(0,1200] ⊄ (0,600]: wider does not subsume tighter",
        "relation":      "subsumption",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "width lteq 1200 → (0, 1200]\n"
            "width lteq 600  → (0, 600]\n"
            "(0, 1200] ⊄ (0, 600] → Conflict (subsumption fails)\n"
            "Counterexample: X = 800 ∈ A, X ∉ B."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "1200"^^xsd:decimal ] ] .

drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,         axiom, val(v0)).
fof(val_v600,       axiom, val(v600)).
fof(val_v1200,      axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v0_v1200,   axiom, less(v0, v1200)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct,       axiom, $distinct(v0, v600, v1200)).
""",
        "fof_conjecture": "?[X]: (in_lopen(X, v0, v1200) & ~in_lopen(X, v0, v600))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 1200.0))
(assert (not (<= x 600.0)))""",
    },

    # ------------------------------------------------------------------
    # ODRL311 — gteq ⊆ gteq: higher lower-bound subsumes → Compatible
    # ------------------------------------------------------------------
    {
        "id":            "ODRL311",
        "subdir":        "SingleAxis",
        "name":          "[800,∞) ⊆ [400,∞): higher lower-bound subsumes",
        "relation":      "subsumption",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "width gteq 800 → [800, ∞)\n"
            "width gteq 400 → [400, ∞)\n"
            "[800, ∞) ⊆ [400, ∞) → Compatible (subsumption)"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ;
      odrl:rightOperand "800"^^xsd:decimal ] ] .

drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ;
      odrl:rightOperand "400"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,        axiom, val(v0)).
fof(val_v400,      axiom, val(v400)).
fof(val_v800,      axiom, val(v800)).
fof(ord_v0_v400,   axiom, less(v0, v400)).
fof(ord_v0_v800,   axiom, less(v0, v800)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(distinct,      axiom, $distinct(v0, v400, v800)).
""",
        "fof_conjecture": "![X]: (leq(v800, X) => leq(v400, X))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (>= x 800.0))
(assert (not (>= x 400.0)))""",
    },

    # ------------------------------------------------------------------
    # ODRL312 — eq ⊆ lteq: point inside interval → Compatible
    # ------------------------------------------------------------------
    {
        "id":            "ODRL312",
        "subdir":        "SingleAxis",
        "name":          "{400} ⊆ (0,600]: point inside interval",
        "relation":      "subsumption",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "width eq 400   → {400}\n"
            "width lteq 600 → (0, 600]\n"
            "{400} ⊆ (0, 600] → Compatible (subsumption)"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ;
      odrl:rightOperand "400"^^xsd:decimal ] ] .

drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,        axiom, val(v0)).
fof(val_v400,      axiom, val(v400)).
fof(val_v600,      axiom, val(v600)).
fof(ord_v0_v400,   axiom, less(v0, v400)).
fof(ord_v0_v600,   axiom, less(v0, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct,      axiom, $distinct(v0, v400, v600)).
""",
        "fof_conjecture": "![X]: (in_closed(X, v400, v400) => in_lopen(X, v0, v600))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (= x 400.0))
(assert (not (<= x 600.0)))""",
    },

    # ------------------------------------------------------------------
    # ODRL313 — BSB running example: width conflict → Conflict
    # ------------------------------------------------------------------
    {
        "id":            "ODRL313",
        "subdir":        "SingleAxis",
        "name":          "BSB running example: width ≤ 600 vs width ≥ 1200",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "BSB license: width lteq 600  → (0, 600]\n"
            "Museum request: width gteq 1200 → [1200, ∞)\n"
            "(0, 600] ∩ [1200, ∞) = ∅ → Conflict\n"
            "Paper running example (Datenraum Kultur / BSB scenario)."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyBSB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .

drk:policyMuseum a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ;
      odrl:rightOperand "1200"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,         axiom, val(v0)).
fof(val_v600,       axiom, val(v600)).
fof(val_v1200,      axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v0_v1200,   axiom, less(v0, v1200)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct,       axiom, $distinct(v0, v600, v1200)).
""",
        "fof_conjecture": "~?[X]: (in_lopen(X, v0, v600) & leq(v1200, X))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 600.0))
(assert (>= x 1200.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL314 — BSB running example: height compatible → Compatible
    # ------------------------------------------------------------------
    {
        "id":            "ODRL314",
        "subdir":        "SingleAxis",
        "name":          "BSB running example: height ≤ 600 vs height ≥ 400",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "BSB license: height lteq 600  → (0, 600]\n"
            "Museum request: height gteq 400 → [400, ∞)\n"
            "(0, 600] ∩ [400, ∞) = [400, 600] ≠ ∅ → Compatible\n"
            "Paper running example: height axis is compatible."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyBSB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeHeight ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .

drk:policyMuseum a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeHeight ;
      odrl:operator odrl:gteq ;
      odrl:rightOperand "400"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,        axiom, val(v0)).
fof(val_v400,      axiom, val(v400)).
fof(val_v600,      axiom, val(v600)).
fof(ord_v0_v400,   axiom, less(v0, v400)).
fof(ord_v0_v600,   axiom, less(v0, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct,      axiom, $distinct(v0, v400, v600)).
""",
        "fof_conjecture": "?[X]: (in_lopen(X, v0, v600) & leq(v400, X))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 600.0))
(assert (>= x 400.0))""",
    },

]