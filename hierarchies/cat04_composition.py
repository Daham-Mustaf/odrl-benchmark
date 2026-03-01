"""
hierarchies/cat04_composition.py
Category 4: Multi-dimensional AND/OR/XONE Composition — ODRL040-047.

Each problem has TWO dimensions (spatial + purpose), each with its own
variable (Xs, Xp). The Kleene connective determines how per-dimension
verdicts combine into the overall verdict.

Composition table used:
  AND:  all dims compatible → Compatible; any dim conflict → Conflict
  OR:   any dim compatible  → Compatible; all dims conflict → Conflict
  XONE: exactly one dim compatible → Compatible; otherwise → Unknown or Conflict

SMT2 encoding for two-dimensional problems:
  AND-Compatible: ¬(∃Xs.φ_s ∧ ∃Xp.φ_p)  expect unsat  (both witnesses exist)
  AND-Conflict:   ∃Xp.φ_p                 expect unsat  (purpose intersection empty)
  OR-Compatible:  ¬∃Xs.φ_s ∧ ¬∃Xp.φ_p   expect unsat  (purpose compatible)
  XONE-Compatible: negated form           expect unsat

Paper references: Definition 6 (Multi-dimensional Composition).
"""
from .models import (
    Category, Constraint, KB, KBProblem, Op, SZS, Verdict
)
from .kb_smt2 import geo_dpv_full_smt2_preamble, geo_full_smt2_preamble

_GEO_DPV_PREAMBLE = None
_GEO_PREAMBLE = None


def _preamble_geo_dpv() -> str:
    global _GEO_DPV_PREAMBLE
    if _GEO_DPV_PREAMBLE is None:
        _GEO_DPV_PREAMBLE = "(set-logic UF)\n\n" + geo_dpv_full_smt2_preamble()
    return _GEO_DPV_PREAMBLE


def _preamble_geo() -> str:
    global _GEO_PREAMBLE
    if _GEO_PREAMBLE is None:
        _GEO_PREAMBLE = "(set-logic UF)\n\n" + geo_full_smt2_preamble()
    return _GEO_PREAMBLE


def _smt2(block: str) -> str:
    return f"{block}\n(check-sat)\n(exit)"


def _ttl_2dim(s_rule, s_op, s_val, p_rule, p_op, p_val) -> str:
    return (
        f"%   ex:policyA a odrl:Set ;\n"
        f"%     odrl:{s_rule} [\n"
        f"%       odrl:action odrl:use ;\n"
        f"%       odrl:constraint [ odrl:leftOperand odrl:spatial ;"
        f" odrl:operator odrl:{s_op} ; odrl:rightOperand geo:{s_val} ] ;\n"
        f"%       odrl:constraint [ odrl:leftOperand odrl:hasPurpose ;"
        f" odrl:operator odrl:{p_op} ; odrl:rightOperand dpv:{p_val} ] ] .\n"
        f"%\n"
        f"%   ex:policyB a odrl:Set ;\n"
        f"%     odrl:{p_rule} [\n"
        f"%       odrl:action odrl:use ;\n"
        f"%       odrl:constraint [ odrl:leftOperand odrl:spatial ;"
        f" odrl:operator odrl:{s_op} ; odrl:rightOperand geo:{s_val} ] ;\n"
        f"%       odrl:constraint [ odrl:leftOperand odrl:hasPurpose ;"
        f" odrl:operator odrl:{p_op} ; odrl:rightOperand dpv:{p_val} ] ] ."
    )


def composition() -> list[KBProblem]:
    problems = []

    # ──────────────────────────────────────────────────────────────────────
    # ODRL040 — AND-Compatible: V_spatial=Compatible ∧ V_purpose=Compatible
    # spatial:  isPartOf(europe) ∩ eq(germany)      → Compatible [germany]
    # purpose:  isA(R&D) ∩ isA(academicResearch)    → Compatible [academicResearch]
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=40, name="AND-compatible-spatial-and-purpose",
        category=Category.SPATIAL,
        verdict=Verdict.COMPATIBLE, szs=SZS.THEOREM,
        kbs=[KB.GEO, KB.DPV],
        c1=None, c2=None,
        description="AND-Compatible: V_spatial=Compatible ∧ V_purpose=Compatible",
        formal=(
            "Xs=germany:   leq(germany,europe) ∧ germany=germany  ✓\n"
            "%   Xp=academicResearch: leq(aR,R&D) ∧ leq(aR,aR)   ✓\n"
            "%   AND: both ✓ → Compatible"
        ),
        paper_ref="Definition 6 (Composition, and)",
        difficulty="Medium",
        policy_ttl=_ttl_2dim(
            "permission", "isPartOf", "europe",
            "prohibition", "isA", "ResearchAndDevelopment"
        ),
        conjecture_fof=(
            "fof(odrl040, conjecture,\n"
            "    ( ?[Xs]: ( in_denotation(Xs, europe, isPartOf)\n"
            "             & in_denotation(Xs, germany, eq) )\n"
            "    & ?[Xp]: ( in_denotation(Xp, researchAndDevelopment, isA)\n"
            "             & in_denotation(Xp, academicResearch, isA) ) ))."
        ),
        conjecture_smt2=_smt2(
            "; AND-Compatible: ¬(∃Xs.φ_s ∧ ∃Xp.φ_p) → unsat (both witnesses exist)\n"
            "(assert (not (exists ((Xs C)(Xp C))\n"
            "    (and (leq Xs europe)(= Xs germany)\n"
            "         (leq Xp researchAndDevelopment)(leq Xp academicResearch)))))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL041 — AND-Conflict: V_spatial=Compatible ∧ V_purpose=Conflict
    # purpose: isA(academicResearch) ∩ isA(marketing) → Conflict [disj]
    # AND: one dimension conflicts → overall Conflict
    # Uses flip_conj (prove the conflicting dimension universally)
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=41, name="AND-conflict-purpose-dimension",
        category=Category.SPATIAL,
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        kbs=[KB.GEO, KB.DPV],
        c1=None, c2=None,
        description="AND-Conflict: V_spatial=Compatible ∧ V_purpose=Conflict",
        formal=(
            "purpose: isA(academicResearch) ∩ isA(marketing)\n"
            "%   disj(academicResearch, marketing) in DPV000-0.ax\n"
            "%   → disj_downward → ∀X: leq(X,aR) ∧ leq(X,mk) → contradiction\n"
            "%   AND: purpose conflict → overall Conflict"
        ),
        paper_ref="Definition 6 (Composition, and)",
        difficulty="Hard",
        notes="flip_conj targets purpose dimension only — sufficient for AND-Conflict.",
        policy_ttl=_ttl_2dim(
            "permission", "isPartOf", "europe",
            "prohibition", "isA", "AcademicResearch"
        ),
        conjecture_fof=(
            "fof(odrl041, conjecture,\n"
            "    ![Xp]: ~( in_denotation(Xp, academicResearch, isA)\n"
            "            & in_denotation(Xp, marketing, isA) ))."
        ),
        conjecture_smt2=_smt2(
            "; AND-Conflict: purpose dimension empty\n"
            "; Negated: ∃Xp. leq(Xp,academicResearch) ∧ leq(Xp,marketing)\n"
            "(assert (exists ((Xp C))\n"
            "    (and (leq Xp academicResearch)(leq Xp marketing))))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL042 — OR-Compatible: V_spatial=Conflict ∨ V_purpose=Compatible
    # spatial: isPartOf(wE) ∩ isPartOf(eE) → Conflict
    # purpose: isA(R&D) ∩ isA(academicResearch) → Compatible
    # OR: at least one compatible → Compatible
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=42, name="OR-compatible-purpose-saves-spatial-conflict",
        category=Category.SPATIAL,
        verdict=Verdict.COMPATIBLE, szs=SZS.THEOREM,
        kbs=[KB.GEO, KB.DPV],
        c1=None, c2=None,
        description="OR-Compatible: V_spatial=Conflict ∨ V_purpose=Compatible",
        formal=(
            "spatial: isPartOf(wE) ∩ isPartOf(eE) = ∅  [disjoint siblings]\n"
            "%   purpose: isA(R&D) ∩ isA(aR) ≠ ∅  [aR ≤ R&D, witness: academicResearch]\n"
            "%   OR: purpose ✓ → Compatible despite spatial ✗"
        ),
        paper_ref="Definition 6 (Composition, or)",
        difficulty="Hard",
        conjecture_fof=(
            "fof(odrl042, conjecture,\n"
            "    ( ?[Xs]: ( in_denotation(Xs, westernEurope, isPartOf)\n"
            "             & in_denotation(Xs, easternEurope, isPartOf) )\n"
            "    | ?[Xp]: ( in_denotation(Xp, researchAndDevelopment, isA)\n"
            "             & in_denotation(Xp, academicResearch, isA) ) ))."
        ),
        conjecture_smt2=_smt2(
            "; OR-Compatible: negate both disjuncts simultaneously → unsat\n"
            "; ¬∃Xs.φ_s ∧ ¬∃Xp.φ_p — purpose compat makes 2nd assert impossible\n"
            "(assert (not (exists ((Xs C))\n"
            "    (and (leq Xs westernEurope)(leq Xs easternEurope)))))\n"
            "(assert (not (exists ((Xp C))\n"
            "    (and (leq Xp researchAndDevelopment)(leq Xp academicResearch)))))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL043 — OR-Conflict: V_spatial=Conflict ∧ V_purpose=Conflict
    # Both dimensions conflict → OR-Conflict
    # Uses flip_conj: prove both conflicts universally
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=43, name="OR-conflict-both-dimensions",
        category=Category.SPATIAL,
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        kbs=[KB.GEO, KB.DPV],
        c1=None, c2=None,
        description="OR-Conflict: V_spatial=Conflict ∧ V_purpose=Conflict",
        formal=(
            "spatial: isPartOf(wE) ∩ isPartOf(eE) = ∅  [disj(wE,eE)]\n"
            "%   purpose: isA(academicResearch) ∩ isA(marketing) = ∅  [disj(aR,mk)]\n"
            "%   OR: both ✗ → Conflict"
        ),
        paper_ref="Definition 6 (Composition, or)",
        difficulty="Hard",
        conjecture_fof=(
            "fof(odrl043, conjecture,\n"
            "    ( ![Xs]: ~( in_denotation(Xs, westernEurope, isPartOf)\n"
            "              & in_denotation(Xs, easternEurope, isPartOf) )\n"
            "    & ![Xp]: ~( in_denotation(Xp, academicResearch, isA)\n"
            "              & in_denotation(Xp, marketing, isA) ) ))."
        ),
        conjecture_smt2=_smt2(
            "; OR-Conflict: assert both intersections non-empty → unsat\n"
            "(assert (exists ((Xs C))\n"
            "    (and (leq Xs westernEurope)(leq Xs easternEurope))))\n"
            "(assert (exists ((Xp C))\n"
            "    (and (leq Xp academicResearch)(leq Xp marketing))))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL044 — Self-conflict: single rule with contradictory constraints
    # Same operand (spatial), two constraints: isPartOf(wE) ∧ isPartOf(eE)
    # disjoint(wE,eE) → rule is vacuously true / policy is self-conflicting
    # GEO only, no DPV needed
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=44, name="self-conflict-single-rule-contradictory",
        category=Category.SPATIAL,
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.IS_PART_OF, "westernEurope"),
        c2=Constraint("spatial", Op.IS_PART_OF, "easternEurope"),
        description="Self-conflict: single rule with isPartOf(wE) ∧ isPartOf(eE)",
        formal=(
            "Same rule, same operand, two spatial constraints:\n"
            "%   isPartOf(wE) ∧ isPartOf(eE) → must satisfy BOTH\n"
            "%   disj(wE,eE) → no X satisfies both → rule vacuously empty"
        ),
        paper_ref="Definition 5 (self-conflict within single rule)",
        difficulty="Medium",
        policy_ttl=(
            "%   ex:policy1 a odrl:Set ;\n"
            "%     odrl:permission [\n"
            "%       odrl:action odrl:use ;\n"
            "%       odrl:constraint [ odrl:leftOperand odrl:spatial ;"
            " odrl:operator odrl:isPartOf ; odrl:rightOperand geo:westernEurope ] ;\n"
            "%       odrl:constraint [ odrl:leftOperand odrl:spatial ;"
            " odrl:operator odrl:isPartOf ; odrl:rightOperand geo:easternEurope ] ] ."
        ),
        conjecture_fof=(
            "fof(odrl044, conjecture,\n"
            "    ![X]: ~( in_denotation(X, westernEurope, isPartOf)\n"
            "           & in_denotation(X, easternEurope, isPartOf) ))."
        ),
        conjecture_smt2=_smt2(
            "; Self-conflict: ∃X. leq(X,wE) ∧ leq(X,eE) → unsat\n"
            "(assert (exists ((X C))\n"
            "    (and (leq X westernEurope)(leq X easternEurope))))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL045 — XONE-Compatible: purpose ✓ ⊕ spatial ✗
    # Exactly one dimension compatible → XONE-Compatible
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=45, name="XONE-compatible-purpose-only",
        category=Category.SPATIAL,
        verdict=Verdict.COMPATIBLE, szs=SZS.THEOREM,
        kbs=[KB.GEO, KB.DPV],
        c1=None, c2=None,
        description="XONE-Compatible: purpose ✓ ⊕ spatial ✗ → Compatible",
        formal=(
            "purpose: isA(R&D) ∩ isA(aR) ≠ ∅           ✓\n"
            "%   spatial: isPartOf(wE) ∩ isPartOf(eE) = ∅  ✗\n"
            "%   XONE: exactly one ✓ → Compatible"
        ),
        paper_ref="Definition 6 (Composition, xone)",
        difficulty="Very Hard",
        conjecture_fof=(
            "fof(odrl045, conjecture,\n"
            "    ( ?[Xp]: ( in_denotation(Xp, researchAndDevelopment, isA)\n"
            "             & in_denotation(Xp, academicResearch, isA) )\n"
            "    & ~( ?[Xs]: ( in_denotation(Xs, westernEurope, isPartOf)\n"
            "                & in_denotation(Xs, easternEurope, isPartOf) ) ) ))."
        ),
        conjecture_smt2=_smt2(
            "; XONE-Compatible: negate (∃Xp.φ_p ∧ ¬∃Xs.φ_s)\n"
            "; = ¬∃Xp.φ_p ∨ ∃Xs.φ_s\n"
            "; Assert ¬∃Xp.φ_p → unsat (academicResearch witnesses it)\n"
            "(assert (not (exists ((Xp C))\n"
            "    (and (leq Xp researchAndDevelopment)(leq Xp academicResearch)))))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL046 — XONE-Unknown: both dimensions compatible → exclusivity fails
    # We test the flip_conj (Theorem): that both ARE simultaneously compatible.
    # This witnesses the Unknown verdict: XONE exclusivity cannot hold.
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=46, name="XONE-unknown-both-compatible",
        category=Category.SPATIAL,
        verdict=Verdict.UNKNOWN, szs=SZS.THEOREM,
        kbs=[KB.GEO, KB.DPV],
        c1=None, c2=None,
        description="XONE-Unknown: both dims compatible → exclusivity fails",
        formal=(
            "spatial: isPartOf(europe) ∩ eq(germany) ≠ ∅  ✓  [germany]\n"
            "%   purpose: isA(R&D) ∩ isA(aR) ≠ ∅            ✓  [academicResearch]\n"
            "%   XONE: both ✓ → neither exclusively satisfies → Unknown\n"
            "%   Test: flip_conj proves both compatible simultaneously"
        ),
        paper_ref="Definition 6 (Composition, xone)",
        difficulty="Very Hard",
        notes="flip_conj is Theorem; main XONE form is CounterSatisfiable.",
        conjecture_fof=(
            "% XONE exclusivity fails — test that both dims are simultaneously compatible\n"
            "fof(odrl046, conjecture,\n"
            "    ( ?[Xs]: ( in_denotation(Xs, europe, isPartOf)\n"
            "             & in_denotation(Xs, germany, eq) )\n"
            "    & ?[Xp]: ( in_denotation(Xp, researchAndDevelopment, isA)\n"
            "             & in_denotation(Xp, academicResearch, isA) ) ))."
        ),
        conjecture_smt2=_smt2(
            "; Both compatible → XONE unknown. Prove both hold simultaneously.\n"
            "; Negated: ¬(∃Xs.φ_s ∧ ∃Xp.φ_p) → unsat\n"
            "(assert (not (exists ((Xs C)(Xp C))\n"
            "    (and (leq Xs europe)(= Xs germany)\n"
            "         (leq Xp researchAndDevelopment)(leq Xp academicResearch)))))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL047 — XONE-Conflict: both dimensions conflict
    # Uses flip_conj: prove both conflicts universally (same as ODRL043)
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=47, name="XONE-conflict-both-dimensions",
        category=Category.SPATIAL,
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        kbs=[KB.GEO, KB.DPV],
        c1=None, c2=None,
        description="XONE-Conflict: V_spatial=Conflict ∧ V_purpose=Conflict",
        formal=(
            "spatial: isPartOf(wE) ∩ isPartOf(eE) = ∅  [disj(wE,eE)]\n"
            "%   purpose: isA(academicResearch) ∩ isA(marketing) = ∅  [disj(aR,mk)]\n"
            "%   XONE: all dims ✗ → Conflict (no dim can be the exclusive ✓)"
        ),
        paper_ref="Definition 6 (Composition, xone)",
        difficulty="Hard",
        conjecture_fof=(
            "fof(odrl047, conjecture,\n"
            "    ( ![Xs]: ~( in_denotation(Xs, westernEurope, isPartOf)\n"
            "              & in_denotation(Xs, easternEurope, isPartOf) )\n"
            "    & ![Xp]: ~( in_denotation(Xp, academicResearch, isA)\n"
            "              & in_denotation(Xp, marketing, isA) ) ))."
        ),
        conjecture_smt2=_smt2(
            "; XONE-Conflict: both intersections empty → assert non-empty → unsat\n"
            "(assert (exists ((Xs C))\n"
            "    (and (leq Xs westernEurope)(leq Xs easternEurope))))\n"
            "(assert (exists ((Xp C))\n"
            "    (and (leq Xp academicResearch)(leq Xp marketing))))"
        ),
    ))

    # Inject preambles: ODRL044 is GEO-only, rest need GEO+DPV
    geo_dpv = _preamble_geo_dpv()
    geo_only = _preamble_geo()
    for prob in problems:
        if KB.DPV in prob.kbs:
            prob.inline_smt2_kb = geo_dpv
        else:
            prob.inline_smt2_kb = geo_only

    return problems
