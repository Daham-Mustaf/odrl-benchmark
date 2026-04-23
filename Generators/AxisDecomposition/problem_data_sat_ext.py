"""
problem_data_sat_ext.py
=======================
Additional SAT problems: ODRL755-769 (10 problems).
Appended to problem_data_sat.py PROBLEMS list.

All TTL entries now encode the actual ODRL policy structure matching
the FOF/SMT semantics (not empty odrl:Set stubs).
"""

PROBLEMS_EXT = [
    # ── SingleAxis ───────────────────────────────────────────────────
    {
        "id": "ODRL755", "subdir": "SAT",
        "name": "SAT SingleAxis: lteq constraint is satisfiable",
        "verdict": "Satisfiable", "status_fof": "Satisfiable", "status_smt": "sat",
        "difficulty": "Easy",
        "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "description": "width lteq 800: (0,800] is non-empty. Witness: v400.\n",
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:ODRL755 a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand  oax:absoluteSizeWidth ;
      odrl:operator     odrl:lteq ;
      odrl:rightOperand "800"^^xsd:decimal
    ]
  ] .""",
        "fof_extra_decls": (
            "fof(val_v0,   axiom, val(v0)).\n"
            "fof(val_v400, axiom, val(v400)).\n"
            "fof(val_v800, axiom, val(v800)).\n"
            "fof(ord_v0_v400,   axiom, less(v0,   v400)).\n"
            "fof(ord_v400_v800, axiom, less(v400, v800)).\n"
            "fof(distinct, axiom, $distinct(v0, v400, v800)).\n"
            "fof(witness,  axiom, in_lopen(v400, v0, v800)).\n"
        ),
        "fof_conjecture": None,
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": "(assert (> x 0.0))\n(assert (<= x 800.0))",
    },

    {
        "id": "ODRL756", "subdir": "SAT",
        "name": "SAT SingleAxis: gteq constraint is satisfiable",
        "verdict": "Satisfiable", "status_fof": "Satisfiable", "status_smt": "sat",
        "difficulty": "Easy",
        "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "description": "width gteq 200: [200,inf) is non-empty. Witness: v400.\n",
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:ODRL756 a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand  oax:absoluteSizeWidth ;
      odrl:operator     odrl:gteq ;
      odrl:rightOperand "200"^^xsd:decimal
    ]
  ] .""",
        "fof_extra_decls": (
            "fof(val_v200, axiom, val(v200)).\n"
            "fof(val_v400, axiom, val(v400)).\n"
            "fof(ord_v200_v400, axiom, less(v200, v400)).\n"
            "fof(distinct, axiom, $distinct(v200, v400)).\n"
            "fof(witness,  axiom, leq(v200, v400)).\n"
        ),
        "fof_conjecture": None,
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": "(assert (>= x 200.0))",
    },

    # ── Box2D ────────────────────────────────────────────────────────
    {
        "id": "ODRL757", "subdir": "SAT",
        "name": "SAT Box2D: 2D box constraint is satisfiable",
        "verdict": "Satisfiable", "status_fof": "Satisfiable", "status_smt": "sat",
        "difficulty": "Easy",
        "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "description": (
            "Width [200,800], Height [100,600]. Box non-empty.\n"
            "Witness: (x,y) = (v400, v300) inside both closed intervals.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:ODRL757 a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand  oax:absoluteSizeWidth ;
          odrl:operator     odrl:gteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
        [ odrl:leftOperand  oax:absoluteSizeWidth ;
          odrl:operator     odrl:lteq ;
          odrl:rightOperand "800"^^xsd:decimal ]
        [ odrl:leftOperand  oax:absoluteSizeHeight ;
          odrl:operator     odrl:gteq ;
          odrl:rightOperand "100"^^xsd:decimal ]
        [ odrl:leftOperand  oax:absoluteSizeHeight ;
          odrl:operator     odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": (
            "fof(val_v100, axiom, val(v100)).\n"
            "fof(val_v200, axiom, val(v200)).\n"
            "fof(val_v300, axiom, val(v300)).\n"
            "fof(val_v400, axiom, val(v400)).\n"
            "fof(val_v600, axiom, val(v600)).\n"
            "fof(val_v800, axiom, val(v800)).\n"
            "fof(ord_v100_v200, axiom, less(v100, v200)).\n"
            "fof(ord_v200_v300, axiom, less(v200, v300)).\n"
            "fof(ord_v300_v400, axiom, less(v300, v400)).\n"
            "fof(ord_v400_v600, axiom, less(v400, v600)).\n"
            "fof(ord_v600_v800, axiom, less(v600, v800)).\n"
            "fof(distinct, axiom, $distinct(v100, v200, v300, v400, v600, v800)).\n"
            "fof(witness_x, axiom, leq(v200, v400) & leq(v400, v800)).\n"
            "fof(witness_y, axiom, leq(v100, v300) & leq(v300, v600)).\n"
        ),
        "fof_conjecture": None,
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": (
            "(assert (>= x 200.0))(assert (<= x 800.0))\n"
            "(assert (>= y 100.0))(assert (<= y 600.0))"
        ),
    },

    {
        "id": "ODRL758", "subdir": "SAT",
        "name": "SAT Box2D: axis_compatible 2D is satisfiable",
        "verdict": "Satisfiable", "status_fof": "Satisfiable", "status_smt": "sat",
        "difficulty": "Easy",
        "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "description": (
            "Two overlapping 1D intervals:\n"
            "policyA = [v0, v600], policyB = [v400, v800], overlap = [v400, v600] != empty.\n"
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
      odrl:leftOperand  oax:absoluteSizeWidth ;
      odrl:operator     odrl:lteq ;
      odrl:rightOperand "600"^^xsd:decimal
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand  oax:absoluteSizeWidth ;
      odrl:operator     odrl:gteq ;
      odrl:rightOperand "400"^^xsd:decimal
    ]
  ] .""",
        "fof_extra_decls": (
            "fof(val_v0,   axiom, val(v0)).\n"
            "fof(val_v400, axiom, val(v400)).\n"
            "fof(val_v600, axiom, val(v600)).\n"
            "fof(val_v800, axiom, val(v800)).\n"
            "fof(ord_v0_v400,   axiom, less(v0,   v400)).\n"
            "fof(ord_v400_v600, axiom, less(v400, v600)).\n"
            "fof(ord_v600_v800, axiom, less(v600, v800)).\n"
            "fof(distinct, axiom, $distinct(v0, v400, v600, v800)).\n"
            "fof(witness,  axiom, axis_compatible(v0, v600, v400, v800)).\n"
        ),
        "fof_conjecture": None,
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": (
            "(assert (>= x 0.0))(assert (<= x 600.0))\n"
            "(assert (>= x 400.0))(assert (<= x 800.0))"
        ),
    },

    # ── Box3D ────────────────────────────────────────────────────────
    {
        "id": "ODRL759", "subdir": "SAT",
        "name": "SAT Box3D: 3D box constraint is satisfiable",
        "verdict": "Satisfiable", "status_fof": "Satisfiable", "status_smt": "sat",
        "difficulty": "Easy",
        "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "description": (
            "3D box: width [200,800], height [100,600], depth [8,32] is non-empty.\n"
            "Witness: (x,y,z) = (v400, v300, v16), all inside their closed intervals.\n"
            "Unfolded into leq primitives so Vampire-FMB closes without instantiating in_box3.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:ODRL759 a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand  oax:absoluteSizeWidth ;
          odrl:operator     odrl:gteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
        [ odrl:leftOperand  oax:absoluteSizeWidth ;
          odrl:operator     odrl:lteq ;
          odrl:rightOperand "800"^^xsd:decimal ]
        [ odrl:leftOperand  oax:absoluteSizeHeight ;
          odrl:operator     odrl:gteq ;
          odrl:rightOperand "100"^^xsd:decimal ]
        [ odrl:leftOperand  oax:absoluteSizeHeight ;
          odrl:operator     odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand  oax:absoluteSizeDepth ;
          odrl:operator     odrl:gteq ;
          odrl:rightOperand "8"^^xsd:decimal ]
        [ odrl:leftOperand  oax:absoluteSizeDepth ;
          odrl:operator     odrl:lteq ;
          odrl:rightOperand "32"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": (
            "fof(val_v8,   axiom, val(v8)).\n"
            "fof(val_v16,  axiom, val(v16)).\n"
            "fof(val_v32,  axiom, val(v32)).\n"
            "fof(val_v100, axiom, val(v100)).\n"
            "fof(val_v200, axiom, val(v200)).\n"
            "fof(val_v300, axiom, val(v300)).\n"
            "fof(val_v400, axiom, val(v400)).\n"
            "fof(val_v600, axiom, val(v600)).\n"
            "fof(val_v800, axiom, val(v800)).\n"
            "fof(ord_v8_v16,    axiom, less(v8,   v16)).\n"
            "fof(ord_v16_v32,   axiom, less(v16,  v32)).\n"
            "fof(ord_v32_v100,  axiom, less(v32,  v100)).\n"
            "fof(ord_v100_v200, axiom, less(v100, v200)).\n"
            "fof(ord_v200_v300, axiom, less(v200, v300)).\n"
            "fof(ord_v300_v400, axiom, less(v300, v400)).\n"
            "fof(ord_v400_v600, axiom, less(v400, v600)).\n"
            "fof(ord_v600_v800, axiom, less(v600, v800)).\n"
            "fof(distinct, axiom, "
            "$distinct(v8, v16, v32, v100, v200, v300, v400, v600, v800)).\n"
            "fof(witness_x, axiom, leq(v200, v400) & leq(v400, v800)).\n"
            "fof(witness_y, axiom, leq(v100, v300) & leq(v300, v600)).\n"
            "fof(witness_z, axiom, leq(v8,   v16)  & leq(v16,  v32)).\n"
        ),
        "fof_conjecture": None,
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)",
        "smt2_asserts": (
            "(assert (>= x 200.0))(assert (<= x 800.0))\n"
            "(assert (>= y 100.0))(assert (<= y 600.0))\n"
            "(assert (>= z 8.0))  (assert (<= z 32.0))"
        ),
    },

    # ── Box3D: three axis_conflict facts are consistent ──────────────
    {
        "id": "ODRL767", "subdir": "SAT",
        "name": "SAT Box3D: three axis_conflict facts on distinct axes are consistent",
        "verdict": "Satisfiable", "status_fof": "Satisfiable", "status_smt": "sat",
        "difficulty": "Easy",
        "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
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
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand  oax:absoluteSizeWidth ;
          odrl:operator     odrl:lteq ;
          odrl:rightOperand "2"^^xsd:decimal ]
        [ odrl:leftOperand  oax:absoluteSizeHeight ;
          odrl:operator     odrl:lteq ;
          odrl:rightOperand "3"^^xsd:decimal ]
        [ odrl:leftOperand  oax:absoluteSizeDepth ;
          odrl:operator     odrl:lteq ;
          odrl:rightOperand "4"^^xsd:decimal ]
      )
    ]
  ] .

drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand  oax:absoluteSizeWidth ;
          odrl:operator     odrl:gteq ;
          odrl:rightOperand "3"^^xsd:decimal ]
        [ odrl:leftOperand  oax:absoluteSizeHeight ;
          odrl:operator     odrl:gteq ;
          odrl:rightOperand "4"^^xsd:decimal ]
        [ odrl:leftOperand  oax:absoluteSizeDepth ;
          odrl:operator     odrl:gteq ;
          odrl:rightOperand "5"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": (
            "fof(val_v1, axiom, val(v1)).\n"
            "fof(val_v2, axiom, val(v2)).\n"
            "fof(val_v3, axiom, val(v3)).\n"
            "fof(val_v4, axiom, val(v4)).\n"
            "fof(val_v5, axiom, val(v5)).\n"
            "fof(val_v6, axiom, val(v6)).\n"
            "fof(ord_v1_v2, axiom, less(v1, v2)).\n"
            "fof(ord_v2_v3, axiom, less(v2, v3)).\n"
            "fof(ord_v3_v4, axiom, less(v3, v4)).\n"
            "fof(ord_v4_v5, axiom, less(v4, v5)).\n"
            "fof(ord_v5_v6, axiom, less(v5, v6)).\n"
            "fof(distinct, axiom, $distinct(v1, v2, v3, v4, v5, v6)).\n"
            "fof(cf_width,  axiom, axis_conflict(v1, v2, v3, v4)).\n"
            "fof(cf_height, axiom, axis_conflict(v2, v3, v4, v5)).\n"
            "fof(cf_depth,  axiom, axis_conflict(v3, v4, v5, v6)).\n"
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

    # ── PolicyQuality: HD video ──────────────────────────────────────
    {
        "id": "ODRL768", "subdir": "SAT",
        "name": "SAT PolicyQuality: real-world HD policy is satisfiable",
        "verdict": "Satisfiable", "status_fof": "Satisfiable", "status_smt": "sat",
        "difficulty": "Easy",
        "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "description": (
            "HD video: width [640, 1920], height [480, 1080].\n"
            "Witness: (x,y) = (1280, 720) -- classic 720p resolution.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:ODRL768 a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand  oax:absoluteSizeWidth ;
          odrl:operator     odrl:gteq ;
          odrl:rightOperand "640"^^xsd:decimal ]
        [ odrl:leftOperand  oax:absoluteSizeWidth ;
          odrl:operator     odrl:lteq ;
          odrl:rightOperand "1920"^^xsd:decimal ]
        [ odrl:leftOperand  oax:absoluteSizeHeight ;
          odrl:operator     odrl:gteq ;
          odrl:rightOperand "480"^^xsd:decimal ]
        [ odrl:leftOperand  oax:absoluteSizeHeight ;
          odrl:operator     odrl:lteq ;
          odrl:rightOperand "1080"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": (
            "fof(val_v480,  axiom, val(v480)).\n"
            "fof(val_v640,  axiom, val(v640)).\n"
            "fof(val_v720,  axiom, val(v720)).\n"
            "fof(val_v1080, axiom, val(v1080)).\n"
            "fof(val_v1280, axiom, val(v1280)).\n"
            "fof(val_v1920, axiom, val(v1920)).\n"
            "fof(ord_v480_v640,   axiom, less(v480,  v640)).\n"
            "fof(ord_v640_v720,   axiom, less(v640,  v720)).\n"
            "fof(ord_v720_v1080,  axiom, less(v720,  v1080)).\n"
            "fof(ord_v1080_v1280, axiom, less(v1080, v1280)).\n"
            "fof(ord_v1280_v1920, axiom, less(v1280, v1920)).\n"
            "fof(distinct, axiom, "
            "$distinct(v480, v640, v720, v1080, v1280, v1920)).\n"
            "fof(witness_x, axiom, leq(v640, v1280) & leq(v1280, v1920)).\n"
            "fof(witness_y, axiom, leq(v480, v720)  & leq(v720,  v1080)).\n"
        ),
        "fof_conjecture": None,
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": (
            "(assert (>= x 640.0))(assert (<= x 1920.0))\n"
            "(assert (>= y 480.0))(assert (<= y 1080.0))"
        ),
    },

    # ── PolicyQuality: 4-axis drone ──────────────────────────────────
    {
        "id": "ODRL769", "subdir": "SAT",
        "name": "SAT PolicyQuality: 4-axis drone policy is satisfiable",
        "verdict": "Satisfiable", "status_fof": "Satisfiable", "status_smt": "sat",
        "difficulty": "Easy",
        "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "description": (
            "Drone envelope: width [200,800], height [100,600], depth [8,32], altitude [72,300].\n"
            "Witness: (x,y,z,w) = (400, 300, 16, 150), inside all four axis bounds.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:ODRL769 a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand  oax:absoluteSizeWidth ;
          odrl:operator     odrl:gteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
        [ odrl:leftOperand  oax:absoluteSizeWidth ;
          odrl:operator     odrl:lteq ;
          odrl:rightOperand "800"^^xsd:decimal ]
        [ odrl:leftOperand  oax:absoluteSizeHeight ;
          odrl:operator     odrl:gteq ;
          odrl:rightOperand "100"^^xsd:decimal ]
        [ odrl:leftOperand  oax:absoluteSizeHeight ;
          odrl:operator     odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand  oax:absoluteSizeDepth ;
          odrl:operator     odrl:gteq ;
          odrl:rightOperand "8"^^xsd:decimal ]
        [ odrl:leftOperand  oax:absoluteSizeDepth ;
          odrl:operator     odrl:lteq ;
          odrl:rightOperand "32"^^xsd:decimal ]
        [ odrl:leftOperand  oax:spatialCoordinatesAltitude ;
          odrl:operator     odrl:gteq ;
          odrl:rightOperand "72"^^xsd:decimal ]
        [ odrl:leftOperand  oax:spatialCoordinatesAltitude ;
          odrl:operator     odrl:lteq ;
          odrl:rightOperand "300"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": (
            "fof(val_v8,   axiom, val(v8)).\n"
            "fof(val_v16,  axiom, val(v16)).\n"
            "fof(val_v32,  axiom, val(v32)).\n"
            "fof(val_v72,  axiom, val(v72)).\n"
            "fof(val_v100, axiom, val(v100)).\n"
            "fof(val_v150, axiom, val(v150)).\n"
            "fof(val_v200, axiom, val(v200)).\n"
            "fof(val_v300, axiom, val(v300)).\n"
            "fof(val_v400, axiom, val(v400)).\n"
            "fof(val_v600, axiom, val(v600)).\n"
            "fof(val_v800, axiom, val(v800)).\n"
            "fof(ord_v8_v16,    axiom, less(v8,   v16)).\n"
            "fof(ord_v16_v32,   axiom, less(v16,  v32)).\n"
            "fof(ord_v32_v72,   axiom, less(v32,  v72)).\n"
            "fof(ord_v72_v100,  axiom, less(v72,  v100)).\n"
            "fof(ord_v100_v150, axiom, less(v100, v150)).\n"
            "fof(ord_v150_v200, axiom, less(v150, v200)).\n"
            "fof(ord_v200_v300, axiom, less(v200, v300)).\n"
            "fof(ord_v300_v400, axiom, less(v300, v400)).\n"
            "fof(ord_v400_v600, axiom, less(v400, v600)).\n"
            "fof(ord_v600_v800, axiom, less(v600, v800)).\n"
            "fof(distinct, axiom, "
            "$distinct(v8, v16, v32, v72, v100, v150, v200, v300, v400, v600, v800)).\n"
            "fof(witness_x, axiom, leq(v200, v400) & leq(v400, v800)).\n"
            "fof(witness_y, axiom, leq(v100, v300) & leq(v300, v600)).\n"
            "fof(witness_z, axiom, leq(v8,   v16)  & leq(v16,  v32)).\n"
            "fof(witness_w, axiom, leq(v72,  v150) & leq(v150, v300)).\n"
        ),
        "fof_conjecture": None,
        "smt2_logic": "QF_LRA",
        "smt2_decls": (
            "(declare-const x Real)\n"
            "(declare-const y Real)\n"
            "(declare-const z Real)\n"
            "(declare-const w Real)"
        ),
        "smt2_asserts": (
            "(assert (>= x 200.0))(assert (<= x 800.0))\n"
            "(assert (>= y 100.0))(assert (<= y 600.0))\n"
            "(assert (>= z 8.0))  (assert (<= z 32.0))\n"
            "(assert (>= w 72.0)) (assert (<= w 300.0))"
        ),
    },

    # ── SemanticCore ─────────────────────────────────────────────────
    {
        "id": "ODRL763", "subdir": "SAT",
        "name": "SAT SemanticCore: core axioms with overlap witness are satisfiable",
        "verdict": "Satisfiable", "status_fof": "Satisfiable", "status_smt": "sat",
        "difficulty": "Easy",
        "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "description": (
            "ORD000 + AXIS000 are consistent. Witness: in_closed(v400, v0, v600) -- v400 is inside [v0, v600].\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:ODRL763 a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand  oax:absoluteSizeWidth ;
          odrl:operator     odrl:gteq ;
          odrl:rightOperand "0"^^xsd:decimal ]
        [ odrl:leftOperand  oax:absoluteSizeWidth ;
          odrl:operator     odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": (
            "fof(val_v0,   axiom, val(v0)).\n"
            "fof(val_v400, axiom, val(v400)).\n"
            "fof(val_v600, axiom, val(v600)).\n"
            "fof(ord_v0_v400,   axiom, less(v0,   v400)).\n"
            "fof(ord_v400_v600, axiom, less(v400, v600)).\n"
            "fof(distinct, axiom, $distinct(v0, v400, v600)).\n"
            "fof(witness,  axiom, in_closed(v400, v0, v600)).\n"
        ),
        "fof_conjecture": None,
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": "(assert (>= x 0.0))(assert (<= x 600.0))",
    },

    {
        "id": "ODRL764", "subdir": "SAT",
        "name": "SAT SemanticCore: verdict algebra constants are consistent",
        "verdict": "Satisfiable", "status_fof": "Satisfiable", "status_smt": "sat",
        "difficulty": "Easy",
        "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "description": (
            "AXIS000 verdict algebra: conflict, compatible, unknown are three\n"
            "distinct is_verdict constants. Axioms are consistent, no contradiction.\n"
            "Meta-level consistency check; TTL is a minimal Set placeholder since\n"
            "the scenario is about the verdict ontology itself, not a concrete policy.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

# ODRL764 is a meta-level consistency check over the verdict algebra
# (conflict, compatible, unknown). It has no per-axis policy; the Set
# below is a placeholder satisfying odrl:Policy well-formedness.
drk:ODRL764 a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use
  ] .""",
        "fof_extra_decls": (
            "fof(v_distinct, axiom, "
            "conflict != compatible & compatible != unknown & conflict != unknown).\n"
        ),
        "fof_conjecture": None,
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": "(assert (= x 1.0))",
    },
]