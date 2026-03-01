"""
hierarchies/cat09_runtime.py
Category 9: Runtime Semantics — ODRL090-095.

Paper §3.2.1 — Definitions 9, 10, Theorem 3.

Runtime predicates (RUNTIME000-0.ax — 7 axioms):
  assigns(Omega, X)       — context ω assigns grounded concept X
  satisfies(Omega, G, Op) — context satisfies (_, Op, v) where γ(v) = G
  ungrounded(G)           — G has no KB grounding (⟦c⟧ = ⊤ case)

Parts A-C are strictly EPR. Part D (satisfies_needs_assignment) enables
Theorem 3 refutation proofs by providing assigns(ω_sk, X) for Skolem
contexts from negated universal conjectures.

SMT2 encoding:
  Ctx sort for execution context constants (distinct from C).
  All 7 runtime axioms encoded as universally quantified assertions.
  Op sort already declared in ODRL core (isPartOf, eq, neq, isA, ...).
  concept/1 predicate needed: satisfaction_to_denotation guard + assigns_typed.

  ODRL090/095 (Theorem 3 forward):
    Assert existential ∃Ω: satisfies(Ω,G1,Op)∧satisfies(Ω,G2,Op) → unsat
  ODRL091/092/093/094 (witnesses and permissive):
    Assert context ground facts, negate conjecture → unsat
"""
from .models import (
    Category, Constraint, KB, KBProblem, Op, SZS, Verdict
)
from .kb_smt2 import (
    geo_runtime_smt2_preamble,
    geo_dpv_runtime_smt2_preamble,
)

_GEO_RT_PREAMBLE   = None
_GEO_DPV_RT_PREAMBLE = None


def _p_geo() -> str:
    global _GEO_RT_PREAMBLE
    if _GEO_RT_PREAMBLE is None:
        _GEO_RT_PREAMBLE = "(set-logic UF)\n\n" + geo_runtime_smt2_preamble()
    return _GEO_RT_PREAMBLE


def _p_geo_dpv() -> str:
    global _GEO_DPV_RT_PREAMBLE
    if _GEO_DPV_RT_PREAMBLE is None:
        _GEO_DPV_RT_PREAMBLE = "(set-logic UF)\n\n" + geo_dpv_runtime_smt2_preamble()
    return _GEO_DPV_RT_PREAMBLE


def _smt2(preamble_fn, ctx_decls: str, assertion: str) -> str:
    """
    Build a complete SMT2 file:
      preamble + context constant declarations + assertion + check-sat.
    ctx_decls: e.g. '(declare-const omega090 Ctx)'
    assertion: the (assert ...) block to check
    """
    return (
        f"{ctx_decls}\n\n"
        f"; ─── Conjecture (negated for refutation) ────────────────────────────\n"
        f"{assertion}\n"
        f"(check-sat)\n(exit)"
    )


def runtime() -> list[KBProblem]:
    problems = []

    # ──────────────────────────────────────────────────────────────────────
    # ODRL090 — Theorem 3 (forward): Conflict → no runtime context exists
    #
    # Static: isPartOf(wE) ∩ isPartOf(eE) = ∅  [ODRL013 conflict]
    # Runtime: ∀Ω: ¬(satisfies(Ω, wE, isPartOf) ∧ satisfies(Ω, eE, isPartOf))
    #
    # 6-step refutation:
    #   1. satisfies_needs_assignment → assigns(ω_sk, X)
    #   2. satisfaction_to_denotation → in_den(X, wE/eE, isPartOf)
    #   3. context_functional → same X for both
    #   4. den_isPartOf_onlyif → leq(X, wE) ∧ leq(X, eE)
    #   5. disj_downward(wE ⊥ eE) → disjoint(X, X)
    #   6. disj_irrefl → contradiction □
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=90, name="theorem3-forward-conflict-no-context",
        category=Category.SPATIAL,
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        kbs=[KB.GEO, KB.RUNTIME],
        c1=Constraint("spatial", Op.IS_PART_OF, "westernEurope"),
        c2=Constraint("spatial", Op.IS_PART_OF, "easternEurope"),
        description="Theorem 3 (forward): static Conflict → no runtime context satisfies both",
        formal=(
            "Static: ⟦isPartOf(wE)⟧ ∩ ⟦isPartOf(eE)⟧ = ∅  [Conflict, ODRL013]\n"
            "%   Runtime: ∀Ω: ¬(satisfies(Ω,wE,isPartOf) ∧ satisfies(Ω,eE,isPartOf))\n"
            "%   6-step refutation via satisfies_needs_assignment + backward bridge"
        ),
        paper_ref="Theorem 3 — Runtime Soundness (Conflict → no context)",
        difficulty="Hard",
        notes=(
            "Key: Part D (satisfies_needs_assignment) provides assigns(ω_sk,X) "
            "for the Skolem context; without it, the backward bridge cannot fire."
        ),
        conjecture_fof=(
            "fof(odrl090, conjecture,\n"
            "    ![Omega]: ~( satisfies(Omega, westernEurope, isPartOf)\n"
            "              & satisfies(Omega, easternEurope, isPartOf) ))."
        ),
        conjecture_smt2=_smt2(
            _p_geo,
            "; omega090 context + explicit Skolem witness for assigns (Part D)\n"
            "(declare-const omega090 Ctx)\n"
            "(declare-const omega090v C) ; Skolem witness: assigns(omega090, omega090v)",
            "; Theorem 3: negate universal — assert ∃Ω satisfying both → unsat\n"
            "; Skolem: assigns(omega090, omega090v) replaces Part D existential\n"
            "(assert (assigns omega090 omega090v))\n"
            "(assert (satisfies omega090 westernEurope isPartOf))\n"
            "(assert (satisfies omega090 easternEurope isPartOf))"
        ),
        inline_smt2_kb=_p_geo(),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL091 — Runtime witness for Compatible verdict (Def. 10)
    #
    # Static: isPartOf(europe) ∩ eq(germany) = {germany} ≠ ∅  [Compatible]
    # Runtime: assigns(ω, germany) → denotation_to_satisfaction
    #   → satisfies(ω, europe, isPartOf) ∧ satisfies(ω, germany, eq)
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=91, name="runtime-witness-compatible-europe-germany",
        category=Category.SPATIAL,
        verdict=Verdict.COMPATIBLE, szs=SZS.THEOREM,
        kbs=[KB.GEO, KB.RUNTIME],
        c1=Constraint("spatial", Op.IS_PART_OF, "europe"),
        c2=Constraint("spatial", Op.EQ, "germany"),
        description="Runtime witness: Compatible verdict → satisfying context exists",
        formal=(
            "assigns(ω, germany)\n"
            "%   → leq(germany, europe) [GEO KB] → in_den(germany, europe, isPartOf)\n"
            "%   → satisfies(ω, europe, isPartOf)  [denotation_to_satisfaction]\n"
            "%   → germany = germany → in_den(germany, germany, eq)\n"
            "%   → satisfies(ω, germany, eq)  [denotation_to_satisfaction]"
        ),
        paper_ref="Definition 10 — Runtime Witness for Compatible Verdict",
        difficulty="Medium",
        inline_axioms="fof(runtime_context_091, axiom, assigns(omega091, germany)).",
        conjecture_fof=(
            "fof(odrl091, conjecture,\n"
            "    ( satisfies(omega091, europe, isPartOf)\n"
            "    & satisfies(omega091, germany, eq) ))."
        ),
        conjecture_smt2=_smt2(
            _p_geo,
            "(declare-const omega091 Ctx)",
            "; Compatible witness: assigns(omega091, germany) → satisfies both\n"
            "(assert (assigns omega091 germany))\n"
            "(assert (not (and\n"
            "    (satisfies omega091 europe isPartOf)\n"
            "    (satisfies omega091 germany eq))))"
        ),
        inline_smt2_kb=_p_geo(),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL092 — Theorem 3 (contrapositive): runtime witness → ¬Conflict
    #
    # Contrapositive: ∃Ω satisfying c1 ∧ c2 → verdict ≠ Conflict
    # Runtime: assigns(ω, france), france ≤ wE, france ≠ germany
    #   → satisfies(ω, wE, isPartOf) ∧ satisfies(ω, germany, neq)
    #   → static overlap: ∃X in both denotations
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=92, name="theorem3-contrapositive-witness-compatible",
        category=Category.SPATIAL,
        verdict=Verdict.COMPATIBLE, szs=SZS.THEOREM,
        kbs=[KB.GEO, KB.RUNTIME],
        c1=Constraint("spatial", Op.IS_PART_OF, "westernEurope"),
        c2=Constraint("spatial", Op.NEQ, "germany"),
        description="Theorem 3 (contrapositive): runtime witness → verdict ≠ Conflict",
        formal=(
            "assigns(ω, france).\n"
            "%   france ≤ wE  [GEO] → in_den(france, wE, isPartOf)\n"
            "%   france ≠ germany  [UNA in GEO] → in_den(france, germany, neq)\n"
            "%   → ∃X: in_den(X, wE, isPartOf) ∧ in_den(X, germany, neq)"
        ),
        paper_ref="Theorem 3 (contrapositive) — Runtime Witness → Static Compatible",
        difficulty="Medium",
        inline_axioms="fof(runtime_context_092, axiom, assigns(omega092, france)).",
        conjecture_fof=(
            "fof(odrl092, conjecture,\n"
            "    ?[X]: ( in_denotation(X, westernEurope, isPartOf)\n"
            "          & in_denotation(X, germany, neq) ))."
        ),
        conjecture_smt2=_smt2(
            _p_geo,
            "(declare-const omega092 Ctx)",
            "; Contrapositive: assigns(omega092,france) → france ∈ ↓wE ∩ neq(germany)\n"
            "(assert (assigns omega092 france))\n"
            "(assert (not (exists ((X C))\n"
            "    (and (in_denotation X westernEurope isPartOf)\n"
            "         (in_denotation X germany neq)))))"
        ),
        inline_smt2_kb=_p_geo(),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL093 — Permissive satisfaction for ungrounded constraint (⊤ case)
    #
    # Def. 10 case 1: when ⟦c⟧ = ⊤, any grounded context satisfies.
    # assigns(ω, germany) ∧ ungrounded(unknownConcept)
    #   → permissive_satisfaction → satisfies(ω, unknownConcept, isPartOf)
    # Backward bridge blocked: concept(unknownConcept) fails.
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=93, name="permissive-satisfaction-ungrounded",
        category=Category.SPATIAL,
        verdict=Verdict.CONSISTENT, szs=SZS.THEOREM,
        kbs=[KB.GEO, KB.RUNTIME],
        c1=None, c2=None,
        description="Permissive ⊤: ungrounded constraint → satisfy by default",
        formal=(
            "assigns(ω, germany) ∧ ungrounded(unknownConcept)\n"
            "%   → permissive_satisfaction → satisfies(ω, unknownConcept, isPartOf)\n"
            "%   Backward bridge blocked: ungrounded_not_concept prevents concept(unknownConcept)\n"
            "%   → satisfaction_to_denotation guard fails → no in_denotation contradiction"
        ),
        paper_ref="Definition 10 (⊤ case) — Permissive Satisfaction",
        difficulty="Easy",
        notes=(
            "Tests the ⊤ branch of Def. 10. The guard concept(G) on the backward "
            "bridge is essential: without it, permissive_sat + backward → in_den(X,unkG,Op) "
            "→ leq(X,unkG) → concept(unkG) contradicts ungrounded(unkG)."
        ),
        inline_axioms=(
            "fof(runtime_context_093, axiom, assigns(omega093, germany)).\n"
            "fof(unknown_ungrounded, axiom, ungrounded(unknownConcept))."
        ),
        conjecture_fof=(
            "fof(odrl093, conjecture,\n"
            "    satisfies(omega093, unknownConcept, isPartOf))."
        ),
        conjecture_smt2=_smt2(
            _p_geo,
            "(declare-const omega093 Ctx)\n"
            "(declare-const unknownConcept C)",
            "; Permissive: assigns(omega093,germany) ∧ ungrounded(unknownConcept) → satisfies\n"
            "(assert (assigns omega093 germany))\n"
            "(assert (ungrounded unknownConcept))\n"
            "(assert (not (satisfies omega093 unknownConcept isPartOf)))"
        ),
        inline_smt2_kb=_p_geo(),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL094 — Multi-operand runtime (Def. 6 + Theorem 3)
    #
    # AND composition: ω must satisfy ALL operand constraints.
    # Per-operand context constants (Assumption 2: operand independence):
    #   omega094s ↦ germany (spatial)
    #   omega094p ↦ academicResearch (purpose)
    #
    # Prove: all four satisfaction facts hold simultaneously.
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=94, name="multi-operand-runtime-spatial-purpose",
        category=Category.SPATIAL,
        verdict=Verdict.COMPATIBLE, szs=SZS.THEOREM,
        kbs=[KB.GEO, KB.DPV, KB.RUNTIME],
        c1=None, c2=None,
        description="Multi-operand AND: runtime witness for 2-operand Compatible verdict",
        formal=(
            "omega094s ↦ germany:  germany ≤ europe → satisfies(s, europe, isPartOf)\n"
            "%                       germany = germany → satisfies(s, germany, eq)\n"
            "%   omega094p ↦ academicResearch:\n"
            "%                       academicResearch ≤ R&D → satisfies(p, R&D, isA)\n"
            "%                       academicResearch ≤ academicResearch → satisfies(p, aR, isA)"
        ),
        paper_ref="Theorem 2 + 3 — Multi-Operand Runtime Soundness",
        difficulty="Hard",
        notes=(
            "Operand independence (Assumption 2): separate Ctx constants per operand. "
            "Spatial and purpose constraints are evaluated independently. "
            "Static verdict is AND-Compatible on both dimensions."
        ),
        inline_axioms=(
            "% Per-operand contexts (Assumption 2: operand independence)\n"
            "fof(ctx_spatial, axiom, assigns(omega094s, germany)).\n"
            "fof(ctx_purpose, axiom, assigns(omega094p, academicResearch))."
        ),
        conjecture_fof=(
            "fof(odrl094, conjecture,\n"
            "    ( satisfies(omega094s, europe, isPartOf)\n"
            "    & satisfies(omega094s, germany, eq)\n"
            "    & satisfies(omega094p, researchAndDevelopment, isA)\n"
            "    & satisfies(omega094p, academicResearch, isA) ))."
        ),
        conjecture_smt2=_smt2(
            _p_geo_dpv,
            "; Per-operand contexts with explicit assignments\n"
            "(declare-const omega094s Ctx)\n"
            "(declare-const omega094p Ctx)",
            "; Multi-operand: assigns + negate AND conjunction → unsat\n"
            "(assert (assigns omega094s germany))\n"
            "(assert (assigns omega094p academicResearch))\n"
            "(assert (not (and\n"
            "    (satisfies omega094s europe isPartOf)\n"
            "    (satisfies omega094s germany eq)\n"
            "    (satisfies omega094p researchAndDevelopment isA)\n"
            "    (satisfies omega094p academicResearch isA))))"
        ),
        inline_smt2_kb=_p_geo_dpv(),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL095 — Conflict propagation at runtime (Lemma 2 + Theorem 3)
    #
    # Lemma 2: isPartOf(germany) ⊑ isPartOf(wE) ∧ conflict(wE,eE)
    #          → conflict(germany, eE)
    # Theorem 3: conflict(germany, eE)
    #          → ∀Ω: ¬(satisfies(Ω, germany, isPartOf) ∧ satisfies(Ω, eE, isPartOf))
    #
    # 7-step refutation (ODRL090 + one extra leq_trans step):
    #   1. satisfies_needs_assignment → assigns(ω_sk, X)
    #   2. satisfaction_to_denotation → in_den(X, germany/eE, isPartOf)
    #   3. context_functional → same X
    #   4. den_isPartOf_onlyif → leq(X, germany) ∧ leq(X, eE)
    #   5. leq_trans: leq(X,germany) ∧ leq(germany,wE) → leq(X,wE)
    #   6. disj_downward(wE ⊥ eE) → disjoint(X, X)
    #   7. disj_irrefl → contradiction □
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=95, name="runtime-conflict-propagation-lemma2-theorem3",
        category=Category.SPATIAL,
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        kbs=[KB.GEO, KB.RUNTIME],
        c1=Constraint("spatial", Op.IS_PART_OF, "germany"),
        c2=Constraint("spatial", Op.IS_PART_OF, "easternEurope"),
        description="Lemma 2 + Theorem 3: runtime conflict propagation via subsumption",
        formal=(
            "Lemma 2: isPartOf(germany) ⊑ isPartOf(wE)  [germany ≤ wE in GEO]\n"
            "%   disj(wE, eE) + leq(germany, wE) → conflict(germany, eE)\n"
            "%   Theorem 3: ∀Ω: ¬(satisfies(Ω,germany,isPartOf)∧satisfies(Ω,eE,isPartOf))\n"
            "%   7-step refutation: ODRL090 proof + one extra leq_trans at step 5"
        ),
        paper_ref="Lemma 2 + Theorem 3 — Runtime Conflict Propagation",
        difficulty="Very Hard",
        notes=(
            "Hardest runtime problem: requires Vampire to chain leq_trans before "
            "disj_downward. The 7-step proof requires deeper search than ODRL090."
        ),
        conjecture_fof=(
            "fof(odrl095, conjecture,\n"
            "    ![Omega]: ~( satisfies(Omega, germany, isPartOf)\n"
            "              & satisfies(Omega, easternEurope, isPartOf) ))."
        ),
        conjecture_smt2=_smt2(
            _p_geo,
            "; omega095 context + explicit Skolem witness for assigns (Part D)\n"
            "(declare-const omega095 Ctx)\n"
            "(declare-const omega095v C) ; Skolem witness: assigns(omega095, omega095v)",
            "; Conflict propagation via leq_trans + disj_downward → unsat\n"
            "; Proof: leq(X,germany)→leq(X,wE) [trans], disj(wE,eE)→disj(X,X)→⊥\n"
            "(assert (assigns omega095 omega095v))\n"
            "(assert (satisfies omega095 germany isPartOf))\n"
            "(assert (satisfies omega095 easternEurope isPartOf))"
        ),
        inline_smt2_kb=_p_geo(),
    ))

    return problems
