"""
problem_data_runtime.py
=======================
Runtime benchmark problems: ODRL770-779 (10 problems).
Category: Runtime/

Tests the runtime-evaluation layer of Sec 8:
  - Def 23 (Request):      a partial mapping rho assigning axis values.
  - Def 24 (Satisfaction): rho |= c  iff  rho(l_a_k) in [[c]].
  - Thm 6 (Runtime Soundness): verdict(C1,C2)=Conflict => no rho
                               satisfies both C1 and C2.

DESIGN NOTE -- no new axiom.
  Def 24 reduces runtime satisfaction to interval membership: a request
  value rho(l_a_k) satisfies constraint c exactly when it lies in the
  denotation [[c]].  The runtime layer therefore needs NO additional
  axiomatisation; it is a corollary of the denotational semantics and
  rides on ORD000 + AXIS000.  Each problem encodes a concrete request
  value (a named constant) and asks whether the membership that defines
  satisfaction holds (permit) or fails (deny), or -- for Thm 6 -- whether
  ANY request value can satisfy two conflicting policies (it cannot).

  permit  : rho(l) in [[c]]            -> FOL Theorem, SMT sat
  deny    : rho(l) not in [[c]]        -> FOL Theorem (proves ~member), SMT unsat
  joint   : exists rho in both         -> FOL Theorem (witness),  SMT sat
  rt-sound: forall rho, not in both    -> FOL Theorem,            SMT unsat

All values are taken from the BSB-BnF running example (Ex 1):
  BSB offer:  width lteq 1920, height lteq 1080, depth lteq 50
  BnF request: width eq 2400, height eq 800
so the runtime group ties directly to the paper's worked example.

TTL prefix: drk: <http://w3id.org/drk/ontology/>
SMT2 comments use ; not %.
"""
PROBLEMS = [
    # ──────────────────────────────────────────────────────────────────
    # ODRL770 — permit (single axis): request height 800 satisfies lteq 1080
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL770",
        "subdir":        "Runtime",
        "name":          "Runtime permit: request height 800 satisfies lteq 1080",
        "relation":      "runtime",
        "verdict":       "Permit",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "includes":      ["ORD000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "Def 24 satisfaction: BnF request rho(height)=800 against BSB\n"
            "height constraint lteq 1080 -> (0,1080].  800 in (0,1080], so\n"
            "rho satisfies the constraint and the Evaluator state is permit.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyBSB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeHeight ;
      odrl:operator odrl:lteq ; odrl:rightOperand "1080"^^xsd:decimal ] ] .
# request rho: absoluteSizeHeight = 800""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v800,  axiom, val(v800)).
fof(val_v1080, axiom, val(v1080)).
fof(ord_v0_v800,    axiom, less(v0, v800)).
fof(ord_v800_v1080, axiom, less(v800, v1080)).
fof(distinct, axiom, $distinct(v0, v800, v1080)).
""",
        "fof_conjecture": "in_lopen(v800, v0, v1080)",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (= x 800.0))
(assert (> x 0.0)) (assert (<= x 1080.0))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL771 — deny (single axis): request width 2400 violates lteq 1920
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL771",
        "subdir":        "Runtime",
        "name":          "Runtime deny: request width 2400 violates lteq 1920",
        "relation":      "runtime",
        "verdict":       "Deny",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["ORD000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "Def 24 satisfaction: BnF request rho(width)=2400 against BSB\n"
            "width constraint lteq 1920 -> (0,1920].  2400 not in (0,1920],\n"
            "so rho fails the constraint and the Evaluator state is deny.\n"
            "FOL proves the non-membership; SMT shows x=2400 & x in (0,1920]\n"
            "is unsatisfiable.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyBSB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ; odrl:rightOperand "1920"^^xsd:decimal ] ] .
# request rho: absoluteSizeWidth = 2400""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v1920, axiom, val(v1920)).
fof(val_v2400, axiom, val(v2400)).
fof(ord_v0_v1920,    axiom, less(v0, v1920)).
fof(ord_v1920_v2400, axiom, less(v1920, v2400)).
fof(distinct, axiom, $distinct(v0, v1920, v2400)).
""",
        "fof_conjecture": "~in_lopen(v2400, v0, v1920)",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (= x 2400.0))
(assert (> x 0.0)) (assert (<= x 1920.0))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL772 — runtime soundness (Thm 6), width conflict
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL772",
        "subdir":        "Runtime",
        "name":          "Runtime soundness: no request satisfies both lteq 1920 and eq 2400",
        "relation":      "runtime",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["ORD000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "Thm 6 (Runtime Soundness): the width axis conflicts between BSB\n"
            "(lteq 1920 -> (0,1920]) and BnF (eq 2400 -> {2400}).  Therefore\n"
            "no request value W satisfies both constraints, i.e. the static\n"
            "Conflict verdict guarantees no joint permit at runtime.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyBSB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ; odrl:rightOperand "1920"^^xsd:decimal ] ] .
drk:policyBnF a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:eq ; odrl:rightOperand "2400"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v1920, axiom, val(v1920)).
fof(val_v2400, axiom, val(v2400)).
fof(ord_v0_v1920,    axiom, less(v0, v1920)).
fof(ord_v1920_v2400, axiom, less(v1920, v2400)).
fof(distinct, axiom, $distinct(v0, v1920, v2400)).
""",
        "fof_conjecture": (
            "![W]: ~(in_lopen(W, v0, v1920) & in_closed(W, v2400, v2400))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 1920.0))
(assert (= x 2400.0))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL773 — joint permit exists (height compatible)
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL773",
        "subdir":        "Runtime",
        "name":          "Runtime joint permit: a request satisfies both lteq 1080 and eq 800",
        "relation":      "runtime",
        "verdict":       "Permit",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "includes":      ["ORD000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "Height axis is compatible: BSB lteq 1080 -> (0,1080] and BnF\n"
            "eq 800 -> {800} share the value 800.  A request rho(height)=800\n"
            "satisfies both, so a joint permit exists (existential witness).\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyBSB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeHeight ;
      odrl:operator odrl:lteq ; odrl:rightOperand "1080"^^xsd:decimal ] ] .
drk:policyBnF a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeHeight ;
      odrl:operator odrl:eq ; odrl:rightOperand "800"^^xsd:decimal ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v800,  axiom, val(v800)).
fof(val_v1080, axiom, val(v1080)).
fof(ord_v0_v800,    axiom, less(v0, v800)).
fof(ord_v800_v1080, axiom, less(v800, v1080)).
fof(distinct, axiom, $distinct(v0, v800, v1080)).
""",
        "fof_conjecture": (
            "?[W]: (in_lopen(W, v0, v1080) & in_closed(W, v800, v800))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 1080.0))
(assert (= x 800.0))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL774 — and-satisfaction: request satisfies both axes of a box
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL774",
        "subdir":        "Runtime",
        "name":          "Runtime and-permit: request (1500,900) satisfies width&height box",
        "relation":      "runtime",
        "verdict":       "Permit",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "includes":      ["ORD000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "Def 24 and-satisfaction: rho |= and(B1,B2) iff rho satisfies\n"
            "every branch.  Request rho(width)=1500, rho(height)=900 against\n"
            "BSB and(width lteq 1920, height lteq 1080): 1500 in (0,1920] and\n"
            "900 in (0,1080], so both branches hold and rho permits.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyBSB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:and (
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:lteq ; odrl:rightOperand "1920"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeHeight ;
        odrl:operator odrl:lteq ; odrl:rightOperand "1080"^^xsd:decimal ]
    ) ] ] .
# request rho: width = 1500, height = 900""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v900,  axiom, val(v900)).
fof(val_v1080, axiom, val(v1080)).
fof(val_v1500, axiom, val(v1500)).
fof(val_v1920, axiom, val(v1920)).
fof(ord_v0_v900,     axiom, less(v0, v900)).
fof(ord_v0_v1500,    axiom, less(v0, v1500)).
fof(ord_v900_v1080,  axiom, less(v900, v1080)).
fof(ord_v1080_v1500, axiom, less(v1080, v1500)).
fof(ord_v1500_v1920, axiom, less(v1500, v1920)).
fof(distinct, axiom, $distinct(v0, v900, v1080, v1500, v1920)).
""",
        "fof_conjecture": (
            "(in_lopen(v1500, v0, v1920) & in_lopen(v900, v0, v1080))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (= x 1500.0)) (assert (> x 0.0)) (assert (<= x 1920.0))
(assert (= y 900.0))  (assert (> y 0.0)) (assert (<= y 1080.0))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL775 — and-deny: request fails one axis, so the conjunction fails
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL775",
        "subdir":        "Runtime",
        "name":          "Runtime and-deny: request (2400,900) fails width, so box denied",
        "relation":      "runtime",
        "verdict":       "Deny",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "includes":      ["ORD000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "Def 24 and-satisfaction: a single failing branch breaks the\n"
            "conjunction.  Request rho(width)=2400 fails width lteq 1920\n"
            "even though rho(height)=900 satisfies height lteq 1080, so\n"
            "rho does not satisfy the and-policy and is denied.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyBSB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:and (
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:lteq ; odrl:rightOperand "1920"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeHeight ;
        odrl:operator odrl:lteq ; odrl:rightOperand "1080"^^xsd:decimal ]
    ) ] ] .
# request rho: width = 2400, height = 900""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v900,  axiom, val(v900)).
fof(val_v1080, axiom, val(v1080)).
fof(val_v1920, axiom, val(v1920)).
fof(val_v2400, axiom, val(v2400)).
fof(ord_v0_v900,     axiom, less(v0, v900)).
fof(ord_v900_v1080,  axiom, less(v900, v1080)).
fof(ord_v1080_v1920, axiom, less(v1080, v1920)).
fof(ord_v1920_v2400, axiom, less(v1920, v2400)).
fof(distinct, axiom, $distinct(v0, v900, v1080, v1920, v2400)).
""",
        "fof_conjecture": (
            "~(in_lopen(v2400, v0, v1920) & in_lopen(v900, v0, v1080))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (= x 2400.0)) (assert (> x 0.0)) (assert (<= x 1920.0))
(assert (= y 900.0))  (assert (> y 0.0)) (assert (<= y 1080.0))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL776 — or-satisfaction: request satisfies at least one branch
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL776",
        "subdir":        "Runtime",
        "name":          "Runtime or-permit: request width 1200 satisfies the archival branch",
        "relation":      "runtime",
        "verdict":       "Permit",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "includes":      ["ORD000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "Def 24 or-satisfaction: rho |= or(B1,B2) iff rho satisfies some\n"
            "branch.  BnF request is or(kiosk: width eq 2400, archival:\n"
            "width eq 1200).  rho(width)=1200 satisfies the archival branch\n"
            "(not the kiosk branch), so the or-policy permits.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyBnF a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:or (
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:eq ; odrl:rightOperand "2400"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:eq ; odrl:rightOperand "1200"^^xsd:decimal ]
    ) ] ] .
# request rho: width = 1200""",
        "fof_extra_decls": """\
fof(val_v1200, axiom, val(v1200)).
fof(val_v2400, axiom, val(v2400)).
fof(ord_v1200_v2400, axiom, less(v1200, v2400)).
fof(distinct, axiom, $distinct(v1200, v2400)).
""",
        "fof_conjecture": (
            "(in_closed(v1200, v1200, v1200) | in_closed(v1200, v2400, v2400))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (= x 1200.0))
(assert (or (= x 1200.0) (= x 2400.0)))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL777 — xone-satisfaction: request satisfies exactly one branch
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL777",
        "subdir":        "Runtime",
        "name":          "Runtime xone-permit: request width 1200 satisfies exactly one branch",
        "relation":      "runtime",
        "verdict":       "Permit",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Medium",
        "includes":      ["ORD000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "Def 24 xone-satisfaction: rho |= xone(B1,B2) iff rho satisfies\n"
            "exactly one branch.  BnF request is xone(width eq 1200,\n"
            "width eq 2400).  rho(width)=1200 satisfies the first branch and\n"
            "not the second (1200 != 2400), so exactly one holds and the\n"
            "xone-policy permits.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyBnF a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:xone (
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:eq ; odrl:rightOperand "1200"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:eq ; odrl:rightOperand "2400"^^xsd:decimal ]
    ) ] ] .
# request rho: width = 1200""",
        "fof_extra_decls": """\
fof(val_v1200, axiom, val(v1200)).
fof(val_v2400, axiom, val(v2400)).
fof(ord_v1200_v2400, axiom, less(v1200, v2400)).
fof(distinct, axiom, $distinct(v1200, v2400)).
""",
        "fof_conjecture": (
            "(in_closed(v1200, v1200, v1200) & ~in_closed(v1200, v2400, v2400))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (= x 1200.0))
(assert (xor (= x 1200.0) (= x 2400.0)))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL778 — runtime soundness across the full box (width kills joint)
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL778",
        "subdir":        "Runtime",
        "name":          "Runtime soundness (box): no request satisfies both BSB and BnF",
        "relation":      "runtime",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "includes":      ["ORD000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "Thm 6 across the box: BSB and(width lteq 1920, height lteq 1080)\n"
            "vs BnF and(width eq 2400, height eq 800).  The width axis\n"
            "conflicts (2400 not in (0,1920]), so by Thm 6 no request (W,H)\n"
            "satisfies both policies regardless of the compatible height.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyBSB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:and (
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:lteq ; odrl:rightOperand "1920"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeHeight ;
        odrl:operator odrl:lteq ; odrl:rightOperand "1080"^^xsd:decimal ]
    ) ] ] .
drk:policyBnF a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:and (
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:eq ; odrl:rightOperand "2400"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeHeight ;
        odrl:operator odrl:eq ; odrl:rightOperand "800"^^xsd:decimal ]
    ) ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v800,  axiom, val(v800)).
fof(val_v1080, axiom, val(v1080)).
fof(val_v1920, axiom, val(v1920)).
fof(val_v2400, axiom, val(v2400)).
fof(ord_v0_v800,     axiom, less(v0, v800)).
fof(ord_v800_v1080,  axiom, less(v800, v1080)).
fof(ord_v1080_v1920, axiom, less(v1080, v1920)).
fof(ord_v1920_v2400, axiom, less(v1920, v2400)).
fof(distinct, axiom, $distinct(v0, v800, v1080, v1920, v2400)).
""",
        "fof_conjecture": (
            "![W,H]: ~(in_lopen(W, v0, v1920) & in_closed(W, v2400, v2400) &\n"
            "          in_lopen(H, v0, v1080) & in_closed(H, v800, v800))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)\n(declare-const y Real)",
        "smt2_asserts": """\
(assert (> x 0.0)) (assert (<= x 1920.0)) (assert (= x 2400.0))
(assert (> y 0.0)) (assert (<= y 1080.0)) (assert (= y 800.0))""",
    },
    # ──────────────────────────────────────────────────────────────────
    # ODRL779 — permit at the closed upper boundary
    # ──────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL779",
        "subdir":        "Runtime",
        "name":          "Runtime permit at boundary: request width 1920 satisfies lteq 1920",
        "relation":      "runtime",
        "verdict":       "Permit",
        "status_fof":    "Theorem",
        "status_smt":    "sat",
        "difficulty":    "Easy",
        "includes":      ["ORD000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "Boundary satisfaction: lteq 1920 -> (0,1920] is closed at the\n"
            "upper end, so the request rho(width)=1920 lies exactly on the\n"
            "boundary and is permitted (1920 in (0,1920]).  Confirms the\n"
            "endpoint-inclusion of lteq at runtime.\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyBSB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:leftOperand oax:absoluteSizeWidth ;
      odrl:operator odrl:lteq ; odrl:rightOperand "1920"^^xsd:decimal ] ] .
# request rho: absoluteSizeWidth = 1920 (exactly on the boundary)""",
        "fof_extra_decls": """\
fof(val_v0,    axiom, val(v0)).
fof(val_v1920, axiom, val(v1920)).
fof(ord_v0_v1920, axiom, less(v0, v1920)).
fof(distinct, axiom, $distinct(v0, v1920)).
""",
        "fof_conjecture": "in_lopen(v1920, v0, v1920)",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": """\
(assert (= x 1920.0))
(assert (> x 0.0)) (assert (<= x 1920.0))""",
    },
]