"""
problem_data_boundary.py
========================
Boundary benchmark problems: ODRL420-435 (16 problems).

Category G: Tests all 10 operator-pair combinations at a shared boundary
value (thm:criterion), plus 2D/3D extensions and subsumption.

The 10 single-axis operator pairs (ODRL420-429):
  cc (lteq ∩ gteq):  (0,v]∩[v,∞)={v}         Compatible
  co (lteq ∩ gt):    (0,v]∩(v,∞)=∅             Conflict
  oc (lt ∩ gteq):    (0,v)∩[v,∞)=∅             Conflict
  oo (lt ∩ gt):      (0,v)∩(v,∞)=∅             Conflict
  eq∩lteq:           {v}∩(0,v]={v}             Compatible
  eq∩gteq:           {v}∩[v,∞)={v}             Compatible
  eq∩lt:             {v}∩(0,v)=∅               Conflict
  eq∩gt:             {v}∩(v,∞)=∅               Conflict
  lt∩lteq:           (0,v)∩(0,v]=(0,v)≠∅       Compatible  ← density
  gt∩gteq:           (v,∞)∩[v,∞)=(v,∞)≠∅       Compatible  ← sentinel

Density/sentinel notes:
  ODRL428 (lt∩lteq): witness in (0,600) — requires ORD001-0.ax.
  ODRL429 (gt∩gteq): witness above v600 — adds sentinel v1200.

TTL: single odrl:constraint for 1D; odrl:and for multi-axis.
TTL prefix: drk: <http://w3id.org/drk/ontology/>
"""

PROBLEMS = [

    # ──────────────────────────────────────────────────────────────────
    # ODRL420 — cc: lteq ∩ gteq — shared boundary point Compatible
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL420",
        "subdir":        "Boundary",
        "name":          "cc: lteq ∩ gteq — shared boundary point Compatible",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "includes":     ["ORD000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "thm:criterion cc: (0,600]∩[600,∞)={600}≠∅ Compatible\n"
            "Witness: X=v600 (named constant). Tightest possible overlap.\n"
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
      odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "600"^^xsd:decimal
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ;
      odrl:rightOperand "600"^^xsd:decimal
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct, axiom, $distinct(v0, v600)).
""",
        "fof_conjecture": (
            "?[X]: (in_lopen(X, v0, v600) & leq(v600, X))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 600.0))
(assert (>= x 600.0))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL421 — co: lteq ∩ gt — boundary excluded on right → Conflict
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL421",
        "subdir":        "Boundary",
        "name":          "co: lteq ∩ gt — boundary excluded on right → Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":     ["ORD000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "thm:criterion co: (0,600]∩(600,∞)=∅ Conflict\n"
            "Proof: X≤600 AND X>600 is order contradiction.\n"
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
      odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "600"^^xsd:decimal
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gt ;
      odrl:rightOperand "600"^^xsd:decimal
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct, axiom, $distinct(v0, v600)).
""",
        "fof_conjecture": (
            "![X]: ~(in_lopen(X, v0, v600) & less(v600, X))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 600.0))
(assert (> x 600.0))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL422 — oc: lt ∩ gteq — boundary excluded on left → Conflict
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL422",
        "subdir":        "Boundary",
        "name":          "oc: lt ∩ gteq — boundary excluded on left → Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":     ["ORD000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "thm:criterion oc: (0,600)∩[600,∞)=∅ Conflict\n"
            "Proof: X<600 AND X≥600 is order contradiction.\n"
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
      odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lt ;
      odrl:rightOperand "600"^^xsd:decimal
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ;
      odrl:rightOperand "600"^^xsd:decimal
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct, axiom, $distinct(v0, v600)).
""",
        "fof_conjecture": (
            "![X]: ~(in_open(X, v0, v600) & leq(v600, X))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (< x 600.0))
(assert (>= x 600.0))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL423 — oo: lt ∩ gt — boundary excluded both sides → Conflict
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL423",
        "subdir":        "Boundary",
        "name":          "oo: lt ∩ gt — boundary excluded both sides → Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":     ["ORD000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "thm:criterion oo: (0,600)∩(600,∞)=∅ Conflict\n"
            "Proof: X<600 AND X>600 is order contradiction.\n"
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
      odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lt ;
      odrl:rightOperand "600"^^xsd:decimal
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gt ;
      odrl:rightOperand "600"^^xsd:decimal
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct, axiom, $distinct(v0, v600)).
""",
        "fof_conjecture": (
            "![X]: ~(in_open(X, v0, v600) & less(v600, X))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (< x 600.0))
(assert (> x 600.0))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL424 — eq ∩ lteq — eq value included in lteq → Compatible
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL424",
        "subdir":        "Boundary",
        "name":          "eq ∩ lteq — eq value included in lteq → Compatible",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "includes":     ["ORD000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "thm:criterion eq∩lteq: {600}∩(0,600]={600}≠∅ Compatible\n"
            "Witness: X=v600.\n"
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
      odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ;
      odrl:rightOperand "600"^^xsd:decimal
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "600"^^xsd:decimal
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct, axiom, $distinct(v0, v600)).
""",
        "fof_conjecture": (
            "?[X]: (in_closed(X, v600, v600) & in_lopen(X, v0, v600))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (= x 600.0))
(assert (<= x 600.0))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL425 — eq ∩ gteq — eq value included in gteq → Compatible
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL425",
        "subdir":        "Boundary",
        "name":          "eq ∩ gteq — eq value included in gteq → Compatible",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "includes":     ["ORD000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "thm:criterion eq∩gteq: {600}∩[600,∞)={600}≠∅ Compatible\n"
            "Witness: X=v600.\n"
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
      odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ;
      odrl:rightOperand "600"^^xsd:decimal
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ;
      odrl:rightOperand "600"^^xsd:decimal
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct, axiom, $distinct(v0, v600)).
""",
        "fof_conjecture": (
            "?[X]: (in_closed(X, v600, v600) & leq(v600, X))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (= x 600.0))
(assert (>= x 600.0))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL426 — eq ∩ lt — eq value at boundary excluded by lt → Conflict
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL426",
        "subdir":        "Boundary",
        "name":          "eq ∩ lt — eq value at boundary excluded by lt → Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":     ["ORD000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "thm:criterion eq∩lt: {600}∩(0,600)=∅ Conflict\n"
            "Proof: X=600 AND X<600 is order contradiction.\n"
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
      odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ;
      odrl:rightOperand "600"^^xsd:decimal
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lt ;
      odrl:rightOperand "600"^^xsd:decimal
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct, axiom, $distinct(v0, v600)).
""",
        "fof_conjecture": (
            "![X]: ~(in_closed(X, v600, v600) & in_open(X, v0, v600))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (= x 600.0))
(assert (< x 600.0))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL427 — eq ∩ gt — eq value at boundary excluded by gt → Conflict
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL427",
        "subdir":        "Boundary",
        "name":          "eq ∩ gt — eq value at boundary excluded by gt → Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
         "includes":     ["ORD000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "thm:criterion eq∩gt: {600}∩(600,∞)=∅ Conflict\n"
            "Proof: X=600 AND X>600 is order contradiction.\n"
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
      odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ;
      odrl:rightOperand "600"^^xsd:decimal
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gt ;
      odrl:rightOperand "600"^^xsd:decimal
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct, axiom, $distinct(v0, v600)).
""",
        "fof_conjecture": (
            "![X]: ~(in_closed(X, v600, v600) & less(v600, X))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (= x 600.0))
(assert (> x 600.0))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL428 — lt ∩ lteq — open subset of closed → Compatible (density)
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL428",
        "subdir":        "Boundary",
        "name":          "lt ∩ lteq — open subset of closed → Compatible (density)",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "includes":     ["ORD000-0.ax", "ORD001-0.ax", "AXIS000-0.ax"],
        "needs_density": True,
        "description": (
            "thm:criterion lt∩lteq: (0,600)∩(0,600]=(0,600)≠∅ Compatible\n"
            "Witness must be strictly inside (0,600) — no named constant.\n"
            "Requires ORD001-0.ax (density) for Vampire to find witness.\n"
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
      odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lt ;
      odrl:rightOperand "600"^^xsd:decimal
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "600"^^xsd:decimal
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct, axiom, $distinct(v0, v600)).
""",
        "fof_conjecture": (
            "?[X]: (in_open(X, v0, v600) & in_lopen(X, v0, v600))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (< x 600.0))
(assert (<= x 600.0))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL429 — gt ∩ gteq — open superset of closed → Compatible (sentinel)
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL429",
        "subdir":        "Boundary",
        "name":          "gt ∩ gteq — open superset of closed → Compatible (sentinel)",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "includes":     ["ORD000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "thm:criterion gt∩gteq: (600,∞)∩[600,∞)=(600,∞)≠∅ Compatible\n"
            "Witness must be above v600 — adds sentinel v1200 with less(v600,v1200).\n"
            "X=v1200 satisfies less(v600,X) AND leq(v600,X).\n"
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
      odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gt ;
      odrl:rightOperand "600"^^xsd:decimal
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ;
      odrl:rightOperand "600"^^xsd:decimal
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v1200, axiom, less(v0, v1200)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct, axiom, $distinct(v0, v600, v1200)).
""",
        "fof_conjecture": (
            "?[X]: (less(v600, X) & leq(v600, X))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (> x 600.0))
(assert (>= x 600.0))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL430 — 2D cc×cc — both axes touch → Compatible
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL430",
        "subdir":        "Boundary",
        "name":          "2D cc×cc — both axes touch → Compatible",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "includes":     ["ORD000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "Width:  (0,600]∩[600,∞)={600}≠∅ Compatible (cc)\n"
            "Height: (0,400]∩[400,∞)={400}≠∅ Compatible (cc)\n"
            "Witnesses: X=v600, Y=v400.\n"
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
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct, axiom, $distinct(v0, v400, v600)).
""",
        "fof_conjecture": (
            "?[X,Y]: (in_lopen(X, v0, v600) & leq(v600, X) &\n"
            "           in_lopen(Y, v0, v400) & leq(v400, Y))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 600.0)) (assert (>= x 600.0))
(assert (> y 0.0)) (assert (<= y 400.0)) (assert (>= y 400.0))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL431 — 2D cc×oc — Y boundary excluded on left kills box → Conflict
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL431",
        "subdir":        "Boundary",
        "name":          "2D cc×oc — Y boundary excluded on left kills box → Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "includes":     ["ORD000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "Width:  cc: (0,600]∩[600,∞)={600} Compatible\n"
            "Height: oc: (0,400)∩[400,∞)=∅ Conflict\n"
            "Height contradiction kills the box.\n"
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
          odrl:operator odrl:lt ;
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
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct, axiom, $distinct(v0, v400, v600)).
""",
        "fof_conjecture": (
            "![X,Y]: ~(in_lopen(X, v0, v600) & leq(v600, X) &\n"
            "          in_open(Y, v0, v400) & leq(v400, Y))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 600.0)) (assert (>= x 600.0))
(assert (> y 0.0)) (assert (< y 400.0)) (assert (>= y 400.0))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL432 — 3D cc×co×cc — Y boundary excluded on right kills 3D box → Conflict
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL432",
        "subdir":        "Boundary",
        "name":          "3D cc×co×cc — Y boundary excluded on right kills 3D box → Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "includes":     ["ORD000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "Width:  cc: (0,600]∩[600,∞)={600} Compatible\n"
            "Height: co: (0,400]∩(400,∞)=∅ Conflict\n"
            "Depth:  cc: (0,200]∩[200,∞)={200} Compatible\n"
            "Height contradiction kills the 3D box.\n"
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
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gt ;
          odrl:rightOperand "400"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
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
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct, axiom, $distinct(v0, v200, v400, v600)).
""",
        "fof_conjecture": (
            "![X,Y,Z]: ~(in_lopen(X, v0, v600) & leq(v600, X) &\n"
            "           in_lopen(Y, v0, v400) & less(v400, Y) &\n"
            "           in_lopen(Z, v0, v200) & leq(v200, Z))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 600.0)) (assert (>= x 600.0))
(assert (> y 0.0)) (assert (<= y 400.0)) (assert (> y 400.0))
(assert (> z 0.0)) (assert (<= z 200.0)) (assert (>= z 200.0))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL433 — Subsumption: lt⊆lteq on width, lteq⊆lteq on height → Compatible
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL433",
        "subdir":        "Boundary",
        "name":          "Subsumption: lt⊆lteq on width, lteq⊆lteq on height → Compatible",
        "relation":      "subsumption",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "includes":      ["ORD000-0.ax", "AXIS000-0.ax", "SUBS000-0.ax"],
        "needs_density": False,
        "description": (
            "Width:  (0,600) ⊆ (0,600] Compatible (open subset of closed)\n"
            "Height: (0,400] ⊆ (0,800] Compatible\n"
            "A ⊆ B on all axes → Compatible [def:box-containment]\n"
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
          odrl:operator odrl:lt ;
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
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "800"^^xsd:decimal ]
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
            "![X,Y]: ((in_open(X, v0, v600) & in_lopen(Y, v0, v400)) =>\n"
            "           (in_lopen(X, v0, v600) & in_lopen(Y, v0, v800)))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (< x 600.0))
(assert (> y 0.0)) (assert (<= y 400.0))
(assert (not (and (<= x 600.0) (<= y 800.0))))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL434 — Subsumption escape: X=600∈(0,600] but X∉(0,600) → Conflict
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL434",
        "subdir":        "Boundary",
        "name":          "Subsumption escape: X=600∈(0,600] but X∉(0,600) → Conflict",
        "relation":      "subsumption",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "includes":     ["ORD000-0.ax", "AXIS000-0.ax", "SUBS000-0.ax"],
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "PolicyA: width lteq 600 → (0,600]; PolicyB: width lt 600 → (0,600)\n"
            "Escape: X=v600 ∈ (0,600] but v600∉(0,600)\n"
            "SMT2: x=600 satisfies A_x but not B_x → sat\n"
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
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lt ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "800"^^xsd:decimal ]
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
            "?[X,Y]: ((in_lopen(X, v0, v600) & in_lopen(Y, v0, v400)) &\n"
            "           ~(in_open(X, v0, v600) & in_lopen(Y, v0, v800)))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 600.0))
(assert (> y 0.0)) (assert (<= y 400.0))
(assert (not (and (< x 600.0) (<= y 800.0))))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL435 — 3D eq×cc×eq — all three axes touch at named constants → Compatible
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL435",
        "subdir":        "Boundary",
        "name":          "3D eq×cc×eq — all three axes touch at named constants → Compatible",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "includes":     ["ORD000-0.ax", "AXIS000-0.ax"],
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "Width:  eq 600 ∩ lteq 600 = {600} Compatible\n"
            "Height: lteq 400 ∩ gteq 400 = {400} Compatible (cc)\n"
            "Depth:  eq 200 ∩ gteq 200 = {200} Compatible\n"
            "Witnesses: X=v600, Y=v400, Z=v200.\n"
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
          odrl:operator odrl:eq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:eq ;
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
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
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
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct, axiom, $distinct(v0, v200, v400, v600)).
""",
        "fof_conjecture": (
            "?[X,Y,Z]: (in_closed(X, v600, v600) & in_lopen(X, v0, v600) &\n"
            "           in_lopen(Y, v0, v400) & leq(v400, Y) &\n"
            "           in_closed(Z, v200, v200) & leq(v200, Z))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (= x 600.0)) (assert (<= x 600.0))
(assert (> y 0.0)) (assert (<= y 400.0)) (assert (>= y 400.0))
(assert (> z 0.0)) (assert (= z 200.0)) (assert (>= z 200.0))""",
    },

]
