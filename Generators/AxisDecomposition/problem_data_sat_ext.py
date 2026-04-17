"""
problem_data_sat_ext.py
=======================
Additional SAT problems: ODRL755-764 (+10 problems).
Appended to problem_data_sat.py PROBLEMS list.
"""

PROBLEMS_EXT = [
    # ── SingleAxis ───────────────────────────────────────────────────
    {
        "id": "ODRL755", "subdir": "SAT",
        "name": "SAT SingleAxis: lteq constraint is satisfiable",
        "verdict": "Satisfiable", "status_fof": "Satisfiable", "status_smt": "sat",
        "difficulty": "Easy", "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "description": "width lteq 800: (0,800] is non-empty. Witness: v400.\n",
        "ttl": '@prefix odrl: <http://www.w3.org/ns/odrl/2/> .\n@prefix drk: <http://w3id.org/drk/ontology/> .\ndrk:ODRL755 a odrl:Set ; odrl:permission [ odrl:action odrl:use ] .',
        "fof_extra_decls": "fof(val_v0,axiom,val(v0)).\nfof(val_v400,axiom,val(v400)).\nfof(val_v800,axiom,val(v800)).\nfof(ord_v0_v400,axiom,less(v0,v400)).\nfof(ord_v400_v800,axiom,less(v400,v800)).\nfof(distinct,axiom,$distinct(v0,v400,v800)).\nfof(witness,axiom,in_lopen(v400,v0,v800)).\n",
        "fof_conjecture": None,
        "smt2_logic": "QF_LRA", "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": "(assert (> x 0.0))\n(assert (<= x 800.0))",
    },
    {
        "id": "ODRL756", "subdir": "SAT",
        "name": "SAT SingleAxis: gteq constraint is satisfiable",
        "verdict": "Satisfiable", "status_fof": "Satisfiable", "status_smt": "sat",
        "difficulty": "Easy", "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "description": "width gteq 200: [200,∞) is non-empty. Witness: v400.\n",
        "ttl": '@prefix odrl: <http://www.w3.org/ns/odrl/2/> .\n@prefix drk: <http://w3id.org/drk/ontology/> .\ndrk:ODRL756 a odrl:Set ; odrl:permission [ odrl:action odrl:use ] .',
        "fof_extra_decls": "fof(val_v200,axiom,val(v200)).\nfof(val_v400,axiom,val(v400)).\nfof(ord_v200_v400,axiom,less(v200,v400)).\nfof(distinct,axiom,$distinct(v200,v400)).\nfof(witness,axiom,leq(v200,v400)).\n",
        "fof_conjecture": None,
        "smt2_logic": "QF_LRA", "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": "(assert (>= x 200.0))",
    },
    # ── Box2D ────────────────────────────────────────────────────────
    {
        "id": "ODRL757", "subdir": "SAT",
        "name": "SAT Box2D: 2D box constraint is satisfiable",
        "verdict": "Satisfiable", "status_fof": "Satisfiable", "status_smt": "sat",
        "difficulty": "Easy", "includes": ["ORD000-0.ax", "PROJ000-0.ax", "AXIS000-0.ax"],
        "description": "Width [200,800], Height [100,600]. Box non-empty. Witness: (400,300).\n",
        "ttl": '@prefix odrl: <http://www.w3.org/ns/odrl/2/> .\n@prefix drk: <http://w3id.org/drk/ontology/> .\ndrk:ODRL757 a odrl:Set ; odrl:permission [ odrl:action odrl:use ] .',
        "fof_extra_decls": "fof(val_v0,axiom,val(v0)).\nfof(val_v100,axiom,val(v100)).\nfof(val_v200,axiom,val(v200)).\nfof(val_v300,axiom,val(v300)).\nfof(val_v400,axiom,val(v400)).\nfof(val_v600,axiom,val(v600)).\nfof(val_v800,axiom,val(v800)).\nfof(ord_v0_v100,axiom,less(v0,v100)).\nfof(ord_v100_v200,axiom,less(v100,v200)).\nfof(ord_v200_v300,axiom,less(v200,v300)).\nfof(ord_v300_v400,axiom,less(v300,v400)).\nfof(ord_v400_v600,axiom,less(v400,v600)).\nfof(ord_v600_v800,axiom,less(v600,v800)).\nfof(distinct,axiom,$distinct(v0,v100,v200,v300,v400,v600,v800)).\nfof(witness,axiom,in_box2(v400,v300,v200,v800,v100,v600)).\n",
        "fof_conjecture": None,
        "smt2_logic": "QF_LRA", "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": "(assert (>= x 200.0))(assert (<= x 800.0))\n(assert (>= y 100.0))(assert (<= y 600.0))",
    },
    {
        "id": "ODRL758", "subdir": "SAT",
        "name": "SAT Box2D: axis_compatible 2D is satisfiable",
        "verdict": "Satisfiable", "status_fof": "Satisfiable", "status_smt": "sat",
        "difficulty": "Easy", "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "description": "[v0,v600]∩[v400,v800]=[v400,v600]≠∅. axis_compatible holds.\n",
        "ttl": '@prefix odrl: <http://www.w3.org/ns/odrl/2/> .\n@prefix drk: <http://w3id.org/drk/ontology/> .\ndrk:ODRL758 a odrl:Set ; odrl:permission [ odrl:action odrl:use ] .',
        "fof_extra_decls": "fof(val_v0,axiom,val(v0)).\nfof(val_v400,axiom,val(v400)).\nfof(val_v600,axiom,val(v600)).\nfof(val_v800,axiom,val(v800)).\nfof(ord_v0_v400,axiom,less(v0,v400)).\nfof(ord_v400_v600,axiom,less(v400,v600)).\nfof(ord_v600_v800,axiom,less(v600,v800)).\nfof(distinct,axiom,$distinct(v0,v400,v600,v800)).\nfof(witness,axiom,axis_compatible(v0,v600,v400,v800)).\n",
        "fof_conjecture": None,
        "smt2_logic": "QF_LRA", "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": "(assert (>= x 0.0))(assert (<= x 600.0))\n(assert (>= x 400.0))(assert (<= x 800.0))",
    },
    # ── Box3D ────────────────────────────────────────────────────────
    {
        "id": "ODRL759", "subdir": "SAT",
        "name": "SAT Box3D: 3D box constraint is satisfiable",
        "verdict": "Satisfiable", "status_fof": "Satisfiable", "status_smt": "sat",
        "difficulty": "Easy", "includes": ["ORD000-0.ax", "PROJ000-0.ax", "AXIS000-0.ax"],
        "description": "Width [200,800], Height [100,600], Depth [8,32]. Witness: (400,300,16).\n",
        "ttl": '@prefix odrl: <http://www.w3.org/ns/odrl/2/> .\n@prefix drk: <http://w3id.org/drk/ontology/> .\ndrk:ODRL759 a odrl:Set ; odrl:permission [ odrl:action odrl:use ] .',
        "fof_extra_decls": "fof(val_v0,axiom,val(v0)).\nfof(val_v8,axiom,val(v8)).\nfof(val_v16,axiom,val(v16)).\nfof(val_v32,axiom,val(v32)).\nfof(val_v100,axiom,val(v100)).\nfof(val_v200,axiom,val(v200)).\nfof(val_v300,axiom,val(v300)).\nfof(val_v400,axiom,val(v400)).\nfof(val_v600,axiom,val(v600)).\nfof(val_v800,axiom,val(v800)).\nfof(ord_v0_v8,axiom,less(v0,v8)).\nfof(ord_v8_v16,axiom,less(v8,v16)).\nfof(ord_v16_v32,axiom,less(v16,v32)).\nfof(ord_v32_v100,axiom,less(v32,v100)).\nfof(ord_v100_v200,axiom,less(v100,v200)).\nfof(ord_v200_v300,axiom,less(v200,v300)).\nfof(ord_v300_v400,axiom,less(v300,v400)).\nfof(ord_v400_v600,axiom,less(v400,v600)).\nfof(ord_v600_v800,axiom,less(v600,v800)).\nfof(distinct,axiom,$distinct(v0,v8,v16,v32,v100,v200,v300,v400,v600,v800)).\nfof(witness,axiom,in_box3(v400,v300,v16,v200,v800,v100,v600,v8,v32)).\n",
        "fof_conjecture": None,
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)",
        "smt2_asserts": "(assert (>= x 200.0))(assert (<= x 800.0))\n(assert (>= y 100.0))(assert (<= y 600.0))\n(assert (>= z 8.0))(assert (<= z 32.0))",
    },
{
    "id": "ODRL767", "subdir": "SAT",
    "name": "SAT Box3D: three axis_conflict facts on distinct axes are consistent",
    "verdict": "Satisfiable", "status_fof": "Satisfiable", "status_smt": "sat",
    "difficulty": "Easy", "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
    "description": (
        "Three axis_conflict facts on distinct (width, height, depth) 4-tuples\n"
        "coexist. Each uses a different pair of disjoint intervals drawn from a\n"
        "shared strict chain v1 < v2 < ... < v6. No shared variable forces a\n"
        "contradiction; the axioms are consistent.\n"
        "Width:  [v1,v2] vs [v3,v4]  disjoint (less(v2,v3))\n"
        "Height: [v2,v3] vs [v4,v5]  disjoint (less(v3,v4))\n"
        "Depth:  [v3,v4] vs [v5,v6]  disjoint (less(v4,v5))\n"
    ),
    "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:and (
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:lteq ; odrl:rightOperand "2"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeHeight ;
        odrl:operator odrl:lteq ; odrl:rightOperand "3"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeDepth ;
        odrl:operator odrl:lteq ; odrl:rightOperand "4"^^xsd:decimal ]
    ) ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:and (
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:gteq ; odrl:rightOperand "3"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeHeight ;
        odrl:operator odrl:gteq ; odrl:rightOperand "4"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeDepth ;
        odrl:operator odrl:gteq ; odrl:rightOperand "5"^^xsd:decimal ]
    ) ] ] .""",
    "fof_extra_decls": (
        "fof(val_v1,axiom,val(v1)).\n"
        "fof(val_v2,axiom,val(v2)).\n"
        "fof(val_v3,axiom,val(v3)).\n"
        "fof(val_v4,axiom,val(v4)).\n"
        "fof(val_v5,axiom,val(v5)).\n"
        "fof(val_v6,axiom,val(v6)).\n"
        "fof(ord_v1_v2,axiom,less(v1,v2)).\n"
        "fof(ord_v2_v3,axiom,less(v2,v3)).\n"
        "fof(ord_v3_v4,axiom,less(v3,v4)).\n"
        "fof(ord_v4_v5,axiom,less(v4,v5)).\n"
        "fof(ord_v5_v6,axiom,less(v5,v6)).\n"
        "fof(distinct,axiom,$distinct(v1,v2,v3,v4,v5,v6)).\n"
        "fof(cf_width, axiom, axis_conflict(v1, v2, v3, v4)).\n"
        "fof(cf_height,axiom, axis_conflict(v2, v3, v4, v5)).\n"
        "fof(cf_depth, axiom, axis_conflict(v3, v4, v5, v6)).\n"
    ),
    "fof_conjecture": None,
    "smt2_logic": "QF_LRA",
    "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)",
    "smt2_asserts": (
        "(assert (>= x 1.0))(assert (<= x 2.0))\n"
        "(assert (>= y 2.0))(assert (<= y 3.0))\n"
        "(assert (>= z 3.0))(assert (<= z 4.0))"
    ),
},
    # ── PolicyQuality ────────────────────────────────────────────────
    {
        "id": "ODRL768", "subdir": "SAT",
        "name": "SAT PolicyQuality: real-world HD policy is satisfiable",
        "verdict": "Satisfiable", "status_fof": "Satisfiable", "status_smt": "sat",
        "difficulty": "Easy", "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "description": "HD: width [640,1920], height [480,1080]. Witness: (1280,720).\n",
        "ttl": '@prefix odrl: <http://www.w3.org/ns/odrl/2/> .\n@prefix drk: <http://w3id.org/drk/ontology/> .\ndrk:ODRL768 a odrl:Set ; odrl:permission [ odrl:action odrl:use ] .',
        "fof_extra_decls": "fof(val_v640,axiom,val(v640)).\nfof(val_v720,axiom,val(v720)).\nfof(val_v1080,axiom,val(v1080)).\nfof(val_v1280,axiom,val(v1280)).\nfof(val_v1920,axiom,val(v1920)).\nfof(val_v480,axiom,val(v480)).\nfof(ord_v480_v640,axiom,less(v480,v640)).\nfof(ord_v640_v720,axiom,less(v640,v720)).\nfof(ord_v720_v1080,axiom,less(v720,v1080)).\nfof(ord_v1080_v1280,axiom,less(v1080,v1280)).\nfof(ord_v1280_v1920,axiom,less(v1280,v1920)).\nfof(distinct,axiom,$distinct(v480,v640,v720,v1080,v1280,v1920)).\nfof(witness,axiom,leq(v640,v1280) & leq(v1280,v1920) & leq(v480,v720) & leq(v720,v1080)).\n",
        "fof_conjecture": None,
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": "(assert (>= x 640.0))(assert (<= x 1920.0))\n(assert (>= y 480.0))(assert (<= y 1080.0))",
    },
    {
        "id": "ODRL769", "subdir": "SAT",
        "name": "SAT PolicyQuality: 4-axis drone policy is satisfiable",
        "verdict": "Satisfiable", "status_fof": "Satisfiable", "status_smt": "sat",
        "difficulty": "Easy", "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "description": "Drone: W [200,800], H [100,600], D [8,32], Alt [72,300]. Witness: (400,300,16,150).\n",
        "ttl": '@prefix odrl: <http://www.w3.org/ns/odrl/2/> .\n@prefix drk: <http://w3id.org/drk/ontology/> .\ndrk:ODRL769 a odrl:Set ; odrl:permission [ odrl:action odrl:use ] .',
        "fof_extra_decls": "fof(val_v0,axiom,val(v0)).\nfof(val_v8,axiom,val(v8)).\nfof(val_v16,axiom,val(v16)).\nfof(val_v32,axiom,val(v32)).\nfof(val_v72,axiom,val(v72)).\nfof(val_v100,axiom,val(v100)).\nfof(val_v150,axiom,val(v150)).\nfof(val_v200,axiom,val(v200)).\nfof(val_v300,axiom,val(v300)).\nfof(val_v400,axiom,val(v400)).\nfof(val_v600,axiom,val(v600)).\nfof(val_v800,axiom,val(v800)).\nfof(ord_v0_v8,axiom,less(v0,v8)).\nfof(ord_v8_v16,axiom,less(v8,v16)).\nfof(ord_v16_v32,axiom,less(v16,v32)).\nfof(ord_v32_v72,axiom,less(v32,v72)).\nfof(ord_v72_v100,axiom,less(v72,v100)).\nfof(ord_v100_v150,axiom,less(v100,v150)).\nfof(ord_v150_v200,axiom,less(v150,v200)).\nfof(ord_v200_v300,axiom,less(v200,v300)).\nfof(ord_v300_v400,axiom,less(v300,v400)).\nfof(ord_v400_v600,axiom,less(v400,v600)).\nfof(ord_v600_v800,axiom,less(v600,v800)).\nfof(distinct,axiom,$distinct(v0,v8,v16,v32,v72,v100,v150,v200,v300,v400,v600,v800)).\nfof(witness,axiom,leq(v200,v400) & leq(v400,v800) & leq(v100,v300) & leq(v300,v600) & leq(v8,v16) & leq(v16,v32) & leq(v72,v150) & leq(v150,v300)).\n",
        "fof_conjecture": None,
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)\n(declare-const w Real)",
        "smt2_asserts": "(assert (>= x 200.0))(assert (<= x 800.0))\n(assert (>= y 100.0))(assert (<= y 600.0))\n(assert (>= z 8.0))(assert (<= z 32.0))\n(assert (>= w 72.0))(assert (<= w 300.0))",
    },
    # ── SemanticCore ─────────────────────────────────────────────────
    {
        "id": "ODRL763", "subdir": "SAT",
        "name": "SAT SemanticCore: core axioms with overlap witness are satisfiable",
        "verdict": "Satisfiable", "status_fof": "Satisfiable", "status_smt": "sat",
        "difficulty": "Easy", "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "description": "ORD000+AXIS000 consistent. Witness: in_closed(v400,v0,v600).\n",
        "ttl": '@prefix odrl: <http://www.w3.org/ns/odrl/2/> .\n@prefix drk: <http://w3id.org/drk/ontology/> .\ndrk:ODRL763 a odrl:Set ; odrl:permission [ odrl:action odrl:use ] .',
        "fof_extra_decls": "fof(val_v0,axiom,val(v0)).\nfof(val_v400,axiom,val(v400)).\nfof(val_v600,axiom,val(v600)).\nfof(ord_v0_v400,axiom,less(v0,v400)).\nfof(ord_v400_v600,axiom,less(v400,v600)).\nfof(distinct,axiom,$distinct(v0,v400,v600)).\nfof(witness,axiom,in_closed(v400,v0,v600)).\n",
        "fof_conjecture": None,
        "smt2_logic": "QF_LRA", "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": "(assert (>= x 0.0))(assert (<= x 600.0))",
    },
    {
        "id": "ODRL764", "subdir": "SAT",
        "name": "SAT SemanticCore: verdict algebra constants are consistent",
        "verdict": "Satisfiable", "status_fof": "Satisfiable", "status_smt": "sat",
        "difficulty": "Easy", "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "description": "conflict, compatible, unknown are distinct is_verdict constants.\nAxioms consistent.\n",
        "ttl": '@prefix odrl: <http://www.w3.org/ns/odrl/2/> .\n@prefix drk: <http://w3id.org/drk/ontology/> .\ndrk:ODRL764 a odrl:Set ; odrl:permission [ odrl:action odrl:use ] .',
        "fof_extra_decls": "fof(v_distinct,axiom,conflict != compatible & compatible != unknown & conflict != unknown).\n",
        "fof_conjecture": None,
        "smt2_logic": "QF_LRA", "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": "(assert (= x 1.0))",
    },
]
