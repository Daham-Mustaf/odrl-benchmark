"""
problem_data_box3d.py
=====================
Box3D benchmark problems: ODRL340-353 (14 problems).

Category C: Three-axis box verdict aggregation.
Tests def:box-verdict Kleene conjunction nested over width × height × depth.
All problems use absoluteSize with D_k = (0, ∞) for all three axes.

Nesting pattern (paper: def:box-verdict — "for n axes nest associatively"):
  box_verdict(V_w, box_verdict(V_h, V_d))

Interval predicates (paper: def:interval-denotation, D_k = (0,∞)):
  lteq v → in_lopen(X, v0, v)    encodes (0, v]
  gteq v → leq(v, X)             encodes [v, ∞)
  lt   v → in_open(X, v0, v)     encodes (0, v)
  gt   v → less(v, X)            encodes (v, ∞)
  eq   v → in_closed(X, v, v)    encodes {v}

Conjecture structure (3D box = X=width, Y=height, Z=depth):
  conflict/Conflict:   ~?[X,Y,Z]: (A_w(X)&B_w(X) & A_h(Y)&B_h(Y) & A_d(Z)&B_d(Z))
  conflict/Compatible:  ?[X,Y,Z]: (A_w(X)&B_w(X) & A_h(Y)&B_h(Y) & A_d(Z)&B_d(Z))
  subsumption/Compatible: ![X,Y,Z]: (A(X,Y,Z) => B(X,Y,Z))
  subsumption/Conflict:    ?[X,Y,Z]: (A(X,Y,Z) & ~B(X,Y,Z))

Include pattern:
  Discrete : include('Axioms/AXIS000-0.ax').
  Continuous: include('Axioms/ORD001-0.ax').   ← BEFORE AXIS000
              include('Axioms/AXIS000-0.ax').

TTL: explicit odrl:and over 3 constraints per permission [ODRL 2.2 §4.3].
SMT2: three variables x (width), y (height), z (depth), all Real > 0.
TTL prefix: drk: <http://w3id.org/drk/ontology/>
"""

PROBLEMS = [

    # ------------------------------------------------------------------
    # ODRL340 — All three axes conflict → box Conflict
    # Paper: def:box-verdict Rule 1
    # Width:  (0,600] ∩ [800,∞)  = ∅  Conflict
    # Height: (0,300] ∩ [500,∞)  = ∅  Conflict
    # Depth:  (0,8]   ∩ [24,∞)   = ∅  Conflict
    # ------------------------------------------------------------------
    {
        "id":            "ODRL340",
        "subdir":        "Box3D",
        "name":          "All three axes conflict → box Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "Width:  lteq 600 → (0,600]  ∩  gteq 800 → [800,∞)  = ∅  Conflict\n"
            "Height: lteq 300 → (0,300]  ∩  gteq 500 → [500,∞)  = ∅  Conflict\n"
            "Depth:  lteq 8   → (0,8]    ∩  gteq 24  → [24,∞)   = ∅  Conflict\n"
            "box_verdict(Conflict, box_verdict(Conflict, Conflict)) = Conflict"
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
          odrl:rightOperand "300"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "8"^^xsd:decimal ]
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
          odrl:rightOperand "500"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "24"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0,        axiom, val(v0)).
fof(val_v8,        axiom, val(v8)).
fof(val_v24,       axiom, val(v24)).
fof(val_v300,      axiom, val(v300)).
fof(val_v500,      axiom, val(v500)).
fof(val_v600,      axiom, val(v600)).
fof(val_v800,      axiom, val(v800)).
fof(ord_v0_v8,     axiom, less(v0,   v8)).
fof(ord_v0_v24,    axiom, less(v0,   v24)).
fof(ord_v0_v300,   axiom, less(v0,   v300)).
fof(ord_v0_v500,   axiom, less(v0,   v500)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v0_v800,   axiom, less(v0,   v800)).
fof(ord_v8_v24,    axiom, less(v8,   v24)).
fof(ord_v8_v300,   axiom, less(v8,   v300)).
fof(ord_v8_v500,   axiom, less(v8,   v500)).
fof(ord_v8_v600,   axiom, less(v8,   v600)).
fof(ord_v8_v800,   axiom, less(v8,   v800)).
fof(ord_v24_v300,  axiom, less(v24,  v300)).
fof(ord_v24_v500,  axiom, less(v24,  v500)).
fof(ord_v24_v600,  axiom, less(v24,  v600)).
fof(ord_v24_v800,  axiom, less(v24,  v800)).
fof(ord_v300_v500, axiom, less(v300, v500)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v300_v800, axiom, less(v300, v800)).
fof(ord_v500_v600, axiom, less(v500, v600)).
fof(ord_v500_v800, axiom, less(v500, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v8, v24, v300, v500, v600, v800)).
""",
        "fof_conjecture": (
            "~?[X,Y,Z]: (in_lopen(X, v0, v600) & leq(v800, X) &\n"
            "            in_lopen(Y, v0, v300) & leq(v500, Y) &\n"
            "            in_lopen(Z, v0, v8)   & leq(v24,  Z))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 600.0)) (assert (>= x 800.0))
(assert (> y 0.0)) (assert (<= y 300.0)) (assert (>= y 500.0))
(assert (> z 0.0)) (assert (<= z 8.0))   (assert (>= z 24.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL341 — Width conflict × height+depth compatible → box Conflict
    # Paper: def:box-verdict Rule 1
    # Width:  (0,600] ∩ [1200,∞) = ∅  Conflict
    # Height: (0,800] ∩ [200,∞)  ≠ ∅  Compatible
    # Depth:  (0,32]  ∩ [8,∞)    ≠ ∅  Compatible
    # Kleene: Conflict ⊗ Compatible ⊗ Compatible = Conflict
    # ------------------------------------------------------------------
    {
        "id":            "ODRL341",
        "subdir":        "Box3D",
        "name":          "Width conflict × height+depth compatible → box Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "Width:  lteq 600  → (0,600]  ∩  gteq 1200 → [1200,∞) = ∅  Conflict\n"
            "Height: lteq 800  → (0,800]  ∩  gteq 200  → [200,∞)  ≠ ∅  Compatible\n"
            "Depth:  lteq 32   → (0,32]   ∩  gteq 8    → [8,∞)    ≠ ∅  Compatible\n"
            "box_verdict(Conflict, box_verdict(Compatible, Compatible)) = Conflict"
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
          odrl:rightOperand "800"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "32"^^xsd:decimal ]
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
          odrl:rightOperand "1200"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "8"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0,         axiom, val(v0)).
fof(val_v8,         axiom, val(v8)).
fof(val_v32,        axiom, val(v32)).
fof(val_v200,       axiom, val(v200)).
fof(val_v600,       axiom, val(v600)).
fof(val_v800,       axiom, val(v800)).
fof(val_v1200,      axiom, val(v1200)).
fof(ord_v0_v8,      axiom, less(v0,   v8)).
fof(ord_v0_v32,     axiom, less(v0,   v32)).
fof(ord_v0_v200,    axiom, less(v0,   v200)).
fof(ord_v0_v600,    axiom, less(v0,   v600)).
fof(ord_v0_v800,    axiom, less(v0,   v800)).
fof(ord_v0_v1200,   axiom, less(v0,   v1200)).
fof(ord_v8_v32,     axiom, less(v8,   v32)).
fof(ord_v8_v200,    axiom, less(v8,   v200)).
fof(ord_v8_v600,    axiom, less(v8,   v600)).
fof(ord_v8_v800,    axiom, less(v8,   v800)).
fof(ord_v8_v1200,   axiom, less(v8,   v1200)).
fof(ord_v32_v200,   axiom, less(v32,  v200)).
fof(ord_v32_v600,   axiom, less(v32,  v600)).
fof(ord_v32_v800,   axiom, less(v32,  v800)).
fof(ord_v32_v1200,  axiom, less(v32,  v1200)).
fof(ord_v200_v600,  axiom, less(v200, v600)).
fof(ord_v200_v800,  axiom, less(v200, v800)).
fof(ord_v200_v1200, axiom, less(v200, v1200)).
fof(ord_v600_v800,  axiom, less(v600, v800)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(ord_v800_v1200, axiom, less(v800, v1200)).
fof(distinct, axiom, $distinct(v0, v8, v32, v200, v600, v800, v1200)).
""",
        "fof_conjecture": (
            "~?[X,Y,Z]: (in_lopen(X, v0, v600)  & leq(v1200, X) &\n"
            "            in_lopen(Y, v0, v800)  & leq(v200,  Y) &\n"
            "            in_lopen(Z, v0, v32)   & leq(v8,    Z))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 600.0))  (assert (>= x 1200.0))
(assert (> y 0.0)) (assert (<= y 800.0))  (assert (>= y 200.0))
(assert (> z 0.0)) (assert (<= z 32.0))   (assert (>= z 8.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL342 — Height conflict × width+depth compatible → box Conflict
    # Paper: def:box-verdict Rule 1 (commutativity — conflict at position 2)
    # Width:  (0,800] ∩ [200,∞)  = [200,800] ≠ ∅  Compatible
    # Height: (0,300] ∩ [500,∞)  = ∅              Conflict
    # Depth:  (0,32]  ∩ [8,∞)    = [8,32] ≠ ∅     Compatible
    # NOTE: width is Compatible; height conflict kills the box.
    # ------------------------------------------------------------------
    {
        "id":            "ODRL342",
        "subdir":        "Box3D",
        "name":          "Height conflict × width+depth compatible → box Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "Width:  lteq 800 → (0,800]  ∩  gteq 200 → [200,∞) = [200,800] ≠ ∅  Compatible\n"
            "Height: lteq 300 → (0,300]  ∩  gteq 500 → [500,∞) = ∅               Conflict\n"
            "Depth:  lteq 32  → (0,32]   ∩  gteq 8   → [8,∞)   = [8,32] ≠ ∅    Compatible\n"
            "box_verdict(Compatible, box_verdict(Conflict, Compatible)) = Conflict\n"
            "Tests commutativity: conflict at position 2 kills the box."
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
          odrl:rightOperand "500"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "8"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0,        axiom, val(v0)).
fof(val_v8,        axiom, val(v8)).
fof(val_v32,       axiom, val(v32)).
fof(val_v200,      axiom, val(v200)).
fof(val_v300,      axiom, val(v300)).
fof(val_v500,      axiom, val(v500)).
fof(val_v800,      axiom, val(v800)).
fof(ord_v0_v8,     axiom, less(v0,   v8)).
fof(ord_v0_v32,    axiom, less(v0,   v32)).
fof(ord_v0_v200,   axiom, less(v0,   v200)).
fof(ord_v0_v300,   axiom, less(v0,   v300)).
fof(ord_v0_v500,   axiom, less(v0,   v500)).
fof(ord_v0_v800,   axiom, less(v0,   v800)).
fof(ord_v8_v32,    axiom, less(v8,   v32)).
fof(ord_v8_v200,   axiom, less(v8,   v200)).
fof(ord_v8_v300,   axiom, less(v8,   v300)).
fof(ord_v8_v500,   axiom, less(v8,   v500)).
fof(ord_v8_v800,   axiom, less(v8,   v800)).
fof(ord_v32_v200,  axiom, less(v32,  v200)).
fof(ord_v32_v300,  axiom, less(v32,  v300)).
fof(ord_v32_v500,  axiom, less(v32,  v500)).
fof(ord_v32_v800,  axiom, less(v32,  v800)).
fof(ord_v200_v300, axiom, less(v200, v300)).
fof(ord_v200_v500, axiom, less(v200, v500)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v300_v500, axiom, less(v300, v500)).
fof(ord_v300_v800, axiom, less(v300, v800)).
fof(ord_v500_v800, axiom, less(v500, v800)).
fof(distinct, axiom, $distinct(v0, v8, v32, v200, v300, v500, v800)).
""",
        "fof_conjecture": (
            "~?[X,Y,Z]: (in_lopen(X, v0, v800) & leq(v200, X) &\n"
            "            in_lopen(Y, v0, v300) & leq(v500, Y) &\n"
            "            in_lopen(Z, v0, v32)  & leq(v8,   Z))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 800.0)) (assert (>= x 200.0))
(assert (> y 0.0)) (assert (<= y 300.0)) (assert (>= y 500.0))
(assert (> z 0.0)) (assert (<= z 32.0))  (assert (>= z 8.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL343 — Depth conflict × width+height compatible → box Conflict
    # Paper: def:box-verdict Rule 1 (commutativity — conflict at position 3)
    # Width:  (0,800] ∩ [200,∞)  = [200,800] ≠ ∅  Compatible
    # Height: (0,600] ∩ [100,∞)  = [100,600] ≠ ∅  Compatible
    # Depth:  (0,8]   ∩ [24,∞)   = ∅              Conflict
    # NOTE: width and height are Compatible; depth conflict kills the box.
    # ------------------------------------------------------------------
    {
        "id":            "ODRL343",
        "subdir":        "Box3D",
        "name":          "Depth conflict × width+height compatible → box Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "Width:  lteq 800 → (0,800]  ∩  gteq 200 → [200,∞) = [200,800] ≠ ∅  Compatible\n"
            "Height: lteq 600 → (0,600]  ∩  gteq 100 → [100,∞) = [100,600] ≠ ∅  Compatible\n"
            "Depth:  lteq 8   → (0,8]    ∩  gteq 24  → [24,∞)  = ∅               Conflict\n"
            "box_verdict(Compatible, box_verdict(Compatible, Conflict)) = Conflict\n"
            "Tests commutativity: conflict at position 3 kills the box."
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
          odrl:rightOperand "8"^^xsd:decimal ]
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
          odrl:rightOperand "24"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0,        axiom, val(v0)).
fof(val_v8,        axiom, val(v8)).
fof(val_v24,       axiom, val(v24)).
fof(val_v100,      axiom, val(v100)).
fof(val_v200,      axiom, val(v200)).
fof(val_v600,      axiom, val(v600)).
fof(val_v800,      axiom, val(v800)).
fof(ord_v0_v8,     axiom, less(v0,   v8)).
fof(ord_v0_v24,    axiom, less(v0,   v24)).
fof(ord_v0_v100,   axiom, less(v0,   v100)).
fof(ord_v0_v200,   axiom, less(v0,   v200)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v0_v800,   axiom, less(v0,   v800)).
fof(ord_v8_v24,    axiom, less(v8,   v24)).
fof(ord_v8_v100,   axiom, less(v8,   v100)).
fof(ord_v8_v200,   axiom, less(v8,   v200)).
fof(ord_v8_v600,   axiom, less(v8,   v600)).
fof(ord_v8_v800,   axiom, less(v8,   v800)).
fof(ord_v24_v100,  axiom, less(v24,  v100)).
fof(ord_v24_v200,  axiom, less(v24,  v200)).
fof(ord_v24_v600,  axiom, less(v24,  v600)).
fof(ord_v24_v800,  axiom, less(v24,  v800)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v600, axiom, less(v100, v600)).
fof(ord_v100_v800, axiom, less(v100, v800)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v8, v24, v100, v200, v600, v800)).
""",
        "fof_conjecture": (
            "~?[X,Y,Z]: (in_lopen(X, v0, v800) & leq(v200, X) &\n"
            "            in_lopen(Y, v0, v600) & leq(v100, Y) &\n"
            "            in_lopen(Z, v0, v8)   & leq(v24,  Z))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 800.0)) (assert (>= x 200.0))
(assert (> y 0.0)) (assert (<= y 600.0)) (assert (>= y 100.0))
(assert (> z 0.0)) (assert (<= z 8.0))   (assert (>= z 24.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL344 — Width+height conflict × depth compatible → box Conflict
    # Paper: def:box-verdict Rule 1
    # Width:  (0,600] ∩ [800,∞) = ∅  Conflict
    # Height: (0,300] ∩ [500,∞) = ∅  Conflict
    # Depth:  (0,32]  ∩ [8,∞)   ≠ ∅  Compatible
    # ------------------------------------------------------------------
    {
        "id":            "ODRL344",
        "subdir":        "Box3D",
        "name":          "Width+height conflict × depth compatible → box Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "Width:  lteq 600 → (0,600]  ∩  gteq 800 → [800,∞) = ∅  Conflict\n"
            "Height: lteq 300 → (0,300]  ∩  gteq 500 → [500,∞) = ∅  Conflict\n"
            "Depth:  lteq 32  → (0,32]   ∩  gteq 8   → [8,∞)   ≠ ∅  Compatible\n"
            "box_verdict(Conflict, box_verdict(Conflict, Compatible)) = Conflict"
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
          odrl:rightOperand "300"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "32"^^xsd:decimal ]
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
          odrl:rightOperand "500"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "8"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0,        axiom, val(v0)).
fof(val_v8,        axiom, val(v8)).
fof(val_v32,       axiom, val(v32)).
fof(val_v300,      axiom, val(v300)).
fof(val_v500,      axiom, val(v500)).
fof(val_v600,      axiom, val(v600)).
fof(val_v800,      axiom, val(v800)).
fof(ord_v0_v8,     axiom, less(v0,   v8)).
fof(ord_v0_v32,    axiom, less(v0,   v32)).
fof(ord_v0_v300,   axiom, less(v0,   v300)).
fof(ord_v0_v500,   axiom, less(v0,   v500)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v0_v800,   axiom, less(v0,   v800)).
fof(ord_v8_v32,    axiom, less(v8,   v32)).
fof(ord_v8_v300,   axiom, less(v8,   v300)).
fof(ord_v8_v500,   axiom, less(v8,   v500)).
fof(ord_v8_v600,   axiom, less(v8,   v600)).
fof(ord_v8_v800,   axiom, less(v8,   v800)).
fof(ord_v32_v300,  axiom, less(v32,  v300)).
fof(ord_v32_v500,  axiom, less(v32,  v500)).
fof(ord_v32_v600,  axiom, less(v32,  v600)).
fof(ord_v32_v800,  axiom, less(v32,  v800)).
fof(ord_v300_v500, axiom, less(v300, v500)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v300_v800, axiom, less(v300, v800)).
fof(ord_v500_v600, axiom, less(v500, v600)).
fof(ord_v500_v800, axiom, less(v500, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v8, v32, v300, v500, v600, v800)).
""",
        "fof_conjecture": (
            "~?[X,Y,Z]: (in_lopen(X, v0, v600) & leq(v800, X) &\n"
            "            in_lopen(Y, v0, v300) & leq(v500, Y) &\n"
            "            in_lopen(Z, v0, v32)  & leq(v8,   Z))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 600.0)) (assert (>= x 800.0))
(assert (> y 0.0)) (assert (<= y 300.0)) (assert (>= y 500.0))
(assert (> z 0.0)) (assert (<= z 32.0))  (assert (>= z 8.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL345 — All three axes compatible → box Compatible
    # Paper: def:box-verdict Rule 2
    # Width:  [200,800] ≠ ∅  Compatible
    # Height: [100,600] ≠ ∅  Compatible
    # Depth:  [8,32]    ≠ ∅  Compatible
    # Witnesses: X=v200, Y=v100, Z=v8
    # ------------------------------------------------------------------
    {
        "id":            "ODRL345",
        "subdir":        "Box3D",
        "name":          "All three axes compatible → box Compatible",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "Width:  lteq 800 → (0,800]  ∩  gteq 200 → [200,∞) = [200,800] ≠ ∅  Compatible\n"
            "Height: lteq 600 → (0,600]  ∩  gteq 100 → [100,∞) = [100,600] ≠ ∅  Compatible\n"
            "Depth:  lteq 32  → (0,32]   ∩  gteq 8   → [8,∞)   = [8,32]    ≠ ∅  Compatible\n"
            "box_verdict(Compatible, box_verdict(Compatible, Compatible)) = Compatible\n"
            "Witnesses: (X=v200, Y=v100, Z=v8)."
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
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0,        axiom, val(v0)).
fof(val_v8,        axiom, val(v8)).
fof(val_v32,       axiom, val(v32)).
fof(val_v100,      axiom, val(v100)).
fof(val_v200,      axiom, val(v200)).
fof(val_v600,      axiom, val(v600)).
fof(val_v800,      axiom, val(v800)).
fof(ord_v0_v8,     axiom, less(v0,   v8)).
fof(ord_v0_v32,    axiom, less(v0,   v32)).
fof(ord_v0_v100,   axiom, less(v0,   v100)).
fof(ord_v0_v200,   axiom, less(v0,   v200)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v0_v800,   axiom, less(v0,   v800)).
fof(ord_v8_v32,    axiom, less(v8,   v32)).
fof(ord_v8_v100,   axiom, less(v8,   v100)).
fof(ord_v8_v200,   axiom, less(v8,   v200)).
fof(ord_v8_v600,   axiom, less(v8,   v600)).
fof(ord_v8_v800,   axiom, less(v8,   v800)).
fof(ord_v32_v100,  axiom, less(v32,  v100)).
fof(ord_v32_v200,  axiom, less(v32,  v200)).
fof(ord_v32_v600,  axiom, less(v32,  v600)).
fof(ord_v32_v800,  axiom, less(v32,  v800)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v600, axiom, less(v100, v600)).
fof(ord_v100_v800, axiom, less(v100, v800)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v8, v32, v100, v200, v600, v800)).
""",
        "fof_conjecture": (
            "?[X,Y,Z]: (in_lopen(X, v0, v800) & leq(v200, X) &\n"
            "           in_lopen(Y, v0, v600) & leq(v100, Y) &\n"
            "           in_lopen(Z, v0, v32)  & leq(v8,   Z))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 800.0)) (assert (>= x 200.0))
(assert (> y 0.0)) (assert (<= y 600.0)) (assert (>= y 100.0))
(assert (> z 0.0)) (assert (<= z 32.0))  (assert (>= z 8.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL346 — All three axes touch → single-point box Compatible
    # Paper: def:box-verdict Rule 2, thm:criterion (cc: u=l, not disjoint)
    # Width:  {600} ≠ ∅  Compatible (touching)
    # Height: {400} ≠ ∅  Compatible (touching)
    # Depth:  {16}  ≠ ∅  Compatible (touching)
    # Witness: (X=v600, Y=v400, Z=v16) — single point in R³
    # ------------------------------------------------------------------
    {
        "id":            "ODRL346",
        "subdir":        "Box3D",
        "name":          "All three axes touch → single-point box Compatible",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "Width:  lteq 600 → (0,600] ∩ gteq 600 → [600,∞) = {600} ≠ ∅  Compatible\n"
            "Height: lteq 400 → (0,400] ∩ gteq 400 → [400,∞) = {400} ≠ ∅  Compatible\n"
            "Depth:  lteq 16  → (0,16]  ∩ gteq 16  → [16,∞)  = {16}  ≠ ∅  Compatible\n"
            "box_verdict(Compatible, box_verdict(Compatible, Compatible)) = Compatible\n"
            "Witness: (v600, v400, v16). Box intersection is a single point in R³."
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
          odrl:rightOperand "400"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "16"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0,        axiom, val(v0)).
fof(val_v16,       axiom, val(v16)).
fof(val_v400,      axiom, val(v400)).
fof(val_v600,      axiom, val(v600)).
fof(ord_v0_v16,    axiom, less(v0,   v16)).
fof(ord_v0_v400,   axiom, less(v0,   v400)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v16_v400,  axiom, less(v16,  v400)).
fof(ord_v16_v600,  axiom, less(v16,  v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct, axiom, $distinct(v0, v16, v400, v600)).
""",
        "fof_conjecture": (
            "?[X,Y,Z]: (in_lopen(X, v0, v600) & leq(v600, X) &\n"
            "           in_lopen(Y, v0, v400) & leq(v400, Y) &\n"
            "           in_lopen(Z, v0, v16)  & leq(v16,  Z))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 600.0)) (assert (>= x 600.0))
(assert (> y 0.0)) (assert (<= y 400.0)) (assert (>= y 400.0))
(assert (> z 0.0)) (assert (<= z 16.0))  (assert (>= z 16.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL347 — All three axes open overlap → Compatible (density)
    # Paper: def:box-verdict Rule 2, lem:totality, ORD001-0.ax
    # Width:  (200,800) ≠ ∅  Compatible (open witness needs density)
    # Height: (100,500) ≠ ∅  Compatible (open witness needs density)
    # Depth:  (8,32)    ≠ ∅  Compatible (open witness needs density)
    # INCLUDE ORDER: ORD001 BEFORE AXIS000
    # ------------------------------------------------------------------
    {
        "id":            "ODRL347",
        "subdir":        "Box3D",
        "name":          "All three axes open overlap → box Compatible",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "needs_density": True,
        "description": (
            "Width:  gt 200 → (200,∞)  ∩  lt 800 → (0,800) = (200,800) ≠ ∅  Compatible\n"
            "Height: gt 100 → (100,∞)  ∩  lt 500 → (0,500) = (100,500) ≠ ∅  Compatible\n"
            "Depth:  gt 8   → (8,∞)    ∩  lt 32  → (0,32)  = (8,32)    ≠ ∅  Compatible\n"
            "All witnesses inside open intervals → requires ORD001-0.ax (density)."
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
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0,        axiom, val(v0)).
fof(val_v8,        axiom, val(v8)).
fof(val_v32,       axiom, val(v32)).
fof(val_v100,      axiom, val(v100)).
fof(val_v200,      axiom, val(v200)).
fof(val_v500,      axiom, val(v500)).
fof(val_v800,      axiom, val(v800)).
fof(ord_v0_v8,     axiom, less(v0,   v8)).
fof(ord_v0_v32,    axiom, less(v0,   v32)).
fof(ord_v0_v100,   axiom, less(v0,   v100)).
fof(ord_v0_v200,   axiom, less(v0,   v200)).
fof(ord_v0_v500,   axiom, less(v0,   v500)).
fof(ord_v0_v800,   axiom, less(v0,   v800)).
fof(ord_v8_v32,    axiom, less(v8,   v32)).
fof(ord_v8_v100,   axiom, less(v8,   v100)).
fof(ord_v8_v200,   axiom, less(v8,   v200)).
fof(ord_v8_v500,   axiom, less(v8,   v500)).
fof(ord_v8_v800,   axiom, less(v8,   v800)).
fof(ord_v32_v100,  axiom, less(v32,  v100)).
fof(ord_v32_v200,  axiom, less(v32,  v200)).
fof(ord_v32_v500,  axiom, less(v32,  v500)).
fof(ord_v32_v800,  axiom, less(v32,  v800)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v500, axiom, less(v100, v500)).
fof(ord_v100_v800, axiom, less(v100, v800)).
fof(ord_v200_v500, axiom, less(v200, v500)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v500_v800, axiom, less(v500, v800)).
fof(distinct, axiom, $distinct(v0, v8, v32, v100, v200, v500, v800)).
""",
        "fof_conjecture": (
            "?[X,Y,Z]: (less(v200, X) & in_open(X, v0, v800) &\n"
            "           less(v100, Y) & in_open(Y, v0, v500) &\n"
            "           less(v8,   Z) & in_open(Z, v0, v32))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (> x 200.0)) (assert (< x 800.0))
(assert (> y 0.0)) (assert (> y 100.0)) (assert (< y 500.0))
(assert (> z 0.0)) (assert (> z 8.0))   (assert (< z 32.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL348 — Depth open/closed boundary conflict kills 3D box
    # Paper: def:box-verdict Rule 1, thm:criterion (oc case on depth)
    # Width:  (0,800] ∩ [200,∞)  = [200,800] ≠ ∅  Compatible
    # Height: (0,600] ∩ [100,∞)  = [100,600] ≠ ∅  Compatible
    # Depth:  (0,16)  ∩ [16,∞)   = ∅              Conflict (oc case)
    # NOTE: width and height are Compatible; depth oc conflict kills the box.
    # needs_density=False: depth proof is order contradiction (Z<16 & Z≥16).
    # ------------------------------------------------------------------
    {
        "id":            "ODRL348",
        "subdir":        "Box3D",
        "name":          "Depth open/closed boundary conflict kills 3D box",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Hard",
        "needs_density": False,
        "description": (
            "Width:  lteq 800 → (0,800]  ∩  gteq 200 → [200,∞) = [200,800] ≠ ∅  Compatible\n"
            "Height: lteq 600 → (0,600]  ∩  gteq 100 → [100,∞) = [100,600] ≠ ∅  Compatible\n"
            "Depth:  lt 16    → (0,16)   ∩  gteq 16  → [16,∞)  = ∅               Conflict (oc)\n"
            "box_verdict(Compatible, box_verdict(Compatible, Conflict)) = Conflict\n"
            "Depth: order contradiction (Z<16 & Z≥16), no density needed.\n"
            "Tests open-boundary conflict on axis 3 kills the box."
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
          odrl:operator odrl:lt ;
          odrl:rightOperand "16"^^xsd:decimal ]
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
          odrl:rightOperand "16"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0,        axiom, val(v0)).
fof(val_v16,       axiom, val(v16)).
fof(val_v100,      axiom, val(v100)).
fof(val_v200,      axiom, val(v200)).
fof(val_v600,      axiom, val(v600)).
fof(val_v800,      axiom, val(v800)).
fof(ord_v0_v16,    axiom, less(v0,   v16)).
fof(ord_v0_v100,   axiom, less(v0,   v100)).
fof(ord_v0_v200,   axiom, less(v0,   v200)).
fof(ord_v0_v600,   axiom, less(v0,   v600)).
fof(ord_v0_v800,   axiom, less(v0,   v800)).
fof(ord_v16_v100,  axiom, less(v16,  v100)).
fof(ord_v16_v200,  axiom, less(v16,  v200)).
fof(ord_v16_v600,  axiom, less(v16,  v600)).
fof(ord_v16_v800,  axiom, less(v16,  v800)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v600, axiom, less(v100, v600)).
fof(ord_v100_v800, axiom, less(v100, v800)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v16, v100, v200, v600, v800)).
""",
        "fof_conjecture": (
            "~?[X,Y,Z]: (in_lopen(X, v0, v800) & leq(v200, X) &\n"
            "            in_lopen(Y, v0, v600) & leq(v100, Y) &\n"
            "            in_open(Z,  v0, v16)  & leq(v16,  Z))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 800.0)) (assert (>= x 200.0))
(assert (> y 0.0)) (assert (<= y 600.0)) (assert (>= y 100.0))
(assert (> z 0.0)) (assert (< z 16.0))   (assert (>= z 16.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL349 — 3D box A ⊆ B on all axes → Compatible
    # Paper: def:box-containment (Compatible case)
    # (0,600]×(0,400]×(0,16] ⊆ (0,1200]×(0,800]×(0,32]
    # ------------------------------------------------------------------
    {
        "id":            "ODRL349",
        "subdir":        "Box3D",
        "name":          "3D box A ⊆ B on all axes → Compatible",
        "relation":      "subsumption",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "Width:  (0,600]  ⊆ (0,1200]  Compatible\n"
            "Height: (0,400]  ⊆ (0,800]   Compatible\n"
            "Depth:  (0,16]   ⊆ (0,32]    Compatible\n"
            "box_containment: A ⊆ B on all 3 axes → Compatible  [def:box-containment]\n"
            "SMT: no escape witness in any axis → unsat."
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
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0,         axiom, val(v0)).
fof(val_v16,        axiom, val(v16)).
fof(val_v32,        axiom, val(v32)).
fof(val_v400,       axiom, val(v400)).
fof(val_v600,       axiom, val(v600)).
fof(val_v800,       axiom, val(v800)).
fof(val_v1200,      axiom, val(v1200)).
fof(ord_v0_v16,     axiom, less(v0,   v16)).
fof(ord_v0_v32,     axiom, less(v0,   v32)).
fof(ord_v0_v400,    axiom, less(v0,   v400)).
fof(ord_v0_v600,    axiom, less(v0,   v600)).
fof(ord_v0_v800,    axiom, less(v0,   v800)).
fof(ord_v0_v1200,   axiom, less(v0,   v1200)).
fof(ord_v16_v32,    axiom, less(v16,  v32)).
fof(ord_v16_v400,   axiom, less(v16,  v400)).
fof(ord_v16_v600,   axiom, less(v16,  v600)).
fof(ord_v16_v800,   axiom, less(v16,  v800)).
fof(ord_v16_v1200,  axiom, less(v16,  v1200)).
fof(ord_v32_v400,   axiom, less(v32,  v400)).
fof(ord_v32_v600,   axiom, less(v32,  v600)).
fof(ord_v32_v800,   axiom, less(v32,  v800)).
fof(ord_v32_v1200,  axiom, less(v32,  v1200)).
fof(ord_v400_v600,  axiom, less(v400, v600)).
fof(ord_v400_v800,  axiom, less(v400, v800)).
fof(ord_v400_v1200, axiom, less(v400, v1200)).
fof(ord_v600_v800,  axiom, less(v600, v800)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(ord_v800_v1200, axiom, less(v800, v1200)).
fof(distinct, axiom, $distinct(v0, v16, v32, v400, v600, v800, v1200)).
""",
        "fof_conjecture": (
            "![X,Y,Z]: ((in_lopen(X, v0, v600) & in_lopen(Y, v0, v400) & in_lopen(Z, v0, v16)) =>\n"
            "           (in_lopen(X, v0, v1200) & in_lopen(Y, v0, v800) & in_lopen(Z, v0, v32)))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 600.0))
(assert (> y 0.0)) (assert (<= y 400.0))
(assert (> z 0.0)) (assert (<= z 16.0))
(assert (not (and (<= x 1200.0) (<= y 800.0) (<= z 32.0))))""",
    },

    # ------------------------------------------------------------------
    # ODRL350 — Depth breaks 3D subsumption → Conflict
    # Paper: def:box-containment (Conflict case)
    # Width:  (0,600]  ⊆ (0,1200]  Compatible
    # Height: (0,400]  ⊆ (0,800]   Compatible
    # Depth:  (0,32]   ⊄ (0,16]    Conflict — escape witness Z=v32∈A_d, Z∉B_d
    # ------------------------------------------------------------------
    {
        "id":            "ODRL350",
        "subdir":        "Box3D",
        "name":          "Depth breaks 3D subsumption → Conflict",
        "relation":      "subsumption",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "Width:  (0,600]  ⊆ (0,1200]  Compatible\n"
            "Height: (0,400]  ⊆ (0,800]   Compatible\n"
            "Depth:  (0,32]   ⊄ (0,16]    Conflict — escape Z=v32 ∈ A_d, Z ∉ B_d\n"
            "box_containment: depth escape → Conflict  [def:box-containment]\n"
            "SMT: escape witness (any x∈A_w, any y∈A_h, z=32) → sat."
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
          odrl:rightOperand "32"^^xsd:decimal ]
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
          odrl:rightOperand "16"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0,         axiom, val(v0)).
fof(val_v16,        axiom, val(v16)).
fof(val_v32,        axiom, val(v32)).
fof(val_v400,       axiom, val(v400)).
fof(val_v600,       axiom, val(v600)).
fof(val_v800,       axiom, val(v800)).
fof(val_v1200,      axiom, val(v1200)).
fof(ord_v0_v16,     axiom, less(v0,   v16)).
fof(ord_v0_v32,     axiom, less(v0,   v32)).
fof(ord_v0_v400,    axiom, less(v0,   v400)).
fof(ord_v0_v600,    axiom, less(v0,   v600)).
fof(ord_v0_v800,    axiom, less(v0,   v800)).
fof(ord_v0_v1200,   axiom, less(v0,   v1200)).
fof(ord_v16_v32,    axiom, less(v16,  v32)).
fof(ord_v16_v400,   axiom, less(v16,  v400)).
fof(ord_v16_v600,   axiom, less(v16,  v600)).
fof(ord_v16_v800,   axiom, less(v16,  v800)).
fof(ord_v16_v1200,  axiom, less(v16,  v1200)).
fof(ord_v32_v400,   axiom, less(v32,  v400)).
fof(ord_v32_v600,   axiom, less(v32,  v600)).
fof(ord_v32_v800,   axiom, less(v32,  v800)).
fof(ord_v32_v1200,  axiom, less(v32,  v1200)).
fof(ord_v400_v600,  axiom, less(v400, v600)).
fof(ord_v400_v800,  axiom, less(v400, v800)).
fof(ord_v400_v1200, axiom, less(v400, v1200)).
fof(ord_v600_v800,  axiom, less(v600, v800)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(ord_v800_v1200, axiom, less(v800, v1200)).
fof(distinct, axiom, $distinct(v0, v16, v32, v400, v600, v800, v1200)).
""",
        "fof_conjecture": (
            "?[X,Y,Z]: ((in_lopen(X, v0, v600) & in_lopen(Y, v0, v400) & in_lopen(Z, v0, v32)) &\n"
            "           ~(in_lopen(X, v0, v1200) & in_lopen(Y, v0, v800) & in_lopen(Z, v0, v16)))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 600.0))
(assert (> y 0.0)) (assert (<= y 400.0))
(assert (> z 0.0)) (assert (<= z 32.0))
(assert (not (and (<= x 1200.0) (<= y 800.0) (<= z 16.0))))""",
    },

    # ------------------------------------------------------------------
    # ODRL351 — BSB extended to 3D: width conflict × h+d compatible → Conflict
    # Paper: def:box-verdict Rule 1, ex:bsb extended to 3 axes
    # Width:  (0,600] ∩ [1200,∞) = ∅  Conflict
    # Height: (0,600] ∩ [400,∞)  ≠ ∅  Compatible
    # Depth:  (0,32]  ∩ [8,∞)    ≠ ∅  Compatible
    # ------------------------------------------------------------------
    {
        "id":            "ODRL351",
        "subdir":        "Box3D",
        "name":          "BSB 3D: width conflict × height+depth compatible → box Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "Width:  lteq 600  → (0,600]  ∩  gteq 1200 → [1200,∞) = ∅  Conflict\n"
            "Height: lteq 600  → (0,600]  ∩  gteq 400  → [400,∞)  ≠ ∅  Compatible\n"
            "Depth:  lteq 32   → (0,32]   ∩  gteq 8    → [8,∞)    ≠ ∅  Compatible\n"
            "box_verdict(Conflict, box_verdict(Compatible, Compatible)) = Conflict\n"
            "BSB running example extended to 3 axes (ex:bsb)."
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
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "32"^^xsd:decimal ]
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
          odrl:rightOperand "1200"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "8"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0,         axiom, val(v0)).
fof(val_v8,         axiom, val(v8)).
fof(val_v32,        axiom, val(v32)).
fof(val_v400,       axiom, val(v400)).
fof(val_v600,       axiom, val(v600)).
fof(val_v1200,      axiom, val(v1200)).
fof(ord_v0_v8,      axiom, less(v0,   v8)).
fof(ord_v0_v32,     axiom, less(v0,   v32)).
fof(ord_v0_v400,    axiom, less(v0,   v400)).
fof(ord_v0_v600,    axiom, less(v0,   v600)).
fof(ord_v0_v1200,   axiom, less(v0,   v1200)).
fof(ord_v8_v32,     axiom, less(v8,   v32)).
fof(ord_v8_v400,    axiom, less(v8,   v400)).
fof(ord_v8_v600,    axiom, less(v8,   v600)).
fof(ord_v8_v1200,   axiom, less(v8,   v1200)).
fof(ord_v32_v400,   axiom, less(v32,  v400)).
fof(ord_v32_v600,   axiom, less(v32,  v600)).
fof(ord_v32_v1200,  axiom, less(v32,  v1200)).
fof(ord_v400_v600,  axiom, less(v400, v600)).
fof(ord_v400_v1200, axiom, less(v400, v1200)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct, axiom, $distinct(v0, v8, v32, v400, v600, v1200)).
""",
        "fof_conjecture": (
            "~?[X,Y,Z]: (in_lopen(X, v0, v600)  & leq(v1200, X) &\n"
            "            in_lopen(Y, v0, v600)  & leq(v400,  Y) &\n"
            "            in_lopen(Z, v0, v32)   & leq(v8,    Z))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 600.0))  (assert (>= x 1200.0))
(assert (> y 0.0)) (assert (<= y 600.0))  (assert (>= y 400.0))
(assert (> z 0.0)) (assert (<= z 32.0))   (assert (>= z 8.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL352 — Associativity of 3-axis box_verdict nesting  [KEY TEST]
    # Paper: def:box-verdict — "For n axes nest associatively"
    # Tests both nestings give the same result:
    #   box_verdict(conflict, box_verdict(compatible, compatible)) = conflict
    #   box_verdict(box_verdict(conflict, compatible), compatible) = conflict
    # Forces Vampire to use Section D axioms — no interval arithmetic.
    # No ordering constants needed.
    # ------------------------------------------------------------------
    {
        "id":            "ODRL352",
        "subdir":        "Box3D",
        "name":          "Associativity: both nestings of box_verdict give Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "Tests def:box-verdict associativity:\n"
            "box_verdict(conflict, box_verdict(compatible, compatible)) = conflict\n"
            "AND\n"
            "box_verdict(box_verdict(conflict, compatible), compatible) = conflict\n"
            "Both nestings produce the same result (conflict dominates).\n"
            "Forces Section D axioms directly — no interval arithmetic."
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
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "32"^^xsd:decimal ]
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
          odrl:rightOperand "200"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "8"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": "",
        "fof_conjecture": (
            "box_verdict(conflict, box_verdict(compatible, compatible)) = conflict &\n"
            "box_verdict(box_verdict(conflict, compatible), compatible) = conflict"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "",
        "smt2_asserts": """\
; Kleene: conflict=0, compatible=2, box_verdict = min
; Negation: min(0,min(2,2))!=0 OR min(min(0,2),2)!=0
; min(0,2)=0, min(2,2)=2, min(0,2)=0 -> both =0, negation is unsat
(assert (not (and (= (ite (<= 0.0 (ite (<= 2.0 2.0) 2.0 2.0)) 0.0 (ite (<= 2.0 2.0) 2.0 2.0)) 0.0)
                  (= (ite (<= (ite (<= 0.0 2.0) 0.0 2.0) 2.0) (ite (<= 0.0 2.0) 0.0 2.0) 2.0) 0.0))))""",
    },

    # ------------------------------------------------------------------
    # ODRL353 — prop:monotone in 3D context
    # Paper: prop:monotone, lem:conflict-propagation
    # Narrowing the width axis (A_narrow ⊆ A_wide) propagates Conflict:
    # A_wide width [0,800] conflicts with B width [900,1200]
    # → A_narrow width [200,600] also conflicts with B width [900,1200]
    # → box verdict = Conflict (one conflicting axis kills the 3D box)
    # Uses axis_subsumes + axis_conflict from Section B, then 3D box.
    # ------------------------------------------------------------------
    {
        "id":            "ODRL353",
        "subdir":        "Box3D",
        "name":          "prop:monotone in 3D: narrowing width propagates Conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "axis_subsumes(v200,v600, v0,v800): [200,600] ⊆ [0,800]  (narrow ⊆ wide)\n"
            "axis_conflict(v0,v800, v900,v1200): [0,800] ∩ [900,1200] = ∅  (wide conflicts)\n"
            "Height+Depth: compatible on both policies\n"
            "prop:monotone → axis_conflict(v200,v600, v900,v1200) → box Conflict\n"
            "Uses Section B predicates. No new axioms needed."
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
          odrl:operator odrl:gteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "32"^^xsd:decimal ]
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
          odrl:rightOperand "900"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "100"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "8"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0,          axiom, val(v0)).
fof(val_v8,          axiom, val(v8)).
fof(val_v32,         axiom, val(v32)).
fof(val_v100,        axiom, val(v100)).
fof(val_v200,        axiom, val(v200)).
fof(val_v400,        axiom, val(v400)).
fof(val_v600,        axiom, val(v600)).
fof(val_v800,        axiom, val(v800)).
fof(val_v900,        axiom, val(v900)).
fof(val_v1200,       axiom, val(v1200)).
fof(ord_v0_v8,       axiom, less(v0,   v8)).
fof(ord_v0_v32,      axiom, less(v0,   v32)).
fof(ord_v0_v100,     axiom, less(v0,   v100)).
fof(ord_v0_v200,     axiom, less(v0,   v200)).
fof(ord_v0_v400,     axiom, less(v0,   v400)).
fof(ord_v0_v600,     axiom, less(v0,   v600)).
fof(ord_v0_v800,     axiom, less(v0,   v800)).
fof(ord_v0_v900,     axiom, less(v0,   v900)).
fof(ord_v0_v1200,    axiom, less(v0,   v1200)).
fof(ord_v8_v32,      axiom, less(v8,   v32)).
fof(ord_v8_v100,     axiom, less(v8,   v100)).
fof(ord_v8_v200,     axiom, less(v8,   v200)).
fof(ord_v8_v400,     axiom, less(v8,   v400)).
fof(ord_v8_v600,     axiom, less(v8,   v600)).
fof(ord_v8_v800,     axiom, less(v8,   v800)).
fof(ord_v8_v900,     axiom, less(v8,   v900)).
fof(ord_v8_v1200,    axiom, less(v8,   v1200)).
fof(ord_v32_v100,    axiom, less(v32,  v100)).
fof(ord_v32_v200,    axiom, less(v32,  v200)).
fof(ord_v32_v400,    axiom, less(v32,  v400)).
fof(ord_v32_v600,    axiom, less(v32,  v600)).
fof(ord_v32_v800,    axiom, less(v32,  v800)).
fof(ord_v32_v900,    axiom, less(v32,  v900)).
fof(ord_v32_v1200,   axiom, less(v32,  v1200)).
fof(ord_v100_v200,   axiom, less(v100, v200)).
fof(ord_v100_v400,   axiom, less(v100, v400)).
fof(ord_v100_v600,   axiom, less(v100, v600)).
fof(ord_v100_v800,   axiom, less(v100, v800)).
fof(ord_v100_v900,   axiom, less(v100, v900)).
fof(ord_v100_v1200,  axiom, less(v100, v1200)).
fof(ord_v200_v400,   axiom, less(v200, v400)).
fof(ord_v200_v600,   axiom, less(v200, v600)).
fof(ord_v200_v800,   axiom, less(v200, v800)).
fof(ord_v200_v900,   axiom, less(v200, v900)).
fof(ord_v200_v1200,  axiom, less(v200, v1200)).
fof(ord_v400_v600,   axiom, less(v400, v600)).
fof(ord_v400_v800,   axiom, less(v400, v800)).
fof(ord_v400_v900,   axiom, less(v400, v900)).
fof(ord_v400_v1200,  axiom, less(v400, v1200)).
fof(ord_v600_v800,   axiom, less(v600, v800)).
fof(ord_v600_v900,   axiom, less(v600, v900)).
fof(ord_v600_v1200,  axiom, less(v600, v1200)).
fof(ord_v800_v900,   axiom, less(v800, v900)).
fof(ord_v800_v1200,  axiom, less(v800, v1200)).
fof(ord_v900_v1200,  axiom, less(v900, v1200)).
fof(distinct, axiom, $distinct(v0, v8, v32, v100, v200, v400, v600, v800, v900, v1200)).
""",
        "fof_conjecture": (
            "(axis_subsumes(v200, v600, v0, v800) &\n"
            " axis_conflict(v0, v800, v900, v1200))\n"
            "=> ~?[X,Y,Z]: (in_lopen(X, v0, v600) & leq(v900,  X) &\n"
            "               in_lopen(Y, v0, v400) & leq(v100,  Y) &\n"
            "               in_lopen(Z, v0, v32)  & leq(v8,    Z))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)",
        "smt2_asserts": """\
; Negation: x in [200,600] AND x in [900,1200] (monotone conclusion fails)
(assert (>= x 200.0)) (assert (<= x 600.0))
(assert (>= x 900.0)) (assert (<= x 1200.0))
(assert (> y 0.0))    (assert (<= y 400.0))  (assert (>= y 100.0))
(assert (> z 0.0))    (assert (<= z 32.0))   (assert (>= z 8.0))""",
    },

]
