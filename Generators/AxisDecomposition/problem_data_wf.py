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
  ODRL610 — wf_eq: V in [InfD,SupD]                    Theorem
  ODRL611 — wf_lteq: V in [InfD,SupD]                  Theorem
  ODRL612 — wf_gteq: V in [InfD,SupD]                  Theorem
  ODRL613 — wf_lt: V != InfD required                  Theorem
  ODRL614 — wf_lt violation: V=InfD => not wf          Theorem
  ODRL615 — wf_gt: V != SupD required                  Theorem
  ODRL616 — wf_gt violation: V=SupD => not wf           Theorem
  ODRL617 — nonempty: wf => sem_nonempty (all 5 ops)   Theorem

SMT convention (all Theorem problems):
    assert domain hypotheses + negated conjecture → UNSAT.
    The negated conjecture is the arithmetic negation of what
    wf/sem_nonempty asserts, residualised under the hypotheses.

Fixes vs. original:
  ODRL610: SMT (assert (not (= v v))) was tautologically false (v≠v is
           always impossible) — tested nothing meaningful.
           Fixed to (assert (or (< v 0.0) (> v 1200.0))), the correct
           negation of wf_eq: V ∉ [InfD, SupD].
  ODRL613: SMT (assert (not (< v 1200.0))) = v >= 1200.  Combined with
           (assert (<= v 1200.0)) this gives v = 1200, which satisfies
           (assert (> v 0.0)) → SAT.  status_smt claimed "unsat" — wrong.
           Fixed to (assert (> v 1200.0)): the correct residual negation
           of wf_lt under hypotheses v > 0 & v <= 1200, which is UNSAT.
  ODRL615: SMT (assert (not (> v 0.0))) = v <= 0.  Combined with
           (assert (>= v 0.0)) gives v = 0, which satisfies
           (assert (< v 1200.0)) → SAT.  status_smt claimed "unsat" — wrong.
           Fixed to (assert (>= v 1200.0)): the correct residual negation
           of wf_gt under hypotheses v >= 0 & v < 1200, which is UNSAT.
  ODRL617: Same root bug as ODRL613: (assert (not (< v 1200.0))) = v >= 1200
           is SAT (v = 1200 satisfies all three asserts).
           Fixed to (assert (<= v 0.0)): negated sem_nonempty(lt) under
           hypothesis v > 0 means the interval [InfD,V) would be empty,
           i.e., V <= InfD → v <= 0, which contradicts v > 0 → UNSAT.
"""

PROBLEMS = [
    # ─────────────────────────────────────────────────────────────────
    # ODRL610 — wf_eq: value inside domain is well-formed
    #
    # FIX: SMT (assert (not (= v v))) = v≠v is tautologically false —
    #      always UNSAT regardless of domain, tests nothing.
    #      Replaced with (assert (or (< v 0.0) (> v 1200.0))):
    #      the negated wf_eq condition V ∉ [InfD,SupD].
    #      Combined with v >= 0 & v <= 1200 → UNSAT ✓
    # ─────────────────────────────────────────────────────────────────
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
            "def:profile wf_eq: leq(InfD,V) & leq(V,SupD) => wf(eq,V,InfD,SupD)\n"
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
(assert (>= v 0.0))
(assert (<= v 1200.0))
(assert (or (< v 0.0) (> v 1200.0)))""",
    },

    # ─────────────────────────────────────────────────────────────────
    # ODRL611 — wf_lteq
    # ─────────────────────────────────────────────────────────────────
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
            "def:profile wf_lteq: leq(InfD,V) & leq(V,SupD) => wf(lteq,V,InfD,SupD)\n"
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
(assert (>= v 0.0))
(assert (<= v 1200.0))
(assert (not (<= v 1200.0)))""",
    },

    # ─────────────────────────────────────────────────────────────────
    # ODRL612 — wf_gteq
    # ─────────────────────────────────────────────────────────────────
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
            "def:profile wf_gteq: leq(InfD,V) & leq(V,SupD) => wf(gteq,V,InfD,SupD)\n"
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
(assert (>= v 0.0))
(assert (>= 1200.0 v))
(assert (not (>= v 0.0)))""",
    },

    # ─────────────────────────────────────────────────────────────────
    # ODRL613 — wf_lt: V strictly inside domain
    #
    # FIX: SMT (assert (not (< v 1200.0))) = v >= 1200.
    #      Combined with (assert (<= v 1200.0)): v = 1200.
    #      Combined with (assert (> v 0.0)): v=1200 satisfies all → SAT.
    #      status_smt was "unsat" — wrong.
    #      Fix: (assert (> v 1200.0)).
    #      Residual negation of wf_lt given v > 0 & v <= 1200:
    #        ~wf_lt = v<0 | v>1200 | v=0; hypotheses rule out v<0 and v=0;
    #        remainder is v > 1200. With v <= 1200 → UNSAT ✓
    # ─────────────────────────────────────────────────────────────────
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
            "def:profile wf_lt condition (ii): V != InfD required.\n"
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
(assert (> v 0.0))
(assert (<= v 1200.0))
(assert (> v 1200.0))""",
    },

    # ─────────────────────────────────────────────────────────────────
    # ODRL614 — wf_lt violation: V=InfD => NOT wf(lt)
    # ─────────────────────────────────────────────────────────────────
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
            "def:profile condition (ii): V=InfD => ~wf(lt,V,InfD,SupD)\n"
            "lt at the infimum gives empty denotation — not well-formed.\n"
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
        # Tests that denotation of lt InfD = [InfD,InfD) = ∅:
        # no v satisfies v >= 0 and v < 0 simultaneously.
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const v Real)",
        "smt2_asserts": """\
(assert (= v 0.0))
(assert (< v 0.0))""",
    },

    # ─────────────────────────────────────────────────────────────────
    # ODRL615 — wf_gt: V strictly below SupD
    #
    # FIX: SMT (assert (not (> v 0.0))) = v <= 0.
    #      Combined with (assert (>= v 0.0)): v = 0.
    #      Combined with (assert (< v 1200.0)): 0 < 1200 ✓ → SAT.
    #      status_smt was "unsat" — wrong.
    #      Fix: (assert (>= v 1200.0)).
    #      Residual negation of wf_gt given v >= 0 & v < 1200:
    #        ~wf_gt = v<0 | v>1200 | v=1200; hypotheses rule out v<0,
    #        v>1200, and v=1200; so negation is (>= v 1200.0).
    #      With v < 1200 → UNSAT ✓
    # ─────────────────────────────────────────────────────────────────
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
            "def:profile condition (iii): V != SupD required for gt.\n"
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
(assert (>= v 0.0))
(assert (< v 1200.0))
(assert (>= v 1200.0))""",
    },

    # ─────────────────────────────────────────────────────────────────
    # ODRL616 — wf_gt violation: V=SupD => NOT wf(gt)
    # ─────────────────────────────────────────────────────────────────
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
            "def:profile condition (iii): V=SupD => ~wf(gt,V,InfD,SupD)\n"
            "gt at the supremum gives empty denotation — not well-formed.\n"
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
        # Tests that denotation of gt SupD = (SupD,∞) = ∅:
        # no v satisfies v = 1200 and v > 1200 simultaneously.
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const v Real)",
        "smt2_asserts": """\
(assert (= v 1200.0))
(assert (> v 1200.0))""",
    },

    # ─────────────────────────────────────────────────────────────────
    # ODRL617 — nonempty: wf(lt) => sem_nonempty(lt)
    #
    # FIX: SMT (assert (not (< v 1200.0))) = v >= 1200.
    #      Same root bug as ODRL613: v=1200 satisfies all three
    #      asserts → SAT. status_smt was "unsat" — wrong.
    #      Fix: (assert (<= v 0.0)).
    #      sem_nonempty(lt, V, InfD, SupD) means [InfD, V) is non-empty,
    #      i.e., V > InfD. Given hypothesis v > 0 (V > InfD = 0),
    #      negated sem_nonempty = V <= InfD = v <= 0.
    #      With v > 0 → UNSAT ✓
    # ─────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL617",
        "subdir":        "WellFormedness",
        "name":          "nonempty: wf(lt) implies sem_nonempty(lt)",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "lem:totality: wf(lt,V,InfD,SupD) => sem_nonempty(lt,V,InfD,SupD)\n"
            "Every well-formed constraint has a non-empty denotation.\n"
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
        # sem_nonempty(lt,V,InfD,SupD): the interval [InfD,V) is non-empty.
        # Arithmetic equivalent: V > InfD (= v > 0, given by hypothesis).
        # Negated: V <= InfD = v <= 0. Contradicts hypothesis v > 0 → UNSAT.
        "smt2_logic":  "QF_LRA",
        "smt2_decls":  "(declare-const v Real)",
        "smt2_asserts": """\
(assert (> v 0.0))
(assert (<= v 1200.0))
(assert (<= v 0.0))""",
    },
]