"""
problem_data.py
===============
SingleAxis benchmark problems: ODRL300-314 (15 problems).
Category A: Single-axis interval conflict / compatible / subsumption.
Tests all five ODRL operators (eq, lt, lteq, gt, gteq) and both
discrete (no density) and continuous (density) domains.

Verdict algebra (paper: def:verdict-algebra, def:box-containment):
  Three verdicts only: Conflict / Compatible / Unknown
  relation = "conflict"     — tests interval intersection
    Conflict    ~?[X]: (A(X) & B(X))        Theorem  / unsat
    Compatible   ?[X]: (A(X) & B(X))        Theorem  / sat
  relation = "subsumption"  — tests interval containment
    Compatible  ![X]: (A(X) => B(X))        Theorem  / unsat
    Conflict     ?[X]: (A(X) & ~B(X))       Theorem  / sat
  Unknown — axis unconstrained by one policy; not submitted to prover.

Domain encoding (paper: def:interval-denotation, def:profile):
  All problems use absoluteSize axes with D_k = (0, inf).
  v0 represents the domain lower bound (inf D_k = 0), which is
  EXCLUDED from D_k.  The left-open predicate in_lopen(X, v0, v)
  encodes (0, v]; in_open(X, v0, v) encodes (0, v).
  Problem files assert val(v0) and less(v0, vN) for all vN.
  The SMT encoding enforces domain membership via (assert (> x 0.0)).

needs_density flag:
  True  — a witness must be found inside an open interval (200,800).
          Requires ORD001-0.ax (density axiom).
  False — witness is a named constant, or proof is by order contradiction
          (Conflict cases with lt/gt operators are order tautologies;
          density is never needed to prove emptiness of intersection).

TTL prefix: drk: <http://w3id.org/drk/ontology/>
Include pattern:
  Discrete domain : include('Axioms/AXIS000-0.ax').
  Continuous      : include('Axioms/ORD001-0.ax').
                    include('Axioms/AXIS000-0.ax').
"""

PROBLEMS = [
    # ------------------------------------------------------------------
    # ODRL300 — lteq vs gteq: disjoint → Conflict
    # Paper: def:interval-denotation, thm:criterion (cc case: u1 < l2)
    # sem(lteq 600) = (0,600], sem(gteq 800) = [800,inf)
    # (0,600] ∩ [800,inf) = ∅  by less(v600, v800)
    # ------------------------------------------------------------------
    {
        "id":            "ODRL300",
        "subdir":        "SingleAxis",
        "name":          "width ≤ 600 vs width ≥ 800: disjoint intervals",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "width lteq 600 → (0, 600]   [def:interval-denotation, lteq]\n"
            "width gteq 800 → [800, ∞)   [def:interval-denotation, gteq]\n"
            "(0, 600] ∩ [800, ∞) = ∅     by less(v600, v800)\n"
            "Conflict Criterion (cc): u1=600 closed, l2=800 closed → u1 < l2."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ;
      odrl:rightOperand "800"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
% v0 = domain lower bound (excluded); v600, v800 = constraint values
fof(val_v0,        axiom, val(v0)).
fof(val_v600,      axiom, val(v600)).
fof(val_v800,      axiom, val(v800)).
fof(ord_v0_v600,   axiom, less(v0, v600)).
fof(ord_v0_v800,   axiom, less(v0, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct,      axiom, $distinct(v0, v600, v800)).
""",
        "fof_conjecture": "~?[X]: (in_lopen(X, v0, v600) & leq(v800, X))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 600.0))
(assert (>= x 800.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL301 — eq vs eq: distinct points → Conflict
    # Paper: def:interval-denotation (eq), thm:criterion (cc: u1=l1=600 < l2=u2=800)
    # sem(eq 600) = {600}, sem(eq 800) = {800}
    # {600} ∩ {800} = ∅  by distinct(v600, v800)
    # ------------------------------------------------------------------
    {
        "id":            "ODRL301",
        "subdir":        "SingleAxis",
        "name":          "width = 600 vs width = 800: distinct points",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "width eq 600 → {600}         [def:interval-denotation, eq]\n"
            "width eq 800 → {800}         [def:interval-denotation, eq]\n"
            "{600} ∩ {800} = ∅            by $distinct(v600, v800)\n"
            "Conflict Criterion (cc): u1=600, l2=800, both closed → 600 < 800."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ;
      odrl:rightOperand "800"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
% v0 = domain lower bound (excluded); v600, v800 = constraint values
fof(val_v0,        axiom, val(v0)).
fof(val_v600,      axiom, val(v600)).
fof(val_v800,      axiom, val(v800)).
fof(ord_v0_v600,   axiom, less(v0, v600)).
fof(ord_v0_v800,   axiom, less(v0, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct,      axiom, $distinct(v0, v600, v800)).
""",
        "fof_conjecture": "~?[X]: (in_closed(X, v600, v600) & in_closed(X, v800, v800))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (= x 600.0))
(assert (= x 800.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL302 — lt vs gteq: open/closed boundary → Conflict
    # Paper: def:interval-denotation, thm:criterion (oc case: u1 ≤ l2)
    # sem(lt 600)   = (0, 600)   [inf D_k excluded → in_open]
    # sem(gteq 600) = [600, ∞)
    # (0,600) ∩ [600,∞) = ∅  by Conflict Criterion oc: u1=600 open, l2=600 closed → u1 ≤ l2
    # needs_density: False — Conflict proof is an order contradiction (X<600 & X≥600),
    #   no witness required.  Density would be needed only to exhibit a witness inside (0,600).
    # ------------------------------------------------------------------
    {
        "id":            "ODRL302",
        "subdir":        "SingleAxis",
        "name":          "width < 600 vs width ≥ 600: open/closed boundary",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "width lt 600   → (0, 600)    [def:interval-denotation, lt; D_k=(0,∞)]\n"
            "width gteq 600 → [600, ∞)   [def:interval-denotation, gteq]\n"
            "(0, 600) ∩ [600, ∞) = ∅\n"
            "Conflict Criterion (oc): u1=600 open, l2=600 closed → u1 ≤ l2.\n"
            "Proof is order contradiction (X<600 & X≥600); density not needed."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lt ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
% v0 = domain lower bound (excluded); v600 = constraint value
% in_open(X,v0,v600) encodes (0,600) = sem(lt 600) over D_k=(0,inf)
fof(val_v0,      axiom, val(v0)).
fof(val_v600,    axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct,    axiom, $distinct(v0, v600)).
""",
        "fof_conjecture": "~?[X]: (in_open(X, v0, v600) & leq(v600, X))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (< x 600.0))
(assert (>= x 600.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL303 — gt vs lteq: mirror boundary → Conflict
    # Paper: def:interval-denotation, thm:criterion (co case: u2 ≤ l1)
    # sem(gt 600)   = (600, ∞)
    # sem(lteq 600) = (0, 600]
    # (600,∞) ∩ (0,600] = ∅  by Conflict Criterion co: u2=600 closed, l1=600 open → u2 ≤ l1
    # needs_density: False — proof is order contradiction (X>600 & X≤600),
    #   symmetric to ODRL302; no witness required.
    # ------------------------------------------------------------------
    {
        "id":            "ODRL303",
        "subdir":        "SingleAxis",
        "name":          "width > 600 vs width ≤ 600: mirror boundary",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "width gt 600   → (600, ∞)   [def:interval-denotation, gt]\n"
            "width lteq 600 → (0, 600]   [def:interval-denotation, lteq]\n"
            "(600, ∞) ∩ (0, 600] = ∅\n"
            "Conflict Criterion (co): u2=600 closed, l1=600 open → u2 ≤ l1.\n"
            "Symmetric to ODRL302. Proof is order contradiction; density not needed."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gt ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
% v0 = domain lower bound (excluded); v600 = constraint value
fof(val_v0,      axiom, val(v0)).
fof(val_v600,    axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct,    axiom, $distinct(v0, v600)).
""",
        "fof_conjecture": "~?[X]: (less(v600, X) & in_lopen(X, v0, v600))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (> x 600.0))
(assert (<= x 600.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL304 — lteq vs gteq: overlapping → Compatible
    # Paper: def:interval-denotation, def:axis-verdict (non-empty intersection)
    # sem(lteq 600) = (0, 600], sem(gteq 200) = [200, ∞)
    # (0,600] ∩ [200,∞) = [200,600] ≠ ∅   Witness: X = v200
    # ------------------------------------------------------------------
    {
        "id":            "ODRL304",
        "subdir":        "SingleAxis",
        "name":          "width ≤ 600 vs width ≥ 200: overlapping intervals",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "width lteq 600 → (0, 600]   [def:interval-denotation, lteq]\n"
            "width gteq 200 → [200, ∞)   [def:interval-denotation, gteq]\n"
            "(0, 600] ∩ [200, ∞) = [200, 600] ≠ ∅\n"
            "Witness: X = v200 (named constant, no density needed)."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ;
      odrl:rightOperand "200"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
% v0 = domain lower bound (excluded); v200, v600 = constraint values
fof(val_v0,        axiom, val(v0)).
fof(val_v200,      axiom, val(v200)).
fof(val_v600,      axiom, val(v600)).
fof(ord_v0_v200,   axiom, less(v0, v200)).
fof(ord_v0_v600,   axiom, less(v0, v600)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(distinct,      axiom, $distinct(v0, v200, v600)).
""",
        "fof_conjecture": "?[X]: (in_lopen(X, v0, v600) & leq(v200, X))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 600.0))
(assert (>= x 200.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL305 — lteq touch gteq: touching at boundary → Compatible
    # Paper: def:interval-denotation, thm:criterion (cc: NOT u1 < l2 since u1=l2=600)
    # sem(lteq 600) = (0, 600], sem(gteq 600) = [600, ∞)
    # (0,600] ∩ [600,∞) = {600} ≠ ∅   Witness: X = v600
    # ------------------------------------------------------------------
    {
        "id":            "ODRL305",
        "subdir":        "SingleAxis",
        "name":          "width ≤ 600 vs width ≥ 600: touching at 600",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "needs_density": False,
        "description": (
            "width lteq 600 → (0, 600]   [def:interval-denotation, lteq]\n"
            "width gteq 600 → [600, ∞)   [def:interval-denotation, gteq]\n"
            "(0, 600] ∩ [600, ∞) = {600} ≠ ∅\n"
            "Witness: X = v600. Tests closed-closed boundary touch (cc case).\n"
            "Conflict Criterion: u1=600 closed, l2=600 closed → need u1 < l2,\n"
            "but 600 = 600 so criterion NOT satisfied → Compatible."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] . 
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
% v0 = domain lower bound (excluded); v600 = boundary value (witness)
fof(val_v0,      axiom, val(v0)).
fof(val_v600,    axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct,    axiom, $distinct(v0, v600)).
""",
        "fof_conjecture": "?[X]: (in_lopen(X, v0, v600) & leq(v600, X))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 600.0))
(assert (>= x 600.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL306 — eq vs eq same point → Compatible
    # Paper: def:interval-denotation (eq), def:axis-verdict
    # sem(eq 600) = {600}, {600} ∩ {600} = {600} ≠ ∅
    # Witness: X = v600
    # ------------------------------------------------------------------
    {
        "id":            "ODRL306",
        "subdir":        "SingleAxis",
        "name":          "width = 600 vs width = 600: identical points",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "width eq 600 → {600}         [def:interval-denotation, eq]\n"
            "width eq 600 → {600}         [def:interval-denotation, eq]\n"
            "{600} ∩ {600} = {600} ≠ ∅\n"
            "Witness: X = v600."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
% v0 = domain lower bound (excluded); v600 = constraint value (witness)
fof(val_v0,      axiom, val(v0)).
fof(val_v600,    axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct,    axiom, $distinct(v0, v600)).
""",
        "fof_conjecture": "?[X]: (in_closed(X, v600, v600) & in_closed(X, v600, v600))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (= x 600.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL307 — eq vs lteq: point inside interval → Compatible
    # Paper: def:interval-denotation, def:axis-verdict
    # sem(eq 400) = {400}, sem(lteq 600) = (0, 600]
    # {400} ∩ (0,600] = {400} ≠ ∅   Witness: X = v400
    # ------------------------------------------------------------------
    {
        "id":            "ODRL307",
        "subdir":        "SingleAxis",
        "name":          "width = 400 vs width ≤ 600: point inside interval",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "width eq 400   → {400}       [def:interval-denotation, eq]\n"
            "width lteq 600 → (0, 600]    [def:interval-denotation, lteq]\n"
            "{400} ∩ (0, 600] = {400} ≠ ∅\n"
            "Witness: X = v400 (named constant, no density needed)."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ;
      odrl:rightOperand "400"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
% v0 = domain lower bound (excluded); v400, v600 = constraint values
fof(val_v0,        axiom, val(v0)).
fof(val_v400,      axiom, val(v400)).
fof(val_v600,      axiom, val(v600)).
fof(ord_v0_v400,   axiom, less(v0, v400)).
fof(ord_v0_v600,   axiom, less(v0, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct,      axiom, $distinct(v0, v400, v600)).
""",
        "fof_conjecture": "?[X]: (in_closed(X, v400, v400) & in_lopen(X, v0, v600))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (= x 400.0))
(assert (<= x 600.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL308 — gt vs lt: open overlap → Compatible (density required)
    # Paper: def:interval-denotation, def:axis-verdict, lem:totality + density
    # sem(gt 200)  = (200, ∞)      [def:interval-denotation, gt]
    # sem(lt 800)  = (0, 800)      [def:interval-denotation, lt; D_k=(0,∞)]
    # (200,∞) ∩ (0,800) = (200,800) ≠ ∅
    # Witness lies in open interval (200,800) — requires ORD001-0.ax (density)
    # to guarantee existence of a term strictly between v200 and v800.
    # ------------------------------------------------------------------
    {
        "id":            "ODRL308",
        "subdir":        "SingleAxis",
        "name":          "width > 200 vs width < 800: open overlap",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "needs_density": True,
        "description": (
            "width gt 200 → (200, ∞)     [def:interval-denotation, gt]\n"
            "width lt 800 → (0, 800)     [def:interval-denotation, lt; D_k=(0,∞)]\n"
            "(200, ∞) ∩ (0, 800) = (200, 800) ≠ ∅\n"
            "Witness must lie strictly inside open interval (200,800).\n"
            "Requires ORD001-0.ax: density guarantees ∃Z. v200 < Z < v800."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gt ;
      odrl:rightOperand "200"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lt ;
      odrl:rightOperand "800"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
% v0 = domain lower bound (excluded); v200, v800 = constraint values
% in_open(X,v0,v800) encodes (0,800) = sem(lt 800) over D_k=(0,inf)
fof(val_v0,        axiom, val(v0)).
fof(val_v200,      axiom, val(v200)).
fof(val_v800,      axiom, val(v800)).
fof(ord_v0_v200,   axiom, less(v0, v200)).
fof(ord_v0_v800,   axiom, less(v0, v800)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(distinct,      axiom, $distinct(v0, v200, v800)).
""",
        "fof_conjecture": "?[X]: (less(v200, X) & in_open(X, v0, v800))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (> x 200.0))
(assert (< x 800.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL309 — lteq ⊆ lteq: tighter subsumes wider → Compatible
    # Paper: def:box-containment, lem:conflict-propagation
    # sem(lteq 600) = (0,600] ⊆ (0,1200] = sem(lteq 1200)
    # FOF: ∀X. X∈A → X∈B    SMT: ∄X. X∈A ∧ X∉B (unsat)
    # ------------------------------------------------------------------
    {
        "id":            "ODRL309",
        "subdir":        "SingleAxis",
        "name":          "(0,600] ⊆ (0,1200]: tighter bound subsumes wider",
        "relation":      "subsumption",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "width lteq 600  → (0, 600]   [def:interval-denotation, lteq]\n"
            "width lteq 1200 → (0, 1200]  [def:interval-denotation, lteq]\n"
            "(0, 600] ⊆ (0, 1200]         [def:box-containment, Compatible]\n"
            "SMT: ∄x. x∈(0,600] ∧ x∉(0,1200] → unsat."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "1200"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
% v0 = domain lower bound (excluded); v600, v1200 = constraint values
fof(val_v0,         axiom, val(v0)).
fof(val_v600,       axiom, val(v600)).
fof(val_v1200,      axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v0_v1200,   axiom, less(v0, v1200)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct,       axiom, $distinct(v0, v600, v1200)).
""",
        "fof_conjecture": "![X]: (in_lopen(X, v0, v600) => in_lopen(X, v0, v1200))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 600.0))
(assert (not (<= x 1200.0)))""",
    },

    # ------------------------------------------------------------------
    # ODRL310 — lteq ⊄ lteq: wider does not subsume tighter → Conflict
    # Paper: def:box-containment (Conflict case), lem:conflict-propagation
    # sem(lteq 1200) = (0,1200] ⊄ (0,600] = sem(lteq 600)
    # Counterexample: X = v800 ∈ (0,1200] but v800 ∉ (0,600]
    # ------------------------------------------------------------------
    {
        "id":            "ODRL310",
        "subdir":        "SingleAxis",
        "name":          "(0,1200] ⊄ (0,600]: wider does not subsume tighter",
        "relation":      "subsumption",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "width lteq 1200 → (0, 1200]  [def:interval-denotation, lteq]\n"
            "width lteq 600  → (0, 600]   [def:interval-denotation, lteq]\n"
            "(0, 1200] ⊄ (0, 600]         [def:box-containment, Conflict]\n"
            "Counterexample: X = v800 ∈ (0,1200] but v800 ∉ (0,600]\n"
            "since less(v600, v800) and less(v800, v1200)."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "1200"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
% v0 = domain lower bound (excluded); v600, v800, v1200 = constraint/witness values
% v800 witnesses X ∈ A \ B
fof(val_v0,         axiom, val(v0)).
fof(val_v600,       axiom, val(v600)).
fof(val_v800,       axiom, val(v800)).
fof(val_v1200,      axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v0_v800,    axiom, less(v0, v800)).
fof(ord_v0_v1200,   axiom, less(v0, v1200)).
fof(ord_v600_v800,  axiom, less(v600, v800)).
fof(ord_v800_v1200, axiom, less(v800, v1200)).
fof(distinct,       axiom, $distinct(v0, v600, v800, v1200)).
""",
        "fof_conjecture": "?[X]: (in_lopen(X, v0, v1200) & ~in_lopen(X, v0, v600))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 1200.0))
(assert (not (<= x 600.0)))""",
    },

    # ------------------------------------------------------------------
    # ODRL311 — gteq ⊆ gteq: higher lower-bound subsumes → Compatible
    # Paper: def:box-containment, lem:conflict-propagation
    # sem(gteq 800) = [800,∞) ⊆ [400,∞) = sem(gteq 400)
    # ------------------------------------------------------------------
    {
        "id":            "ODRL311",
        "subdir":        "SingleAxis",
        "name":          "[800,∞) ⊆ [400,∞): higher lower-bound subsumes",
        "relation":      "subsumption",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "width gteq 800 → [800, ∞)   [def:interval-denotation, gteq]\n"
            "width gteq 400 → [400, ∞)   [def:interval-denotation, gteq]\n"
            "[800, ∞) ⊆ [400, ∞)          [def:box-containment, Compatible]\n"
            "since less(v400, v800) → ∀X. X≥800 → X≥400."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ;
      odrl:rightOperand "800"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ;
      odrl:rightOperand "400"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
% v0 = domain lower bound (excluded); v400, v800 = constraint values
fof(val_v0,        axiom, val(v0)).
fof(val_v400,      axiom, val(v400)).
fof(val_v800,      axiom, val(v800)).
fof(ord_v0_v400,   axiom, less(v0, v400)).
fof(ord_v0_v800,   axiom, less(v0, v800)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(distinct,      axiom, $distinct(v0, v400, v800)).
""",
        "fof_conjecture": "![X]: (leq(v800, X) => leq(v400, X))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (>= x 800.0))
(assert (not (>= x 400.0)))""",
    },

    # ------------------------------------------------------------------
    # ODRL312 — eq ⊆ lteq: point inside interval → Compatible
    # Paper: def:box-containment, lem:totality
    # sem(eq 400) = {400} ⊆ (0,600] = sem(lteq 600)
    # since less(v0,v400) & less(v400,v600) → v400 ∈ (0,600]
    # ------------------------------------------------------------------
    {
        "id":            "ODRL312",
        "subdir":        "SingleAxis",
        "name":          "{400} ⊆ (0,600]: point inside interval",
        "relation":      "subsumption",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "width eq 400   → {400}       [def:interval-denotation, eq]\n"
            "width lteq 600 → (0, 600]    [def:interval-denotation, lteq]\n"
            "{400} ⊆ (0, 600]             [def:box-containment, Compatible]\n"
            "since less(v0,v400) and less(v400,v600) → v400 ∈ (0,600]."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ;
      odrl:rightOperand "400"^^xsd:decimal ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
% v0 = domain lower bound (excluded); v400, v600 = constraint values
fof(val_v0,        axiom, val(v0)).
fof(val_v400,      axiom, val(v400)).
fof(val_v600,      axiom, val(v600)).
fof(ord_v0_v400,   axiom, less(v0, v400)).
fof(ord_v0_v600,   axiom, less(v0, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct,      axiom, $distinct(v0, v400, v600)).
""",
        "fof_conjecture": "![X]: (in_closed(X, v400, v400) => in_lopen(X, v0, v600))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (= x 400.0))
(assert (not (<= x 600.0)))""",
    },

    # ------------------------------------------------------------------
    # ODRL313 — BSB running example: width conflict → Conflict
    # Paper: ex:bsb, thm:criterion (cc case)
    # sem(lteq 600)  = (0,600],  sem(gteq 1200) = [1200,∞)
    # (0,600] ∩ [1200,∞) = ∅  by less(v600, v1200)
    # ------------------------------------------------------------------
    {
        "id":            "ODRL313",
        "subdir":        "SingleAxis",
        "name":          "BSB running example: width ≤ 600 vs width ≥ 1200",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "BSB license:    width lteq 600  → (0, 600]    [ex:bsb]\n"
            "Museum request: width gteq 1200 → [1200, ∞)  [ex:bsb]\n"
            "(0, 600] ∩ [1200, ∞) = ∅        by less(v600, v1200)\n"
            "Paper running example (Datenraum Kultur / BSB scenario).\n"
            "Width axis alone yields Conflict → box verdict = Conflict."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyBSB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .
drk:policyMuseum a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:gteq ;
      odrl:rightOperand "1200"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
% v0 = domain lower bound (excluded); v600, v1200 = constraint values
fof(val_v0,         axiom, val(v0)).
fof(val_v600,       axiom, val(v600)).
fof(val_v1200,      axiom, val(v1200)).
fof(ord_v0_v600,    axiom, less(v0, v600)).
fof(ord_v0_v1200,   axiom, less(v0, v1200)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct,       axiom, $distinct(v0, v600, v1200)).
""",
        "fof_conjecture": "~?[X]: (in_lopen(X, v0, v600) & leq(v1200, X))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 600.0))
(assert (>= x 1200.0))""",
    },

    # ------------------------------------------------------------------
    # ODRL314 — BSB running example: height compatible → Compatible
    # Paper: ex:bsb, def:axis-verdict (Compatible)
    # sem(lteq 600) = (0,600], sem(gteq 400) = [400,∞)
    # (0,600] ∩ [400,∞) = [400,600] ≠ ∅   Witness: X = v400
    # ------------------------------------------------------------------
    {
        "id":            "ODRL314",
        "subdir":        "SingleAxis",
        "name":          "BSB running example: height ≤ 600 vs height ≥ 400",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "needs_density": False,
        "description": (
            "BSB license:    height lteq 600 → (0, 600]   [ex:bsb]\n"
            "Museum request: height gteq 400 → [400, ∞)   [ex:bsb]\n"
            "(0, 600] ∩ [400, ∞) = [400, 600] ≠ ∅\n"
            "Witness: X = v400 (named constant, no density needed).\n"
            "Paper running example: height axis is Compatible;\n"
            "combined with ODRL313 (width Conflict) → box verdict Conflict."
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .

drk:policyBSB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeHeight ;
      odrl:operator odrl:lteq ;
      odrl:rightOperand "600"^^xsd:decimal ] ] .
drk:policyMuseum a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeHeight ;
      odrl:operator odrl:gteq ;
      odrl:rightOperand "400"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
% v0 = domain lower bound (excluded); v400, v600 = constraint values
fof(val_v0,        axiom, val(v0)).
fof(val_v400,      axiom, val(v400)).
fof(val_v600,      axiom, val(v600)).
fof(ord_v0_v400,   axiom, less(v0, v400)).
fof(ord_v0_v600,   axiom, less(v0, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct,      axiom, $distinct(v0, v400, v600)).
""",
        "fof_conjecture": "?[X]: (in_lopen(X, v0, v600) & leq(v400, X))",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0))
(assert (<= x 600.0))
(assert (>= x 400.0))""",
    },
]