"""
problem_data_wf.py
==================
WellFormedness benchmark problems: ODRL610-617 (8 problems).
Category L: Tests wf/4 and sem_nonempty/4 from WF000-0.ax.
Include pattern:
    include('Axioms/ORD000-0.ax').
    include('Axioms/WF000-0.ax').
    include('Axioms/AXIS000-0.ax').

Problem overview:
  ODRL610 -- wf_eq: V in [InfD,SupD]                                Theorem
  ODRL611 -- wf_lteq: V in [InfD,SupD]                              Theorem
  ODRL612 -- wf_gteq: V in [InfD,SupD]                              Theorem
  ODRL613 -- wf_lt: V != InfD required                              Theorem
  ODRL614 -- wf_lt violation: V=InfD => not wf                      Theorem
  ODRL615 -- wf_gt: V != SupD required                              Theorem
  ODRL616 -- wf_gt violation: V=SupD => not wf                      Theorem
  ODRL617 -- nonempty (FOL-only): wf(lt) => sem_nonempty(lt)        Theorem

Change log (v1.1):
  - ODRL610 SMT: was structurally (v in D) AND (v not in D), tautological
                 regardless of D's bounds.  Now pin-witness pattern:
                 v = 600 AND v not in [0, 1200].
  - ODRL611 SMT: was (<= v 1200) AND (not (<= v 1200)), P AND NOT P.
                 Now pin-witness pattern (same shape as ODRL610).
  - ODRL612 SMT: was (>= v 0) AND (not (>= v 0)), P AND NOT P.
                 Now pin-witness pattern (same shape as ODRL610).
  - ODRL613 SMT: was (<= v 1200) AND (> v 1200), P AND NOT P.
                 Now pin-witness with v=InfD disjunct in the negation.
  - ODRL615 SMT: was (< v 1200) AND (>= v 1200), P AND NOT P.
                 Now pin-witness with v=SupD disjunct in the negation.
  - ODRL617 SMT: was (> v 0) AND (<= v 0), P AND NOT P.  The underlying
                 implication wf(lt) => sem_nonempty(lt) is arithmetically
                 vacuous (both sides reduce to V > InfD), so no semantic
                 SMT encoding exists.  Dropped (FOL-only), like ODRL608 in
                 ConflictCriterion and ODRL637 in Completion's earlier rev.
  - ODRL614 SMT, ODRL616 SMT: kept (irreflexivity-at-a-point pattern;
                 specific value matters, like ODRL637 in Completion).
"""

PROBLEMS = [

    # =====================================================================
    # ODRL610 -- wf_eq: value inside domain is well-formed
    # SMT v1.1: pin-witness pattern.  v = 600 (the specific witness from
    # the FOL conjecture) and assert the negated wf_eq condition:
    # v not in [0, 1200].  Unsat depends on 0 <= 600 <= 1200.
    # =====================================================================
    {
        "id":            "ODRL610",
        "subdir":        "WellFormedness",
        "name":          "wf_eq: value inside domain is well-formed",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "def:well-formed wf_eq: leq(InfD,V) & leq(V,SupD) => wf(eq,V,InfD,SupD)\n"
            "v600 in [v0,v1200] is well-formed for eq operator.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v600,  axiom, val(v600)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct, axiom, $distinct(v0, v600, v1200)).
""",
        "fof_conjecture": "wf(eq, v600, v0, v1200)",
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const v Real)",
        "smt2_asserts": """\
; Pin the witness v=600 and assert the negated wf_eq condition.
; Unsat iff 600 is in [0, 1200].  Verified semantic by perturbation:
; changing v=600 -> v=2000, or upper 1200 -> 500, flips to sat.
(assert (= v 600.0))
(assert (or (< v 0.0) (> v 1200.0)))
""",
    },

    # =====================================================================
    # ODRL611 -- wf_lteq: same shape as wf_eq (V in domain is sufficient)
    # SMT v1.1: same pin-witness pattern as ODRL610.
    # =====================================================================
    {
        "id":            "ODRL611",
        "subdir":        "WellFormedness",
        "name":          "wf_lteq: value inside domain is well-formed",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "def:well-formed wf_lteq: leq(InfD,V) & leq(V,SupD) => wf(lteq,V,InfD,SupD)\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v600,  axiom, val(v600)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct, axiom, $distinct(v0, v600, v1200)).
""",
        "fof_conjecture": "wf(lteq, v600, v0, v1200)",
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const v Real)",
        "smt2_asserts": """\
; Pin-witness: v=600 in [0, 1200] => wf_lteq holds.
(assert (= v 600.0))
(assert (or (< v 0.0) (> v 1200.0)))
""",
    },

    # =====================================================================
    # ODRL612 -- wf_gteq: same shape as wf_eq
    # =====================================================================
    {
        "id":            "ODRL612",
        "subdir":        "WellFormedness",
        "name":          "wf_gteq: value inside domain is well-formed",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "def:well-formed wf_gteq: leq(InfD,V) & leq(V,SupD) => wf(gteq,V,InfD,SupD)\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v600,  axiom, val(v600)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct, axiom, $distinct(v0, v600, v1200)).
""",
        "fof_conjecture": "wf(gteq, v600, v0, v1200)",
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const v Real)",
        "smt2_asserts": """\
; Pin-witness: v=600 in [0, 1200] => wf_gteq holds.
(assert (= v 600.0))
(assert (or (< v 0.0) (> v 1200.0)))
""",
    },

    # =====================================================================
    # ODRL613 -- wf_lt: V strictly above InfD
    # SMT v1.1: pin-witness pattern.  Negated wf_lt is "v outside domain
    # OR v = InfD".  With witness v=600, all three disjuncts fail.
    # =====================================================================
    {
        "id":            "ODRL613",
        "subdir":        "WellFormedness",
        "name":          "wf_lt: V strictly above InfD is well-formed",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "def:well-formed wf_lt: V in [InfD,SupD] & V != InfD => wf(lt,V,InfD,SupD)\n"
            "v600 != v0 and v600 in [v0,v1200] => wf(lt,v600,v0,v1200).\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lt ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v600,  axiom, val(v600)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct, axiom, $distinct(v0, v600, v1200)).
""",
        "fof_conjecture": "wf(lt, v600, v0, v1200)",
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const v Real)",
        "smt2_asserts": """\
; Pin-witness: v=600 outside-domain-or-equal-InfD => negation of wf_lt.
; Three disjuncts: v<0, v>1200, v=0.  All false at v=600 => unsat.
(assert (= v 600.0))
(assert (or (< v 0.0) (> v 1200.0) (= v 0.0)))
""",
    },

    # =====================================================================
    # ODRL614 -- wf_lt violation: V=InfD => NOT wf(lt)
    # SMT v1.1: unchanged.  The (= v 0) AND (< v 0) pattern is
    # irreflexivity-at-a-point: substituting different cutoffs flips the
    # result, so the specific value 0 matters.  Same shape as ODRL637 in
    # Completion's earlier revision.
    # =====================================================================
    {
        "id":            "ODRL614",
        "subdir":        "WellFormedness",
        "name":          "wf_lt violation: V=InfD implies not wf(lt)",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "def:well-formed condition (ii): V=InfD => ~wf(lt,V,InfD,SupD)\n"
            "lt at the infimum gives empty denotation -- not well-formed.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lt ;
      odrl:rightOperand "0"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v1200, axiom, less(v0, v1200)).
fof(distinct, axiom, $distinct(v0, v1200)).
""",
        "fof_conjecture": "~wf(lt, v0, v0, v1200)",
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const v Real)",
        "smt2_asserts": """\
; Irreflexivity at the value 0: lt at InfD requires V != InfD, but v=0
; here.  Mirrors the FOL conjecture's derivation via wf_lt_def's third
; conjunct V != InfD failing at v=InfD=0.
(assert (= v 0.0))
(assert (< v 0.0))
""",
    },

    # =====================================================================
    # ODRL615 -- wf_gt: V strictly below SupD
    # SMT v1.1: pin-witness pattern with v=SupD disjunct.
    # =====================================================================
    {
        "id":            "ODRL615",
        "subdir":        "WellFormedness",
        "name":          "wf_gt: V strictly below SupD is well-formed",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "def:well-formed wf_gt: V in [InfD,SupD] & V != SupD => wf(gt,V,InfD,SupD)\n"
            "v600 != v1200 and v600 in [v0,v1200] => wf(gt,v600,v0,v1200).\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gt ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v600,  axiom, val(v600)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct, axiom, $distinct(v0, v600, v1200)).
""",
        "fof_conjecture": "wf(gt, v600, v0, v1200)",
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const v Real)",
        "smt2_asserts": """\
; Pin-witness: v=600 outside-domain-or-equal-SupD => negation of wf_gt.
; Three disjuncts: v<0, v>1200, v=1200.  All false at v=600 => unsat.
(assert (= v 600.0))
(assert (or (< v 0.0) (> v 1200.0) (= v 1200.0)))
""",
    },

    # =====================================================================
    # ODRL616 -- wf_gt violation: V=SupD => NOT wf(gt)
    # SMT v1.1: unchanged (irreflexivity at value 1200).
    # =====================================================================
    {
        "id":            "ODRL616",
        "subdir":        "WellFormedness",
        "name":          "wf_gt violation: V=SupD implies not wf(gt)",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "def:well-formed condition (iii): V=SupD => ~wf(gt,V,InfD,SupD)\n"
            "gt at the supremum gives empty denotation -- not well-formed.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gt ;
      odrl:rightOperand "1200"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v1200, axiom, less(v0, v1200)).
fof(distinct, axiom, $distinct(v0, v1200)).
""",
        "fof_conjecture": "~wf(gt, v1200, v0, v1200)",
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const v Real)",
        "smt2_asserts": """\
; Irreflexivity at value 1200: gt at SupD requires V != SupD, but v=1200.
; Mirrors the FOL via wf_gt_def's third conjunct V != SupD failing.
(assert (= v 1200.0))
(assert (> v 1200.0))
""",
    },

    # =====================================================================
    # ODRL617 -- nonempty: wf(lt) => sem_nonempty(lt)
    # SMT v1.1: DROPPED (FOL-only).  The implication is arithmetically
    # vacuous because wf_lt's load-bearing condition (V > InfD) IS
    # sem_nonempty_lt's condition.  Any SMT encoding reduces to P AND ~P
    # at the arithmetic level.  Same situation as ODRL608 in
    # ConflictCriterion (OR-commutativity) and ODRL614 in earlier
    # Completion (negative existence).  status_smt = None and the writer
    # should skip the .smt2 file for this problem.
    # =====================================================================
    {
        "id":            "ODRL617",
        "subdir":        "WellFormedness",
        "name":          "nonempty: wf(lt) implies sem_nonempty(lt) (FOL-only)",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    None,
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "lem:totality: wf(lt,V,InfD,SupD) => sem_nonempty(lt,V,InfD,SupD)\n"
            "Every well-formed constraint has a non-empty denotation.\n"
            "FOL-only: no faithful SMT encoding -- the implication is\n"
            "arithmetically vacuous since both sides reduce to V > InfD.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lt ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v600,  axiom, val(v600)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct, axiom, $distinct(v0, v600, v1200)).
""",
        "fof_conjecture": (
            "wf(lt, v600, v0, v1200) => sem_nonempty(lt, v600, v0, v1200)"
        ),
        "smt2_logic":   "",
        "smt2_decls":   "",
        "smt2_asserts": "",
    },
]