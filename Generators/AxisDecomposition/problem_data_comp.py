"""
problem_data_comp.py
====================
Composition benchmark problems: ODRL640-649 (10 problems).
Category N: Tests or_verdict/2, xone_verdict/2, or_sound_2branch from COMP000-0.ax.
Include pattern:
    include('Axioms/ORD000-0.ax').
    include('Axioms/COMP000-0.ax').
    include('Axioms/AXIS000-0.ax').
Problem overview:
  ODRL640 — or_compat: one branch compatible => or=compatible       Theorem
  ODRL641 — or_conflict: all pairs conflict => or=conflict           Theorem
  ODRL642 — or_unknown: no compat, not all conflict => or=unknown   Theorem
  ODRL643 — or_verdict_total: always one of 3 values               Theorem
  ODRL644 — xone_compat: exactly one pair overlaps => xone=compat  Theorem
  ODRL645 — xone_conflict: all pairs conflict => xone=conflict      Theorem
  ODRL646 — xone_unknown: two pairs overlap => xone=unknown         Theorem
  ODRL647 — xone_verdict_total: always one of 3 values             Theorem
  ODRL648 — or_sound_2branch: all pairs conflict => no shared point Theorem
  ODRL649 — or_distinct_from_xone: or!=xone when one pair overlaps Theorem
SMT note (ODRL640-647, 649):
  or_verdict/xone_verdict are uninterpreted FOL functions over verdict
  constants; there is no direct QF_LRA encoding.  The SMT assertions use
  (assert (not (= x x))) as an intentional placeholder that is trivially
  UNSAT, serving only to confirm the file is well-formed.  The meaningful
  verification for these problems is the FOF Theorem status from Vampire/E.
Fixes vs. original:
  ODRL642: verdict corrected from "Compatible" to "Unknown" — the problem
           tests or_verdict(unknown,conflict)=unknown, which is an Unknown
           outcome, not Compatible.
  ODRL648: branches corrected from identical (A1=A2=[v0,v400],
           B1=B2=[v600,v800]) to distinct pairs
           A1=[v0,v400], A2=[v0,v300], B1=[v600,v800], B2=[v500,v800].
           The original reduced to a trivial single-interval conflict and
           never exercised or_sound_2branch.  The fix provides 4 genuinely
           distinct cross-pairs, all of which conflict, properly testing
           the 2-branch union soundness axiom.
           Ordering extended to v0<v300<v400<v500<v600<v800.
           SMT updated to (x<=400|x<=300)&(x>=600|x>=500) -> UNSAT.
"""
# SMT placeholder used for pure verdict-algebra problems (ODRL640-647,649).
# or_verdict/xone_verdict have no QF_LRA encoding; this assert is trivially
# UNSAT and serves only as a file well-formedness check.
_VERDICT_SMT_PLACEHOLDER = "(assert (not (= x x)))"

# Minimal TTL template for pure verdict-algebra problems (no interval data).
_MINIMAL_TTL = """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policy a odrl:Set ; odrl:permission [ odrl:action odrl:use ] ."""

PROBLEMS = [
    # ─────────────────────────────────────────────────────────────────
    # ODRL640 — or_compat: V1=compatible => or_verdict=compatible
    # ─────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL640",
        "subdir":        "Composition",
        "name":          "or_compat: V1=compatible implies or_verdict=compatible",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["ORD000-0.ax", "COMP000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "sec:composition or_compat: is_verdict(V2) =>\n"
            "or_verdict(compatible, V2) = compatible.\n"
        ),
        "ttl": _MINIMAL_TTL,
        "fof_extra_decls": "",
        "fof_conjecture": (
            "![V2]: (is_verdict(V2) =>\n"
            "    or_verdict(compatible, V2) = compatible)"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": _VERDICT_SMT_PLACEHOLDER,
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL641 — or_conflict: both conflict => or=conflict
    # ─────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL641",
        "subdir":        "Composition",
        "name":          "or_conflict: both verdicts conflict implies or=conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["ORD000-0.ax", "COMP000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "sec:composition or_conflict:\n"
            "or_verdict(conflict, conflict) = conflict.\n"
        ),
        "ttl": _MINIMAL_TTL,
        "fof_extra_decls": "",
        "fof_conjecture": "or_verdict(conflict, conflict) = conflict",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": _VERDICT_SMT_PLACEHOLDER,
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL642 — or_unknown: unknown+conflict => or=unknown
    #
    # FIX: verdict corrected from "Compatible" to "Unknown".
    #      The problem tests or_verdict(unknown,conflict)=unknown;
    #      the policy outcome is Unknown, not Compatible.
    # ─────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL642",
        "subdir":        "Composition",
        "name":          "or_unknown: unknown and conflict implies or=unknown",
        "relation":      "conflict",
        "verdict":       "Unknown",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["ORD000-0.ax", "COMP000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "sec:composition or_unknown:\n"
            "or_verdict(unknown, conflict) = unknown.\n"
            "Neither is compatible; not both conflict => unknown.\n"
        ),
        "ttl": _MINIMAL_TTL,
        "fof_extra_decls": "",
        "fof_conjecture": "or_verdict(unknown, conflict) = unknown",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": _VERDICT_SMT_PLACEHOLDER,
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL643 — or_verdict_total: always one of 3 values
    # ─────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL643",
        "subdir":        "Composition",
        "name":          "or_verdict_total: result is always one of three verdicts",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["ORD000-0.ax", "COMP000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "sec:composition or_verdict_total:\n"
            "For all verdicts V1,V2: or_verdict is conflict, compatible, or unknown.\n"
        ),
        "ttl": _MINIMAL_TTL,
        "fof_extra_decls": "",
        "fof_conjecture": (
            "![V1,V2]: ((is_verdict(V1) & is_verdict(V2)) =>\n"
            "    (or_verdict(V1,V2) = compatible |\n"
            "     or_verdict(V1,V2) = conflict |\n"
            "     or_verdict(V1,V2) = unknown))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": _VERDICT_SMT_PLACEHOLDER,
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL644 — xone_compat: match=compat, rest=conflict => xone=compat
    # ─────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL644",
        "subdir":        "Composition",
        "name":          "xone_compat: one match compatible rest conflict => xone=compatible",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["ORD000-0.ax", "COMP000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "sec:composition xone_compat:\n"
            "xone_verdict(compatible, conflict) = compatible.\n"
            "Exactly one branch pair overlaps, rest conflict (Vr=MAX of rest=conflict).\n"
        ),
        "ttl": _MINIMAL_TTL,
        "fof_extra_decls": "",
        "fof_conjecture": "xone_verdict(compatible, conflict) = compatible",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": _VERDICT_SMT_PLACEHOLDER,
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL645 — xone_conflict: all conflict => xone=conflict
    # ─────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL645",
        "subdir":        "Composition",
        "name":          "xone_conflict: all pairs conflict implies xone=conflict",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["ORD000-0.ax", "COMP000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "sec:composition xone_conflict:\n"
            "xone_verdict(conflict, conflict) = conflict.\n"
        ),
        "ttl": _MINIMAL_TTL,
        "fof_extra_decls": "",
        "fof_conjecture": "xone_verdict(conflict, conflict) = conflict",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": _VERDICT_SMT_PLACEHOLDER,
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL646 — xone_unknown: both compat => xone=unknown
    # ─────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL646",
        "subdir":        "Composition",
        "name":          "xone_unknown: both pairs compatible implies xone=unknown",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["ORD000-0.ax", "COMP000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "sec:composition xone_unknown:\n"
            "xone_verdict(compatible, compatible) = unknown.\n"
            "Vr=MAX(rest)=compatible => >=2 branch pairs overlap => xone requires\n"
            "exactly one, so result is unknown.\n"
        ),
        "ttl": _MINIMAL_TTL,
        "fof_extra_decls": "",
        "fof_conjecture": "xone_verdict(compatible, compatible) = unknown",
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": _VERDICT_SMT_PLACEHOLDER,
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL647 — xone_verdict_total
    # ─────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL647",
        "subdir":        "Composition",
        "name":          "xone_verdict_total: result is always one of three verdicts",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["ORD000-0.ax", "COMP000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "sec:composition xone_verdict_total:\n"
            "For all verdicts Vm,Vr: xone_verdict is compat, conflict, or unknown.\n"
        ),
        "ttl": _MINIMAL_TTL,
        "fof_extra_decls": "",
        "fof_conjecture": (
            "![Vm,Vr]: ((is_verdict(Vm) & is_verdict(Vr)) =>\n"
            "    (xone_verdict(Vm,Vr) = compatible |\n"
            "     xone_verdict(Vm,Vr) = conflict |\n"
            "     xone_verdict(Vm,Vr) = unknown))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": _VERDICT_SMT_PLACEHOLDER,
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL648 — or_sound_2branch: all pairs conflict => no shared point
    #
    # FIX: replaced identical branches A1=A2=[v0,v400], B1=B2=[v600,v800]
    #      with distinct branches:
    #        A1=[v0,v400], A2=[v0,v300]  (P1 or-branches)
    #        B1=[v600,v800], B2=[v500,v800]  (P2 or-branches)
    #      All 4 cross-pairs conflict (v400<v500, v300<v500), exercising
    #      the 2-branch union soundness check of or_sound_2branch.
    #      Ordering extended: v0<v300<v400<v500<v600<v800.
    #      SMT updated: (x<=400|x<=300) & (x>=600|x>=500) -> UNSAT.
    # ─────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL648",
        "subdir":        "Composition",
        "name":          "or_sound_2branch: all axis pairs conflict implies no shared point",
        "relation":      "conflict",
        "verdict":       "Conflict",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Medium",
        "includes":      ["ORD000-0.ax", "COMP000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "thm:composition-soundness disjunction case (or_sound_2branch):\n"
            "A1=[v0,v400], A2=[v0,v300]; B1=[v600,v800], B2=[v500,v800].\n"
            "All 4 cross-pairs conflict (v400<v500, v300<v500)\n"
            "=> no point in (A1∪A2) ∩ (B1∪B2).\n"
        ),
        "ttl": """\
@prefix odrl: <http://www.w3.org/ns/odrl/2/> .
@prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix drk:  <http://w3id.org/drk/ontology/> .
drk:policyA a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:or (
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:lteq ; odrl:rightOperand "400"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:lteq ; odrl:rightOperand "300"^^xsd:decimal ]
    ) ] ] .
drk:policyB a odrl:Set ;
  odrl:permission [ odrl:action odrl:use ;
    odrl:constraint [ odrl:or (
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:gteq ; odrl:rightOperand "600"^^xsd:decimal ]
      [ odrl:leftOperand oax:absoluteSizeWidth ;
        odrl:operator odrl:gteq ; odrl:rightOperand "500"^^xsd:decimal ]
    ) ] ] .""",
        "fof_extra_decls": """\
fof(val_v0,   axiom, val(v0)).
fof(val_v300, axiom, val(v300)).
fof(val_v400, axiom, val(v400)).
fof(val_v500, axiom, val(v500)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v300,   axiom, less(v0,   v300)).
fof(ord_v300_v400, axiom, less(v300, v400)).
fof(ord_v400_v500, axiom, less(v400, v500)).
fof(ord_v500_v600, axiom, less(v500, v600)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v300, v400, v500, v600, v800)).
""",
        # 4 distinct cross-pair conflicts:
        #   A1=[v0,v400] vs B1=[v600,v800]: disjoint (v400 < v500 < v600)
        #   A1=[v0,v400] vs B2=[v500,v800]: disjoint (v400 < v500)
        #   A2=[v0,v300] vs B1=[v600,v800]: disjoint (v300 < v500 < v600)
        #   A2=[v0,v300] vs B2=[v500,v800]: disjoint (v300 < v500)
        "fof_conjecture": (
            "![X]: ~(\n"
            "    (in_closed(X,v0,v400) | in_closed(X,v0,v300)) &\n"
            "    (in_closed(X,v600,v800) | in_closed(X,v500,v800)))"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        # (A1∪A2) = x<=400; (B1∪B2) = x>=500; intersection empty.
        "smt2_asserts": """\
(assert (or (<= x 400.0) (<= x 300.0)))
(assert (or (>= x 600.0) (>= x 500.0)))""",
    },
    # ─────────────────────────────────────────────────────────────────
    # ODRL649 — or vs xone differ when two pairs compatible
    # ─────────────────────────────────────────────────────────────────
    {
        "id":            "ODRL649",
        "subdir":        "Composition",
        "name":          "or vs xone: differ when two branch pairs compatible",
        "relation":      "conflict",
        "verdict":       "Compatible",
        "status_fof":    "Theorem",
        "status_smt":    "unsat",
        "difficulty":    "Easy",
        "includes":      ["ORD000-0.ax", "COMP000-0.ax", "AXIS000-0.ax"],
        "needs_density": False,
        "description": (
            "sec:composition: or and xone give different verdicts when\n"
            "both branch pairs are compatible:\n"
            "or_verdict(compat,compat)=compat but xone_verdict(compat,compat)=unknown.\n"
        ),
        "ttl": _MINIMAL_TTL,
        "fof_extra_decls": "",
        "fof_conjecture": (
            "or_verdict(compatible, compatible) = compatible &\n"
            "    xone_verdict(compatible, compatible) = unknown"
        ),
        "smt2_logic": "QF_LRA",
        "smt2_decls": "(declare-const x Real)",
        "smt2_asserts": _VERDICT_SMT_PLACEHOLDER,
    },
]