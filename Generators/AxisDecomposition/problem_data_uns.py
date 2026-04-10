"""
problem_data_uns.py
===================
UNS benchmark problems: ODRL760-762 (3 problems).
Category: UNS/
Three Remark 3.4 intra-policy self-contradiction patterns.
A single policy whose constraint set has empty denotation.

Status: Unsatisfiable for all.
"""

PROBLEMS = [
    # ─────────────────────────────────────────────────────────────────
    # ODRL760 — eq 600 AND gteq 700: {600} ∩ [700,∞) = ∅
    # ─────────────────────────────────────────────────────────────────
    {
        "id":          "ODRL760",
        "subdir":      "UNS",
        "name":        "intra-policy: eq 600 AND gteq 700 gives empty denotation",
        "verdict":     "Unsatisfiable",
        "status_fof":  "Unsatisfiable",
        "status_smt":  "unsat",
        "difficulty":  "Easy",
        "description": (
            "Remark 3.4 intra-policy self-contradiction.\n"
            "width eq 600: {600}; width gteq 700: [700,∞).\n"
            "{600} ∩ [700,∞) = ∅ — no request satisfies both.\n"
        ),
        "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:and (
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:eq ; odrl:rightOperand "600"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:gteq ; odrl:rightOperand "700"^^xsd:decimal ]
    ) ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,   axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(val_v700, axiom, val(v700)).
fof(ord_v0_v600,   axiom, less(v0, v600)).
fof(ord_v600_v700, axiom, less(v600, v700)).
fof(distinct, axiom, $distinct(v0, v600, v700)).
fof(contradiction, axiom, less(v700,v600) & less(v600,v700)).
""",
        "fof_conjecture": None,
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (= x 600.0))
(assert (>= x 700.0))""",
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL761 — lteq 600 AND gteq 800: (0,600] ∩ [800,∞) = ∅
    # ─────────────────────────────────────────────────────────────────
    {
        "id":          "ODRL761",
        "subdir":      "UNS",
        "name":        "intra-policy: lteq 600 AND gteq 800 gives empty denotation",
        "verdict":     "Unsatisfiable",
        "status_fof":  "Unsatisfiable",
        "status_smt":  "unsat",
        "difficulty":  "Easy",
        "description": (
            "Remark 3.4 intra-policy self-contradiction.\n"
            "width lteq 600: (0,600]; width gteq 800: [800,∞).\n"
            "(0,600] ∩ [800,∞) = ∅ — no request satisfies both.\n"
        ),
        "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:and (
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:lteq ; odrl:rightOperand "600"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:gteq ; odrl:rightOperand "800"^^xsd:decimal ]
    ) ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,   axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v600,   axiom, less(v0, v600)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v600, v800)).
fof(contradiction, axiom, less(v800,v600) & less(v600,v800)).
""",
        "fof_conjecture": None,
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 600.0))
(assert (>= x 800.0))""",
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL762 — lt 0 (V=InfD): wf_lt condition (ii) violated
    # ─────────────────────────────────────────────────────────────────
    {
        "id":          "ODRL762",
        "subdir":      "UNS",
        "name":        "intra-policy: lt InfD violates wf condition (ii) — empty denotation",
        "verdict":     "Unsatisfiable",
        "status_fof":  "Unsatisfiable",
        "status_smt":  "unsat",
        "difficulty":  "Easy",
        "description": (
            "Remark 3.4 intra-policy self-contradiction via wf_lt condition (ii).\n"
            "width lt v0 (infimum): [infD, v0) with v0=InfD => empty.\n"
            "def:profile condition (ii): op=lt => V != InfD.\n"
            "Violated: denotation is empty, policy is ill-formed.\n"
        ),
        "includes": ["ORD000-0.ax", "WF000-0.ax", "AXIS000-0.ax"],
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lt ; odrl:rightOperand "0"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v1200, axiom, less(v0, v1200)).
fof(distinct, axiom, $distinct(v0, v1200)).
fof(contradiction, axiom, less(v0,v0)).
""",
        "fof_conjecture": None,
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (>= x 0.0))
(assert (< x 0.0))""",
    },
]
