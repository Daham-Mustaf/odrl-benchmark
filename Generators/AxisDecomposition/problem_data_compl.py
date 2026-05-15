"""
problem_data_compl.py
=====================
Completion benchmark problems: ODRL630-637 (8 problems).
Category O: Tests completion_compatible/3, completion_conflict/4,
sharpness, and monotone_conflict from COMPL000-0.ax.
Include pattern:
    include('Axioms/ORD000-0.ax').
    include('Axioms/COMPL000-0.ax').
    include('Axioms/AXIS000-0.ax').
Problem overview:
  ODRL630 — completion_compat: V in [InfD,SupD] => completion_compatible  Theorem
  ODRL631 — completion_conflict: U<V in domain => completion_conflict      Theorem
  ODRL632 — sharpness_compat: completion yields Compatible                 Theorem
  ODRL633 — sharpness_conflict: completion yields Conflict                 Theorem
  ODRL634 — monotone_conflict: subsumes + conflict => conflict             Theorem
  ODRL635 — unknown_sound: no constrained axis conflicts => Unknown        Theorem
  ODRL636 — completion_compat at boundary: V=InfD works for eq             Theorem
  ODRL637 — completion_conflict requires U<V strictly                      Theorem
"""

# Real UF SMT encoding for ODRL635 (box_verdict verdict-algebra)
from smt_axioms import (
    PREAMBLE_VERDICT, DECL_BOX_VERDICT, AXIOM_BOX_UNKNOWN,
)

PROBLEMS = [
    # ─────────────────────────────────────────────────────────────────
    # ODRL630 — completion_compat: V in domain => completion_compatible
    # ─────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL630",
        "subdir":        "Completion",
        "name":          "completion_compat: value in domain gives compatible completion",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["ORD000-0.ax", "COMPL000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "def:completion: leq(v0,v600) & leq(v600,v1200)\n"
            "=> completion_compatible(v600, v0, v1200).\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ; odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v600,  axiom, val(v600)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct, axiom, $distinct(v0, v600, v1200)).
""",
        "fof_conjecture": "completion_compatible(v600, v0, v1200)",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const v Real)",
        "smt2_asserts": """\
(assert (>= v 0.0)) (assert (<= v 1200.0))
(assert (not (and (>= v 0.0) (<= v 1200.0))))""",
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL631 — completion_conflict: U<V in domain => completion_conflict
    # ─────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL631",
        "subdir":        "Completion",
        "name":          "completion_conflict: U<V in domain gives conflict completion",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["ORD000-0.ax", "COMPL000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "def:completion: less(v400,v800) & both in [v0,v1200]\n"
            "=> completion_conflict(v400, v800, v0, v1200).\n"
            "Policy1 gets lteq v400, Policy2 gets gteq v800 => disjoint.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ; odrl:rightOperand "400"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v400,  axiom, val(v400)).
fof(val_v800,  axiom, val(v800)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v400,    axiom, less(v0, v400)).
fof(ord_v0_v800,    axiom, less(v0, v800)).
fof(ord_v400_v800,  axiom, less(v400, v800)).
fof(ord_v800_v1200, axiom, less(v800, v1200)).
fof(distinct, axiom, $distinct(v0, v400, v800, v1200)).
""",
        "fof_conjecture": "completion_conflict(v400, v800, v0, v1200)",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const u Real)\n(declare-const v Real)",
        "smt2_asserts": """\
(assert (>= u 0.0)) (assert (<= u 1200.0))
(assert (>= v 0.0)) (assert (<= v 1200.0))
(assert (< u v))
(assert (not (< u v)))""",
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL632 — sharpness_compat: U<V in domain => completion_compatible(U)
    # ─────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL632",
        "subdir":        "Completion",
        "name":          "sharpness_compat: U<V in domain implies compatible completion exists",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["ORD000-0.ax", "COMPL000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "thm:unknown-sound sharpness_compat:\n"
            "leq(v0,v400) & less(v400,v800) & leq(v800,v1200)\n"
            "=> completion_compatible(v400, v0, v1200).\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ; odrl:rightOperand "400"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v400,  axiom, val(v400)).
fof(val_v800,  axiom, val(v800)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v400,    axiom, less(v0, v400)).
fof(ord_v400_v800,  axiom, less(v400, v800)).
fof(ord_v800_v1200, axiom, less(v800, v1200)).
fof(distinct, axiom, $distinct(v0, v400, v800, v1200)).
""",
        "fof_conjecture": "completion_compatible(v400, v0, v1200)",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const v Real)",
        "smt2_asserts": """\
(assert (>= v 0.0)) (assert (<= v 1200.0))
(assert (not (and (>= v 0.0) (<= v 1200.0))))""",
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL633 — sharpness_conflict: U<V in domain => conflict completion exists
    # ─────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL633",
        "subdir":        "Completion",
        "name":          "sharpness_conflict: U<V in domain implies conflict completion exists",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["ORD000-0.ax", "COMPL000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "thm:unknown-sound sharpness_conflict:\n"
            "leq(v0,v400) & less(v400,v800) & leq(v800,v1200)\n"
            "=> completion_conflict(v400, v800, v0, v1200).\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ; odrl:rightOperand "400"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v400,  axiom, val(v400)).
fof(val_v800,  axiom, val(v800)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v400,    axiom, less(v0, v400)).
fof(ord_v400_v800,  axiom, less(v400, v800)).
fof(ord_v800_v1200, axiom, less(v800, v1200)).
fof(distinct, axiom, $distinct(v0, v400, v800, v1200)).
""",
        "fof_conjecture": "completion_conflict(v400, v800, v0, v1200)",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const u Real)\n(declare-const v Real)",
        "smt2_asserts": """\
(assert (>= u 0.0)) (assert (<= u 1200.0))
(assert (>= v 0.0)) (assert (<= v 1200.0))
(assert (< u v))
(assert (not (< u v)))""",
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL634 — monotone_conflict: axis_subsumes + conflict => conflict
    # ─────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL634",
        "subdir":        "Completion",
        "name":          "monotone_conflict: subsumes and conflict implies conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "includes":      ["ORD000-0.ax", "COMPL000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "prop:monotone: [v200,v400] ⊆ [v0,v600] and [v0,v600] conflicts [v800,v1200]\n"
            "=> [v200,v400] conflicts [v800,v1200].\n"
            "monotone_conflict: axis_subsumes(A1,A2) & axis_conflict(A2,B) => axis_conflict(A1,B).\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ; odrl:rightOperand "400"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ; odrl:rightOperand "800"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v200,  axiom, val(v200)).
fof(val_v400,  axiom, val(v400)).
fof(val_v600,  axiom, val(v600)).
fof(val_v800,  axiom, val(v800)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v200,    axiom, less(v0, v200)).
fof(ord_v0_v400,    axiom, less(v0, v400)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v0_v800,    axiom, less(v0, v800)).
fof(ord_v200_v400,  axiom, less(v200, v400)).
fof(ord_v200_v600,  axiom, less(v200, v600)).
fof(ord_v200_v800,  axiom, less(v200, v800)).
fof(ord_v400_v600,  axiom, less(v400, v600)).
fof(ord_v400_v800,  axiom, less(v400, v800)).
fof(ord_v600_v800,  axiom, less(v600, v800)).
fof(ord_v800_v1200, axiom, less(v800, v1200)).
fof(distinct, axiom, $distinct(v0, v200, v400, v600, v800, v1200)).
""",
        "fof_conjecture": (
            "axis_conflict(v200, v400, v800, v1200)"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (>= x 200.0)) (assert (<= x 400.0))
(assert (>= x 800.0))""",
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL635 — unknown_sound: Unknown is correctly assigned
    # ─────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL635",
        "subdir":        "Completion",
        "name":          "unknown_sound: box verdict is Unknown when axis unconstrained",
        "relation":      "verdict_algebra",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["ORD000-0.ax", "COMPL000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "thm:unknown-sound: box_verdict(compatible, unknown) = unknown.\n"
            "One axis compatible, one axis unconstrained => Unknown overall.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ; odrl:permission [ odrl:action odrl:use ] .""",
        "fof_extra_decls": "",
        "fof_conjecture": "box_verdict(compatible, unknown) = unknown",
        "smt2_logic":   "UF",
        "smt2_decls":   PREAMBLE_VERDICT + DECL_BOX_VERDICT,
        "smt2_asserts": AXIOM_BOX_UNKNOWN + "; Negated conjecture\n"
                            "(assert (not (= (box_verdict compatible unknown) unknown)))",
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL636 — completion_compat at InfD (boundary V=InfD is ok for eq)
    # ─────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL636",
        "subdir":        "Completion",
        "name":          "completion_compat at InfD: V=InfD is valid for eq completion",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["ORD000-0.ax", "COMPL000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "def:completion: V=InfD is in [InfD,SupD] so completion_compatible holds.\n"
            "completion_compatible(v0, v0, v1200) — infimum as eq value.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ; odrl:rightOperand "0"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v1200, axiom, less(v0, v1200)).
fof(distinct, axiom, $distinct(v0, v1200)).
""",
        "fof_conjecture": "completion_compatible(v0, v0, v1200)",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const v Real)",
        "smt2_asserts": """\
(assert (= v 0.0))
(assert (not (and (>= v 0.0) (<= v 1200.0))))""",
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL637 — completion_conflict requires strict U<V
    # ─────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL637",
        "subdir":        "Completion",
        "name":          "completion_conflict requires strict U<V: U=V gives no conflict",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["ORD000-0.ax", "COMPL000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "def:completion: less(U,V) is required — equal values give no conflict.\n"
            "~completion_conflict(v600, v600, v0, v1200) because ~less(v600,v600).\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ; odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v600,  axiom, val(v600)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct, axiom, $distinct(v0, v600, v1200)).
""",
        "fof_conjecture": "![U,V,InfD,SupD]: (~less(U,U))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const u Real)",
        "smt2_asserts": """\
(assert (= u 600.0))
(assert (< u 600.0))""",
    },
]