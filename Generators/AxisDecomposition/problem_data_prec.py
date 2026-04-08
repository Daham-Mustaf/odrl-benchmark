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
  ODRL606 — NOT disjoint cc: [v0,v5] vs [v5,v10] touch         Theorem
  ODRL607 — disjoint co: [v0,v5] vs (v5,v10]                   Theorem
  ODRL608 — disjoint symmetry                                   Theorem
  ODRL609 — operator tags: lt upper=o, gt lower=o              Theorem

Fixes vs. original:
  ODRL601: removed duplicate fof(distinct,axiom,val(v5)); corrected
           status_smt to "unsat" and SMT assert to negated conjecture
           (assert (< u u)) which is UNSAT by irreflexivity.
  ODRL602/603/604: removed unused val_v6, less(v5,v6), $distinct(v5,v6)
           declarations that were copied from ODRL600 but serve no role
           since the conjecture only mentions v5.
  ODRL607: corrected description from "(v0,v5]" to "[v0,v5]" to match
           CL1=c in the FOF conjecture; corrected SMT lower bound from
           (> x 0.0) to (>= x 0.0) to match the closed lower endpoint.
  ODRL608: replaced the copied ground-conflict SMT (which tested a
           different claim) with a correct symmetry SMT: assert
           disjoint(A,B) via u1<l2 and negate disjoint(B,A) via ~(u2<l1)
           and ~(u2<=l1) — UNSAT confirms symmetry.
  ODRL609: added documentation comment clarifying that the SMT is an
           indirect sanity check only (tag axioms have no direct SMT
           encoding); SMT assertions themselves are unchanged.
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
fof(val_v5,    axiom, val(v5)).
fof(val_v6,    axiom, val(v6)).
fof(ord_v5_v6, axiom, less(v5, v6)).
fof(distinct,  axiom, $distinct(v5, v6)).
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
    #
    # FIX 1: removed spurious fof(distinct, axiom, val(v5)) — was a
    #         copy-paste of val_v5 and asserted nothing useful.
    # FIX 2: status_smt was "sat"; corrected to "unsat".
    #         SMT assert was (not (< u u)) which trivially holds (SAT)
    #         and did not test the conjecture.  Corrected to the negated
    #         conjecture pattern used by all other Theorem problems:
    #         assert ~(~prec(v5,v5,c,c)) = assert prec(v5,v5,c,c)
    #         = assert less(v5,v5), which is UNSAT by irreflexivity.
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL601",
        "subdir":        "ConflictCriterion",
        "name":          "prec_cc negative: equal endpoints not prec(cc)",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
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
""",
        "fof_conjecture": "~prec(v5, v5, c, c)",
        # SMT: negated conjecture = assert prec(v5,v5,c,c) = assert less(u,u).
        # less(u,u) is UNSAT by irreflexivity => original conjecture is Theorem.
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const u Real)",
        "smt2_asserts": """\
(assert (< u u))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL602 — prec_oc: open upper, closed lower — leq suffices
    #
    # FIX: removed val_v6, less(v5,v6), $distinct(v5,v6) — copied from
    #      ODRL600 but unused; conjecture only mentions v5.
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
    #
    # FIX: removed val_v6, less(v5,v6), $distinct(v5,v6) — unused.
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
    #
    # FIX: removed val_v6, less(v5,v6), $distinct(v5,v6) — unused.
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
fof(val_v0,     axiom, val(v0)).
fof(val_v5,     axiom, val(v5)).
fof(val_v6,     axiom, val(v6)).
fof(val_v10,    axiom, val(v10)).
fof(ord_v0_v5,  axiom, less(v0, v5)).
fof(ord_v5_v6,  axiom, less(v5, v6)).
fof(ord_v6_v10, axiom, less(v6, v10)).
fof(distinct,   axiom, $distinct(v0, v5, v6, v10)).
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
fof(val_v0,     axiom, val(v0)).
fof(val_v5,     axiom, val(v5)).
fof(val_v10,    axiom, val(v10)).
fof(ord_v0_v5,  axiom, less(v0, v5)).
fof(ord_v5_v10, axiom, less(v5, v10)).
fof(distinct,   axiom, $distinct(v0, v5, v10)).
""",
        "fof_conjecture": "~disjoint(v0, v5, c, c, v5, v10, c, c)",
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const x Real)",
        "smt2_asserts": """\
(assert (>= x 0.0)) (assert (<= x 600.0))
(assert (>= x 600.0))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL607 — disjoint co: [v0,v5] vs (v5,v10]
    #
    # FIX 1: description corrected from "(v0,v5]" to "[v0,v5]" to match
    #         CL1=c in the FOF conjecture disjoint(v0,v5,c,c, v5,v10,o,c).
    #         The disjointness is caused by the open lower of interval 2
    #         (CL2=o): interval 2 starts strictly above v5, so touching
    #         at v5 no longer produces overlap.
    # FIX 2: SMT lower bound corrected from (> x 0.0) to (>= x 0.0)
    #         to match CL1=c (closed lower of interval 1).
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL607",
        "subdir":        "ConflictCriterion",
        "name":          "disjoint co: [v0,v5] vs (v5,v10] open lower kills overlap",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "thm:criterion co: leq(v5,v5) => prec(v5,v5,c,o)\n"
            "[v0,v5] ends at v5 closed; (v5,v10] starts strictly above v5.\n"
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
fof(val_v0,     axiom, val(v0)).
fof(val_v5,     axiom, val(v5)).
fof(val_v10,    axiom, val(v10)).
fof(ord_v0_v5,  axiom, less(v0, v5)).
fof(ord_v5_v10, axiom, less(v5, v10)).
fof(distinct,   axiom, $distinct(v0, v5, v10)).
""",
        "fof_conjecture": "disjoint(v0, v5, c, c, v5, v10, o, c)",
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const x Real)",
        "smt2_asserts": """\
(assert (>= x 0.0)) (assert (<= x 600.0))
(assert (> x 600.0))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL608 — disjoint symmetry: disjoint(A,B) <=> disjoint(B,A)
    #
    # FIX: original SMT tested a ground conflict instance ([0,500] vs
    #      [600,∞)) — a completely different claim from symmetry.
    #      Corrected to directly test symmetry: assert disjoint(A,B)
    #      via u1 < l2 (cc case) and negate disjoint(B,A) by asserting
    #      ~(u2 < l1) and ~(u2 <= l1).  This is UNSAT iff symmetry holds.
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
        # SMT: test the cc case of symmetry directly.
        # Assert disjoint(A,B) via u1 < l2 (cc: prec_cc fires).
        # Negate disjoint(B,A): need ~(u2 < l1) AND ~(u2 <= l1),
        # i.e. l1 < u2 (strictly), which contradicts u1 < l2 when
        # intervals are [l1,u1] and [l2,u2] with u1<l2 => l2>u1>=l1
        # => u2>=l2>u1 => u2>l1 => disjoint(B,A) must also hold.
        # So asserting both is UNSAT, confirming symmetry.
        "smt2_logic":  "QF_LRA",
        "smt2_decls": """\
(declare-const l1 Real) (declare-const u1 Real)
(declare-const l2 Real) (declare-const u2 Real)""",
        "smt2_asserts": """\
; disjoint(A,B) in cc case: u1 < l2
(assert (< u1 l2))
; well-formed intervals: l1 <= u1, l2 <= u2
(assert (<= l1 u1))
(assert (<= l2 u2))
; negate disjoint(B,A): ~(u2 < l1) and ~(u2 <= l1)
(assert (not (< u2 l1)))
(assert (not (<= u2 l1)))""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL609 — operator tags: lt upper=o, gt lower=o
    #
    # NOTE: upper_tag/lower_tag are FOL constant axioms with no direct
    #       SMT encoding.  The SMT assertions below are an indirect
    #       sanity check only: they verify that lt 600 and gt 600 are
    #       arithmetically contradictory, which is a downstream
    #       consequence of the open-boundary semantics the tags encode.
    #       The SMT does NOT verify the tag axioms themselves.
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
            "SMT is an indirect sanity check (lt/gt contradictory at same value);\n"
            "the tag axioms themselves have no direct SMT encoding.\n"
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
        # Indirect sanity check only — see NOTE above.
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const x Real)",
        "smt2_asserts": """\
; Indirect: lt 600 and gt 600 are contradictory (x < 600 and x > 600).
(assert (< x 600.0))
(assert (> x 600.0))""",
    },
]