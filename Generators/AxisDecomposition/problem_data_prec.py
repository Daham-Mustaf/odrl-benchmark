"""
problem_data_prec.py
====================
ConflictCriterion benchmark problems: ODRL600-609 (10 problems).
Category K: Tests prec/4 and disjoint/8 from PREC000-0.ax directly.
Includes: ORD000-0.ax + PREC000-0.ax + AXIS000-0.ax

Problem overview:
  ODRL600 — prec_cc: less(U,L) => prec(U,L,c,c)               Theorem
  ODRL601 — prec_cc: equal endpoints not prec cc               Theorem
  ODRL602 — prec_oc: leq(U,L) => prec(U,L,o,c)                Theorem
  ODRL603 — prec_co: leq(U,L) => prec(U,L,c,o)                Theorem
  ODRL604 — prec_oo: leq(U,L) => prec(U,L,o,o)                Theorem
  ODRL605 — disjoint cc: [v0,v5] vs [v6,v10]                   Theorem
  ODRL606 — NOT disjoint cc: [v0,v5] vs [v5,v10] touch         CounterSatisfiable
  ODRL607 — disjoint co: (v0,v5] vs (v5,v10]                   Theorem
  ODRL608 — disjoint symmetry                                   Theorem
  ODRL609 — operator tags: lt upper=o, gt lower=o              Theorem
"""

PROBLEMS = [
    # ──────────────────────────────────────────────────────────────────
    # ODRL600 — prec_cc: strict separation required for closed endpoints
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL600",
        "subdir":        "ConflictCriterion",
        "name":          "prec_cc: less(U,L) implies prec(U,L,c,c)",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "thm:criterion prec_cc: less(v5,v6) => prec(v5,v6,c,c)\n"
            "Closed upper v5, closed lower v6: strict separation suffices.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ; odrl:rightOperand "500"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ; odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v5,  axiom, val(v5)).
fof(val_v6,  axiom, val(v6)).
fof(ord_v5_v6, axiom, less(v5, v6)).
fof(distinct, axiom, $distinct(v5, v6)).
""",
        "fof_conjecture": "prec(v5, v6, c, c)",
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const u Real)\n(declare-const l Real)",
        "smt2_asserts": """\
(assert (< u l))
(assert (not (< u l)))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL601 — prec_cc negative: equal endpoints NOT prec cc
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL601",
        "subdir":        "ConflictCriterion",
        "name":          "prec_cc negative: equal endpoints not prec(cc)",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "thm:criterion prec_cc negative: ~less(v5,v5) => ~prec(v5,v5,c,c)\n"
            "Touching closed endpoints are NOT separated: intervals overlap.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ; odrl:rightOperand "600"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ; odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v5, axiom, val(v5)).
fof(distinct, axiom, val(v5)).
""",
        "fof_conjecture": "~prec(v5, v5, c, c)",
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const u Real)",
        "smt2_asserts": """\
(assert (not (< u u)))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL602 — prec_oc: open upper, closed lower — leq suffices
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL602",
        "subdir":        "ConflictCriterion",
        "name":          "prec_oc: leq(U,L) implies prec(U,L,o,c)",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "thm:criterion prec_oc: leq(v5,v5) => prec(v5,v5,o,c)\n"
            "Open upper v5 (excluded), closed lower v5: equal is sufficient.\n"
            "Interval 1 ends before v5, interval 2 starts at v5 => disjoint.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lt ; odrl:rightOperand "600"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ; odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v5, axiom, val(v5)).
fof(val_v6, axiom, val(v6)).
fof(ord_v5_v6, axiom, less(v5, v6)).
fof(distinct, axiom, $distinct(v5, v6)).
""",
        "fof_conjecture": "prec(v5, v5, o, c)",
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const u Real)\n(declare-const l Real)",
        "smt2_asserts": """\
(assert (<= u l))
(assert (not (<= u l)))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL603 — prec_co: closed upper, open lower — leq suffices
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL603",
        "subdir":        "ConflictCriterion",
        "name":          "prec_co: leq(U,L) implies prec(U,L,c,o)",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "thm:criterion prec_co: leq(v5,v5) => prec(v5,v5,c,o)\n"
            "Closed upper v5 (attained), open lower v5 (excluded): equal ok.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ; odrl:rightOperand "600"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gt ; odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v5, axiom, val(v5)).
fof(val_v6, axiom, val(v6)).
fof(ord_v5_v6, axiom, less(v5, v6)).
fof(distinct, axiom, $distinct(v5, v6)).
""",
        "fof_conjecture": "prec(v5, v5, c, o)",
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const u Real)\n(declare-const l Real)",
        "smt2_asserts": """\
(assert (<= u l))
(assert (not (<= u l)))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL604 — prec_oo: both open — leq suffices
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL604",
        "subdir":        "ConflictCriterion",
        "name":          "prec_oo: leq(U,L) implies prec(U,L,o,o)",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "thm:criterion prec_oo: leq(v5,v5) => prec(v5,v5,o,o)\n"
            "Both endpoints open: equal value is enough for separation.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lt ; odrl:rightOperand "600"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gt ; odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v5, axiom, val(v5)).
fof(val_v6, axiom, val(v6)).
fof(ord_v5_v6, axiom, less(v5, v6)).
fof(distinct, axiom, $distinct(v5, v6)).
""",
        "fof_conjecture": "prec(v5, v5, o, o)",
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const u Real)\n(declare-const l Real)",
        "smt2_asserts": """\
(assert (<= u l))
(assert (not (<= u l)))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL605 — disjoint cc: [v0,v5] vs [v6,v10] strictly separated
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL605",
        "subdir":        "ConflictCriterion",
        "name":          "disjoint cc: [v0,v5] vs [v6,v10] strictly separated",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "thm:criterion: less(v5,v6) => disjoint([v0,v5],[v6,v10],cc)\n"
            "Strict gap between v5 and v6: both closed, separated.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ; odrl:rightOperand "500"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ; odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,  axiom, val(v0)).
fof(val_v5,  axiom, val(v5)).
fof(val_v6,  axiom, val(v6)).
fof(val_v10, axiom, val(v10)).
fof(ord_v0_v5,  axiom, less(v0, v5)).
fof(ord_v5_v6,  axiom, less(v5, v6)).
fof(ord_v6_v10, axiom, less(v6, v10)).
fof(distinct, axiom, $distinct(v0, v5, v6, v10)).
""",
        "fof_conjecture": "disjoint(v0, v5, c, c, v6, v10, c, c)",
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const x Real)",
        "smt2_asserts": """\
(assert (>= x 0.0)) (assert (<= x 500.0))
(assert (>= x 600.0))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL606 — NOT disjoint cc: [v0,v5] vs [v5,v10] touch → overlap
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL606",
        "subdir":        "ConflictCriterion",
        "name":          "NOT disjoint cc: [v0,v5] vs [v5,v10] touching",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "thm:criterion: ~less(v5,v5) => ~disjoint([v0,v5],[v5,v10],cc)\n"
            "Touching closed intervals share v5: NOT disjoint.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ; odrl:rightOperand "600"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ; odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,  axiom, val(v0)).
fof(val_v5,  axiom, val(v5)).
fof(val_v10, axiom, val(v10)).
fof(ord_v0_v5,  axiom, less(v0, v5)).
fof(ord_v5_v10, axiom, less(v5, v10)).
fof(distinct, axiom, $distinct(v0, v5, v10)).
""",
        "fof_conjecture": "~disjoint(v0, v5, c, c, v5, v10, c, c)",
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const x Real)",
        "smt2_asserts": """\
(assert (>= x 0.0)) (assert (<= x 600.0))
(assert (>= x 600.0))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL607 — disjoint co: (v0,v5] vs (v5,v10] — open lower kills overlap
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL607",
        "subdir":        "ConflictCriterion",
        "name":          "disjoint co: (v0,v5] vs (v5,v10] open lower kills overlap",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "thm:criterion co: leq(v5,v5) => prec(v5,v5,c,o)\n"
            "(0,v5] ends at v5 closed; (v5,v10] starts above v5 open.\n"
            "They share no point: disjoint.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ; odrl:rightOperand "600"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gt ; odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,  axiom, val(v0)).
fof(val_v5,  axiom, val(v5)).
fof(val_v10, axiom, val(v10)).
fof(ord_v0_v5,  axiom, less(v0, v5)).
fof(ord_v5_v10, axiom, less(v5, v10)).
fof(distinct, axiom, $distinct(v0, v5, v10)).
""",
        "fof_conjecture": "disjoint(v0, v5, c, c, v5, v10, o, c)",
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 600.0))
(assert (> x 600.0))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL608 — disjoint symmetry: disjoint(A,B) <=> disjoint(B,A)
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL608",
        "subdir":        "ConflictCriterion",
        "name":          "disjoint symmetry: disjoint(A,B) iff disjoint(B,A)",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "thm:criterion symmetry: disjoint is symmetric.\n"
            "disjoint(L1,U1,CL1,CU1,L2,U2,CL2,CU2) <=> disjoint(L2,U2,CL2,CU2,L1,U1,CL1,CU1)\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ; odrl:rightOperand "500"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ; odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": "",
        "fof_conjecture": (
            "![L1,U1,CL1,CU1,L2,U2,CL2,CU2]:\n"
            "    (disjoint(L1,U1,CL1,CU1,L2,U2,CL2,CU2) <=>\n"
            "     disjoint(L2,U2,CL2,CU2,L1,U1,CL1,CU1))"
        ),
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const x Real)",
        "smt2_asserts": """\
(assert (>= x 0.0)) (assert (<= x 500.0))
(assert (>= x 600.0))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL609 — operator tags: lt upper=o, gt lower=o
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL609",
        "subdir":        "ConflictCriterion",
        "name":          "operator tags: lt has open upper, gt has open lower",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "Operator tags: lt => upper_tag(lt,o), gt => lower_tag(gt,o)\n"
            "These capture the open-boundary semantics of strict operators.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lt ; odrl:rightOperand "600"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gt ; odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": "",
        "fof_conjecture": "upper_tag(lt, o) & lower_tag(gt, o)",
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const x Real)",
        "smt2_asserts": """\
(assert (< x 600.0))
(assert (> x 600.0))""",
    },
]
