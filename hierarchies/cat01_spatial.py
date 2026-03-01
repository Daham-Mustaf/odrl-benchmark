"""
hierarchies/cat01_spatial.py
Category 1: Basic spatial operator coverage — ODRL010-019.

Tests the six hierarchy-dependent operators (eq, neq, isA/isPartOf,
hasPart) against the GEO KB. All conjectures are prover-friendly
(Theorem for Vampire, unsat for Z3).

Paper references: Definition 2 (Hierarchy), Definition 3 (Denotation),
Definition 5 (Conflict Detection).

Problems:
  ODRL010  KB property: leq transitivity (no ODRL policy)
  ODRL011  Compatible: isPartOf(europe) ∩ eq(germany)
  ODRL012  Conflict:   eq(germany) ∩ eq(france) [UNA]
  ODRL013  Conflict:   isPartOf(wE) ∩ isPartOf(eE) [disj_downward]
  ODRL014  Compatible: hasPart(germany) ∩ isPartOf(europe)
  ODRL015  Conflict:   hasPart(germany) ∩ eq(poland) [Lemma 1]
  ODRL016  Compatible: neq(germany) ∩ isPartOf(westernEurope)
  ODRL017  Conflict:   neq(germany) ∩ eq(germany)
  ODRL018  Compatible: isPartOf(westernEurope) ∩ hasPart(bavaria)
  ODRL019  Conflict:   isPartOf(northernEurope) ∩ isPartOf(southernEurope)
"""
from .models import (
    Category, Constraint, KB, KBProblem, Op, SZS, Verdict
)
from .kb_smt2 import geo_full_smt2_preamble

# Cached preamble (same for all GEO-only problems)
_GEO_PREAMBLE = None


def _preamble() -> str:
    global _GEO_PREAMBLE
    if _GEO_PREAMBLE is None:
        _GEO_PREAMBLE = "(set-logic UF)\n\n" + geo_full_smt2_preamble()
    return _GEO_PREAMBLE


def _smt2(assert_block: str) -> str:
    """Return just the assert + check-sat block.
    The KB preamble goes into inline_smt2_kb, not here.
    """
    return f"{assert_block}\n(check-sat)\n(exit)"


def _ttl_permission(operand: str, operator: str, value: str) -> str:
    return (
        f"%   ex:policyA a odrl:Set ;\n"
        f"%     odrl:permission [\n"
        f"%       odrl:action odrl:use ;\n"
        f"%       odrl:constraint [\n"
        f"%         odrl:leftOperand odrl:{operand} ;\n"
        f"%         odrl:operator odrl:{operator} ;\n"
        f"%         odrl:rightOperand geo:{value} ] ] ."
    )


def _ttl_prohibition(operand: str, operator: str, value: str) -> str:
    return (
        f"%   ex:policyB a odrl:Set ;\n"
        f"%     odrl:prohibition [\n"
        f"%       odrl:action odrl:use ;\n"
        f"%       odrl:constraint [\n"
        f"%         odrl:leftOperand odrl:{operand} ;\n"
        f"%         odrl:operator odrl:{operator} ;\n"
        f"%         odrl:rightOperand geo:{value} ] ] ."
    )


def _ttl(perm_op, perm_val, prohib_op, prohib_val, operand="spatial") -> str:
    return (
        _ttl_permission(operand, perm_op, perm_val) + "\n%\n" +
        _ttl_prohibition(operand, prohib_op, prohib_val)
    )


def spatial_basic() -> list[KBProblem]:
    problems = []

    # ──────────────────────────────────────────────────────────────────────
    # ODRL010 — Pure KB property: leq transitivity
    # No ODRL policy. Tests that Vampire can derive leq(germany, europe)
    # from leq(germany, westernEurope) + leq(westernEurope, europe).
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=10, name="leq-transitivity",
        category=Category.SPATIAL,
        verdict=Verdict.SUBSUMES, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=None, c2=None,
        description="KB property: leq transitivity — germany ⪯ europe",
        formal=(
            "leq(germany, westernEurope) ∧ leq(westernEurope, europe)\n"
            "%   ⟹ leq(germany, europe)  [leq_trans]"
        ),
        paper_ref="Definition 2 (KB: leq transitivity)",
        difficulty="Trivial",
        policy_ttl="% (No ODRL policy — pure KB property test)",
        notes="Validates leq_trans before any operator denotation tests.",
        conjecture_fof=(
            "fof(odrl010, conjecture, leq(germany, europe))."
        ),
        conjecture_smt2=_smt2(
            "; Negated conjecture: germany NOT ≤ europe\n"
            "(assert (not (leq germany europe)))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL011 — Compatible: isPartOf(europe) ∩ eq(germany)
    # Witness: germany ∈ ⟦isPartOf(europe)⟧ ∧ germany = germany
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=11, name="isPartOf-europe-eq-germany-compatible",
        category=Category.SPATIAL,
        verdict=Verdict.COMPATIBLE, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.IS_PART_OF, "europe"),
        c2=Constraint("spatial", Op.EQ, "germany"),
        description="Compatible: isPartOf(europe) ∩ eq(germany) ≠ ∅",
        formal=(
            "⟦isPartOf(europe)⟧ = {x | leq(x, europe)} ∋ germany\n"
            "%   ⟦eq(germany)⟧ = {germany}\n"
            "%   Witness: germany (leq_trans: de ≤ wE ≤ europe)"
        ),
        paper_ref="Definition 3, Definition 5",
        difficulty="Easy",
        policy_ttl=_ttl("isPartOf", "europe", "eq", "germany"),
        conjecture_fof=(
            "fof(odrl011, conjecture,\n"
            "    ?[X]: ( in_denotation(X, europe, isPartOf)\n"
            "          & in_denotation(X, germany, eq) ))."
        ),
        conjecture_smt2=_smt2(
            "; Compatible: ∃X. leq(X, europe) ∧ X = germany\n"
            "; Negated: ∀X. ¬(leq(X, europe) ∧ X = germany)\n"
            "(assert (not (exists ((X C))\n"
            "    (and (leq X europe) (= X germany)))))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL012 — Conflict: eq(germany) ∩ eq(france)
    # germany ≠ france by UNA ($distinct) → ∅
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=12, name="eq-germany-eq-france-conflict",
        category=Category.SPATIAL,
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.EQ, "germany"),
        c2=Constraint("spatial", Op.EQ, "france"),
        description="Conflict: eq(germany) ∩ eq(france) = ∅ [UNA]",
        formal=(
            "⟦eq(germany)⟧ = {germany},  ⟦eq(france)⟧ = {france}\n"
            "%   germany ≠ france  [UNA: $distinct in GEO000-0.ax]\n"
            "%   → intersection = ∅ → Conflict"
        ),
        paper_ref="Definition 3, Definition 5",
        difficulty="Trivial",
        policy_ttl=_ttl("eq", "germany", "eq", "france"),
        notes="Simplest conflict: two distinct singleton denotations.",
        conjecture_fof=(
            "fof(odrl012, conjecture,\n"
            "    ![X]: ~( in_denotation(X, germany, eq)\n"
            "           & in_denotation(X, france, eq) ))."
        ),
        conjecture_smt2=_smt2(
            "; Conflict: ∀X. ¬(X=germany ∧ X=france)\n"
            "; Negated: ∃X. X=germany ∧ X=france\n"
            "(assert (exists ((X C))\n"
            "    (and (= X germany)(= X france))))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL013 — Conflict: isPartOf(westernEurope) ∩ isPartOf(easternEurope)
    # disjoint(wE, eE) + disj_downward + disj_irrefl → ∅
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=13, name="isPartOf-wE-isPartOf-eE-conflict",
        category=Category.SPATIAL,
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.IS_PART_OF, "westernEurope"),
        c2=Constraint("spatial", Op.IS_PART_OF, "easternEurope"),
        description="Conflict: isPartOf(wE) ∩ isPartOf(eE) = ∅ [disj_downward]",
        formal=(
            "disjoint(westernEurope, easternEurope)  [sibling disjointness]\n"
            "%   disj_downward: ∀X. leq(X,wE) ∧ leq(X,eE) → disjoint(X,X)\n"
            "%   disj_irrefl: ¬disjoint(X,X)  →  contradiction  →  ∅"
        ),
        paper_ref="Definition 2 (disj_downward), Definition 5",
        difficulty="Medium",
        policy_ttl=_ttl("isPartOf", "westernEurope", "isPartOf", "easternEurope"),
        notes="Core conflict pattern used in Theorem 1 proof.",
        conjecture_fof=(
            "fof(odrl013, conjecture,\n"
            "    ![X]: ~( in_denotation(X, westernEurope, isPartOf)\n"
            "           & in_denotation(X, easternEurope, isPartOf) ))."
        ),
        conjecture_smt2=_smt2(
            "; Conflict: ∀X. ¬(leq(X,wE) ∧ leq(X,eE))\n"
            "; Negated: ∃X. leq(X,westernEurope) ∧ leq(X,easternEurope)\n"
            "(assert (exists ((X C))\n"
            "    (and (leq X westernEurope)(leq X easternEurope))))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL014 — Compatible: hasPart(germany) ∩ isPartOf(europe)
    # hasPart looks UPWARD: {x | leq(germany, x)} = {germany, wE, europe, world}
    # isPartOf looks DOWNWARD: {x | leq(x, europe)} ∋ germany, wE, europe
    # Witnesses: westernEurope, europe
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=14, name="hasPart-germany-isPartOf-europe-compatible",
        category=Category.SPATIAL,
        verdict=Verdict.COMPATIBLE, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.HAS_PART, "germany"),
        c2=Constraint("spatial", Op.IS_PART_OF, "europe"),
        description="Compatible: hasPart(germany) ∩ isPartOf(europe) ≠ ∅",
        formal=(
            "⟦hasPart(germany)⟧  = {x | leq(germany,x)} = {germany,wE,europe,world}\n"
            "%   ⟦isPartOf(europe)⟧ = {x | leq(x,europe)}\n"
            "%   Witnesses: westernEurope ∈ both (leq(de,wE) ∧ leq(wE,eu))"
        ),
        paper_ref="Definition 3 (hasPart/isPartOf), Definition 5",
        difficulty="Medium",
        policy_ttl=_ttl("hasPart", "germany", "isPartOf", "europe"),
        notes="hasPart traverses UPWARD — important for understanding direction.",
        conjecture_fof=(
            "fof(odrl014, conjecture,\n"
            "    ?[X]: ( in_denotation(X, germany, hasPart)\n"
            "          & in_denotation(X, europe, isPartOf) ))."
        ),
        conjecture_smt2=_smt2(
            "; Compatible: ∃X. leq(germany,X) ∧ leq(X,europe)\n"
            "; Negated: ∀X. ¬(leq(germany,X) ∧ leq(X,europe))\n"
            "(assert (not (exists ((X C))\n"
            "    (and (leq germany X)(leq X europe)))))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL015 — Conflict: hasPart(germany) ∩ eq(poland)
    # disj(eE,wE) + disj_downward → disj(poland,germany)
    # leq(germany,X) requires X at or above germany (in wE branch)
    # poland ∈ eE branch → poland ∉ ⟦hasPart(de)⟧ → ∅
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=15, name="hasPart-germany-eq-poland-conflict",
        category=Category.SPATIAL,
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.HAS_PART, "germany"),
        c2=Constraint("spatial", Op.EQ, "poland"),
        description="Conflict: hasPart(germany) ∩ eq(poland) = ∅ [Lemma 1]",
        formal=(
            "disj(easternEurope, westernEurope)  +  disj_downward\n"
            "%   → disj(poland, germany)         [de ≤ wE, pl ≤ eE]\n"
            "%   disj_order_consistency: leq(germany, poland) → ¬disj(germany,poland)\n"
            "%   But disj(germany,poland) holds  → ¬leq(germany,poland)\n"
            "%   → poland ∉ ⟦hasPart(germany)⟧  → ∅"
        ),
        paper_ref="Definition 3, Definition 5, Lemma 1",
        difficulty="Hard",
        policy_ttl=_ttl("hasPart", "germany", "eq", "poland"),
        notes="Requires Lemma 1 (disj_order_consistency). Harder than ODRL012.",
        conjecture_fof=(
            "fof(odrl015, conjecture,\n"
            "    ![X]: ~( in_denotation(X, germany, hasPart)\n"
            "           & in_denotation(X, poland, eq) ))."
        ),
        conjecture_smt2=_smt2(
            "; Conflict: ∀X. ¬(leq(germany,X) ∧ X=poland)\n"
            "; i.e. ¬leq(germany, poland)\n"
            "; Negated: leq(germany, poland)\n"
            "(assert (leq germany poland))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL016 — Compatible: neq(germany) ∩ isPartOf(westernEurope)
    # ⟦neq(germany)⟧ = C \ {germany}, Witness: france (≤ wE, ≠ germany)
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=16, name="neq-germany-isPartOf-wE-compatible",
        category=Category.SPATIAL,
        verdict=Verdict.COMPATIBLE, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.NEQ, "germany"),
        c2=Constraint("spatial", Op.IS_PART_OF, "westernEurope"),
        description="Compatible: neq(germany) ∩ isPartOf(westernEurope) ≠ ∅",
        formal=(
            "⟦neq(germany)⟧  = C \\ {germany}\n"
            "%   ⟦isPartOf(wE)⟧ = {x | leq(x,wE)}\n"
            "%   Witness: france  (leq(france,wE) ∧ france ≠ germany [UNA])"
        ),
        paper_ref="Definition 3 (neq/isPartOf), Definition 5",
        difficulty="Medium",
        policy_ttl=_ttl("neq", "germany", "isPartOf", "westernEurope"),
        conjecture_fof=(
            "fof(odrl016, conjecture,\n"
            "    ?[X]: ( in_denotation(X, germany, neq)\n"
            "          & in_denotation(X, westernEurope, isPartOf) ))."
        ),
        conjecture_smt2=_smt2(
            "; Compatible: ∃X. X≠germany ∧ leq(X,westernEurope)\n"
            "; Negated: ∀X. X=germany ∨ ¬leq(X,westernEurope)\n"
            "(assert (not (exists ((X C))\n"
            "    (and (not (= X germany))(leq X westernEurope)))))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL017 — Conflict: neq(germany) ∩ eq(germany)
    # X=germany ∧ X≠germany → direct contradiction
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=17, name="neq-germany-eq-germany-conflict",
        category=Category.SPATIAL,
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.NEQ, "germany"),
        c2=Constraint("spatial", Op.EQ, "germany"),
        description="Conflict: neq(germany) ∩ eq(germany) = ∅",
        formal=(
            "⟦neq(germany)⟧ = C \\ {germany},  ⟦eq(germany)⟧ = {germany}\n"
            "%   X=germany ∧ X≠germany  →  direct contradiction  →  ∅"
        ),
        paper_ref="Definition 3 (eq/neq), Definition 5",
        difficulty="Easy",
        policy_ttl=_ttl("neq", "germany", "eq", "germany"),
        notes="Self-negation pattern. Purely propositional — no KB needed.",
        conjecture_fof=(
            "fof(odrl017, conjecture,\n"
            "    ![X]: ~( in_denotation(X, germany, neq)\n"
            "           & in_denotation(X, germany, eq) ))."
        ),
        conjecture_smt2=_smt2(
            "; Conflict: ∀X. ¬(X≠germany ∧ X=germany)\n"
            "; Negated: ∃X. X≠germany ∧ X=germany\n"
            "(assert (exists ((X C))\n"
            "    (and (not (= X germany))(= X germany))))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL018 — Compatible: isPartOf(westernEurope) ∩ hasPart(bavaria)
    # hasPart(bavaria) = {x | leq(bavaria,x)} = {bavaria,germany,wE,europe,world}
    # isPartOf(wE) = {x | leq(x,wE)} ∋ germany
    # Witness: germany  (leq(bavaria,germany) ∧ leq(germany,wE))
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=18, name="isPartOf-wE-hasPart-bavaria-compatible",
        category=Category.SPATIAL,
        verdict=Verdict.COMPATIBLE, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.IS_PART_OF, "westernEurope"),
        c2=Constraint("spatial", Op.HAS_PART, "bavaria"),
        description="Compatible: isPartOf(westernEurope) ∩ hasPart(bavaria) ≠ ∅",
        formal=(
            "⟦isPartOf(wE)⟧  = {x | leq(x,wE)}\n"
            "%   ⟦hasPart(bavaria)⟧ = {x | leq(bavaria,x)}\n"
            "%   Witness: germany  [leq(bavaria,germany) ∧ leq(germany,wE)]"
        ),
        paper_ref="Definition 2, Definition 3",
        difficulty="Medium-Hard",
        policy_ttl=_ttl("isPartOf", "westernEurope", "hasPart", "bavaria"),
        notes="Requires 2-hop witness chain via sub-national concept.",
        conjecture_fof=(
            "fof(odrl018, conjecture,\n"
            "    ?[X]: ( in_denotation(X, westernEurope, isPartOf)\n"
            "          & in_denotation(X, bavaria, hasPart) ))."
        ),
        conjecture_smt2=_smt2(
            "; Compatible: ∃X. leq(X,westernEurope) ∧ leq(bavaria,X)\n"
            "; Negated: ∀X. ¬(leq(X,wE) ∧ leq(bavaria,X))\n"
            "(assert (not (exists ((X C))\n"
            "    (and (leq X westernEurope)(leq bavaria X)))))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL019 — Conflict: isPartOf(northernEurope) ∩ isPartOf(southernEurope)
    # disjoint(nE, sE) [siblings under europe] → ∅
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=19, name="isPartOf-nE-isPartOf-sE-conflict",
        category=Category.SPATIAL,
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.IS_PART_OF, "northernEurope"),
        c2=Constraint("spatial", Op.IS_PART_OF, "southernEurope"),
        description="Conflict: isPartOf(northernEurope) ∩ isPartOf(southernEurope) = ∅",
        formal=(
            "disjoint(northernEurope, southernEurope)  [siblings under europe]\n"
            "%   disj_downward: ∀X. leq(X,nE) ∧ leq(X,sE) → disjoint(X,X)\n"
            "%   disj_irrefl → contradiction → ∅"
        ),
        paper_ref="Definition 2 (disj_downward), Definition 5",
        difficulty="Medium",
        policy_ttl=_ttl("isPartOf", "northernEurope", "isPartOf", "southernEurope"),
        notes="Same proof pattern as ODRL013 but different sibling pair.",
        conjecture_fof=(
            "fof(odrl019, conjecture,\n"
            "    ![X]: ~( in_denotation(X, northernEurope, isPartOf)\n"
            "           & in_denotation(X, southernEurope, isPartOf) ))."
        ),
        conjecture_smt2=_smt2(
            "; Conflict: ∀X. ¬(leq(X,nE) ∧ leq(X,sE))\n"
            "; Negated: ∃X. leq(X,northernEurope) ∧ leq(X,southernEurope)\n"
            "(assert (exists ((X C))\n"
            "    (and (leq X northernEurope)(leq X southernEurope))))"
        ),
    ))

    # Inject the shared GEO preamble into every problem's inline_smt2_kb
    preamble = _preamble()
    for prob in problems:
        prob.inline_smt2_kb = preamble

    return problems
