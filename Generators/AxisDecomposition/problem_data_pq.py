"""
problem_data_pq.py
==================
PolicyQuality benchmark problems: ODRL400-416 (17 problems).
Category F: Difficulty ladder from trivial (3 constants, 1 axis)
to very hard (12 constants, 4 axes, 66 ordering axioms).
The difficulty ladder (paper: "3-66 ordering axioms"):
  3  axioms: ODRL400-401, 403 (1D, 3 constants)
  6  axioms: ODRL404 (2D, 4 constants)
  10 axioms: ODRL402, 406, 407, 416 (2D, 5 constants)
  21 axioms: ODRL405, 411 (3D, 7 constants)
  28 axioms: ODRL410 (4D, 8 constants)
  36 axioms: ODRL408, 409 (4D, 9 constants)
  55 axioms: ODRL414 (4D, 11 constants)
  66 axioms: ODRL412, 413, 415 (4D, 12 constants) — maximum
Axes used by dimension:
  1D: X = oax:absoluteSizeWidth
  2D: X = width, Y = oax:absoluteSizeHeight
  3D: X = width, Y = height, Z = oax:absoluteSizeDepth
  4D: X = width, Y = height, Z = depth,
      W = oax:spatialCoordinatesAltitude
Domain lower bounds:
  Standard: v0 (excluded, D_k=(0,∞))
  Fractional: v1=1, v2=2, v3=3, v4=4 (ODRL412-415)
TTL: explicit odrl:and for multi-axis policies.
     Single-constraint policies use plain odrl:constraint.
SMT2 comments use ; not %.
TTL prefix: drk: <http://w3id.org/drk/ontology/>

Fixes applied (v1.1 audit):
  ODRL409: normalised dict-key indentation; previous version had 10-space
           indents on `verdict`, `status_fof`, `status_smt`, `difficulty`,
           `needs_density`, and `description` while the rest of the dict
           used 8 spaces. Python accepted it but it looked malformed.
           Also added a comment explaining why 'needs_density' is False
           despite the description mentioning density --- the chain
           contains a named constant in every required open interval
           (v300 in (200,800), v200 in (100,500), v16 in (8,32), v100 in
           (72,300)), so the prover finds ground witnesses and density
           is not needed.

  ODRL414: removed commented-out alternative fof_conjecture (dead code).
           Clarified description: the conjecture is existential, finding
           a 4-tuple (X=v600, Y=v1080-ish, Z=v72, W=v16) that lies in A
           but escapes B on multiple axes. Existence of such a
           counter-witness establishes that A is NOT subsumed by B
           (subsumption Conflict).

All 17 problems verified to close as Theorem under ORD000+AXIS000.
"""
PROBLEMS = [
    # ──────────────────────────────────────────────────────────────────
    # ODRL400 — 1D Conflict (3 constants, minimum difficulty)
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL400",
        "subdir":        "PolicyQuality",
        "name":          "1D Conflict (3 constants, minimum difficulty)",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "Width: lteq 600 → (0,600] ∩ gteq 800 → [800,∞) = ∅ Conflict\n"
            "Minimum difficulty: 3 constants, 3 ordering axioms.\n"
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
      odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "600"^^xsd:decimal
    ]
  ] .
drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ;
      odrl:rightOperand "800"^^xsd:decimal
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v600, v800)).
""",
        "fof_conjecture": (
            "![X]: ~(in_lopen(X, v0, v600) & leq(v800, X))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 600.0))
(assert (>= x 800.0))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL401 — 1D Compatible (3 constants)
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL401",
        "subdir":        "PolicyQuality",
        "name":          "1D Compatible (3 constants)",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "Width: lteq 800 → (0,800] ∩ gteq 200 → [200,∞) = [200,800] ≠ ∅ Compatible\n"
            "Witness: X=v200.\n"
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
      odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "800"^^xsd:decimal
    ]
  ] .
drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ;
      odrl:rightOperand "200"^^xsd:decimal
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v200, axiom, val(v200)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(distinct, axiom, $distinct(v0, v200, v800)).
""",
        "fof_conjecture": (
            "?[X]: (in_lopen(X, v0, v800) & leq(v200, X))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 800.0))
(assert (>= x 200.0))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL402 — 2D Conflict via width (5 constants)
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL402",
        "subdir":        "PolicyQuality",
        "name":          "2D Conflict via width (5 constants)",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "Width: lteq 400 ∩ gteq 800 = ∅ Conflict\n"
            "Height: lteq 600 ∩ gteq 200 = [200,600] ≠ ∅ Compatible\n"
            "Box: Conflict kills box.\n"
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
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v200, axiom, val(v200)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v200, v400, v600, v800)).
""",
        "fof_conjecture": (
            "![X,Y]: ~(in_lopen(X, v0, v400) & leq(v800, X) &\n"
            "          in_lopen(Y, v0, v600) & leq(v200, Y))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 400.0)) (assert (>= x 800.0))
(assert (> y 0.0)) (assert (<= y 600.0)) (assert (>= y 200.0))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL403 — 1D subsumption Compatible (3 constants)
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL403",
        "subdir":        "PolicyQuality",
        "name":          "1D subsumption Compatible (3 constants)",
        "relation":      "subsumption",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "Width: (0,400] ⊆ (0,800] Compatible\n"
            "Minimum difficulty subsumption: 3 constants.\n"
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
      odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "400"^^xsd:decimal
    ]
  ] .
drk:policyB a odrl:Set ;
  odrl:permission [
    odrl:action odrl:use ;
    odrl:constraint [
      odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "800"^^xsd:decimal
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v400, axiom, val(v400)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(distinct, axiom, $distinct(v0, v400, v800)).
""",
        "fof_conjecture": (
            "![X]: (in_lopen(X, v0, v400) => in_lopen(X, v0, v800))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 400.0))
(assert (not (<= x 800.0)))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL404 — 2D oc boundary conflict × compatible (4 constants)
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL404",
        "subdir":        "PolicyQuality",
        "name":          "2D oc boundary conflict × compatible (4 constants)",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "Width: lt 600 → (0,600) ∩ gteq 600 → [600,∞) = ∅ Conflict (oc)\n"
            "Height: lteq 800 ∩ gteq 200 = [200,800] ≠ ∅ Compatible\n"
            "Proof: order contradiction (X<600 & X≥600), no density.\n"
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
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v200, axiom, val(v200)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v200, v600, v800)).
""",
        "fof_conjecture": (
            "![X,Y]: ~(in_open(X, v0, v600) & leq(v600, X) &\n"
            "          in_lopen(Y, v0, v800) & leq(v200, Y))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (< x 600.0)) (assert (>= x 600.0))
(assert (> y 0.0)) (assert (<= y 800.0)) (assert (>= y 200.0))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL405 — 3D mixed operators Compatible (7 constants)
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL405",
        "subdir":        "PolicyQuality",
        "name":          "3D mixed operators Compatible (7 constants)",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "Width: eq 600 ∩ lteq 800 = {600} ≠ ∅ Compatible\n"
            "Height: gteq 200 ∩ lteq 400 = [200,400] ≠ ∅ Compatible\n"
            "Depth: gteq 16 ∩ lteq 32 = [16,32] ≠ ∅ Compatible\n"
            "Witnesses: X=v600, Y=v200, Z=v16 (named constants, no density).\n"
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
          odrl:operator odrl:gteq ;
          odrl:rightOperand "200"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:gteq ;
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
          odrl:rightOperand "800"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "400"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "32"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v16, axiom, val(v16)).
fof(val_v32, axiom, val(v32)).
fof(val_v200, axiom, val(v200)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v16, axiom, less(v0, v16)).
fof(ord_v0_v32, axiom, less(v0, v32)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v16_v32, axiom, less(v16, v32)).
fof(ord_v16_v200, axiom, less(v16, v200)).
fof(ord_v16_v400, axiom, less(v16, v400)).
fof(ord_v16_v600, axiom, less(v16, v600)).
fof(ord_v16_v800, axiom, less(v16, v800)).
fof(ord_v32_v200, axiom, less(v32, v200)).
fof(ord_v32_v400, axiom, less(v32, v400)).
fof(ord_v32_v600, axiom, less(v32, v600)).
fof(ord_v32_v800, axiom, less(v32, v800)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v16, v32, v200, v400, v600, v800)).
""",
        "fof_conjecture": (
            "?[X,Y,Z]: (in_closed(X, v600, v600) & in_lopen(X, v0, v800) &\n"
            "           leq(v200, Y) & in_lopen(Y, v0, v400) &\n"
            "           in_lopen(Z, v0, v32) & leq(v16, Z))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (= x 600.0)) (assert (<= x 800.0))
(assert (> y 0.0)) (assert (<= y 400.0)) (assert (>= y 200.0))
(assert (> z 0.0)) (assert (<= z 32.0)) (assert (>= z 16.0))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL406 — 2D near-miss gap=1 both axes (5 constants)
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL406",
        "subdir":        "PolicyQuality",
        "name":          "2D near-miss gap=1 both axes (5 constants)",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "Width: lteq 599 ∩ gteq 601 = (0,599]∩[601,∞) = ∅ Conflict (599<601)\n"
            "Height: lteq 399 ∩ gteq 401 = (0,399]∩[401,∞) = ∅ Conflict (399<401)\n"
            "Both axes conflict, minimum integer gap.\n"
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
          odrl:rightOperand "599"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "399"^^xsd:decimal ]
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
          odrl:rightOperand "601"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "401"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v399, axiom, val(v399)).
fof(val_v401, axiom, val(v401)).
fof(val_v599, axiom, val(v599)).
fof(val_v601, axiom, val(v601)).
fof(ord_v0_v399, axiom, less(v0, v399)).
fof(ord_v0_v401, axiom, less(v0, v401)).
fof(ord_v0_v599, axiom, less(v0, v599)).
fof(ord_v0_v601, axiom, less(v0, v601)).
fof(ord_v399_v401, axiom, less(v399, v401)).
fof(ord_v399_v599, axiom, less(v399, v599)).
fof(ord_v399_v601, axiom, less(v399, v601)).
fof(ord_v401_v599, axiom, less(v401, v599)).
fof(ord_v401_v601, axiom, less(v401, v601)).
fof(ord_v599_v601, axiom, less(v599, v601)).
fof(distinct, axiom, $distinct(v0, v399, v401, v599, v601)).
""",
        "fof_conjecture": (
            "![X,Y]: ~(in_lopen(X, v0, v599) & leq(v601, X) &\n"
            "          in_lopen(Y, v0, v399) & leq(v401, Y))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 599.0)) (assert (>= x 601.0))
(assert (> y 0.0)) (assert (<= y 399.0)) (assert (>= y 401.0))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL407 — 2D subsumption Compatible (5 constants)
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL407",
        "subdir":        "PolicyQuality",
        "name":          "2D subsumption Compatible (5 constants)",
        "relation":      "subsumption",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "Width: (0,600] ⊆ (0,1200] Compatible\n"
            "Height: (0,400] ⊆ (0,800] Compatible\n"
            "box_containment: A ⊆ B on both axes.\n"
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
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v0_v1200, axiom, less(v0, v1200)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(ord_v400_v1200, axiom, less(v400, v1200)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(ord_v800_v1200, axiom, less(v800, v1200)).
fof(distinct, axiom, $distinct(v0, v400, v600, v800, v1200)).
""",
        "fof_conjecture": (
            "![X,Y]: ((in_lopen(X, v0, v600) & in_lopen(Y, v0, v400)) =>\n"
            "           (in_lopen(X, v0, v1200) & in_lopen(Y, v0, v800)))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 600.0))
(assert (> y 0.0)) (assert (<= y 400.0))
(assert (not (and (<= x 1200.0) (<= y 800.0))))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL408 — 4D near-miss width gap=1 (9 constants)
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL408",
        "subdir":        "PolicyQuality",
        "name":          "4D near-miss width gap=1 (9 constants)",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Hard",
        "needs_density": False,
        "description": (
            "Width: lteq 599 ∩ gteq 601 = ∅ Conflict (599<601)\n"
            "Height/Depth/Alt: all compatible\n"
            "High difficulty: 9 constants, 36 ordering axioms.\n"
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
          odrl:rightOperand "599"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "1080"^^xsd:decimal ]
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
          odrl:rightOperand "601"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "480"^^xsd:decimal ]
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
fof(val_v300, axiom, val(v300)).
fof(val_v480, axiom, val(v480)).
fof(val_v599, axiom, val(v599)).
fof(val_v601, axiom, val(v601)).
fof(val_v1080, axiom, val(v1080)).
fof(ord_v0_v8, axiom, less(v0, v8)).
fof(ord_v0_v32, axiom, less(v0, v32)).
fof(ord_v0_v72, axiom, less(v0, v72)).
fof(ord_v0_v300, axiom, less(v0, v300)).
fof(ord_v0_v480, axiom, less(v0, v480)).
fof(ord_v0_v599, axiom, less(v0, v599)).
fof(ord_v0_v601, axiom, less(v0, v601)).
fof(ord_v0_v1080, axiom, less(v0, v1080)).
fof(ord_v8_v32, axiom, less(v8, v32)).
fof(ord_v8_v72, axiom, less(v8, v72)).
fof(ord_v8_v300, axiom, less(v8, v300)).
fof(ord_v8_v480, axiom, less(v8, v480)).
fof(ord_v8_v599, axiom, less(v8, v599)).
fof(ord_v8_v601, axiom, less(v8, v601)).
fof(ord_v8_v1080, axiom, less(v8, v1080)).
fof(ord_v32_v72, axiom, less(v32, v72)).
fof(ord_v32_v300, axiom, less(v32, v300)).
fof(ord_v32_v480, axiom, less(v32, v480)).
fof(ord_v32_v599, axiom, less(v32, v599)).
fof(ord_v32_v601, axiom, less(v32, v601)).
fof(ord_v32_v1080, axiom, less(v32, v1080)).
fof(ord_v72_v300, axiom, less(v72, v300)).
fof(ord_v72_v480, axiom, less(v72, v480)).
fof(ord_v72_v599, axiom, less(v72, v599)).
fof(ord_v72_v601, axiom, less(v72, v601)).
fof(ord_v72_v1080, axiom, less(v72, v1080)).
fof(ord_v300_v480, axiom, less(v300, v480)).
fof(ord_v300_v599, axiom, less(v300, v599)).
fof(ord_v300_v601, axiom, less(v300, v601)).
fof(ord_v300_v1080, axiom, less(v300, v1080)).
fof(ord_v480_v599, axiom, less(v480, v599)).
fof(ord_v480_v601, axiom, less(v480, v601)).
fof(ord_v480_v1080, axiom, less(v480, v1080)).
fof(ord_v599_v601, axiom, less(v599, v601)).
fof(ord_v599_v1080, axiom, less(v599, v1080)).
fof(ord_v601_v1080, axiom, less(v601, v1080)).
fof(distinct, axiom, $distinct(v0, v8, v32, v72, v300, v480, v599, v601, v1080)).
""",
        "fof_conjecture": (
            "![X,Y,Z,W]: ~(in_lopen(X, v0, v599) & leq(v601, X) &\n"
            "             in_lopen(Y, v0, v1080) & leq(v480, Y) &\n"
            "             in_lopen(Z, v0, v32)   & leq(v8,   Z) &\n"
            "             in_lopen(W, v0, v300)  & leq(v72,  W))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)\n(declare-const w Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 599.0)) (assert (>= x 601.0))
(assert (> y 0.0)) (assert (<= y 1080.0)) (assert (>= y 480.0))
(assert (> z 0.0)) (assert (<= z 32.0))   (assert (>= z 8.0))
(assert (> w 0.0)) (assert (<= w 300.0))  (assert (>= w 72.0))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL409 — 4D all open intervals — density (9 constants)
    # v1.1: normalised dict-key indentation (was mixed 8/10-space).
    # No density needed: chain contains a named constant in each required
    # open interval (v300 in (v200,v800), v200 in (v100,v500),
    # v16 in (v8,v32), v100 in (v72,v300)).
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL409",
        "subdir":        "PolicyQuality",
        "name":          "4D all open intervals — density (9 constants)",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Hard",
        "needs_density": False,
        "description": (
            "Width:  gt 200 ∩ lt 800 = (200,800) ≠ ∅ Compatible\n"
            "Height: gt 100 ∩ lt 500 = (100,500) ≠ ∅ Compatible\n"
            "Depth:  gt 8   ∩ lt 32  = (8,32)    ≠ ∅ Compatible\n"
            "Alt:    gt 72  ∩ lt 300 = (72,300)  ≠ ∅ Compatible\n"
            "Witnesses available from named-constant chain; no density required.\n"
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
fof(ord_v16_v32, axiom, less(v16, v32)).
fof(ord_v16_v72, axiom, less(v16, v72)).
fof(ord_v16_v100, axiom, less(v16, v100)).
fof(ord_v16_v200, axiom, less(v16, v200)).
fof(ord_v16_v300, axiom, less(v16, v300)).
fof(ord_v16_v500, axiom, less(v16, v500)).
fof(ord_v16_v800, axiom, less(v16, v800)).
fof(ord_v8_v100, axiom, less(v8, v100)).
fof(ord_v8_v200, axiom, less(v8, v200)).
fof(ord_v8_v300, axiom, less(v8, v300)).
fof(ord_v8_v500, axiom, less(v8, v500)).
fof(ord_v8_v800, axiom, less(v8, v800)).
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
            "?[X,Y,Z,W]: (less(v200, X) & in_open(X, v0, v800) &\n"
            "             less(v100, Y) & in_open(Y, v0, v500) &\n"
            "             less(v8,   Z) & in_open(Z, v0, v32)  &\n"
            "             less(v72,  W) & in_open(W, v0, v300))"
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
    # ODRL410 — 4D subsumption Compatible — scaling (8 constants)
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL410",
        "subdir":        "PolicyQuality",
        "name":          "4D subsumption Compatible — scaling (8 constants)",
        "relation":      "subsumption",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Hard",
        "needs_density": False,
        "description": (
            "Width:  (0,600]  ⊆ (0,1920]  Compatible\n"
            "Height: (0,400]  ⊆ (0,1080]  Compatible\n"
            "Depth:  (0,16]   ⊆ (0,48]    Compatible\n"
            "Alt:    (0,150]  ⊆ (0,600]   Compatible\n"
            "28 ordering axioms, HD video scaling scenario.\n"
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
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v16, axiom, val(v16)).
fof(val_v48, axiom, val(v48)).
fof(val_v150, axiom, val(v150)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(val_v1080, axiom, val(v1080)).
fof(val_v1920, axiom, val(v1920)).
fof(ord_v0_v16, axiom, less(v0, v16)).
fof(ord_v0_v48, axiom, less(v0, v48)).
fof(ord_v0_v150, axiom, less(v0, v150)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v1080, axiom, less(v0, v1080)).
fof(ord_v0_v1920, axiom, less(v0, v1920)).
fof(ord_v16_v48, axiom, less(v16, v48)).
fof(ord_v16_v150, axiom, less(v16, v150)).
fof(ord_v16_v400, axiom, less(v16, v400)).
fof(ord_v16_v600, axiom, less(v16, v600)).
fof(ord_v16_v1080, axiom, less(v16, v1080)).
fof(ord_v16_v1920, axiom, less(v16, v1920)).
fof(ord_v48_v150, axiom, less(v48, v150)).
fof(ord_v48_v400, axiom, less(v48, v400)).
fof(ord_v48_v600, axiom, less(v48, v600)).
fof(ord_v48_v1080, axiom, less(v48, v1080)).
fof(ord_v48_v1920, axiom, less(v48, v1920)).
fof(ord_v150_v400, axiom, less(v150, v400)).
fof(ord_v150_v600, axiom, less(v150, v600)).
fof(ord_v150_v1080, axiom, less(v150, v1080)).
fof(ord_v150_v1920, axiom, less(v150, v1920)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v400_v1080, axiom, less(v400, v1080)).
fof(ord_v400_v1920, axiom, less(v400, v1920)).
fof(ord_v600_v1080, axiom, less(v600, v1080)).
fof(ord_v600_v1920, axiom, less(v600, v1920)).
fof(ord_v1080_v1920, axiom, less(v1080, v1920)).
fof(distinct, axiom, $distinct(v0, v16, v48, v150, v400, v600, v1080, v1920)).
""",
        "fof_conjecture": (
            "![X,Y,Z,W]: ((in_lopen(X, v0, v600) & in_lopen(Y, v0, v400) & in_lopen(Z, v0, v16) & in_lopen(W, v0, v150)) =>\n"
            "              (in_lopen(X, v0, v1920) & in_lopen(Y, v0, v1080) & in_lopen(Z, v0, v48) & in_lopen(W, v0, v600)))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)\n(declare-const w Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 600.0))
(assert (> y 0.0)) (assert (<= y 400.0))
(assert (> z 0.0)) (assert (<= z 16.0))
(assert (> w 0.0)) (assert (<= w 150.0))
(assert (not (and (<= x 1920.0) (<= y 1080.0) (<= z 48.0) (<= w 600.0))))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL411 — 3D eq conflict via distinctness (7 constants)
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL411",
        "subdir":        "PolicyQuality",
        "name":          "3D eq conflict via distinctness (7 constants)",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "Width: eq 600 ∩ eq 601 = {600}∩{601} = ∅ Conflict (distinct)\n"
            "Height: gt 300 ∩ lt 500 = (300,500) Compatible\n"
            "Depth: gteq 16 ∩ lteq 32 = [16,32] Compatible\n"
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
          odrl:rightOperand "300"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:gteq ;
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
          odrl:operator odrl:eq ;
          odrl:rightOperand "601"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lt ;
          odrl:rightOperand "500"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "32"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v16, axiom, val(v16)).
fof(val_v32, axiom, val(v32)).
fof(val_v300, axiom, val(v300)).
fof(val_v500, axiom, val(v500)).
fof(val_v600, axiom, val(v600)).
fof(val_v601, axiom, val(v601)).
fof(ord_v0_v16, axiom, less(v0, v16)).
fof(ord_v0_v32, axiom, less(v0, v32)).
fof(ord_v0_v300, axiom, less(v0, v300)).
fof(ord_v0_v500, axiom, less(v0, v500)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v601, axiom, less(v0, v601)).
fof(ord_v16_v32, axiom, less(v16, v32)).
fof(ord_v16_v300, axiom, less(v16, v300)).
fof(ord_v16_v500, axiom, less(v16, v500)).
fof(ord_v16_v600, axiom, less(v16, v600)).
fof(ord_v16_v601, axiom, less(v16, v601)).
fof(ord_v32_v300, axiom, less(v32, v300)).
fof(ord_v32_v500, axiom, less(v32, v500)).
fof(ord_v32_v600, axiom, less(v32, v600)).
fof(ord_v32_v601, axiom, less(v32, v601)).
fof(ord_v300_v500, axiom, less(v300, v500)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v300_v601, axiom, less(v300, v601)).
fof(ord_v500_v600, axiom, less(v500, v600)).
fof(ord_v500_v601, axiom, less(v500, v601)).
fof(ord_v600_v601, axiom, less(v600, v601)).
fof(distinct, axiom, $distinct(v0, v16, v32, v300, v500, v600, v601)).
""",
        "fof_conjecture": (
            "![X,Y,Z]: ~(in_closed(X, v600, v600) & in_closed(X, v601, v601) &\n"
            "            less(v300, Y) & in_open(Y, v0, v500) &\n"
            "            leq(v16, Z) & in_lopen(Z, v0, v32))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (= x 600.0)) (assert (= x 601.0))
(assert (> y 0.0)) (assert (> y 300.0)) (assert (< y 500.0))
(assert (> z 0.0)) (assert (<= z 32.0)) (assert (>= z 16.0))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL412 — 4D fractional bounds Conflict (12 constants)
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL412",
        "subdir":        "PolicyQuality",
        "name":          "4D fractional bounds Conflict (12 constants)",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Hard",
        "needs_density": False,
        "description": (
            "Width: lt 599.5 (lb=1) ∩ gteq 600 → X<599.5 AND X≥600 = ∅ Conflict\n"
            "Domain lower bounds: v1,v2,v3,v4 (not v0).\n"
            "Fractional threshold: tests sub-integer precision.\n"
            "66 ordering axioms — maximum difficulty.\n"
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
          odrl:rightOperand "599.5"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gt ;
          odrl:rightOperand "479.5"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:gt ;
          odrl:rightOperand "15.5"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:lt ;
          odrl:rightOperand "71.5"^^xsd:decimal ]
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
          odrl:operator odrl:lt ;
          odrl:rightOperand "480"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lt ;
          odrl:rightOperand "16"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "72"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v1, axiom, val(v1)).
fof(val_v2, axiom, val(v2)).
fof(val_v3, axiom, val(v3)).
fof(val_v4, axiom, val(v4)).
fof(val_v15_5, axiom, val(v15_5)).
fof(val_v16, axiom, val(v16)).
fof(val_v71_5, axiom, val(v71_5)).
fof(val_v72, axiom, val(v72)).
fof(val_v479_5, axiom, val(v479_5)).
fof(val_v480, axiom, val(v480)).
fof(val_v599_5, axiom, val(v599_5)).
fof(val_v600, axiom, val(v600)).
fof(ord_v1_v2, axiom, less(v1, v2)).
fof(ord_v1_v3, axiom, less(v1, v3)).
fof(ord_v1_v4, axiom, less(v1, v4)).
fof(ord_v1_v15_5, axiom, less(v1, v15_5)).
fof(ord_v1_v16, axiom, less(v1, v16)).
fof(ord_v1_v71_5, axiom, less(v1, v71_5)).
fof(ord_v1_v72, axiom, less(v1, v72)).
fof(ord_v1_v479_5, axiom, less(v1, v479_5)).
fof(ord_v1_v480, axiom, less(v1, v480)).
fof(ord_v1_v599_5, axiom, less(v1, v599_5)).
fof(ord_v1_v600, axiom, less(v1, v600)).
fof(ord_v2_v3, axiom, less(v2, v3)).
fof(ord_v2_v4, axiom, less(v2, v4)).
fof(ord_v2_v15_5, axiom, less(v2, v15_5)).
fof(ord_v2_v16, axiom, less(v2, v16)).
fof(ord_v2_v71_5, axiom, less(v2, v71_5)).
fof(ord_v2_v72, axiom, less(v2, v72)).
fof(ord_v2_v479_5, axiom, less(v2, v479_5)).
fof(ord_v2_v480, axiom, less(v2, v480)).
fof(ord_v2_v599_5, axiom, less(v2, v599_5)).
fof(ord_v2_v600, axiom, less(v2, v600)).
fof(ord_v3_v4, axiom, less(v3, v4)).
fof(ord_v3_v15_5, axiom, less(v3, v15_5)).
fof(ord_v3_v16, axiom, less(v3, v16)).
fof(ord_v3_v71_5, axiom, less(v3, v71_5)).
fof(ord_v3_v72, axiom, less(v3, v72)).
fof(ord_v3_v479_5, axiom, less(v3, v479_5)).
fof(ord_v3_v480, axiom, less(v3, v480)).
fof(ord_v3_v599_5, axiom, less(v3, v599_5)).
fof(ord_v3_v600, axiom, less(v3, v600)).
fof(ord_v4_v15_5, axiom, less(v4, v15_5)).
fof(ord_v4_v16, axiom, less(v4, v16)).
fof(ord_v4_v71_5, axiom, less(v4, v71_5)).
fof(ord_v4_v72, axiom, less(v4, v72)).
fof(ord_v4_v479_5, axiom, less(v4, v479_5)).
fof(ord_v4_v480, axiom, less(v4, v480)).
fof(ord_v4_v599_5, axiom, less(v4, v599_5)).
fof(ord_v4_v600, axiom, less(v4, v600)).
fof(ord_v15_5_v16, axiom, less(v15_5, v16)).
fof(ord_v15_5_v71_5, axiom, less(v15_5, v71_5)).
fof(ord_v15_5_v72, axiom, less(v15_5, v72)).
fof(ord_v15_5_v479_5, axiom, less(v15_5, v479_5)).
fof(ord_v15_5_v480, axiom, less(v15_5, v480)).
fof(ord_v15_5_v599_5, axiom, less(v15_5, v599_5)).
fof(ord_v15_5_v600, axiom, less(v15_5, v600)).
fof(ord_v16_v71_5, axiom, less(v16, v71_5)).
fof(ord_v16_v72, axiom, less(v16, v72)).
fof(ord_v16_v479_5, axiom, less(v16, v479_5)).
fof(ord_v16_v480, axiom, less(v16, v480)).
fof(ord_v16_v599_5, axiom, less(v16, v599_5)).
fof(ord_v16_v600, axiom, less(v16, v600)).
fof(ord_v71_5_v72, axiom, less(v71_5, v72)).
fof(ord_v71_5_v479_5, axiom, less(v71_5, v479_5)).
fof(ord_v71_5_v480, axiom, less(v71_5, v480)).
fof(ord_v71_5_v599_5, axiom, less(v71_5, v599_5)).
fof(ord_v71_5_v600, axiom, less(v71_5, v600)).
fof(ord_v72_v479_5, axiom, less(v72, v479_5)).
fof(ord_v72_v480, axiom, less(v72, v480)).
fof(ord_v72_v599_5, axiom, less(v72, v599_5)).
fof(ord_v72_v600, axiom, less(v72, v600)).
fof(ord_v479_5_v480, axiom, less(v479_5, v480)).
fof(ord_v479_5_v599_5, axiom, less(v479_5, v599_5)).
fof(ord_v479_5_v600, axiom, less(v479_5, v600)).
fof(ord_v480_v599_5, axiom, less(v480, v599_5)).
fof(ord_v480_v600, axiom, less(v480, v600)).
fof(ord_v599_5_v600, axiom, less(v599_5, v600)).
fof(distinct, axiom, $distinct(v1, v2, v3, v4, v15_5, v16, v71_5, v72, v479_5, v480, v599_5, v600)).
""",
        "fof_conjecture": (
            "![X,Y,Z,W]: ~(in_open(X, v1, v599_5) & leq(v600, X) &\n"
            "             less(v479_5, Y) & in_open(Y, v2, v480) &\n"
            "             less(v15_5,  Z) & in_open(Z, v3, v16)  &\n"
            "             in_open(W, v4, v71_5) & leq(v72, W))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)\n(declare-const w Real)",
        "smt2_asserts": """\
(assert (> x 1.0))   (assert (< x 599.5))  (assert (>= x 600.0))
(assert (> y 2.0))   (assert (> y 479.5))  (assert (< y 480.0))
(assert (> z 3.0))   (assert (> z 15.5))   (assert (< z 16.0))
(assert (> w 4.0))   (assert (< w 71.5))   (assert (>= w 72.0))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL413 — 4D fractional bounds Compatible (12 constants)
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL413",
        "subdir":        "PolicyQuality",
        "name":          "4D fractional bounds Compatible (12 constants)",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Hard",
        "needs_density": False,
        "description": (
            "Width: lteq 600.5 (lb=1) ∩ gteq 600 → X∈[600,600.5] ≠ ∅ Compatible\n"
            "Height: lteq 480.5 ∩ gteq 480 → [480,480.5] ≠ ∅ Compatible\n"
            "Depth: lteq 16.5 ∩ gteq 16 → [16,16.5] ≠ ∅ Compatible\n"
            "Alt: lteq 72.5 ∩ gteq 72 → [72,72.5] ≠ ∅ Compatible\n"
            "Witnesses: X=600, Y=480, Z=16, W=72 (named constants).\n"
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
          odrl:rightOperand "600.5"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "480.5"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "16.5"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "72.5"^^xsd:decimal ]
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
          odrl:rightOperand "480"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "16"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "72"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v1, axiom, val(v1)).
fof(val_v2, axiom, val(v2)).
fof(val_v3, axiom, val(v3)).
fof(val_v4, axiom, val(v4)).
fof(val_v16, axiom, val(v16)).
fof(val_v16_5, axiom, val(v16_5)).
fof(val_v72, axiom, val(v72)).
fof(val_v72_5, axiom, val(v72_5)).
fof(val_v480, axiom, val(v480)).
fof(val_v480_5, axiom, val(v480_5)).
fof(val_v600, axiom, val(v600)).
fof(val_v600_5, axiom, val(v600_5)).
fof(ord_v1_v2, axiom, less(v1, v2)).
fof(ord_v1_v3, axiom, less(v1, v3)).
fof(ord_v1_v4, axiom, less(v1, v4)).
fof(ord_v1_v16, axiom, less(v1, v16)).
fof(ord_v1_v16_5, axiom, less(v1, v16_5)).
fof(ord_v1_v72, axiom, less(v1, v72)).
fof(ord_v1_v72_5, axiom, less(v1, v72_5)).
fof(ord_v1_v480, axiom, less(v1, v480)).
fof(ord_v1_v480_5, axiom, less(v1, v480_5)).
fof(ord_v1_v600, axiom, less(v1, v600)).
fof(ord_v1_v600_5, axiom, less(v1, v600_5)).
fof(ord_v2_v3, axiom, less(v2, v3)).
fof(ord_v2_v4, axiom, less(v2, v4)).
fof(ord_v2_v16, axiom, less(v2, v16)).
fof(ord_v2_v16_5, axiom, less(v2, v16_5)).
fof(ord_v2_v72, axiom, less(v2, v72)).
fof(ord_v2_v72_5, axiom, less(v2, v72_5)).
fof(ord_v2_v480, axiom, less(v2, v480)).
fof(ord_v2_v480_5, axiom, less(v2, v480_5)).
fof(ord_v2_v600, axiom, less(v2, v600)).
fof(ord_v2_v600_5, axiom, less(v2, v600_5)).
fof(ord_v3_v4, axiom, less(v3, v4)).
fof(ord_v3_v16, axiom, less(v3, v16)).
fof(ord_v3_v16_5, axiom, less(v3, v16_5)).
fof(ord_v3_v72, axiom, less(v3, v72)).
fof(ord_v3_v72_5, axiom, less(v3, v72_5)).
fof(ord_v3_v480, axiom, less(v3, v480)).
fof(ord_v3_v480_5, axiom, less(v3, v480_5)).
fof(ord_v3_v600, axiom, less(v3, v600)).
fof(ord_v3_v600_5, axiom, less(v3, v600_5)).
fof(ord_v4_v16, axiom, less(v4, v16)).
fof(ord_v4_v16_5, axiom, less(v4, v16_5)).
fof(ord_v4_v72, axiom, less(v4, v72)).
fof(ord_v4_v72_5, axiom, less(v4, v72_5)).
fof(ord_v4_v480, axiom, less(v4, v480)).
fof(ord_v4_v480_5, axiom, less(v4, v480_5)).
fof(ord_v4_v600, axiom, less(v4, v600)).
fof(ord_v4_v600_5, axiom, less(v4, v600_5)).
fof(ord_v16_v16_5, axiom, less(v16, v16_5)).
fof(ord_v16_v72, axiom, less(v16, v72)).
fof(ord_v16_v72_5, axiom, less(v16, v72_5)).
fof(ord_v16_v480, axiom, less(v16, v480)).
fof(ord_v16_v480_5, axiom, less(v16, v480_5)).
fof(ord_v16_v600, axiom, less(v16, v600)).
fof(ord_v16_v600_5, axiom, less(v16, v600_5)).
fof(ord_v16_5_v72, axiom, less(v16_5, v72)).
fof(ord_v16_5_v72_5, axiom, less(v16_5, v72_5)).
fof(ord_v16_5_v480, axiom, less(v16_5, v480)).
fof(ord_v16_5_v480_5, axiom, less(v16_5, v480_5)).
fof(ord_v16_5_v600, axiom, less(v16_5, v600)).
fof(ord_v16_5_v600_5, axiom, less(v16_5, v600_5)).
fof(ord_v72_v72_5, axiom, less(v72, v72_5)).
fof(ord_v72_v480, axiom, less(v72, v480)).
fof(ord_v72_v480_5, axiom, less(v72, v480_5)).
fof(ord_v72_v600, axiom, less(v72, v600)).
fof(ord_v72_v600_5, axiom, less(v72, v600_5)).
fof(ord_v72_5_v480, axiom, less(v72_5, v480)).
fof(ord_v72_5_v480_5, axiom, less(v72_5, v480_5)).
fof(ord_v72_5_v600, axiom, less(v72_5, v600)).
fof(ord_v72_5_v600_5, axiom, less(v72_5, v600_5)).
fof(ord_v480_v480_5, axiom, less(v480, v480_5)).
fof(ord_v480_v600, axiom, less(v480, v600)).
fof(ord_v480_v600_5, axiom, less(v480, v600_5)).
fof(ord_v480_5_v600, axiom, less(v480_5, v600)).
fof(ord_v480_5_v600_5, axiom, less(v480_5, v600_5)).
fof(ord_v600_v600_5, axiom, less(v600, v600_5)).
fof(distinct, axiom, $distinct(v1, v2, v3, v4, v16, v16_5, v72, v72_5, v480, v480_5, v600, v600_5)).
""",
        "fof_conjecture": (
            "?[X,Y,Z,W]: (in_lopen(X, v1, v600_5) & leq(v600, X) &\n"
            "           in_lopen(Y, v2, v480_5) & leq(v480, Y) &\n"
            "           in_lopen(Z, v3, v16_5)  & leq(v16,  Z) &\n"
            "           in_lopen(W, v4, v72_5)  & leq(v72,  W))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)\n(declare-const w Real)",
        "smt2_asserts": """\
(assert (> x 1.0)) (assert (<= x 600.5)) (assert (>= x 600.0))
(assert (> y 2.0)) (assert (<= y 480.5)) (assert (>= y 480.0))
(assert (> z 3.0)) (assert (<= z 16.5))  (assert (>= z 16.0))
(assert (> w 4.0)) (assert (<= w 72.5))  (assert (>= w 72.0))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL414 — 4D fractional subsumption Conflict — alt escape (11 constants)
    # v1.1: removed commented-out dead alternative conjecture.
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL414",
        "subdir":        "PolicyQuality",
        "name":          "4D fractional subsumption Conflict — alt escape (11 constants)",
        "relation":      "subsumption",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Hard",
        "needs_density": False,
        "description": (
            "Subsumption Conflict: existential witness exists in A but not in B.\n"
            "  A: eq 600 (width) & gt 300 (height) & gteq 16 (depth) & lt 300 (alt)\n"
            "  B: lteq 1920 (width) & lt 1080 (height) & lteq 48 (depth) & gteq 72 (alt)\n"
            "Witness lies in A but escapes B on multiple axes (e.g., Y near v1080,\n"
            "Z>v48, or W<v72). Existence of such a witness establishes A ⊄ B,\n"
            "i.e., subsumption fails.\n"
            "55 ordering axioms.\n"
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
          odrl:rightOperand "300"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "16"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:lt ;
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
          odrl:rightOperand "1920"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lt ;
          odrl:rightOperand "1080"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "48"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "72"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v1, axiom, val(v1)).
fof(val_v2, axiom, val(v2)).
fof(val_v3, axiom, val(v3)).
fof(val_v4, axiom, val(v4)).
fof(val_v16, axiom, val(v16)).
fof(val_v48, axiom, val(v48)).
fof(val_v72, axiom, val(v72)).
fof(val_v300, axiom, val(v300)).
fof(val_v600, axiom, val(v600)).
fof(val_v1080, axiom, val(v1080)).
fof(val_v1920, axiom, val(v1920)).
fof(ord_v1_v2, axiom, less(v1, v2)).
fof(ord_v1_v3, axiom, less(v1, v3)).
fof(ord_v1_v4, axiom, less(v1, v4)).
fof(ord_v1_v16, axiom, less(v1, v16)).
fof(ord_v1_v48, axiom, less(v1, v48)).
fof(ord_v1_v72, axiom, less(v1, v72)).
fof(ord_v1_v300, axiom, less(v1, v300)).
fof(ord_v1_v600, axiom, less(v1, v600)).
fof(ord_v1_v1080, axiom, less(v1, v1080)).
fof(ord_v1_v1920, axiom, less(v1, v1920)).
fof(ord_v2_v3, axiom, less(v2, v3)).
fof(ord_v2_v4, axiom, less(v2, v4)).
fof(ord_v2_v16, axiom, less(v2, v16)).
fof(ord_v2_v48, axiom, less(v2, v48)).
fof(ord_v2_v72, axiom, less(v2, v72)).
fof(ord_v2_v300, axiom, less(v2, v300)).
fof(ord_v2_v600, axiom, less(v2, v600)).
fof(ord_v2_v1080, axiom, less(v2, v1080)).
fof(ord_v2_v1920, axiom, less(v2, v1920)).
fof(ord_v3_v4, axiom, less(v3, v4)).
fof(ord_v3_v16, axiom, less(v3, v16)).
fof(ord_v3_v48, axiom, less(v3, v48)).
fof(ord_v3_v72, axiom, less(v3, v72)).
fof(ord_v3_v300, axiom, less(v3, v300)).
fof(ord_v3_v600, axiom, less(v3, v600)).
fof(ord_v3_v1080, axiom, less(v3, v1080)).
fof(ord_v3_v1920, axiom, less(v3, v1920)).
fof(ord_v4_v16, axiom, less(v4, v16)).
fof(ord_v4_v48, axiom, less(v4, v48)).
fof(ord_v4_v72, axiom, less(v4, v72)).
fof(ord_v4_v300, axiom, less(v4, v300)).
fof(ord_v4_v600, axiom, less(v4, v600)).
fof(ord_v4_v1080, axiom, less(v4, v1080)).
fof(ord_v4_v1920, axiom, less(v4, v1920)).
fof(ord_v16_v48, axiom, less(v16, v48)).
fof(ord_v16_v72, axiom, less(v16, v72)).
fof(ord_v16_v300, axiom, less(v16, v300)).
fof(ord_v16_v600, axiom, less(v16, v600)).
fof(ord_v16_v1080, axiom, less(v16, v1080)).
fof(ord_v16_v1920, axiom, less(v16, v1920)).
fof(ord_v48_v72, axiom, less(v48, v72)).
fof(ord_v48_v300, axiom, less(v48, v300)).
fof(ord_v48_v600, axiom, less(v48, v600)).
fof(ord_v48_v1080, axiom, less(v48, v1080)).
fof(ord_v48_v1920, axiom, less(v48, v1920)).
fof(ord_v72_v300, axiom, less(v72, v300)).
fof(ord_v72_v600, axiom, less(v72, v600)).
fof(ord_v72_v1080, axiom, less(v72, v1080)).
fof(ord_v72_v1920, axiom, less(v72, v1920)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v300_v1080, axiom, less(v300, v1080)).
fof(ord_v300_v1920, axiom, less(v300, v1920)).
fof(ord_v600_v1080, axiom, less(v600, v1080)).
fof(ord_v600_v1920, axiom, less(v600, v1920)).
fof(ord_v1080_v1920, axiom, less(v1080, v1920)).
fof(distinct, axiom, $distinct(v1, v2, v3, v4, v16, v48, v72, v300, v600, v1080, v1920)).
""",
        "fof_conjecture": (
            "?[X,Y,Z,W]: ((in_closed(X, v600, v600) & less(v300, Y) & leq(v16, Z) & in_open(W, v4, v300))\n"
            "             & ~(in_lopen(X, v1, v1920) & in_open(Y, v2, v1080) & in_lopen(Z, v3, v48) & leq(v72, W)))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)\n(declare-const w Real)",
        "smt2_asserts": """\
(assert (= x 600.0))
(assert (> y 300.0)) (assert (< y 1080.0))
(assert (>= z 16.0)) (assert (<= z 48.0))
(assert (> w 4.0))   (assert (< w 72.0))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL415 — 4D fractional subsumption Compatible — maximum difficulty (12 constants, 66 orderings)
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL415",
        "subdir":        "PolicyQuality",
        "name":          "4D fractional subsumption Compatible — maximum difficulty (12 constants, 66 orderings)",
        "relation":      "subsumption",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "VeryHard",
        "needs_density": False,
        "description": (
            "Width:  (1,599.5] ⊆ (1,600.5] Compatible (599.5<600.5)\n"
            "Height: (2,479.5] ⊆ (2,480.5] Compatible (479.5<480.5)\n"
            "Depth:  (3,15.5]  ⊆ (3,16.5]  Compatible (15.5<16.5)\n"
            "Alt:    (4,71.5]  ⊆ (4,72.5]  Compatible (71.5<72.5)\n"
            "Maximum difficulty: 12 constants, C(12,2)=66 ordering axioms.\n"
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
          odrl:rightOperand "599.5"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "479.5"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "15.5"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "71.5"^^xsd:decimal ]
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
          odrl:rightOperand "600.5"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "480.5"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "16.5"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "72.5"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v1, axiom, val(v1)).
fof(val_v2, axiom, val(v2)).
fof(val_v3, axiom, val(v3)).
fof(val_v4, axiom, val(v4)).
fof(val_v15_5, axiom, val(v15_5)).
fof(val_v16_5, axiom, val(v16_5)).
fof(val_v71_5, axiom, val(v71_5)).
fof(val_v72_5, axiom, val(v72_5)).
fof(val_v479_5, axiom, val(v479_5)).
fof(val_v480_5, axiom, val(v480_5)).
fof(val_v599_5, axiom, val(v599_5)).
fof(val_v600_5, axiom, val(v600_5)).
fof(ord_v1_v2, axiom, less(v1, v2)).
fof(ord_v1_v3, axiom, less(v1, v3)).
fof(ord_v1_v4, axiom, less(v1, v4)).
fof(ord_v1_v15_5, axiom, less(v1, v15_5)).
fof(ord_v1_v16_5, axiom, less(v1, v16_5)).
fof(ord_v1_v71_5, axiom, less(v1, v71_5)).
fof(ord_v1_v72_5, axiom, less(v1, v72_5)).
fof(ord_v1_v479_5, axiom, less(v1, v479_5)).
fof(ord_v1_v480_5, axiom, less(v1, v480_5)).
fof(ord_v1_v599_5, axiom, less(v1, v599_5)).
fof(ord_v1_v600_5, axiom, less(v1, v600_5)).
fof(ord_v2_v3, axiom, less(v2, v3)).
fof(ord_v2_v4, axiom, less(v2, v4)).
fof(ord_v2_v15_5, axiom, less(v2, v15_5)).
fof(ord_v2_v16_5, axiom, less(v2, v16_5)).
fof(ord_v2_v71_5, axiom, less(v2, v71_5)).
fof(ord_v2_v72_5, axiom, less(v2, v72_5)).
fof(ord_v2_v479_5, axiom, less(v2, v479_5)).
fof(ord_v2_v480_5, axiom, less(v2, v480_5)).
fof(ord_v2_v599_5, axiom, less(v2, v599_5)).
fof(ord_v2_v600_5, axiom, less(v2, v600_5)).
fof(ord_v3_v4, axiom, less(v3, v4)).
fof(ord_v3_v15_5, axiom, less(v3, v15_5)).
fof(ord_v3_v16_5, axiom, less(v3, v16_5)).
fof(ord_v3_v71_5, axiom, less(v3, v71_5)).
fof(ord_v3_v72_5, axiom, less(v3, v72_5)).
fof(ord_v3_v479_5, axiom, less(v3, v479_5)).
fof(ord_v3_v480_5, axiom, less(v3, v480_5)).
fof(ord_v3_v599_5, axiom, less(v3, v599_5)).
fof(ord_v3_v600_5, axiom, less(v3, v600_5)).
fof(ord_v4_v15_5, axiom, less(v4, v15_5)).
fof(ord_v4_v16_5, axiom, less(v4, v16_5)).
fof(ord_v4_v71_5, axiom, less(v4, v71_5)).
fof(ord_v4_v72_5, axiom, less(v4, v72_5)).
fof(ord_v4_v479_5, axiom, less(v4, v479_5)).
fof(ord_v4_v480_5, axiom, less(v4, v480_5)).
fof(ord_v4_v599_5, axiom, less(v4, v599_5)).
fof(ord_v4_v600_5, axiom, less(v4, v600_5)).
fof(ord_v15_5_v16_5, axiom, less(v15_5, v16_5)).
fof(ord_v15_5_v71_5, axiom, less(v15_5, v71_5)).
fof(ord_v15_5_v72_5, axiom, less(v15_5, v72_5)).
fof(ord_v15_5_v479_5, axiom, less(v15_5, v479_5)).
fof(ord_v15_5_v480_5, axiom, less(v15_5, v480_5)).
fof(ord_v15_5_v599_5, axiom, less(v15_5, v599_5)).
fof(ord_v15_5_v600_5, axiom, less(v15_5, v600_5)).
fof(ord_v16_5_v71_5, axiom, less(v16_5, v71_5)).
fof(ord_v16_5_v72_5, axiom, less(v16_5, v72_5)).
fof(ord_v16_5_v479_5, axiom, less(v16_5, v479_5)).
fof(ord_v16_5_v480_5, axiom, less(v16_5, v480_5)).
fof(ord_v16_5_v599_5, axiom, less(v16_5, v599_5)).
fof(ord_v16_5_v600_5, axiom, less(v16_5, v600_5)).
fof(ord_v71_5_v72_5, axiom, less(v71_5, v72_5)).
fof(ord_v71_5_v479_5, axiom, less(v71_5, v479_5)).
fof(ord_v71_5_v480_5, axiom, less(v71_5, v480_5)).
fof(ord_v71_5_v599_5, axiom, less(v71_5, v599_5)).
fof(ord_v71_5_v600_5, axiom, less(v71_5, v600_5)).
fof(ord_v72_5_v479_5, axiom, less(v72_5, v479_5)).
fof(ord_v72_5_v480_5, axiom, less(v72_5, v480_5)).
fof(ord_v72_5_v599_5, axiom, less(v72_5, v599_5)).
fof(ord_v72_5_v600_5, axiom, less(v72_5, v600_5)).
fof(ord_v479_5_v480_5, axiom, less(v479_5, v480_5)).
fof(ord_v479_5_v599_5, axiom, less(v479_5, v599_5)).
fof(ord_v479_5_v600_5, axiom, less(v479_5, v600_5)).
fof(ord_v480_5_v599_5, axiom, less(v480_5, v599_5)).
fof(ord_v480_5_v600_5, axiom, less(v480_5, v600_5)).
fof(ord_v599_5_v600_5, axiom, less(v599_5, v600_5)).
fof(distinct, axiom, $distinct(v1, v2, v3, v4, v15_5, v16_5, v71_5, v72_5, v479_5, v480_5, v599_5, v600_5)).
""",
        "fof_conjecture": (
            "![X,Y,Z,W]: ((in_lopen(X, v1, v599_5) & in_lopen(Y, v2, v479_5) & in_lopen(Z, v3, v15_5) & in_lopen(W, v4, v71_5)) =>\n"
            "              (in_lopen(X, v1, v600_5) & in_lopen(Y, v2, v480_5) & in_lopen(Z, v3, v16_5) & in_lopen(W, v4, v72_5)))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)\n(declare-const w Real)",
        "smt2_asserts": """\
(assert (> x 1.0)) (assert (<= x 599.5))
(assert (> y 2.0)) (assert (<= y 479.5))
(assert (> z 3.0)) (assert (<= z 15.5))
(assert (> w 4.0)) (assert (<= w 71.5))
(assert (not (and (> x 1.0) (<= x 600.5) (> y 2.0) (<= y 480.5) (> z 3.0) (<= z 16.5) (> w 4.0) (<= w 72.5))))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL416 — 4D all-touch single point Compatible (5 constants)
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL416",
        "subdir":        "PolicyQuality",
        "name":          "4D all-touch single point Compatible (5 constants)",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Hard",
        "needs_density": False,
        "description": (
            "Width:  lteq 600 ∩ gteq 600 = {600} ≠ ∅ Compatible\n"
            "Height: lteq 480 ∩ gteq 480 = {480} ≠ ∅ Compatible\n"
            "Depth:  lteq 16  ∩ gteq 16  = {16}  ≠ ∅ Compatible\n"
            "Alt:    lteq 72  ∩ gteq 72  = {72}  ≠ ∅ Compatible\n"
            "Box intersection is a single point in R⁴.\n"
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
          odrl:rightOperand "480"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:lteq ;
          odrl:rightOperand "16"^^xsd:decimal ]
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
          odrl:rightOperand "600"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeHeight ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "480"^^xsd:decimal ]
        [ odrl:leftOperand oax:absoluteSizeDepth ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "16"^^xsd:decimal ]
        [ odrl:leftOperand oax:spatialCoordinatesAltitude ;
          odrl:operator odrl:gteq ;
          odrl:rightOperand "72"^^xsd:decimal ]
      )
    ]
  ] .""",
        "fof_extra_decls": """\
fof(val_v0, axiom, val(v0)).
fof(val_v16, axiom, val(v16)).
fof(val_v72, axiom, val(v72)).
fof(val_v480, axiom, val(v480)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v16, axiom, less(v0, v16)).
fof(ord_v0_v72, axiom, less(v0, v72)).
fof(ord_v0_v480, axiom, less(v0, v480)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v16_v72, axiom, less(v16, v72)).
fof(ord_v16_v480, axiom, less(v16, v480)).
fof(ord_v16_v600, axiom, less(v16, v600)).
fof(ord_v72_v480, axiom, less(v72, v480)).
fof(ord_v72_v600, axiom, less(v72, v600)).
fof(ord_v480_v600, axiom, less(v480, v600)).
fof(distinct, axiom, $distinct(v0, v16, v72, v480, v600)).
""",
        "fof_conjecture": (
            "?[X,Y,Z,W]: (in_lopen(X, v0, v600) & leq(v600, X) &\n"
            "           in_lopen(Y, v0, v480) & leq(v480, Y) &\n"
            "           in_lopen(Z, v0, v16)  & leq(v16,  Z) &\n"
            "           in_lopen(W, v0, v72)  & leq(v72,  W))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)\n(declare-const z Real)\n(declare-const w Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 600.0)) (assert (>= x 600.0))
(assert (> y 0.0)) (assert (<= y 480.0)) (assert (>= y 480.0))
(assert (> z 0.0)) (assert (<= z 16.0))  (assert (>= z 16.0))
(assert (> w 0.0)) (assert (<= w 72.0))  (assert (>= w 72.0))""",
    },
]