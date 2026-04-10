"""
problem_data_sat.py
===================
SAT benchmark problems: ODRL750-754 (5 problems).
Category: SAT/
One consistency witness per axiom layer — confirms each axiom file
is satisfiable in isolation with ground constants.

Include patterns vary per problem (one axiom layer each).
Status: Satisfiable for all.
"""

PROBLEMS = [
    # ─────────────────────────────────────────────────────────────────
    # ODRL750 — ORD000 strict total order is satisfiable
    # ─────────────────────────────────────────────────────────────────
    {
        "id":          "ODRL750",
        "subdir":      "SAT",
        "name":        "ORD000 strict total order is satisfiable",
        "verdict":     "Satisfiable",
        "status_fof":  "Satisfiable",
        "status_smt":  "sat",
        "difficulty":  "Easy",
        "description": (
            "The strict total order axioms of ORD000-0.ax are consistent.\n"
            "Witness: v0 < v600 < v1200 forms a valid strict total order.\n"
        ),
        "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:ODRL750 a odrl:Set ; odrl:permission [ odrl:action odrl:use ] .""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v600,  axiom, val(v600)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct, axiom, $distinct(v0, v600, v1200)).
""",
        "fof_conjecture": None,
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (< 0.0 600.0))
(assert (< 600.0 1200.0))""",
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL751 — AXIS000 verdict algebra is satisfiable
    # ─────────────────────────────────────────────────────────────────
    {
        "id":          "ODRL751",
        "subdir":      "SAT",
        "name":        "AXIS000 verdict algebra is satisfiable",
        "verdict":     "Satisfiable",
        "status_fof":  "Satisfiable",
        "status_smt":  "sat",
        "difficulty":  "Easy",
        "description": (
            "The AXIS000 interval and verdict axioms are consistent.\n"
            "Witness: [v0,v600] and [v400,v800] overlap at v400..v600.\n"
        ),
        "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:ODRL751 a odrl:Set ; odrl:permission [ odrl:action odrl:use ] .""",
        "fof_extra_decls": """\
fof(val_v0,   axiom, val(v0)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v400,   axiom, less(v0, v400)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v400, v600, v800)).
fof(compat_witness, axiom, axis_compatible(v0, v600, v400, v800)).
""",
        "fof_conjecture": None,
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (>= x 0.0)) (assert (<= x 600.0))
(assert (>= x 400.0)) (assert (<= x 800.0))""",
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL752 — PREC000 endpoint precedence is satisfiable
    # ─────────────────────────────────────────────────────────────────
    {
        "id":          "ODRL752",
        "subdir":      "SAT",
        "name":        "PREC000 endpoint precedence is satisfiable",
        "verdict":     "Satisfiable",
        "status_fof":  "Satisfiable",
        "status_smt":  "sat",
        "difficulty":  "Easy",
        "description": (
            "The PREC000 endpoint precedence axioms are consistent.\n"
            "Witness: prec(v5,v6,c,c) holds since less(v5,v6).\n"
        ),
        "includes": ["ORD000-0.ax", "PREC000-0.ax", "AXIS000-0.ax"],
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:ODRL752 a odrl:Set ; odrl:permission [ odrl:action odrl:use ] .""",
        "fof_extra_decls": """\
fof(val_v5, axiom, val(v5)).
fof(val_v6, axiom, val(v6)).
fof(ord_v5_v6, axiom, less(v5, v6)).
fof(distinct, axiom, $distinct(v5, v6)).
fof(prec_witness, axiom, prec(v5, v6, c, c)).
""",
        "fof_conjecture": None,
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const u Real)\n(declare-const l Real)",
        "smt2_asserts": """\
(assert (= u 5.0)) (assert (= l 6.0))
(assert (< u l))""",
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL753 — WF000 well-formedness is satisfiable
    # ─────────────────────────────────────────────────────────────────
    {
        "id":          "ODRL753",
        "subdir":      "SAT",
        "name":        "WF000 well-formedness axioms are satisfiable",
        "verdict":     "Satisfiable",
        "status_fof":  "Satisfiable",
        "status_smt":  "sat",
        "difficulty":  "Easy",
        "description": (
            "The WF000 well-formedness axioms are consistent.\n"
            "Witness: wf(eq,v600,v0,v1200) holds — v600 in [v0,v1200].\n"
        ),
        "includes": ["ORD000-0.ax", "WF000-0.ax", "AXIS000-0.ax"],
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:ODRL753 a odrl:Set ; odrl:permission [ odrl:action odrl:use ] .""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v600,  axiom, val(v600)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct, axiom, $distinct(v0, v600, v1200)).
fof(wf_witness, axiom, wf(eq, v600, v0, v1200)).
""",
        "fof_conjecture": None,
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const v Real)",
        "smt2_asserts": """\
(assert (>= v 0.0)) (assert (<= v 1200.0))
(assert (= v 600.0))""",
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL754 — COMPL000 completion axioms are satisfiable
    # ─────────────────────────────────────────────────────────────────
    {
        "id":          "ODRL754",
        "subdir":      "SAT",
        "name":        "COMPL000 completion axioms are satisfiable",
        "verdict":     "Satisfiable",
        "status_fof":  "Satisfiable",
        "status_smt":  "sat",
        "difficulty":  "Easy",
        "description": (
            "The COMPL000 completion axioms are consistent.\n"
            "Witness: completion_compatible(v600,v0,v1200) holds.\n"
        ),
        "includes": ["ORD000-0.ax", "COMPL000-0.ax", "AXIS000-0.ax"],
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:ODRL754 a odrl:Set ; odrl:permission [ odrl:action odrl:use ] .""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v600,  axiom, val(v600)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct, axiom, $distinct(v0, v600, v1200)).
fof(compl_witness, axiom, completion_compatible(v600, v0, v1200)).
""",
        "fof_conjecture": None,
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const v Real)",
        "smt2_asserts": """\
(assert (>= v 0.0)) (assert (<= v 1200.0))
(assert (= v 600.0))""",
    },
]
