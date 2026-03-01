"""
hierarchies/cat05_edge_cases.py
Category 5: Edge Cases — ODRL050-055.

Tests hasPart directional semantics, identity/tautology,
and counterintuitive subsumption asymmetry (ODRL054-055).

hasPart traverses UPWARD: ⟦hasPart(G)⟧ = {X | leq(G, X)}
Contrast with isPartOf which goes DOWNWARD: ⟦isPartOf(G)⟧ = {X | leq(X, G)}

Paper references: Definition 3 (hasPart denotation), Definition 7.

Problems:
  ODRL050  Identity:  isPartOf(europe) ∩ isPartOf(europe) ≠ ∅
  ODRL051  Upward:    hasPart(germany) ∩ eq(europe)          [root reachable]
  ODRL052  Common ancestor: hasPart(germany) ∩ hasPart(france)
  ODRL053  Cross-branch: hasPart(germany) ∩ hasPart(poland)  [both reach europe]
  ODRL054  Counterintuitive: hasPart(europe) ⊆ hasPart(germany)
  ODRL055  Refuted:   hasPart(germany) ⊄ hasPart(europe)     [germany ∉ ⟦hasPart(eu)⟧]
"""
from .models import (
    Category, Constraint, KB, KBProblem, Op, SZS, Verdict
)
from .kb_smt2 import geo_full_smt2_preamble

_GEO_PREAMBLE = None


def _preamble() -> str:
    global _GEO_PREAMBLE
    if _GEO_PREAMBLE is None:
        _GEO_PREAMBLE = "(set-logic UF)\n\n" + geo_full_smt2_preamble()
    return _GEO_PREAMBLE


def _smt2(block: str) -> str:
    return f"{block}\n(check-sat)\n(exit)"


def _ttl(perm_op, perm_val, prohib_op, prohib_val, operand="spatial") -> str:
    return (
        f"%   ex:policyA a odrl:Set ;\n"
        f"%     odrl:permission [ odrl:action odrl:use ;\n"
        f"%       odrl:constraint [ odrl:leftOperand odrl:{operand} ;"
        f" odrl:operator odrl:{perm_op} ; odrl:rightOperand geo:{perm_val} ] ] .\n"
        f"%\n"
        f"%   ex:policyB a odrl:Set ;\n"
        f"%     odrl:prohibition [ odrl:action odrl:use ;\n"
        f"%       odrl:constraint [ odrl:leftOperand odrl:{operand} ;"
        f" odrl:operator odrl:{prohib_op} ; odrl:rightOperand geo:{prohib_val} ] ] ."
    )


def edge_cases() -> list[KBProblem]:
    problems = []

    # ──────────────────────────────────────────────────────────────────────
    # ODRL050 — Identity: isPartOf(europe) ∩ isPartOf(europe) = isPartOf(europe)
    # Identical constraints on both rules — trivially compatible.
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=50, name="identity-isPartOf-europe",
        category=Category.SPATIAL,
        verdict=Verdict.COMPATIBLE, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.IS_PART_OF, "europe"),
        c2=Constraint("spatial", Op.IS_PART_OF, "europe"),
        description="Identity: isPartOf(europe) ∩ isPartOf(europe) ≠ ∅",
        formal=(
            "⟦isPartOf(europe)⟧ ∩ ⟦isPartOf(europe)⟧ = ⟦isPartOf(europe)⟧ ≠ ∅\n"
            "%   Witness: europe itself  [leq(europe,europe) — reflexivity]"
        ),
        paper_ref="Definition 5 (identity)",
        difficulty="Trivial",
        notes="Base case: any constraint is compatible with itself.",
        policy_ttl=_ttl("isPartOf", "europe", "isPartOf", "europe"),
        conjecture_fof=(
            "fof(odrl050, conjecture,\n"
            "    ?[X]: ( in_denotation(X, europe, isPartOf)\n"
            "          & in_denotation(X, europe, isPartOf) ))."
        ),
        conjecture_smt2=_smt2(
            "; Identity: ∃X. leq(X,europe) ∧ leq(X,europe) — trivially true\n"
            "(assert (not (exists ((X C))\n"
            "    (and (leq X europe)(leq X europe)))))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL051 — Root reachability: hasPart(germany) ∩ eq(europe)
    # hasPart(germany) = {X | leq(germany,X)} = {germany, wE, europe, world}
    # europe ∈ this set → Compatible
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=51, name="hasPart-germany-eq-europe-compatible",
        category=Category.SPATIAL,
        verdict=Verdict.COMPATIBLE, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.HAS_PART, "germany"),
        c2=Constraint("spatial", Op.EQ, "europe"),
        description="Root reachability: hasPart(germany) ∩ eq(europe) ≠ ∅",
        formal=(
            "⟦hasPart(germany)⟧ = {X | leq(germany,X)}\n"
            "%                   = {germany, westernEurope, europe, world}\n"
            "%   europe ∈ this set  [leq(germany,wE) + leq(wE,europe) → leq(germany,europe)]\n"
            "%   Witness: europe"
        ),
        paper_ref="Definition 3 (hasPart)",
        difficulty="Medium",
        notes="hasPart traverses UPWARD — the 'any ancestor' test.",
        policy_ttl=_ttl("hasPart", "germany", "eq", "europe"),
        conjecture_fof=(
            "fof(odrl051, conjecture,\n"
            "    ?[X]: ( in_denotation(X, germany, hasPart)\n"
            "          & in_denotation(X, europe, eq) ))."
        ),
        conjecture_smt2=_smt2(
            "; Compatible: ∃X. leq(germany,X) ∧ X=europe\n"
            "; Negated: ¬leq(germany,europe)\n"
            "(assert (not (exists ((X C))\n"
            "    (and (leq germany X)(= X europe)))))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL052 — Common ancestor: hasPart(germany) ∩ hasPart(france)
    # Both germany and france are in westernEurope
    # → both have wE, europe, world as common ancestors
    # Witness: westernEurope (leq(germany,wE) ∧ leq(france,wE))
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=52, name="hasPart-germany-hasPart-france-common-ancestor",
        category=Category.SPATIAL,
        verdict=Verdict.COMPATIBLE, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.HAS_PART, "germany"),
        c2=Constraint("spatial", Op.HAS_PART, "france"),
        description="Common ancestor: hasPart(germany) ∩ hasPart(france) ≠ ∅",
        formal=(
            "⟦hasPart(germany)⟧ = {X | leq(germany,X)} ∋ westernEurope\n"
            "%   ⟦hasPart(france)⟧  = {X | leq(france,X)}  ∋ westernEurope\n"
            "%   Witness: westernEurope  [leq(germany,wE) ∧ leq(france,wE)]"
        ),
        paper_ref="Definition 3 (hasPart)",
        difficulty="Medium",
        policy_ttl=_ttl("hasPart", "germany", "hasPart", "france"),
        conjecture_fof=(
            "fof(odrl052, conjecture,\n"
            "    ?[X]: ( in_denotation(X, germany, hasPart)\n"
            "          & in_denotation(X, france, hasPart) ))."
        ),
        conjecture_smt2=_smt2(
            "; Compatible: ∃X. leq(germany,X) ∧ leq(france,X)\n"
            "; Negated: ∀X. ¬(leq(germany,X) ∧ leq(france,X))\n"
            "(assert (not (exists ((X C))\n"
            "    (and (leq germany X)(leq france X)))))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL053 — Cross-branch: hasPart(germany) ∩ hasPart(poland)
    # germany ∈ wE, poland ∈ eE → isPartOf(germany) ∩ isPartOf(poland) = ∅
    # BUT hasPart goes UPWARD: both reach europe and world
    # Witness: europe (leq(germany,europe) ∧ leq(poland,europe))
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=53, name="hasPart-germany-hasPart-poland-cross-branch",
        category=Category.SPATIAL,
        verdict=Verdict.COMPATIBLE, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.HAS_PART, "germany"),
        c2=Constraint("spatial", Op.HAS_PART, "poland"),
        description="Cross-branch hasPart: hasPart(germany) ∩ hasPart(poland) ≠ ∅",
        formal=(
            "NOTE: isPartOf(germany) ∩ isPartOf(poland) = ∅  [disj(wE,eE)]\n"
            "%   BUT hasPart goes UPWARD — cross-branch ancestors exist!\n"
            "%   leq(germany,wE) → leq(germany,europe)  [leq_trans]\n"
            "%   leq(poland,eE)  → leq(poland,europe)   [leq_trans]\n"
            "%   Witness: europe ∈ both hasPart sets"
        ),
        paper_ref="Definition 3 (hasPart)",
        difficulty="Medium-Hard",
        notes="Directional reversal: conflict in isPartOf becomes compatible in hasPart.",
        policy_ttl=_ttl("hasPart", "germany", "hasPart", "poland"),
        conjecture_fof=(
            "fof(odrl053, conjecture,\n"
            "    ?[X]: ( in_denotation(X, germany, hasPart)\n"
            "          & in_denotation(X, poland, hasPart) ))."
        ),
        conjecture_smt2=_smt2(
            "; Compatible: ∃X. leq(germany,X) ∧ leq(poland,X)  [europe is witness]\n"
            "(assert (not (exists ((X C))\n"
            "    (and (leq germany X)(leq poland X)))))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL054 — Counterintuitive: hasPart(europe) ⊆ hasPart(germany)
    # ⟦hasPart(europe)⟧ = {europe, world}   (only europe's ancestors)
    # ⟦hasPart(germany)⟧ = {germany,wE,europe,world}  (superset!)
    # Counter-intuitive: the MORE GENERAL concept has FEWER ancestors.
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=54, name="hasPart-europe-subsumes-hasPart-germany",
        category=Category.SPATIAL,
        verdict=Verdict.SUBSUMES, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.HAS_PART, "europe"),
        c2=Constraint("spatial", Op.HAS_PART, "germany"),
        description="Counterintuitive: hasPart(europe) ⊆ hasPart(germany)",
        formal=(
            "⟦hasPart(europe)⟧  = {X | leq(europe,X)} = {europe, world}\n"
            "%   ⟦hasPart(germany)⟧ = {X | leq(germany,X)} = {germany,wE,europe,world}\n"
            "%   {europe,world} ⊆ {germany,wE,europe,world}  →  Subsumption\n"
            "%   Proof: leq(europe,X) ∧ leq(germany,europe) → leq(germany,X)  [leq_trans]"
        ),
        paper_ref="Definition 7",
        difficulty="Medium",
        notes="MORE GENERAL concept → SMALLER hasPart denotation. Reversal of isPartOf.",
        policy_ttl=(
            "%   c1: [ odrl:operator odrl:hasPart ; odrl:rightOperand geo:europe ] .\n"
            "%   c2: [ odrl:operator odrl:hasPart ; odrl:rightOperand geo:germany ] ."
        ),
        conjecture_fof=(
            "fof(odrl054, conjecture,\n"
            "    ![X]: ( in_denotation(X, europe, hasPart)\n"
            "          => in_denotation(X, germany, hasPart) ))."
        ),
        conjecture_smt2=_smt2(
            "; Subsumes: ∀X. leq(europe,X) → leq(germany,X)\n"
            "; Proof: leq(germany,europe) [KB] + leq(europe,X) → leq(germany,X) [trans]\n"
            "; Negated: ∃X. leq(europe,X) ∧ ¬leq(germany,X)\n"
            "(assert (exists ((X C))\n"
            "    (and (leq europe X)\n"
            "         (not (leq germany X)))))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL055 — Refuted: hasPart(germany) ⊄ hasPart(europe)
    # Counterexample: germany ∈ ⟦hasPart(germany)⟧ [reflexivity]
    # but germany ∉ ⟦hasPart(europe)⟧ [leq(europe,germany) not derivable]
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=55, name="hasPart-germany-not-subsumes-hasPart-europe",
        category=Category.SPATIAL,
        verdict=Verdict.REFUTED, szs=SZS.COUNTERSATISFIABLE,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.HAS_PART, "germany"),
        c2=Constraint("spatial", Op.HAS_PART, "europe"),
        description="Subsumption refuted: hasPart(germany) ⊄ hasPart(europe)",
        formal=(
            "Counterexample: germany\n"
            "%   leq(germany,germany)  [reflexivity] → germany ∈ ⟦hasPart(germany)⟧\n"
            "%   leq(europe,germany)   is NOT in KB   → germany ∉ ⟦hasPart(europe)⟧\n"
            "%   → ⟦c1⟧ ⊄ ⟦c2⟧  →  Refuted"
        ),
        paper_ref="Definition 7",
        difficulty="Medium",
        notes="Paired with ODRL054: hasPart subsumption is strictly one-directional.",
        policy_ttl=(
            "%   c1: [ odrl:operator odrl:hasPart ; odrl:rightOperand geo:germany ] .\n"
            "%   c2: [ odrl:operator odrl:hasPart ; odrl:rightOperand geo:europe ] ."
        ),
        conjecture_fof=(
            "fof(odrl055, conjecture,\n"
            "    ?[X]: ( in_denotation(X, germany, hasPart)\n"
            "          & ~in_denotation(X, europe, hasPart) ))."
        ),
        conjecture_smt2=_smt2(
            "; Refuted: ∃X. leq(germany,X) ∧ ¬leq(europe,X)  — expect sat (germany itself)\n"
            "(assert (exists ((X C))\n"
            "    (and (leq germany X)\n"
            "         (not (leq europe X)))))"
        ),
    ))

    preamble = _preamble()
    for prob in problems:
        prob.inline_smt2_kb = preamble

    return problems
