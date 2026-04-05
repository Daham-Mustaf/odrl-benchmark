"""
problem_data_xone.py
====================
LogicalXone benchmark problems: ODRL460-469 (10 problems).

Category I: odrl:xone (exclusive-or) logical constraint composition.
xone(A,B) = (A & ~B) | (~A & B)  — exactly one branch is true.
xone3(A,B,C) = (A&~B&~C) | (~A&B&~C) | (~A&~B&C)

verdictXone = Compatible if ∃ branch pair with non-empty intersection
            = Conflict   if ∀ branch pairs all intersections empty
            = Unknown    otherwise

TTL: odrl:xone for exclusive-or constraints [ODRL 2.2 §4.3].
SMT2: xone(A,B) encoded as (or (and A (not B)) (and (not A) B)).
TTL prefix: drk: <http://w3id.org/drk/ontology/>
"""

PROBLEMS = [

    # ──────────────────────────────────────────────────────────────────
    # ODRL460 — xone-A vs and-B: one branch compatible → Compatible
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL460",
        "subdir":        "LogicalXone",
        "name":          "xone-A vs and-B: one branch compatible → Compatible",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "PolicyA: xone(width lteq 600, height lteq 400) — exactly one\n"
            "PolicyB: and(width lteq 400, height gteq 500)\n"
            "Branch (A_x & ~A_y): X∈(0,400]⊆(0,600] ✓, Y≥500>400 so Y∉(0,400] ✓\n"
            "Witness: X=v400, Y=v500. verdictXone=Compatible\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:xone (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
      )
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "500"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v400, axiom, val(v400)).
fof(val_v500, axiom, val(v500)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v500, axiom, less(v0, v500)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v400_v500, axiom, less(v400, v500)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v500_v600, axiom, less(v500, v600)).
fof(distinct, axiom, $distinct(v0, v400, v500, v600)).
""",
        "fof_conjecture": (
            "?[X,Y]: (((in_lopen(X, v0, v600) & ~(in_lopen(Y, v0, v400))) |\n"
            "              (~(in_lopen(X, v0, v600)) & in_lopen(Y, v0, v400))) &\n"
            "          (in_lopen(X, v0, v400) & leq(v500, Y)))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (> y 0.0))
(assert (or (and (<= x 600.0) (not (<= y 400.0)))
            (and (not (<= x 600.0)) (<= y 400.0))))
(assert (<= x 400.0))
(assert (>= y 500.0))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL461 — xone-A vs and-B: B implies both A-branches → xone never holds → Conflict
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL461",
        "subdir":        "LogicalXone",
        "name":          "xone-A vs and-B: B implies both A-branches → xone never holds → Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "PolicyA: xone(width lteq 600, height lteq 400)\n"
            "PolicyB: and(width lteq 400, height lteq 200)\n"
            "For B: X∈(0,400]⊆(0,600] → A_x always true\n"
            "For B: Y∈(0,200]⊆(0,400] → A_y always true\n"
            "Both simultaneously true → xone fails → Conflict\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:xone (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
      )
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v200, axiom, val(v200)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct, axiom, $distinct(v0, v200, v400, v600)).
""",
        "fof_conjecture": (
            "~?[X,Y]: (((in_lopen(X, v0, v600) & ~(in_lopen(Y, v0, v400))) |\n"
            "              (~(in_lopen(X, v0, v600)) & in_lopen(Y, v0, v400))) &\n"
            "          (in_lopen(X, v0, v400) & in_lopen(Y, v0, v200)))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (> y 0.0))
(assert (or (and (<= x 600.0) (not (<= y 400.0)))
            (and (not (<= x 600.0)) (<= y 400.0))))
(assert (<= x 400.0))
(assert (<= y 200.0))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL462 — and-B vs xone-A: ~A_x & A_y branch matches → Compatible
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL462",
        "subdir":        "LogicalXone",
        "name":          "and-B vs xone-A: ~A_x & A_y branch matches → Compatible",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "PolicyA: xone(width lteq 600, height lteq 400)\n"
            "PolicyB: and(width gteq 800, height lteq 200)\n"
            "Branch (~A_x & A_y): X≥800>600 → X∉(0,600] ✓, Y∈(0,200]⊆(0,400] → A_y ✓\n"
            "Witness: X=v800, Y=v200. verdictXone=Compatible\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:xone (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
      )
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "800"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v200, axiom, val(v200)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v200, v400, v600, v800)).
""",
        "fof_conjecture": (
            "?[X,Y]: ((leq(v800, X) & in_lopen(Y, v0, v200)) &\n"
            "          ((in_lopen(X, v0, v600) & ~(in_lopen(Y, v0, v400))) |\n"
            "              (~(in_lopen(X, v0, v600)) & in_lopen(Y, v0, v400))))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (> y 0.0))
(assert (>= x 800.0))
(assert (<= y 200.0))
(assert (or (and (<= x 600.0) (not (<= y 400.0)))
            (and (not (<= x 600.0)) (<= y 400.0))))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL463 — and-B vs xone-A: B implies both A-branches → Conflict
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL463",
        "subdir":        "LogicalXone",
        "name":          "and-B vs xone-A: B implies both A-branches → Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "PolicyA: xone(width lteq 600, height lteq 400)\n"
            "PolicyB: and(width lteq 400, height lteq 200)\n"
            "For B: X∈(0,400]⊆(0,600] → A_x true; Y∈(0,200]⊆(0,400] → A_y true\n"
            "Both true → xone fails → Conflict\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:xone (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
      )
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v200, axiom, val(v200)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct, axiom, $distinct(v0, v200, v400, v600)).
""",
        "fof_conjecture": (
            "~?[X,Y]: ((in_lopen(X, v0, v400) & in_lopen(Y, v0, v200)) &\n"
            "          ((in_lopen(X, v0, v600) & ~(in_lopen(Y, v0, v400))) |\n"
            "              (~(in_lopen(X, v0, v600)) & in_lopen(Y, v0, v400))))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (> y 0.0))
(assert (<= x 400.0))
(assert (<= y 200.0))
(assert (or (and (<= x 600.0) (not (<= y 400.0)))
            (and (not (<= x 600.0)) (<= y 400.0))))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL464 — xone-A vs xone-B: cross-branch pair overlaps → Compatible
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL464",
        "subdir":        "LogicalXone",
        "name":          "xone-A vs xone-B: cross-branch pair overlaps → Compatible",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "PolicyA: xone(width lteq 400, height lteq 300)\n"
            "PolicyB: xone(width lteq 600, height lteq 500)\n"
            "Branch (A_x&~A_y) & (B_x&~B_y): X∈(0,400], Y>500\n"
            "  X∈(0,400]⊆(0,600]→B_x✓, Y>500→Y∉(0,300]✓ and Y∉(0,500]✓\n"
            "Witness: X=v300, Y=v600. verdictXone=Compatible\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:xone (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "300"^^xsd:decimal ]
      )
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:xone (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "500"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v300, axiom, val(v300)).
fof(val_v400, axiom, val(v400)).
fof(val_v500, axiom, val(v500)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v300, axiom, less(v0, v300)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v500, axiom, less(v0, v500)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v300_v400, axiom, less(v300, v400)).
fof(ord_v300_v500, axiom, less(v300, v500)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v400_v500, axiom, less(v400, v500)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v500_v600, axiom, less(v500, v600)).
fof(distinct, axiom, $distinct(v0, v300, v400, v500, v600)).
""",
        "fof_conjecture": (
            "?[X,Y]: (((in_lopen(X, v0, v400) & ~(in_lopen(Y, v0, v300))) |\n"
            "              (~(in_lopen(X, v0, v400)) & in_lopen(Y, v0, v300))) &\n"
            "          ((in_lopen(X, v0, v600) & ~(in_lopen(Y, v0, v500))) |\n"
            "              (~(in_lopen(X, v0, v600)) & in_lopen(Y, v0, v500))))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (> y 0.0))
(assert (or (and (<= x 400.0) (not (<= y 300.0)))
            (and (not (<= x 400.0)) (<= y 300.0))))
(assert (or (and (<= x 600.0) (not (<= y 500.0)))
            (and (not (<= x 600.0)) (<= y 500.0))))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL465 — 3-branch xone-A vs and-B: B implies 2+ branches → Conflict
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL465",
        "subdir":        "LogicalXone",
        "name":          "3-branch xone-A vs and-B: B implies 2+ branches → Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "PolicyA: xone3(width lteq 600, height lteq 400, depth lteq 200)\n"
            "PolicyB: and(width lteq 400, height lteq 200, depth lteq 100)\n"
            "For B: X∈(0,400]⊆(0,600]→A_x true; Y∈(0,200]⊆(0,400]→A_y true\n"
            "Two branches simultaneously true → xone3 fails → Conflict\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:xone (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
      )
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "100"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v100, axiom, val(v100)).
fof(val_v200, axiom, val(v200)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v100, axiom, less(v0, v100)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v400, axiom, less(v100, v400)).
fof(ord_v100_v600, axiom, less(v100, v600)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct, axiom, $distinct(v0, v100, v200, v400, v600)).
""",
        "fof_conjecture": (
            "~?[X,Y,Z]: (((in_lopen(X, v0, v600) & ~(in_lopen(Y, v0, v400)) & ~(in_lopen(Z, v0, v200))) |\n"
            "              (~(in_lopen(X, v0, v600)) & in_lopen(Y, v0, v400) & ~(in_lopen(Z, v0, v200))) |\n"
            "              (~(in_lopen(X, v0, v600)) & ~(in_lopen(Y, v0, v400)) & in_lopen(Z, v0, v200))) &\n"
            "          (in_lopen(X, v0, v400) & in_lopen(Y, v0, v200) & in_lopen(Z, v0, v100)))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (> y 0.0)) (assert (> z 0.0))
(assert (or (and (<= x 600.0) (not (<= y 400.0)) (not (<= z 200.0)))
            (and (not (<= x 600.0)) (<= y 400.0) (not (<= z 200.0)))
            (and (not (<= x 600.0)) (not (<= y 400.0)) (<= z 200.0))))
(assert (<= x 400.0))
(assert (<= y 200.0))
(assert (<= z 100.0))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL466 — 3-branch xone-A vs and-B: A_x branch alone compatible → Compatible
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL466",
        "subdir":        "LogicalXone",
        "name":          "3-branch xone-A vs and-B: A_x branch alone compatible → Compatible",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "PolicyA: xone3(width lteq 600, height lteq 400, depth lteq 200)\n"
            "PolicyB: and(width lteq 400, height gteq 500, depth gteq 300)\n"
            "Branch (A_x&~A_y&~A_z): X∈(0,400], Y≥500>400→Y∉(0,400]✓, Z≥300>200→Z∉(0,200]✓\n"
            "Witness: X=v300, Y=v500, Z=v300. verdictXone=Compatible\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:xone (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
      )
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "500"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "300"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v200, axiom, val(v200)).
fof(val_v300, axiom, val(v300)).
fof(val_v400, axiom, val(v400)).
fof(val_v500, axiom, val(v500)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v300, axiom, less(v0, v300)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v500, axiom, less(v0, v500)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v200_v300, axiom, less(v200, v300)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v500, axiom, less(v200, v500)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v300_v400, axiom, less(v300, v400)).
fof(ord_v300_v500, axiom, less(v300, v500)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v400_v500, axiom, less(v400, v500)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v500_v600, axiom, less(v500, v600)).
fof(distinct, axiom, $distinct(v0, v200, v300, v400, v500, v600)).
""",
        "fof_conjecture": (
            "?[X,Y,Z]: (((in_lopen(X, v0, v600) & ~(in_lopen(Y, v0, v400)) & ~(in_lopen(Z, v0, v200))) |\n"
            "              (~(in_lopen(X, v0, v600)) & in_lopen(Y, v0, v400) & ~(in_lopen(Z, v0, v200))) |\n"
            "              (~(in_lopen(X, v0, v600)) & ~(in_lopen(Y, v0, v400)) & in_lopen(Z, v0, v200))) &\n"
            "          (in_lopen(X, v0, v400) & leq(v500, Y) & leq(v300, Z)))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (> y 0.0)) (assert (> z 0.0))
(assert (or (and (<= x 600.0) (not (<= y 400.0)) (not (<= z 200.0)))
            (and (not (<= x 600.0)) (<= y 400.0) (not (<= z 200.0)))
            (and (not (<= x 600.0)) (not (<= y 400.0)) (<= z 200.0))))
(assert (<= x 400.0))
(assert (>= y 500.0))
(assert (>= z 300.0))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL467 — or-subsumption: and-A ⊆ xone-B → Compatible
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL467",
        "subdir":        "LogicalXone",
        "name":          "or-subsumption: and-A ⊆ xone-B → Compatible",
        "relation":      "subsumption",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "PolicyA: and(width gteq 800, height lteq 200)\n"
            "PolicyB: xone(width lteq 600, height lteq 400)\n"
            "For A: X≥800>600 → X∉(0,600] → ~B_x; Y∈(0,200]⊆(0,400] → B_y\n"
            "Exactly one B-branch true → xone holds ✓ [~B_x & B_y]\n"
            "or-subsumption Compatible\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "800"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
      )
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:xone (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v200, axiom, val(v200)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v200, v400, v600, v800)).
""",
        "fof_conjecture": (
            "![X,Y]: ((leq(v800, X) & in_lopen(Y, v0, v200)) =>\n"
            "          ((in_lopen(X, v0, v600) & ~(in_lopen(Y, v0, v400))) |\n"
            "              (~(in_lopen(X, v0, v600)) & in_lopen(Y, v0, v400))))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (> y 0.0))
(assert (>= x 800.0))
(assert (<= y 200.0))
(assert (not (or (and (<= x 600.0) (not (<= y 400.0)))
                 (and (not (<= x 600.0)) (<= y 400.0)))))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL468 — xone-subsumption Conflict: A_and ⊄ B_xone — both branches simultaneously true
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL468",
        "subdir":        "LogicalXone",
        "name":          "xone-subsumption Conflict: A_and ⊄ B_xone — both branches simultaneously true",
        "relation":      "subsumption",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "PolicyA: and(width lteq 400, height lteq 200)\n"
            "PolicyB: xone(width lteq 600, height lteq 400)\n"
            "For A: X∈(0,400]⊆(0,600]→B_x true AND Y∈(0,200]⊆(0,400]→B_y true\n"
            "Both B-branches true → xone fails → ~xone → escape witness exists\n"
            "Conflict: A ⊄ B_xone\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
      )
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:xone (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v200, axiom, val(v200)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct, axiom, $distinct(v0, v200, v400, v600)).
""",
        "fof_conjecture": (
            "?[X,Y]: ((in_lopen(X, v0, v400) & in_lopen(Y, v0, v200)) &\n"
            "          ~((in_lopen(X, v0, v600) & ~(in_lopen(Y, v0, v400))) |\n"
            "              (~(in_lopen(X, v0, v600)) & in_lopen(Y, v0, v400))))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (> y 0.0))
(assert (<= x 400.0))
(assert (<= y 200.0))
(assert (not (or (and (<= x 600.0) (not (<= y 400.0)))
                 (and (not (<= x 600.0)) (<= y 400.0)))))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL469 — xone-A vs or-B: ~A_x & A_y branch with B satisfied → Compatible
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL469",
        "subdir":        "LogicalXone",
        "name":          "xone-A vs or-B: ~A_x & A_y branch with B satisfied → Compatible",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "PolicyA: xone(width lteq 600, height lteq 400)\n"
            "PolicyB: or(width gteq 800, height gteq 200)\n"
            "Branch (~A_x & A_y): X≥800>600→X∉(0,600] ✓, Y∈(0,400]→A_y ✓\n"
            "PolicyB: X≥800 ✓\n"
            "Witness: X=v800, Y=v200. verdictXone=Compatible\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:xone (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
      )
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:or (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "800"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v200, axiom, val(v200)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v200, v400, v600, v800)).
""",
        "fof_conjecture": (
            "?[X,Y]: (((in_lopen(X, v0, v600) & ~(in_lopen(Y, v0, v400))) |\n"
            "              (~(in_lopen(X, v0, v600)) & in_lopen(Y, v0, v400))) &\n"
            "          (leq(v800, X) | leq(v200, Y)))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (> y 0.0))
(assert (or (and (<= x 600.0) (not (<= y 400.0)))
            (and (not (<= x 600.0)) (<= y 400.0))))
(assert (or (>= x 800.0) (>= y 200.0)))""",
    },

]
