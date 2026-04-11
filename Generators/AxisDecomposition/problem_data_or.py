"""
problem_data_or.py
==================
LogicalOr benchmark problems: ODRL440-451 (12 problems).

Category H: odrl:or logical constraint composition.
Tests thm:composition-soundness (disjunction):
  verdictOr = Compatible if ∃(Bi,Bj): box_verdict(Bi,Bj) = Compatible
  verdictOr = Conflict   if ∀(Bi,Bj): box_verdict(Bi,Bj) = Conflict
  verdictOr = Unknown    otherwise

Per-axis decomposition does NOT apply for or/xone.
Provers must reason over coupled multi-axis disjunctions.

TTL: odrl:or for disjunctive constraints, odrl:and for conjunctive.
SMT2: encodes the disjunctive structure directly using (or ...).
Include pattern:
  Discrete:   include('Axioms/AXIS000-0.ax').
  Continuous: include('Axioms/ORD001-0.ax').
              include('Axioms/AXIS000-0.ax').
TTL prefix: drk: <http://w3id.org/drk/ontology/>
"""

PROBLEMS = [

    # ──────────────────────────────────────────────────────────────────
    # ODRL440 — PolicyA or-branches: any branch overlaps PolicyB → Compatible
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL440",
        "subdir":        "LogicalOr",
        "name":          "PolicyA or-branches: any branch overlaps PolicyB → Compatible",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "PolicyA: width lteq 400 OR height lteq 800 (odrl:or)\n"
            "PolicyB: width gteq 600 AND height gteq 200 (odrl:and)\n"
            "Branch pair (A2,B): Y∈(0,800]∩[200,∞)=[200,800] ≠ ∅ → Compatible\n"
            "verdictOr=Compatible [thm:composition-soundness]\n"
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
      odrl:or (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "800"^^xsd:decimal ]
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
          odrl:rightOperand "600"^^xsd:decimal ]
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
            "?[X,Y]: ((in_lopen(X, v0, v400) | in_lopen(Y, v0, v800)) &\n"
            "           (leq(v600, X) & leq(v200, Y)))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (> y 0.0))
(assert (or (<= x 400.0) (<= y 800.0)))
(assert (>= x 600.0))
(assert (>= y 200.0))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL441 — All PolicyA or-branches conflict with PolicyB → Conflict
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL441",
        "subdir":        "LogicalOr",
        "name":          "All PolicyA or-branches conflict with PolicyB → Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "PolicyA: width lteq 400 OR height lteq 100 (odrl:or)\n"
            "PolicyB: width gteq 800 AND height gteq 200 (odrl:and)\n"
            "(A1,B): (0,400]∩[800,∞)=∅ Conflict\n"
            "(A2,B): (0,100]∩[200,∞)=∅ Conflict\n"
            "All branch pairs Conflict → verdictOr=Conflict\n"
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
      odrl:or (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "100"^^xsd:decimal ]
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
          odrl:operator odrl:gteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v100, axiom, val(v100)).
fof(val_v200, axiom, val(v200)).
fof(val_v400, axiom, val(v400)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v100, axiom, less(v0, v100)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v400, axiom, less(v100, v400)).
fof(ord_v100_v800, axiom, less(v100, v800)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(distinct, axiom, $distinct(v0, v100, v200, v400, v800)).
""",
        "fof_conjecture": (
            "~?[X,Y]: ((in_lopen(X, v0, v400) | in_lopen(Y, v0, v100)) &\n"
            "            (leq(v800, X) & leq(v200, Y)))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (> y 0.0))
(assert (or (<= x 400.0) (<= y 100.0)))
(assert (>= x 800.0))
(assert (>= y 200.0))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL442 — PolicyA and-constraints: any PolicyB or-branch overlaps → Compatible
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL442",
        "subdir":        "LogicalOr",
        "name":          "PolicyA and-constraints: any PolicyB or-branch overlaps → Compatible",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "PolicyA: width lteq 800 AND height lteq 600 (odrl:and)\n"
            "PolicyB: width gteq 1000 OR height gteq 200 (odrl:or)\n"
            "(A,B2): Y∈(0,600]∩[200,∞)=[200,600] ≠ ∅ → Compatible\n"
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
          odrl:rightOperand "800"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
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
          odrl:rightOperand "1000"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v200, axiom, val(v200)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(val_v1000, axiom, val(v1000)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v0_v1000, axiom, less(v0, v1000)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v200_v1000, axiom, less(v200, v1000)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(ord_v600_v1000, axiom, less(v600, v1000)).
fof(ord_v800_v1000, axiom, less(v800, v1000)).
fof(distinct, axiom, $distinct(v0, v200, v600, v800, v1000)).
""",
        "fof_conjecture": (
            "?[X,Y]: ((in_lopen(X, v0, v800) & in_lopen(Y, v0, v600)) &\n"
            "           (leq(v1000, X) | leq(v200, Y)))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 800.0))
(assert (> y 0.0)) (assert (<= y 600.0))
(assert (or (>= x 1000.0) (>= y 200.0)))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL443 — PolicyA and: all PolicyB or-branches conflict → Conflict
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL443",
        "subdir":        "LogicalOr",
        "name":          "PolicyA and: all PolicyB or-branches conflict → Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "PolicyA: width lteq 400 AND height lteq 100 (odrl:and)\n"
            "PolicyB: width gteq 800 OR height gteq 200 (odrl:or)\n"
            "(A,B1): (0,400]∩[800,∞)=∅ Conflict; (A,B2): (0,100]∩[200,∞)=∅ Conflict\n"
            "All branch pairs Conflict → verdictOr=Conflict\n"
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
          odrl:rightOperand "100"^^xsd:decimal ]
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
fof(val_v100, axiom, val(v100)).
fof(val_v200, axiom, val(v200)).
fof(val_v400, axiom, val(v400)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v100, axiom, less(v0, v100)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v400, axiom, less(v100, v400)).
fof(ord_v100_v800, axiom, less(v100, v800)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(distinct, axiom, $distinct(v0, v100, v200, v400, v800)).
""",
        "fof_conjecture": (
            "~?[X,Y]: ((in_lopen(X, v0, v400) & in_lopen(Y, v0, v100)) &\n"
            "            (leq(v800, X) | leq(v200, Y)))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 400.0))
(assert (> y 0.0)) (assert (<= y 100.0))
(assert (or (>= x 800.0) (>= y 200.0)))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL444 — Both policies or: cross-branch overlap → Compatible
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL444",
        "subdir":        "LogicalOr",
        "name":          "Both policies or: cross-branch overlap → Compatible",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "PolicyA: width lteq 400 OR height lteq 600 (odrl:or)\n"
            "PolicyB: width gteq 300 OR height gteq 500 (odrl:or)\n"
            "Branch pair (A1,B1): (0,400]∩[300,∞)=[300,400] ≠ ∅ → Compatible\n"
            "Tests cross-pick: any overlapping branch pair suffices.\n"
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
      odrl:or (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
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
          odrl:rightOperand "300"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
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
            "?[X,Y]: ((in_lopen(X, v0, v400) | in_lopen(Y, v0, v600)) &\n"
            "           (leq(v300, X) | leq(v500, Y)))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (> y 0.0))
(assert (or (<= x 400.0) (<= y 600.0)))
(assert (or (>= x 300.0) (>= y 500.0)))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL445 — 3-branch or: all branch pairs conflict → Conflict
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL445",
        "subdir":        "LogicalOr",
        "name":          "3-branch or: all branch pairs conflict → Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "PolicyA: width lteq 200 OR height lteq 100 OR depth lteq 50 (odrl:or)\n"
            "PolicyB: width gteq 400 AND height gteq 200 AND depth gteq 100 (odrl:and)\n"
            "All 3 branch pairs Conflict → verdictOr=Conflict\n"
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
      odrl:or (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "100"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "50"^^xsd:decimal ]
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
          odrl:rightOperand "400"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "100"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v50, axiom, val(v50)).
fof(val_v100, axiom, val(v100)).
fof(val_v200, axiom, val(v200)).
fof(val_v400, axiom, val(v400)).
fof(ord_v0_v50, axiom, less(v0, v50)).
fof(ord_v0_v100, axiom, less(v0, v100)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v50_v100, axiom, less(v50, v100)).
fof(ord_v50_v200, axiom, less(v50, v200)).
fof(ord_v50_v400, axiom, less(v50, v400)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v400, axiom, less(v100, v400)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(distinct, axiom, $distinct(v0, v50, v100, v200, v400)).
""",
        "fof_conjecture": (
            "~?[X,Y,Z]: ((in_lopen(X, v0, v200) | in_lopen(Y, v0, v100) | in_lopen(Z, v0, v50)) &\n"
            "            (leq(v400, X) & leq(v200, Y) & leq(v100, Z)))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (> y 0.0)) (assert (> z 0.0))
(assert (or (<= x 200.0) (<= y 100.0) (<= z 50.0)))
(assert (>= x 400.0))
(assert (>= y 200.0))
(assert (>= z 100.0))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL446 — 3-branch or: depth branch overlaps → Compatible
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL446",
        "subdir":        "LogicalOr",
        "name":          "3-branch or: depth branch overlaps → Compatible",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "PolicyA: width lteq 200 OR height lteq 100 OR depth lteq 200 (odrl:or)\n"
            "PolicyB: width gteq 400 AND height gteq 200 AND depth gteq 100 (odrl:and)\n"
            "Branch (A3,B): Z∈(0,200]∩[100,∞)=[100,200] ≠ ∅ → Compatible\n"
            "Witness: X=400, Y=200, Z=100 (named constants).\n"
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
      odrl:or (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "100"^^xsd:decimal ]
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
          odrl:operator odrl:gteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "100"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v100, axiom, val(v100)).
fof(val_v200, axiom, val(v200)).
fof(val_v400, axiom, val(v400)).
fof(ord_v0_v100, axiom, less(v0, v100)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v400, axiom, less(v100, v400)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(distinct, axiom, $distinct(v0, v100, v200, v400)).
""",
        "fof_conjecture": (
            "?[X,Y,Z]: ((in_lopen(X, v0, v200) | in_lopen(Y, v0, v100) | in_lopen(Z, v0, v200)) &\n"
            "           (leq(v400, X) & leq(v200, Y) & leq(v100, Z)))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (> y 0.0)) (assert (> z 0.0))
(assert (or (<= x 200.0) (<= y 100.0) (<= z 200.0)))
(assert (>= x 400.0))
(assert (>= y 200.0))
(assert (>= z 100.0))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL447 — or-subsumption: A_and ⊆ B_or → Compatible
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL447",
        "subdir":        "LogicalOr",
        "name":          "or-subsumption: A_and ⊆ B_or → Compatible",
        "relation":      "subsumption",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "PolicyA: width lteq 600 AND height lteq 400 (odrl:and)\n"
            "PolicyB: width lteq 800 OR height lteq 600 (odrl:or)\n"
            "(0,600]×(0,400] ⊆ (0,800]∪(0,600]: every A-point in A_w ⊆ B_w=(0,800] \n"
            "or-subsumption Compatible [def:box-containment, or variant]\n"
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
          odrl:operator odrl:lteq ;
          odrl:rightOperand "800"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v400, v600, v800)).
""",
        "fof_conjecture": (
            "![X,Y]: ((in_lopen(X, v0, v600) & in_lopen(Y, v0, v400)) =>\n"
            "           (in_lopen(X, v0, v800) | in_lopen(Y, v0, v600)))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 600.0))
(assert (> y 0.0)) (assert (<= y 400.0))
(assert (not (or (<= x 800.0) (<= y 600.0))))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL448 — or-subsumption: B_or ⊄ A_and escape witness → Conflict
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL448",
        "subdir":        "LogicalOr",
        "name":          "or-subsumption: B_or ⊄ A_and escape witness → Conflict",
        "relation":      "subsumption",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "PolicyA: width lteq 800 OR height lteq 600 (odrl:or) [wider]\n"
            "PolicyB: width lteq 600 AND height lteq 400 (odrl:and) [narrower]\n"
            "Escape: X=700 ∈ (0,800] but X∉(0,600] → A ⊄ B Conflict\n"
            "or-subsumption Conflict [def:box-containment escape]\n"
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
      odrl:or (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "800"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
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
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v400, v600, v800)).
""",
        "fof_conjecture": (
            "?[X,Y]: ((in_lopen(X, v0, v800) | in_lopen(Y, v0, v600)) &\n"
            "           ~(in_lopen(X, v0, v600) & in_lopen(Y, v0, v400)))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (> y 0.0))
(assert (or (<= x 800.0) (<= y 600.0)))
(assert (not (and (<= x 600.0) (<= y 400.0))))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL449 — 3-branch or vs 3-branch or: depth branch pair overlaps → Compatible
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL449",
        "subdir":        "LogicalOr",
        "name":          "3-branch or vs 3-branch or: depth branch pair overlaps → Compatible",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "PolicyA: width lteq 200 OR height lteq 100 OR depth lteq 800 (odrl:or)\n"
            "PolicyB: width gteq 400 OR height gteq 200 OR depth gteq 300 (odrl:or)\n"
            "Branch pair (A3,B3): Z∈(0,800]∩[300,∞)=[300,800] ≠ ∅ → Compatible\n"
            "Tests cross-pick across 3-branch or policies.\n"
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
      odrl:or (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "100"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "800"^^xsd:decimal ]
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
          odrl:rightOperand "400"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "300"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v100, axiom, val(v100)).
fof(val_v200, axiom, val(v200)).
fof(val_v300, axiom, val(v300)).
fof(val_v400, axiom, val(v400)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v100, axiom, less(v0, v100)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v300, axiom, less(v0, v300)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v300, axiom, less(v100, v300)).
fof(ord_v100_v400, axiom, less(v100, v400)).
fof(ord_v100_v800, axiom, less(v100, v800)).
fof(ord_v200_v300, axiom, less(v200, v300)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v300_v400, axiom, less(v300, v400)).
fof(ord_v300_v800, axiom, less(v300, v800)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(distinct, axiom, $distinct(v0, v100, v200, v300, v400, v800)).
""",
        "fof_conjecture": (
            "?[X,Y,Z]: ((in_lopen(X, v0, v200) | in_lopen(Y, v0, v100) | in_lopen(Z, v0, v800)) &\n"
            "           (leq(v400, X) | leq(v200, Y) | leq(v300, Z)))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (> y 0.0)) (assert (> z 0.0))
(assert (or (<= x 200.0) (<= y 100.0) (<= z 800.0)))
(assert (or (>= x 400.0) (>= y 200.0) (>= z 300.0)))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL450 — Mixed operators or+and: open interval overlap → Compatible (density)
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL450",
        "subdir":        "LogicalOr",
        "name":          "Mixed operators or+and: open interval overlap → Compatible (density)",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Hard",
        "needs_density": True,
        "description": (
            "PolicyA: width lt 600 OR height gt 200 (odrl:or)\n"
            "PolicyB: width gt 400 AND height lt 800 (odrl:and)\n"
            "Branch (A1,B): X∈(0,600)∩(400,∞)=(400,600) ≠ ∅ → Compatible\n"
            "Witness inside open interval (400,600) → requires ORD001-0.ax.\n"
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
      odrl:or (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lt ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gt ;
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
          odrl:operator odrl:gt ;
          odrl:rightOperand "400"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lt ;
          odrl:rightOperand "800"^^xsd:decimal ]
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
            "?[X,Y]: ((in_open(X, v0, v600) | less(v200, Y)) &\n"
            "           (less(v400, X) & in_open(Y, v0, v800)))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (> y 0.0))
(assert (or (< x 600.0) (> y 200.0)))
(assert (> x 400.0))
(assert (< y 800.0))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL451 — 3-branch or with mixed ops: all branches conflict → Conflict
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL451",
        "subdir":        "LogicalOr",
        "name":          "3-branch or with mixed ops: all branches conflict → Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Hard",
        "needs_density": False,
        "description": (
            "PolicyA: width eq 600 OR height lt 200 OR depth gt 100 (odrl:or)\n"
            "PolicyB: width gt 800 AND height gteq 400 AND depth lteq 50 (odrl:and)\n"
            "(A1,B): {600}∩(800,∞)=∅; (A2,B): (0,200)∩[400,∞)=∅; (A3,B): (100,∞)∩(0,50]=∅\n"
            "All 3 branch pairs Conflict → verdictOr=Conflict\n"
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
      odrl:or (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:eq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lt ;
          odrl:rightOperand "200"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:gt ;
          odrl:rightOperand "100"^^xsd:decimal ]
      )
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:gt ;
          odrl:rightOperand "800"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "50"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v50, axiom, val(v50)).
fof(val_v100, axiom, val(v100)).
fof(val_v200, axiom, val(v200)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v50, axiom, less(v0, v50)).
fof(ord_v0_v100, axiom, less(v0, v100)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v50_v100, axiom, less(v50, v100)).
fof(ord_v50_v200, axiom, less(v50, v200)).
fof(ord_v50_v400, axiom, less(v50, v400)).
fof(ord_v50_v600, axiom, less(v50, v600)).
fof(ord_v50_v800, axiom, less(v50, v800)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v400, axiom, less(v100, v400)).
fof(ord_v100_v600, axiom, less(v100, v600)).
fof(ord_v100_v800, axiom, less(v100, v800)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v50, v100, v200, v400, v600, v800)).
""",
        "fof_conjecture": (
            "~?[X,Y,Z]: ((in_closed(X, v600, v600) | in_open(Y, v0, v200) | less(v100, Z)) &\n"
            "            (less(v800, X) & leq(v400, Y) & in_lopen(Z, v0, v50)))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (> y 0.0)) (assert (> z 0.0))
(assert (or (= x 600.0) (< y 200.0) (> z 100.0)))
(assert (> x 800.0))
(assert (>= y 400.0))
(assert (<= z 50.0))""",
    },

]
