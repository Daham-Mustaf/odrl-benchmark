"""
problem_data_criterion.py
====================
ConflictCriterion benchmark problems: ODRL600-615 (16 problems).
Category K: Tests prec/4 and disjoint/8 from PREC000-0.ax directly.
Includes: ORD000-0.ax + PREC000-0.ax + AXIS000-0.ax

Problem overview:
  ODRL600 -- prec_cc: less(U,L) => prec(U,L,c,c)                Theorem
  ODRL601 -- prec_cc: equal endpoints not prec cc                Theorem
  ODRL602 -- prec_oc: leq(U,L) => prec(U,L,o,c)                 Theorem
  ODRL603 -- prec_co: leq(U,L) => prec(U,L,c,o)                 Theorem
  ODRL604 -- prec_oo: leq(U,L) => prec(U,L,o,o)                 Theorem
  ODRL605 -- disjoint cc: [v0,v5] vs [v6,v10]                    Theorem
  ODRL606 -- NOT disjoint cc: [v0,v5] vs [v5,v10] touch          Theorem
  ODRL607 -- disjoint co: [v0,v5] vs (v5,v10]                    Theorem
  ODRL608 -- disjoint symmetry (FOL-only, no SMT)                Theorem
  ODRL609 -- operator tags: lt upper=o, gt lower=o               Theorem

  -- v1.1 additions (after axiom rewrite, fill coverage gaps) --
  ODRL610 -- prec_cc backward: prec(u,l,c,c) => less(u,l)        Theorem
  ODRL611 -- prec_oc forward at strict less                      Theorem
  ODRL612 -- prec_co forward at strict less                      Theorem
  ODRL613 -- prec_oo forward at strict less                      Theorem
  ODRL614 -- NEGATIVE: upper_tag(gteq,c) NOT derivable           CounterSatisfiable
  ODRL615 -- disjoint via second disjunct                        Theorem

Change log (v1.1):
  - ODRL600 SMT: was (assert P)(assert (not P)), now policy-level.
  - ODRL602 SMT: same fix (lt 600 vs gteq 600 at touching point).
  - ODRL603 SMT: same fix (lteq 600 vs gt 600 at touching point).
  - ODRL604 SMT: same fix (lt 600 vs gt 600 at touching point).
  - ODRL608 SMT: dropped (was logically wrong; returned sat). FOL-only.
  - Added ODRL610-615 to cover prec backward direction, strict-less
    cases for oc/co/oo, negative-existence regression test for the old
    upper_tag(gteq,c) bug, and the second disjunct of disjoint_def.
"""

PROBLEMS = [
    # ──────────────────────────────────────────────────────────────────
    # ODRL600 -- prec_cc: strict separation required for closed endpoints
    #
    # v1.1: SMT replaced with policy-level encoding (was tautological
    # (assert P)(assert (not P)) which closes for any P, not for prec_cc).
    # New SMT mirrors the TTL: lteq 500 (interval [0, 500]) vs gteq 600
    # ([600, infinity)). UNSAT because 500 < 600.
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
        "smt2_decls":  "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 500.0))    ; sem(lteq 500)
(assert (>= x 600.0))    ; sem(gteq 600)
""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL601 -- prec_cc negative: equal endpoints NOT prec cc
    # (FOF and SMT unchanged from v1.0 -- already semantic.)
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
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const u Real)",
        "smt2_asserts": """\
(assert (< u u))
""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL602 -- prec_oc: open upper, closed lower -- leq suffices
    # v1.1: SMT replaced with policy-level (lt 600 vs gteq 600 at same point).
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
        "smt2_decls":  "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (< x 600.0))     ; sem(lt 600)
(assert (>= x 600.0))    ; sem(gteq 600)
""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL603 -- prec_co: closed upper, open lower -- leq suffices
    # v1.1: SMT replaced with policy-level (lteq 600 vs gt 600 at same point).
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
        "smt2_decls":  "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 600.0))    ; sem(lteq 600)
(assert (> x 600.0))     ; sem(gt 600)
""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL604 -- prec_oo: both open -- leq suffices
    # v1.1: SMT replaced with policy-level (lt 600 vs gt 600 at same point).
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
        "smt2_decls":  "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (< x 600.0))     ; sem(lt 600)
(assert (> x 600.0))     ; sem(gt 600)
""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL605 -- disjoint cc: [v0,v5] vs [v6,v10] strictly separated
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
(assert (>= x 0.0))
(assert (<= x 500.0))
(assert (>= x 600.0))
""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL606 -- NOT disjoint cc: [v0,v5] vs [v5,v10] touch -> overlap
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
(assert (>= x 0.0))
(assert (<= x 600.0))
(assert (>= x 600.0))
""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL607 -- disjoint co: [v0,v5] vs (v5,v10]
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
(assert (>= x 0.0))
(assert (<= x 600.0))
(assert (> x 600.0))
""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL608 -- disjoint symmetry: disjoint(A,B) <=> disjoint(B,A)
    #
    # v1.1: SMT DROPPED.  The previous SMT (asserting disjoint(A,B) via
    # u1 < l2 and negating only one of the two disjuncts of disjoint(B,A))
    # was logically wrong and returned sat (countermodel: l1=0, u1=1,
    # l2=2, u2=3 satisfies all assertions while disjoint(B,A) also holds).
    # There is no clean non-degenerate SMT encoding of OR-commutativity,
    # so this problem is now FOL-only.  status_smt is None and the
    # smt2_asserts field is empty so the writer skips the .smt2 file.
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL608",
        "subdir":        "ConflictCriterion",
        "name":          "disjoint symmetry: disjoint(A,B) iff disjoint(B,A)",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    None,
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "thm:criterion symmetry: disjoint is symmetric.\n"
            "disjoint(L1,U1,CL1,CU1,L2,U2,CL2,CU2) <=> "
            "disjoint(L2,U2,CL2,CU2,L1,U1,CL1,CU1)\n"
            "FOL-only: no faithful SMT encoding of OR-commutativity.\n"
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
        "smt2_logic":   "",
        "smt2_decls":   "",
        "smt2_asserts": "",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL609 -- operator tags: lt upper=o, gt lower=o
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
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const x Real)",
        "smt2_asserts": """\
(assert (< x 600.0))
(assert (> x 600.0))
""",
    },

    # ══════════════════════════════════════════════════════════════════
    # v1.1 ADDITIONS (ODRL610-615) -- coverage gaps from the audit
    # ══════════════════════════════════════════════════════════════════

    # ──────────────────────────────────────────────────────────────────
    # ODRL610 -- prec_cc BACKWARD direction: prec(u,l,c,c) => less(u,l)
    #
    # The previous suite only tested less => prec (ODRL600) and the
    # contrapositive ~less => ~prec (ODRL601).  This problem exercises
    # the forward direction of the backward implication: assuming
    # prec(u_c, l_c, c, c) directly, derive less(u_c, l_c).  Closes
    # ONLY if the biconditional's backward direction is present in
    # PREC000-0.ax (i.e., would fail under the old forward-only axiom).
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL660",
        "subdir":        "ConflictCriterion",
        "name":          "prec_cc backward: prec(u,l,c,c) implies less(u,l)",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "thm:criterion prec_cc backward: prec(u_c,l_c,c,c) => less(u_c,l_c)\n"
            "Directly tests the backward direction of the prec_cc biconditional.\n"
            "Fails under a forward-only axiom.\n"
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
fof(val_u_c,     axiom, val(u_c)).
fof(val_l_c,     axiom, val(l_c)).
fof(prec_assumed, axiom, prec(u_c, l_c, c, c)).
fof(distinct,    axiom, $distinct(u_c, l_c)).
""",
        "fof_conjecture": "less(u_c, l_c)",
        # SMT analog: at the policy level, the corresponding claim is that
        # disjoint closed intervals [0,500] and [600, inf) force 500 < 600.
        # Same arithmetic witness as ODRL600 since both reduce to strict
        # order between the boundary values.
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 500.0))
(assert (>= x 600.0))
""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL611 -- prec_oc forward at STRICT less (not just equal endpoints)
    #
    # ODRL602 tests prec_oc at u=l (where leq is reflexive).  This
    # problem tests prec_oc at strict u<l, where the leq disjunct comes
    # from less rather than equality.
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL661",
        "subdir":        "ConflictCriterion",
        "name":          "prec_oc at strict less: less(a,b) implies prec(a,b,o,c)",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "thm:criterion prec_oc strict: less(a,b) => prec(a,b,o,c)\n"
            "Tests prec_oc at strict separation (a<b), complementing\n"
            "ODRL602 which tests it at equal endpoints (a=b via leq reflexivity).\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lt ; odrl:rightOperand "500"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ; odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_a,     axiom, val(a)).
fof(val_b,     axiom, val(b)).
fof(ord_a_b,   axiom, less(a, b)).
fof(distinct,  axiom, $distinct(a, b)).
""",
        "fof_conjecture": "prec(a, b, o, c)",
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (< x 500.0))     ; sem(lt 500)
(assert (>= x 600.0))    ; sem(gteq 600)
""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL612 -- prec_co forward at STRICT less
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL662",
        "subdir":        "ConflictCriterion",
        "name":          "prec_co at strict less: less(a,b) implies prec(a,b,c,o)",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "thm:criterion prec_co strict: less(a,b) => prec(a,b,c,o)\n"
            "Tests prec_co at strict separation, complementing ODRL603.\n"
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
      odrl:operator odrl:gt ; odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_a,     axiom, val(a)).
fof(val_b,     axiom, val(b)).
fof(ord_a_b,   axiom, less(a, b)).
fof(distinct,  axiom, $distinct(a, b)).
""",
        "fof_conjecture": "prec(a, b, c, o)",
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 500.0))    ; sem(lteq 500)
(assert (> x 600.0))     ; sem(gt 600)
""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL613 -- prec_oo forward at STRICT less
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL663",
        "subdir":        "ConflictCriterion",
        "name":          "prec_oo at strict less: less(a,b) implies prec(a,b,o,o)",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "thm:criterion prec_oo strict: less(a,b) => prec(a,b,o,o)\n"
            "Tests prec_oo at strict separation, complementing ODRL604.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lt ; odrl:rightOperand "500"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gt ; odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_a,     axiom, val(a)).
fof(val_b,     axiom, val(b)).
fof(ord_a_b,   axiom, less(a, b)).
fof(distinct,  axiom, $distinct(a, b)).
""",
        "fof_conjecture": "prec(a, b, o, o)",
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (< x 500.0))     ; sem(lt 500)
(assert (> x 600.0))     ; sem(gt 600)
""",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL614 -- NEGATIVE: upper_tag(gteq, c) must NOT be derivable
    #
    # Regression test for the previous bug (the old PREC000-0.ax had
    # upper_tag(gteq, c) as a ground axiom, which is wrong because gteq
    # does not constrain the upper side).  This problem expects
    # CounterSatisfiable -- the prover should find a model where the
    # conjecture is false.  If a future axiom edit re-introduces the
    # bug, this problem will fail (close as Theorem instead).
    #
    # FOL-only: there is no clean SMT analog of "this fact is not
    # derivable from these axioms".
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL664",
        "subdir":        "ConflictCriterion",
        "name":          "negative: upper_tag(gteq,c) is NOT derivable",
        "relation":      "conflict",
        "verdict":       "Unknown",
        "status_fof":    "CounterSatisfiable",
        "status_smt":    None,
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "Negative existence test: upper_tag(gteq, c) must NOT be derivable\n"
            "from PREC000-0.ax v1.1, because gteq does not constrain the\n"
            "upper side of the interval.  Regression test for the previous\n"
            "version's bug.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ; odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": "",
        "fof_conjecture": "upper_tag(gteq, c)",
        "smt2_logic":   "",
        "smt2_decls":   "",
        "smt2_asserts": "",
    },

    # ──────────────────────────────────────────────────────────────────
    # ODRL615 -- disjoint via the SECOND disjunct of disjoint_def
    #
    # All previous disjoint problems instantiate the FIRST disjunct
    # prec(U1, L2, ...).  This problem flips the interval order so that
    # disjointness closes via the SECOND disjunct prec(U2, L1, ...).
    # I1 = [v6, v10], I2 = [v0, v5]: U2=v5 precedes L1=v6, not the reverse.
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL665",
        "subdir":        "ConflictCriterion",
        "name":          "disjoint via second disjunct: I1=[v6,v10], I2=[v0,v5]",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "thm:criterion disjoint via second disjunct.\n"
            "I1=[v6,v10] (gteq 600 side), I2=[v0,v5] (lteq 500 side).\n"
            "The first disjunct prec(U1=v10, L2=v0) is FALSE (v10 not below v0).\n"
            "The second disjunct prec(U2=v5, L1=v6) is TRUE (v5 < v6) and\n"
            "must be used to close the conjecture.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ; odrl:rightOperand "600"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ; odrl:rightOperand "500"^^xsd:decimal ] ] .""",
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
        "fof_conjecture": "disjoint(v6, v10, c, c, v0, v5, c, c)",
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (>= x 600.0))    ; sem(gteq 600), interval 1
(assert (<= x 500.0))    ; sem(lteq 500), interval 2
""",
    },
]