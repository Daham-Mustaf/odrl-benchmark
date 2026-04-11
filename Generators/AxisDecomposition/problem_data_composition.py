"""
problem_data_composition.py
=========================
Composition benchmark problems: ODRL360-371 (12 problems).
Category D: Four-axis AND composition (Mixed ops, scaling).
Tests def:box-verdict Kleene conjunction across 4 axes:
  X = oax:absoluteSizeWidth      D_k = (0, ∞)
  Y = oax:absoluteSizeHeight     D_k = (0, ∞)
  Z = oax:absoluteSizeDepth      D_k = (0, ∞)
  W = oax:spatialCoordinatesAltitude  D_k = ℝ (treated as > 0)
Conjecture structure (4D box = X,Y,Z,W):
  conflict/Conflict:    ~?[X,Y,Z,W]: (A(X)&B(X) & A(Y)&B(Y) & A(Z)&B(Z) & A(W)&B(W))
  conflict/Compatible:  ?[X,Y,Z,W]:  (...)
  subsumption/Compatible: ![X,Y,Z,W]: (A => B)
  subsumption/Conflict:   ?[X,Y,Z,W]: (A & ~B)
Interval predicates (paper: def:interval-denotation, D_k=(0,∞)):
  lteq v → in_lopen(X, v0, v)   (0, v]
  gteq v → leq(v, X)            [v, ∞)
  lt   v → in_open(X, v0, v)    (0, v)
  gt   v → less(v, X)           (v, ∞)
  eq   v → in_closed(X, v, v)   {v}
TTL: explicit odrl:and over 4 constraints [ODRL 2.2 §4.3].
Include pattern:
  Discrete : include('Axioms/AXIS000-0.ax').
  Continuous: include('Axioms/ORD001-0.ax').  ← BEFORE AXIS000
              include('Axioms/AXIS000-0.ax').
SMT2: x,y,z,w all Real.
TTL prefix: drk: <http://w3id.org/drk/ontology/>

Fixes applied:
  ODRL364: fof_extra_decls was corrupted — v16 and v72 were added (meant
           for ODRL370) but v150 and v600 were lost, leaving the conjecture
           with two undeclared constants. Restored to correct set:
           v0,v8,v32,v100,v150,v300,v500,v600,v800. Also corrected
           needs_density: True → False (v150 witnesses Y in open (100,500);
           ORD001 is not needed and was causing E ResourceOut).
  ODRL370: added v16 constant between v8 and v32 (+ 8 ordering facts +
           updated $distinct). The conjecture Z conjunct needs
           less(v8,Z) & in_open(Z,v0,v32): no constant existed strictly
           between v8 and v32. Ground witnesses after fix:
           X=v300, Y=v200, Z=v16, W=v100.
"""
PROBLEMS = [
    # ──────────────────────────────────────────────────────────────────
    # ODRL360 — All 4 axes compatible → box Compatible
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL360",
        "subdir":        "Composition",
        "name":          "All 4 axes compatible → box Compatible",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "Width:  lteq 800 ∩ gteq 200 = [200,800] ≠ ∅  Compatible\n"
            "Height: lteq 600 ∩ gteq 100 = [100,600] ≠ ∅  Compatible\n"
            "Depth:  lteq 32  ∩ gteq 8   = [8,32]    ≠ ∅  Compatible\n"
            "Alt:    lteq 300 ∩ gteq 72  = [72,300]  ≠ ∅  Compatible\n"
            "box_verdict(C,box_verdict(C,box_verdict(C,C)))=Compatible [Rule 2]\n"
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
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "800"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "32"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "300"^^xsd:decimal ]
      )
    ]
  ] .
drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "100"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "8"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "72"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v8, axiom, val(v8)).
fof(val_v32, axiom, val(v32)).
fof(val_v72, axiom, val(v72)).
fof(val_v100, axiom, val(v100)).
fof(val_v200, axiom, val(v200)).
fof(val_v300, axiom, val(v300)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v8, axiom, less(v0, v8)).
fof(ord_v0_v32, axiom, less(v0, v32)).
fof(ord_v0_v72, axiom, less(v0, v72)).
fof(ord_v0_v100, axiom, less(v0, v100)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v300, axiom, less(v0, v300)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v8_v32, axiom, less(v8, v32)).
fof(ord_v8_v72, axiom, less(v8, v72)).
fof(ord_v8_v100, axiom, less(v8, v100)).
fof(ord_v8_v200, axiom, less(v8, v200)).
fof(ord_v8_v300, axiom, less(v8, v300)).
fof(ord_v8_v600, axiom, less(v8, v600)).
fof(ord_v8_v800, axiom, less(v8, v800)).
fof(ord_v32_v72, axiom, less(v32, v72)).
fof(ord_v32_v100, axiom, less(v32, v100)).
fof(ord_v32_v200, axiom, less(v32, v200)).
fof(ord_v32_v300, axiom, less(v32, v300)).
fof(ord_v32_v600, axiom, less(v32, v600)).
fof(ord_v32_v800, axiom, less(v32, v800)).
fof(ord_v72_v100, axiom, less(v72, v100)).
fof(ord_v72_v200, axiom, less(v72, v200)).
fof(ord_v72_v300, axiom, less(v72, v300)).
fof(ord_v72_v600, axiom, less(v72, v600)).
fof(ord_v72_v800, axiom, less(v72, v800)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v300, axiom, less(v100, v300)).
fof(ord_v100_v600, axiom, less(v100, v600)).
fof(ord_v100_v800, axiom, less(v100, v800)).
fof(ord_v200_v300, axiom, less(v200, v300)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v300_v800, axiom, less(v300, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v8, v32, v72, v100, v200, v300, v600, v800)).
""",
        "fof_conjecture": (
            "?[X,Y,Z,W]: (in_lopen(X, v0, v800) & leq(v200, X) &"
            "           in_lopen(Y, v0, v600) & leq(v100, Y) &\n"
            "           in_lopen(Z, v0, v32)  & leq(v8,   Z) &\n"
            "           in_lopen(W, v0, v300) & leq(v72,  W))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)\n(declare-const w Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 800.0)) (assert (>= x 200.0))
(assert (> y 0.0)) (assert (<= y 600.0)) (assert (>= y 100.0))
(assert (> z 0.0)) (assert (<= z 32.0))  (assert (>= z 8.0))
(assert (> w 0.0)) (assert (<= w 300.0)) (assert (>= w 72.0))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL361 — Width conflict × 3 compatible → box Conflict
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL361",
        "subdir":        "Composition",
        "name":          "Width conflict × 3 compatible → box Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "Width:  lteq 400 ∩ gteq 800 = ∅  Conflict\n"
            "Height/Depth/Alt: all compatible\n"
            "box_verdict(Conflict,box_verdict(C,box_verdict(C,C)))=Conflict\n"
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
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "32"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "300"^^xsd:decimal ]
      )
    ]
  ] .
drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "800"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "100"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "8"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "72"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v8, axiom, val(v8)).
fof(val_v32, axiom, val(v32)).
fof(val_v72, axiom, val(v72)).
fof(val_v100, axiom, val(v100)).
fof(val_v200, axiom, val(v200)).
fof(val_v300, axiom, val(v300)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v8, axiom, less(v0, v8)).
fof(ord_v0_v32, axiom, less(v0, v32)).
fof(ord_v0_v72, axiom, less(v0, v72)).
fof(ord_v0_v100, axiom, less(v0, v100)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v300, axiom, less(v0, v300)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v8_v32, axiom, less(v8, v32)).
fof(ord_v8_v72, axiom, less(v8, v72)).
fof(ord_v8_v100, axiom, less(v8, v100)).
fof(ord_v8_v200, axiom, less(v8, v200)).
fof(ord_v8_v300, axiom, less(v8, v300)).
fof(ord_v8_v400, axiom, less(v8, v400)).
fof(ord_v8_v600, axiom, less(v8, v600)).
fof(ord_v8_v800, axiom, less(v8, v800)).
fof(ord_v32_v72, axiom, less(v32, v72)).
fof(ord_v32_v100, axiom, less(v32, v100)).
fof(ord_v32_v200, axiom, less(v32, v200)).
fof(ord_v32_v300, axiom, less(v32, v300)).
fof(ord_v32_v400, axiom, less(v32, v400)).
fof(ord_v32_v600, axiom, less(v32, v600)).
fof(ord_v32_v800, axiom, less(v32, v800)).
fof(ord_v72_v100, axiom, less(v72, v100)).
fof(ord_v72_v200, axiom, less(v72, v200)).
fof(ord_v72_v300, axiom, less(v72, v300)).
fof(ord_v72_v400, axiom, less(v72, v400)).
fof(ord_v72_v600, axiom, less(v72, v600)).
fof(ord_v72_v800, axiom, less(v72, v800)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v300, axiom, less(v100, v300)).
fof(ord_v100_v400, axiom, less(v100, v400)).
fof(ord_v100_v600, axiom, less(v100, v600)).
fof(ord_v100_v800, axiom, less(v100, v800)).
fof(ord_v200_v300, axiom, less(v200, v300)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v300_v400, axiom, less(v300, v400)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v300_v800, axiom, less(v300, v800)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v8, v32, v72, v100, v200, v300, v400, v600, v800)).
""",
        "fof_conjecture": (
            "~?[X,Y,Z,W]: (in_lopen(X, v0, v400) & leq(v800, X) &"
            "            in_lopen(Y, v0, v600) & leq(v100, Y) &\n"
            "            in_lopen(Z, v0, v32)  & leq(v8,   Z) &\n"
            "            in_lopen(W, v0, v300) & leq(v72,  W))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)\n(declare-const w Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 400.0)) (assert (>= x 800.0))
(assert (> y 0.0)) (assert (<= y 600.0)) (assert (>= y 100.0))
(assert (> z 0.0)) (assert (<= z 32.0))  (assert (>= z 8.0))
(assert (> w 0.0)) (assert (<= w 300.0)) (assert (>= w 72.0))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL362 — 4th axis conflict × 3 compatible → box Conflict
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL362",
        "subdir":        "Composition",
        "name":          "4th axis conflict × 3 compatible → box Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "Width/Height/Depth: all compatible\n"
            "Alt: lteq 72 ∩ gteq 300 = ∅  Conflict\n"
            "box_verdict(C,box_verdict(C,box_verdict(C,Conflict)))=Conflict\n"
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
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "800"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "32"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "72"^^xsd:decimal ]
      )
    ]
  ] .
drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "100"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "8"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "300"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v8, axiom, val(v8)).
fof(val_v32, axiom, val(v32)).
fof(val_v72, axiom, val(v72)).
fof(val_v100, axiom, val(v100)).
fof(val_v200, axiom, val(v200)).
fof(val_v300, axiom, val(v300)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v8, axiom, less(v0, v8)).
fof(ord_v0_v32, axiom, less(v0, v32)).
fof(ord_v0_v72, axiom, less(v0, v72)).
fof(ord_v0_v100, axiom, less(v0, v100)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v300, axiom, less(v0, v300)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v8_v32, axiom, less(v8, v32)).
fof(ord_v8_v72, axiom, less(v8, v72)).
fof(ord_v8_v100, axiom, less(v8, v100)).
fof(ord_v8_v200, axiom, less(v8, v200)).
fof(ord_v8_v300, axiom, less(v8, v300)).
fof(ord_v8_v600, axiom, less(v8, v600)).
fof(ord_v8_v800, axiom, less(v8, v800)).
fof(ord_v32_v72, axiom, less(v32, v72)).
fof(ord_v32_v100, axiom, less(v32, v100)).
fof(ord_v32_v200, axiom, less(v32, v200)).
fof(ord_v32_v300, axiom, less(v32, v300)).
fof(ord_v32_v600, axiom, less(v32, v600)).
fof(ord_v32_v800, axiom, less(v32, v800)).
fof(ord_v72_v100, axiom, less(v72, v100)).
fof(ord_v72_v200, axiom, less(v72, v200)).
fof(ord_v72_v300, axiom, less(v72, v300)).
fof(ord_v72_v600, axiom, less(v72, v600)).
fof(ord_v72_v800, axiom, less(v72, v800)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v300, axiom, less(v100, v300)).
fof(ord_v100_v600, axiom, less(v100, v600)).
fof(ord_v100_v800, axiom, less(v100, v800)).
fof(ord_v200_v300, axiom, less(v200, v300)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v300_v800, axiom, less(v300, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v8, v32, v72, v100, v200, v300, v600, v800)).
""",
        "fof_conjecture": (
            "~?[X,Y,Z,W]: (in_lopen(X, v0, v800) & leq(v200, X) &"
            "            in_lopen(Y, v0, v600) & leq(v100, Y) &\n"
            "            in_lopen(Z, v0, v32)  & leq(v8,   Z) &\n"
            "            in_lopen(W, v0, v72)  & leq(v300, W))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)\n(declare-const w Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 800.0)) (assert (>= x 200.0))
(assert (> y 0.0)) (assert (<= y 600.0)) (assert (>= y 100.0))
(assert (> z 0.0)) (assert (<= z 32.0))  (assert (>= z 8.0))
(assert (> w 0.0)) (assert (<= w 72.0))  (assert (>= w 300.0))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL363 — Height conflict × 3 compatible → box Conflict
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL363",
        "subdir":        "Composition",
        "name":          "Height conflict × 3 compatible → box Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "Width/Depth/Alt: all compatible\n"
            "Height: lteq 300 ∩ gteq 600 = ∅  Conflict\n"
            "box_verdict(C,box_verdict(Conflict,box_verdict(C,C)))=Conflict\n"
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
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "800"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "300"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "32"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "300"^^xsd:decimal ]
      )
    ]
  ] .
drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "8"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "72"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v8, axiom, val(v8)).
fof(val_v32, axiom, val(v32)).
fof(val_v72, axiom, val(v72)).
fof(val_v100, axiom, val(v100)).
fof(val_v200, axiom, val(v200)).
fof(val_v300, axiom, val(v300)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v8, axiom, less(v0, v8)).
fof(ord_v0_v32, axiom, less(v0, v32)).
fof(ord_v0_v72, axiom, less(v0, v72)).
fof(ord_v0_v100, axiom, less(v0, v100)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v300, axiom, less(v0, v300)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v8_v32, axiom, less(v8, v32)).
fof(ord_v8_v72, axiom, less(v8, v72)).
fof(ord_v8_v100, axiom, less(v8, v100)).
fof(ord_v8_v200, axiom, less(v8, v200)).
fof(ord_v8_v300, axiom, less(v8, v300)).
fof(ord_v8_v600, axiom, less(v8, v600)).
fof(ord_v8_v800, axiom, less(v8, v800)).
fof(ord_v32_v72, axiom, less(v32, v72)).
fof(ord_v32_v100, axiom, less(v32, v100)).
fof(ord_v32_v200, axiom, less(v32, v200)).
fof(ord_v32_v300, axiom, less(v32, v300)).
fof(ord_v32_v600, axiom, less(v32, v600)).
fof(ord_v32_v800, axiom, less(v32, v800)).
fof(ord_v72_v100, axiom, less(v72, v100)).
fof(ord_v72_v200, axiom, less(v72, v200)).
fof(ord_v72_v300, axiom, less(v72, v300)).
fof(ord_v72_v600, axiom, less(v72, v600)).
fof(ord_v72_v800, axiom, less(v72, v800)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v300, axiom, less(v100, v300)).
fof(ord_v100_v600, axiom, less(v100, v600)).
fof(ord_v100_v800, axiom, less(v100, v800)).
fof(ord_v200_v300, axiom, less(v200, v300)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v300_v800, axiom, less(v300, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v8, v32, v72, v100, v200, v300, v600, v800)).
""",
        "fof_conjecture": (
            "~?[X,Y,Z,W]: (in_lopen(X, v0, v800) & leq(v200, X) &"
            "            in_lopen(Y, v0, v300) & leq(v600, Y) &\n"
            "            in_lopen(Z, v0, v32)  & leq(v8,   Z) &\n"
            "            in_lopen(W, v0, v300) & leq(v72,  W))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)\n(declare-const w Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 800.0)) (assert (>= x 200.0))
(assert (> y 0.0)) (assert (<= y 300.0)) (assert (>= y 600.0))
(assert (> z 0.0)) (assert (<= z 32.0))  (assert (>= z 8.0))
(assert (> w 0.0)) (assert (<= w 300.0)) (assert (>= w 72.0))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL364 — Mixed operators across 4 axes → box Compatible
    #
    # FIX 1: fof_extra_decls restored to correct set: v0,v8,v32,v100,
    #         v150,v300,v500,v600,v800. The previous version had v16 and
    #         v72 added (meant for ODRL370) while v150 and v600 were lost.
    #         The conjecture references v600 (X eq constraint) and v150
    #         (W lower bound) — both were undeclared = serious bug.
    # FIX 2: needs_density: True → False. v150 is declared and witnesses
    #         Y in open (100,500): less(v100,v150) & less(v150,v500) .
    #         ORD001 was included unnecessarily causing E ResourceOut.
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL364",
        "subdir":        "Composition",
        "name":          "Mixed operators across 4 axes → box Compatible",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "Width:  eq 600 ∩ lteq 800 = {600} ≠ ∅  Compatible\n"
            "Height: gt 100 ∩ lt 500  = (100,500) ≠ ∅  Compatible\n"
            "Depth:  gteq 8 ∩ lteq 32 = [8,32] ≠ ∅    Compatible\n"
            "Alt:    gteq 150 ∩ lteq 300 = [150,300] ≠ ∅ Compatible\n"
            "Ground witnesses: X=v600, Y=v150, Z=v8, W=v150. No density needed.\n"
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
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:eq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gt ;
          odrl:rightOperand "100"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "8"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "150"^^xsd:decimal ]
      )
    ]
  ] .
drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "800"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lt ;
          odrl:rightOperand "500"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "32"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "300"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v8, axiom, val(v8)).
fof(val_v32, axiom, val(v32)).
fof(val_v100, axiom, val(v100)).
fof(val_v150, axiom, val(v150)).
fof(val_v300, axiom, val(v300)).
fof(val_v500, axiom, val(v500)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v8, axiom, less(v0, v8)).
fof(ord_v0_v32, axiom, less(v0, v32)).
fof(ord_v0_v100, axiom, less(v0, v100)).
fof(ord_v0_v150, axiom, less(v0, v150)).
fof(ord_v0_v300, axiom, less(v0, v300)).
fof(ord_v0_v500, axiom, less(v0, v500)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v8_v32, axiom, less(v8, v32)).
fof(ord_v8_v100, axiom, less(v8, v100)).
fof(ord_v8_v150, axiom, less(v8, v150)).
fof(ord_v8_v300, axiom, less(v8, v300)).
fof(ord_v8_v500, axiom, less(v8, v500)).
fof(ord_v8_v600, axiom, less(v8, v600)).
fof(ord_v8_v800, axiom, less(v8, v800)).
fof(ord_v32_v100, axiom, less(v32, v100)).
fof(ord_v32_v150, axiom, less(v32, v150)).
fof(ord_v32_v300, axiom, less(v32, v300)).
fof(ord_v32_v500, axiom, less(v32, v500)).
fof(ord_v32_v600, axiom, less(v32, v600)).
fof(ord_v32_v800, axiom, less(v32, v800)).
fof(ord_v100_v150, axiom, less(v100, v150)).
fof(ord_v100_v300, axiom, less(v100, v300)).
fof(ord_v100_v500, axiom, less(v100, v500)).
fof(ord_v100_v600, axiom, less(v100, v600)).
fof(ord_v100_v800, axiom, less(v100, v800)).
fof(ord_v150_v300, axiom, less(v150, v300)).
fof(ord_v150_v500, axiom, less(v150, v500)).
fof(ord_v150_v600, axiom, less(v150, v600)).
fof(ord_v150_v800, axiom, less(v150, v800)).
fof(ord_v300_v500, axiom, less(v300, v500)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v300_v800, axiom, less(v300, v800)).
fof(ord_v500_v600, axiom, less(v500, v600)).
fof(ord_v500_v800, axiom, less(v500, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v8, v32, v100, v150, v300, v500, v600, v800)).
""",
        "fof_conjecture": (
            "in_closed(v600, v600, v600) & in_lopen(v600, v0, v800) &\n"
            "    less(v100, v300) & in_open(v300, v0, v500) &\n"
            "    leq(v8, v8) & in_lopen(v8, v0, v32) &\n"
            "    in_lopen(v300, v0, v300) & leq(v150, v300)"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)\n(declare-const w Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (= x 600.0)) (assert (<= x 800.0))
(assert (> y 0.0)) (assert (> y 100.0)) (assert (< y 500.0))
(assert (> z 0.0)) (assert (>= z 8.0))   (assert (<= z 32.0))
(assert (> w 0.0)) (assert (<= w 300.0)) (assert (>= w 150.0))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL365 — Width eq conflict (mixed ops) → box Conflict
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL365",
        "subdir":        "Composition",
        "name":          "Width eq conflict (mixed ops) → box Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "Width:  eq 600 ∩ eq 800 = {600}∩{800}=∅ Conflict (distinct)\n"
            "Height: gt 100 ∩ lt 500 = (100,500) Compatible\n"
            "Depth/Alt: compatible\n"
            "Conflict proved by X distinctness — no density needed.\n"
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
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:eq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gt ;
          odrl:rightOperand "100"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "8"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "150"^^xsd:decimal ]
      )
    ]
  ] .
drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:eq ;
          odrl:rightOperand "800"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lt ;
          odrl:rightOperand "500"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "32"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "300"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v8, axiom, val(v8)).
fof(val_v32, axiom, val(v32)).
fof(val_v100, axiom, val(v100)).
fof(val_v150, axiom, val(v150)).
fof(val_v300, axiom, val(v300)).
fof(val_v500, axiom, val(v500)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v8, axiom, less(v0, v8)).
fof(ord_v0_v32, axiom, less(v0, v32)).
fof(ord_v0_v100, axiom, less(v0, v100)).
fof(ord_v0_v150, axiom, less(v0, v150)).
fof(ord_v0_v300, axiom, less(v0, v300)).
fof(ord_v0_v500, axiom, less(v0, v500)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v8_v32, axiom, less(v8, v32)).
fof(ord_v8_v100, axiom, less(v8, v100)).
fof(ord_v8_v150, axiom, less(v8, v150)).
fof(ord_v8_v300, axiom, less(v8, v300)).
fof(ord_v8_v500, axiom, less(v8, v500)).
fof(ord_v8_v600, axiom, less(v8, v600)).
fof(ord_v8_v800, axiom, less(v8, v800)).
fof(ord_v32_v100, axiom, less(v32, v100)).
fof(ord_v32_v150, axiom, less(v32, v150)).
fof(ord_v32_v300, axiom, less(v32, v300)).
fof(ord_v32_v500, axiom, less(v32, v500)).
fof(ord_v32_v600, axiom, less(v32, v600)).
fof(ord_v32_v800, axiom, less(v32, v800)).
fof(ord_v100_v150, axiom, less(v100, v150)).
fof(ord_v100_v300, axiom, less(v100, v300)).
fof(ord_v100_v500, axiom, less(v100, v500)).
fof(ord_v100_v600, axiom, less(v100, v600)).
fof(ord_v100_v800, axiom, less(v100, v800)).
fof(ord_v150_v300, axiom, less(v150, v300)).
fof(ord_v150_v500, axiom, less(v150, v500)).
fof(ord_v150_v600, axiom, less(v150, v600)).
fof(ord_v150_v800, axiom, less(v150, v800)).
fof(ord_v300_v500, axiom, less(v300, v500)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v300_v800, axiom, less(v300, v800)).
fof(ord_v500_v600, axiom, less(v500, v600)).
fof(ord_v500_v800, axiom, less(v500, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v8, v32, v100, v150, v300, v500, v600, v800)).
""",
        "fof_conjecture": (
            "~?[X,Y,Z,W]: (in_closed(X, v600, v600) & in_closed(X, v800, v800) &"
            "            less(v100, Y) & in_open(Y, v0, v500) &\n"
            "            leq(v8,   Z) & in_lopen(Z, v0, v32) &\n"
            "            in_lopen(W, v0, v300) & leq(v150, W))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)\n(declare-const w Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (= x 600.0)) (assert (= x 800.0))
(assert (> y 0.0)) (assert (> y 100.0)) (assert (< y 500.0))
(assert (> z 0.0)) (assert (>= z 8.0))   (assert (<= z 32.0))
(assert (> w 0.0)) (assert (<= w 300.0)) (assert (>= w 150.0))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL366 — HD video 4-axis: all compatible
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL366",
        "subdir":        "Composition",
        "name":          "HD video 4-axis: all compatible",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "Width:  lteq 1920 ∩ gteq 640  = [640,1920] ≠ ∅ Compatible\n"
            "Height: lteq 1080 ∩ gteq 480  = [480,1080] ≠ ∅ Compatible\n"
            "Depth:  lteq 48   ∩ gteq 16   = [16,48]    ≠ ∅ Compatible\n"
            "Alt:    lteq 600  ∩ gteq 150  = [150,600]  ≠ ∅ Compatible\n"
            "Scaling test with HD video values.\n"
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
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "1920"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "1080"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "48"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
      )
    ]
  ] .
drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "640"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "480"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "16"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "150"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v16, axiom, val(v16)).
fof(val_v48, axiom, val(v48)).
fof(val_v150, axiom, val(v150)).
fof(val_v480, axiom, val(v480)).
fof(val_v600, axiom, val(v600)).
fof(val_v640, axiom, val(v640)).
fof(val_v1080, axiom, val(v1080)).
fof(val_v1920, axiom, val(v1920)).
fof(ord_v0_v16, axiom, less(v0, v16)).
fof(ord_v0_v48, axiom, less(v0, v48)).
fof(ord_v0_v150, axiom, less(v0, v150)).
fof(ord_v0_v480, axiom, less(v0, v480)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v640, axiom, less(v0, v640)).
fof(ord_v0_v1080, axiom, less(v0, v1080)).
fof(ord_v0_v1920, axiom, less(v0, v1920)).
fof(ord_v16_v48, axiom, less(v16, v48)).
fof(ord_v16_v150, axiom, less(v16, v150)).
fof(ord_v16_v480, axiom, less(v16, v480)).
fof(ord_v16_v600, axiom, less(v16, v600)).
fof(ord_v16_v640, axiom, less(v16, v640)).
fof(ord_v16_v1080, axiom, less(v16, v1080)).
fof(ord_v16_v1920, axiom, less(v16, v1920)).
fof(ord_v48_v150, axiom, less(v48, v150)).
fof(ord_v48_v480, axiom, less(v48, v480)).
fof(ord_v48_v600, axiom, less(v48, v600)).
fof(ord_v48_v640, axiom, less(v48, v640)).
fof(ord_v48_v1080, axiom, less(v48, v1080)).
fof(ord_v48_v1920, axiom, less(v48, v1920)).
fof(ord_v150_v480, axiom, less(v150, v480)).
fof(ord_v150_v600, axiom, less(v150, v600)).
fof(ord_v150_v640, axiom, less(v150, v640)).
fof(ord_v150_v1080, axiom, less(v150, v1080)).
fof(ord_v150_v1920, axiom, less(v150, v1920)).
fof(ord_v480_v600, axiom, less(v480, v600)).
fof(ord_v480_v640, axiom, less(v480, v640)).
fof(ord_v480_v1080, axiom, less(v480, v1080)).
fof(ord_v480_v1920, axiom, less(v480, v1920)).
fof(ord_v600_v640, axiom, less(v600, v640)).
fof(ord_v600_v1080, axiom, less(v600, v1080)).
fof(ord_v600_v1920, axiom, less(v600, v1920)).
fof(ord_v640_v1080, axiom, less(v640, v1080)).
fof(ord_v640_v1920, axiom, less(v640, v1920)).
fof(ord_v1080_v1920, axiom, less(v1080, v1920)).
fof(distinct, axiom, $distinct(v0, v16, v48, v150, v480, v600, v640, v1080, v1920)).
""",
        "fof_conjecture": (
            "?[X,Y,Z,W]: (in_lopen(X, v0, v1920) & leq(v640,  X) &"
            "           in_lopen(Y, v0, v1080) & leq(v480,  Y) &\n"
            "           in_lopen(Z, v0, v48)   & leq(v16,   Z) &\n"
            "           in_lopen(W, v0, v600)  & leq(v150,  W))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)\n(declare-const w Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 1920.0)) (assert (>= x 640.0))
(assert (> y 0.0)) (assert (<= y 1080.0)) (assert (>= y 480.0))
(assert (> z 0.0)) (assert (<= z 48.0))   (assert (>= z 16.0))
(assert (> w 0.0)) (assert (<= w 600.0))  (assert (>= w 150.0))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL367 — HD video width conflict → box Conflict
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL367",
        "subdir":        "Composition",
        "name":          "HD video width conflict → box Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "Width:  lteq 640  ∩ gteq 1920 = ∅  Conflict\n"
            "Height/Depth/Alt: same as ODRL366, all compatible\n"
            "box_verdict(Conflict,box_verdict(C,box_verdict(C,C)))=Conflict\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyBSB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "640"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "1080"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "48"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
      )
    ]
  ] .
drk:policyMuseum a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "1920"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "480"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "16"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "150"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v16, axiom, val(v16)).
fof(val_v48, axiom, val(v48)).
fof(val_v150, axiom, val(v150)).
fof(val_v480, axiom, val(v480)).
fof(val_v600, axiom, val(v600)).
fof(val_v640, axiom, val(v640)).
fof(val_v1080, axiom, val(v1080)).
fof(val_v1920, axiom, val(v1920)).
fof(ord_v0_v16, axiom, less(v0, v16)).
fof(ord_v0_v48, axiom, less(v0, v48)).
fof(ord_v0_v150, axiom, less(v0, v150)).
fof(ord_v0_v480, axiom, less(v0, v480)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v640, axiom, less(v0, v640)).
fof(ord_v0_v1080, axiom, less(v0, v1080)).
fof(ord_v0_v1920, axiom, less(v0, v1920)).
fof(ord_v16_v48, axiom, less(v16, v48)).
fof(ord_v16_v150, axiom, less(v16, v150)).
fof(ord_v16_v480, axiom, less(v16, v480)).
fof(ord_v16_v600, axiom, less(v16, v600)).
fof(ord_v16_v640, axiom, less(v16, v640)).
fof(ord_v16_v1080, axiom, less(v16, v1080)).
fof(ord_v16_v1920, axiom, less(v16, v1920)).
fof(ord_v48_v150, axiom, less(v48, v150)).
fof(ord_v48_v480, axiom, less(v48, v480)).
fof(ord_v48_v600, axiom, less(v48, v600)).
fof(ord_v48_v640, axiom, less(v48, v640)).
fof(ord_v48_v1080, axiom, less(v48, v1080)).
fof(ord_v48_v1920, axiom, less(v48, v1920)).
fof(ord_v150_v480, axiom, less(v150, v480)).
fof(ord_v150_v600, axiom, less(v150, v600)).
fof(ord_v150_v640, axiom, less(v150, v640)).
fof(ord_v150_v1080, axiom, less(v150, v1080)).
fof(ord_v150_v1920, axiom, less(v150, v1920)).
fof(ord_v480_v600, axiom, less(v480, v600)).
fof(ord_v480_v640, axiom, less(v480, v640)).
fof(ord_v480_v1080, axiom, less(v480, v1080)).
fof(ord_v480_v1920, axiom, less(v480, v1920)).
fof(ord_v600_v640, axiom, less(v600, v640)).
fof(ord_v600_v1080, axiom, less(v600, v1080)).
fof(ord_v600_v1920, axiom, less(v600, v1920)).
fof(ord_v640_v1080, axiom, less(v640, v1080)).
fof(ord_v640_v1920, axiom, less(v640, v1920)).
fof(ord_v1080_v1920, axiom, less(v1080, v1920)).
fof(distinct, axiom, $distinct(v0, v16, v48, v150, v480, v600, v640, v1080, v1920)).
""",
        "fof_conjecture": (
            "~?[X,Y,Z,W]: (in_lopen(X, v0, v640)  & leq(v1920, X) &"
            "            in_lopen(Y, v0, v1080) & leq(v480,  Y) &\n"
            "            in_lopen(Z, v0, v48)   & leq(v16,   Z) &\n"
            "            in_lopen(W, v0, v600)  & leq(v150,  W))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)\n(declare-const w Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 640.0))  (assert (>= x 1920.0))
(assert (> y 0.0)) (assert (<= y 1080.0)) (assert (>= y 480.0))
(assert (> z 0.0)) (assert (<= z 48.0))   (assert (>= z 16.0))
(assert (> w 0.0)) (assert (<= w 600.0))  (assert (>= w 150.0))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL368 — 4D box A ⊆ B on all axes → Compatible
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL368",
        "subdir":        "Composition",
        "name":          "4D box A ⊆ B on all axes → Compatible",
        "relation":      "subsumption",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "includes": ["ORD000-0.ax", "AXIS000-0.ax", "SUBS000-0.ax"],
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "Width:  (0,600]  ⊆ (0,1200]  Compatible\n"
            "Height: (0,400]  ⊆ (0,800]   Compatible\n"
            "Depth:  (0,16]   ⊆ (0,32]    Compatible\n"
            "Alt:    (0,150]  ⊆ (0,300]   Compatible\n"
            "box_containment: A ⊆ B on all 4 axes [def:box-containment]\n"
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
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "16"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "150"^^xsd:decimal ]
      )
    ]
  ] .
drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "1200"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "800"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "32"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "300"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v16, axiom, val(v16)).
fof(val_v32, axiom, val(v32)).
fof(val_v150, axiom, val(v150)).
fof(val_v300, axiom, val(v300)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v16, axiom, less(v0, v16)).
fof(ord_v0_v32, axiom, less(v0, v32)).
fof(ord_v0_v150, axiom, less(v0, v150)).
fof(ord_v0_v300, axiom, less(v0, v300)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v0_v1200, axiom, less(v0, v1200)).
fof(ord_v16_v32, axiom, less(v16, v32)).
fof(ord_v16_v150, axiom, less(v16, v150)).
fof(ord_v16_v300, axiom, less(v16, v300)).
fof(ord_v16_v400, axiom, less(v16, v400)).
fof(ord_v16_v600, axiom, less(v16, v600)).
fof(ord_v16_v800, axiom, less(v16, v800)).
fof(ord_v16_v1200, axiom, less(v16, v1200)).
fof(ord_v32_v150, axiom, less(v32, v150)).
fof(ord_v32_v300, axiom, less(v32, v300)).
fof(ord_v32_v400, axiom, less(v32, v400)).
fof(ord_v32_v600, axiom, less(v32, v600)).
fof(ord_v32_v800, axiom, less(v32, v800)).
fof(ord_v32_v1200, axiom, less(v32, v1200)).
fof(ord_v150_v300, axiom, less(v150, v300)).
fof(ord_v150_v400, axiom, less(v150, v400)).
fof(ord_v150_v600, axiom, less(v150, v600)).
fof(ord_v150_v800, axiom, less(v150, v800)).
fof(ord_v150_v1200, axiom, less(v150, v1200)).
fof(ord_v300_v400, axiom, less(v300, v400)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v300_v800, axiom, less(v300, v800)).
fof(ord_v300_v1200, axiom, less(v300, v1200)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(ord_v400_v1200, axiom, less(v400, v1200)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(ord_v800_v1200, axiom, less(v800, v1200)).
fof(distinct, axiom, $distinct(v0, v16, v32, v150, v300, v400, v600, v800, v1200)).
""",
        "fof_conjecture": (
            "![X,Y,Z,W]: ((in_lopen(X, v0, v600) & in_lopen(Y, v0, v400) & in_lopen(Z, v0, v16) & in_lopen(W, v0, v150)) =>"
            "              (in_lopen(X, v0, v1200) & in_lopen(Y, v0, v800) & in_lopen(Z, v0, v32) & in_lopen(W, v0, v300)))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)\n(declare-const w Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 600.0))
(assert (> y 0.0)) (assert (<= y 400.0))
(assert (> z 0.0)) (assert (<= z 16.0))
(assert (> w 0.0)) (assert (<= w 150.0))
(assert (not (and (<= x 1200.0) (<= y 800.0) (<= z 32.0) (<= w 300.0))))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL369 — 4D box A ⊄ B: alt axis escape → Conflict
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL369",
        "subdir":        "Composition",
        "name":          "4D box A ⊄ B: alt axis escape → Conflict",
        "relation":      "subsumption",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "includes": ["ORD000-0.ax", "AXIS000-0.ax", "SUBS000-0.ax"],
        "needs_density": False,
        "description": (
            "Width:  (0,600]  ⊆ (0,1200]  Compatible\n"
            "Height: (0,400]  ⊆ (0,800]   Compatible\n"
            "Depth:  (0,16]   ⊆ (0,32]    Compatible\n"
            "Alt:    (0,300]  ⊄ (0,150]   Conflict — escape W=v300\n"
            "box_containment: alt escape → Conflict [def:box-containment]\n"
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
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "16"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "300"^^xsd:decimal ]
      )
    ]
  ] .
drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "1200"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "800"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "32"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "150"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v16, axiom, val(v16)).
fof(val_v32, axiom, val(v32)).
fof(val_v150, axiom, val(v150)).
fof(val_v300, axiom, val(v300)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v16, axiom, less(v0, v16)).
fof(ord_v0_v32, axiom, less(v0, v32)).
fof(ord_v0_v150, axiom, less(v0, v150)).
fof(ord_v0_v300, axiom, less(v0, v300)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v0_v1200, axiom, less(v0, v1200)).
fof(ord_v16_v32, axiom, less(v16, v32)).
fof(ord_v16_v150, axiom, less(v16, v150)).
fof(ord_v16_v300, axiom, less(v16, v300)).
fof(ord_v16_v400, axiom, less(v16, v400)).
fof(ord_v16_v600, axiom, less(v16, v600)).
fof(ord_v16_v800, axiom, less(v16, v800)).
fof(ord_v16_v1200, axiom, less(v16, v1200)).
fof(ord_v32_v150, axiom, less(v32, v150)).
fof(ord_v32_v300, axiom, less(v32, v300)).
fof(ord_v32_v400, axiom, less(v32, v400)).
fof(ord_v32_v600, axiom, less(v32, v600)).
fof(ord_v32_v800, axiom, less(v32, v800)).
fof(ord_v32_v1200, axiom, less(v32, v1200)).
fof(ord_v150_v300, axiom, less(v150, v300)).
fof(ord_v150_v400, axiom, less(v150, v400)).
fof(ord_v150_v600, axiom, less(v150, v600)).
fof(ord_v150_v800, axiom, less(v150, v800)).
fof(ord_v150_v1200, axiom, less(v150, v1200)).
fof(ord_v300_v400, axiom, less(v300, v400)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v300_v800, axiom, less(v300, v800)).
fof(ord_v300_v1200, axiom, less(v300, v1200)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(ord_v400_v1200, axiom, less(v400, v1200)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(ord_v800_v1200, axiom, less(v800, v1200)).
fof(distinct, axiom, $distinct(v0, v16, v32, v150, v300, v400, v600, v800, v1200)).
""",
        "fof_conjecture": (
            "?[X,Y,Z,W]: ((in_lopen(X, v0, v600) & in_lopen(Y, v0, v400) & in_lopen(Z, v0, v16) & in_lopen(W, v0, v300)) &"
            "             ~(in_lopen(X, v0, v1200) & in_lopen(Y, v0, v800) & in_lopen(Z, v0, v32) & in_lopen(W, v0, v150)))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)\n(declare-const w Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 600.0))
(assert (> y 0.0)) (assert (<= y 400.0))
(assert (> z 0.0)) (assert (<= z 16.0))
(assert (> w 0.0)) (assert (<= w 300.0))
(assert (not (and (<= x 1200.0) (<= y 800.0) (<= z 32.0) (<= w 150.0))))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL370 — All 4 axes open intervals → box Compatible (density)
    #
    # FIX: added v16 constant between v8 and v32 (+ 8 ordering facts
    #      + updated $distinct). Z conjunct needs less(v8,Z) &
    #      in_open(Z,v0,v32): no constant existed strictly between v8
    #      and v32. With v16: less(v8,v16)  in_open(v16,v0,v32) .
    #      Ground witnesses: X=v300, Y=v200, Z=v16, W=v100.
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL370",
        "subdir":        "Composition",
        "name":          "All 4 axes open intervals → box Compatible (density)",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "includes": ["ORD000-0.ax", "ORD001-0.ax", "AXIS000-0.ax"],
        "needs_density": True,
        "description": (
            "Width:  gt 200 ∩ lt 800 = (200,800) ≠ ∅  Compatible\n"
            "Height: gt 100 ∩ lt 500 = (100,500) ≠ ∅  Compatible\n"
            "Depth:  gt 8   ∩ lt 32  = (8,32)    ≠ ∅  Compatible\n"
            "Alt:    gt 72  ∩ lt 300 = (72,300)  ≠ ∅  Compatible\n"
            "All witnesses inside open intervals → requires ORD001-0.ax.\n"
            "Ground witnesses: X=v300, Y=v200, Z=v16, W=v100.\n"
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
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:gt ;
          odrl:rightOperand "200"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gt ;
          odrl:rightOperand "100"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:gt ;
          odrl:rightOperand "8"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:gt ;
          odrl:rightOperand "72"^^xsd:decimal ]
      )
    ]
  ] .
drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lt ;
          odrl:rightOperand "800"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lt ;
          odrl:rightOperand "500"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lt ;
          odrl:rightOperand "32"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:lt ;
          odrl:rightOperand "300"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v8, axiom, val(v8)).
fof(val_v16, axiom, val(v16)).
fof(val_v32, axiom, val(v32)).
fof(val_v72, axiom, val(v72)).
fof(val_v100, axiom, val(v100)).
fof(val_v200, axiom, val(v200)).
fof(val_v300, axiom, val(v300)).
fof(val_v500, axiom, val(v500)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v8, axiom, less(v0, v8)).
fof(ord_v0_v16, axiom, less(v0, v16)).
fof(ord_v0_v32, axiom, less(v0, v32)).
fof(ord_v0_v72, axiom, less(v0, v72)).
fof(ord_v0_v100, axiom, less(v0, v100)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v300, axiom, less(v0, v300)).
fof(ord_v0_v500, axiom, less(v0, v500)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v8_v16, axiom, less(v8, v16)).
fof(ord_v8_v32, axiom, less(v8, v32)).
fof(ord_v8_v72, axiom, less(v8, v72)).
fof(ord_v8_v100, axiom, less(v8, v100)).
fof(ord_v8_v200, axiom, less(v8, v200)).
fof(ord_v8_v300, axiom, less(v8, v300)).
fof(ord_v8_v500, axiom, less(v8, v500)).
fof(ord_v8_v800, axiom, less(v8, v800)).
fof(ord_v16_v32, axiom, less(v16, v32)).
fof(ord_v16_v72, axiom, less(v16, v72)).
fof(ord_v16_v100, axiom, less(v16, v100)).
fof(ord_v16_v200, axiom, less(v16, v200)).
fof(ord_v16_v300, axiom, less(v16, v300)).
fof(ord_v16_v500, axiom, less(v16, v500)).
fof(ord_v16_v800, axiom, less(v16, v800)).
fof(ord_v32_v72, axiom, less(v32, v72)).
fof(ord_v32_v100, axiom, less(v32, v100)).
fof(ord_v32_v200, axiom, less(v32, v200)).
fof(ord_v32_v300, axiom, less(v32, v300)).
fof(ord_v32_v500, axiom, less(v32, v500)).
fof(ord_v32_v800, axiom, less(v32, v800)).
fof(ord_v72_v100, axiom, less(v72, v100)).
fof(ord_v72_v200, axiom, less(v72, v200)).
fof(ord_v72_v300, axiom, less(v72, v300)).
fof(ord_v72_v500, axiom, less(v72, v500)).
fof(ord_v72_v800, axiom, less(v72, v800)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v300, axiom, less(v100, v300)).
fof(ord_v100_v500, axiom, less(v100, v500)).
fof(ord_v100_v800, axiom, less(v100, v800)).
fof(ord_v200_v300, axiom, less(v200, v300)).
fof(ord_v200_v500, axiom, less(v200, v500)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v300_v500, axiom, less(v300, v500)).
fof(ord_v300_v800, axiom, less(v300, v800)).
fof(ord_v500_v800, axiom, less(v500, v800)).
fof(distinct, axiom, $distinct(v0, v8, v16, v32, v72, v100, v200, v300, v500, v800)).
""",
        "fof_conjecture": (
            "less(v200, v500) & in_open(v500, v0, v800) &\n"
            "    less(v100, v300) & in_open(v300, v0, v500) &\n"
            "    less(v8,   v16)  & in_open(v16,  v0, v32)  &\n"
            "    less(v72,  v200) & in_open(v200, v0, v300)"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)\n(declare-const w Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (> x 200.0)) (assert (< x 800.0))
(assert (> y 0.0)) (assert (> y 100.0)) (assert (< y 500.0))
(assert (> z 0.0)) (assert (> z 8.0))   (assert (< z 32.0))
(assert (> w 0.0)) (assert (> w 72.0))  (assert (< w 300.0))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL371 — Width oc boundary conflict × 3 compatible → box Conflict
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL371",
        "subdir":        "Composition",
        "name":          "Width oc boundary conflict × 3 compatible → box Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "includes": ["ORD000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "Width:  lt 600  ∩ gteq 600 = (0,600)∩[600,∞)=∅  Conflict (oc)\n"
            "Height/Depth/Alt: all compatible\n"
            "Width proof: order contradiction (X<600 & X≥600), no density needed.\n"
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
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:lt ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "800"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "32"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "300"^^xsd:decimal ]
      )
    ]
  ] .
drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:and (
        [ odrl:leftOperand oax:absoluteSizeWidth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "8"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "150"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v8, axiom, val(v8)).
fof(val_v32, axiom, val(v32)).
fof(val_v150, axiom, val(v150)).
fof(val_v200, axiom, val(v200)).
fof(val_v300, axiom, val(v300)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v8, axiom, less(v0, v8)).
fof(ord_v0_v32, axiom, less(v0, v32)).
fof(ord_v0_v150, axiom, less(v0, v150)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v300, axiom, less(v0, v300)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v8_v32, axiom, less(v8, v32)).
fof(ord_v8_v150, axiom, less(v8, v150)).
fof(ord_v8_v200, axiom, less(v8, v200)).
fof(ord_v8_v300, axiom, less(v8, v300)).
fof(ord_v8_v600, axiom, less(v8, v600)).
fof(ord_v8_v800, axiom, less(v8, v800)).
fof(ord_v32_v150, axiom, less(v32, v150)).
fof(ord_v32_v200, axiom, less(v32, v200)).
fof(ord_v32_v300, axiom, less(v32, v300)).
fof(ord_v32_v600, axiom, less(v32, v600)).
fof(ord_v32_v800, axiom, less(v32, v800)).
fof(ord_v150_v200, axiom, less(v150, v200)).
fof(ord_v150_v300, axiom, less(v150, v300)).
fof(ord_v150_v600, axiom, less(v150, v600)).
fof(ord_v150_v800, axiom, less(v150, v800)).
fof(ord_v200_v300, axiom, less(v200, v300)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v300_v800, axiom, less(v300, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v8, v32, v150, v200, v300, v600, v800)).
""",
        "fof_conjecture": (
            "~?[X,Y,Z,W]: (in_open(X, v0, v600)  & leq(v600, X) &"
            "            in_lopen(Y, v0, v800) & leq(v200, Y) &\n"
            "            in_lopen(Z, v0, v32)  & leq(v8,   Z) &\n"
            "            in_lopen(W, v0, v300) & leq(v150, W))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)\n(declare-const w Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (< x 600.0)) (assert (>= x 600.0))
(assert (> y 0.0)) (assert (<= y 800.0)) (assert (>= y 200.0))
(assert (> z 0.0)) (assert (<= z 32.0))  (assert (>= z 8.0))
(assert (> w 0.0)) (assert (<= w 300.0)) (assert (>= w 150.0))""",
    },
]