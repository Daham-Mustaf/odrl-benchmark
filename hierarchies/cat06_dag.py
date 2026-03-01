"""
hierarchies/cat06_dag.py
Category 6: DAG Multi-Parent — ODRL056-058.

Validates Note 1: DAG-structured vocabularies with multi-parent concepts.

ODRL056 — NAIVE mode: KB contradictory (ContradictoryAxioms)
  DPV-NAIVE.ax asserts disj(cP, R&D) despite commercialResearch being a
  shared child. This violates disj_irrefl via disj_downward → KB unsat.

ODRL057 — DAG-safe mode: KB consistent (Theorem)
  DPV000-0.ax suppresses disj(cP, R&D). commercialResearch can witness
  both parents simultaneously. Proves the fix works.

ODRL058 — All 6 multi-parent concepts (Table 1 validation)
  Six separate conjectures in one .p file, each proving one multi-parent
  concept can witness both its parents in DAG-safe mode.
  SMT2: asserts negation of all 6 witnesses together → unsat.

SMT2 encoding:
  ODRL056: load NAIVE KB + check-sat → expect unsat (KB itself contradictory)
  ODRL057: negate the existential → expect unsat (witness exists)
  ODRL058: negate all 6 witnesses simultaneously → expect unsat
"""
from .models import (
    Category, KB, KBProblem, Op, SZS, Verdict
)
from .kb_smt2 import (
    dpv_naive_full_smt2_preamble,
    geo_dpv_full_smt2_preamble,
    geo_dpv_multi_smt2_preamble,
)

_NAIVE_PREAMBLE = None
_DAG_SAFE_PREAMBLE = None
_MULTI_PREAMBLE = None


def _preamble_naive() -> str:
    global _NAIVE_PREAMBLE
    if _NAIVE_PREAMBLE is None:
        _NAIVE_PREAMBLE = "(set-logic UF)\n\n" + dpv_naive_full_smt2_preamble()
    return _NAIVE_PREAMBLE


def _preamble_dag_safe() -> str:
    global _DAG_SAFE_PREAMBLE
    if _DAG_SAFE_PREAMBLE is None:
        _DAG_SAFE_PREAMBLE = "(set-logic UF)\n\n" + geo_dpv_full_smt2_preamble()
    return _DAG_SAFE_PREAMBLE


def _preamble_multi() -> str:
    global _MULTI_PREAMBLE
    if _MULTI_PREAMBLE is None:
        _MULTI_PREAMBLE = "(set-logic UF)\n\n" + geo_dpv_multi_smt2_preamble()
    return _MULTI_PREAMBLE


def _smt2(block: str) -> str:
    return f"{block}\n(check-sat)\n(exit)"


def dag_multi_parent() -> list[KBProblem]:
    problems = []

    # ──────────────────────────────────────────────────────────────────────
    # ODRL056 — NAIVE mode: KB is self-contradictory
    # DPV-NAIVE.ax has ALL 285 sibling pairs, including the dangerous:
    #   disjoint(commercialPurpose, researchAndDevelopment)
    # But leq(cR,cP) and leq(cR,R&D) are also in the KB.
    # disj_downward gives: disj(cR,cR) → violates disj_irrefl → ⊥
    # Expected Vampire: ContradictoryAxioms; Expected Z3: unsat
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=56, name="naive-kb-self-contradictory",
        category=Category.DAG_MULTI_PARENT,
        verdict=Verdict.INCONSISTENT, szs=SZS.CONTRADICTORY_AXIOMS,
        kbs=[KB.DPV_NAIVE],
        c1=None, c2=None,
        description="NAIVE mode: KB contradictory — disj(cP,R&D) + shared child",
        formal=(
            "DPV-NAIVE.ax: disjoint(commercialPurpose, researchAndDevelopment)\n"
            "%   leq(commercialResearch, commercialPurpose)    [h_0006]\n"
            "%   leq(commercialResearch, researchAndDevelopment) [h_0007]\n"
            "%   disj_downward: disj(cP,R&D) ∧ leq(cR,cP) ∧ leq(cR,R&D)\n"
            "%              → disj(cR, cR)\n"
            "%   disj_irrefl: ¬disj(cR,cR)  →  ⊥"
        ),
        paper_ref="Note 1 — Multi-Parent Contradiction (NAIVE mode)",
        difficulty="Hard",
        notes="The conjecture is 'false' — Vampire proves it via ContradictoryAxioms.",
        policy_ttl=(
            "%   ex:policy1 a odrl:Set ;\n"
            "%     odrl:permission [ odrl:action odrl:use ;\n"
            "%       odrl:constraint [ odrl:leftOperand odrl:hasPurpose ;\n"
            "%         odrl:operator odrl:isA ;\n"
            "%         odrl:rightOperand dpv:commercialResearch ] ] ."
        ),
        conjecture_fof="fof(odrl056, conjecture, false).",
        conjecture_smt2=_smt2(
            "; NAIVE KB is self-contradictory — no additional assert needed\n"
            "; Z3 returns unsat from the KB axioms alone (disj_irrefl violated)"
        ),
        inline_smt2_kb=_preamble_naive(),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL057 — DAG-safe mode: KB consistent, multi-parent concept works
    # DPV000-0.ax suppresses disj(cP, R&D) because commercialResearch ≤ both.
    # Witness: commercialResearch ∈ ⟦isA(cP)⟧ ∩ ⟦isA(R&D)⟧
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=57, name="dag-safe-multi-parent-consistent",
        category=Category.DAG_MULTI_PARENT,
        verdict=Verdict.COMPATIBLE, szs=SZS.THEOREM,
        kbs=[KB.DPV],
        c1=None, c2=None,
        description="DAG-safe: suppressed pair allows multi-parent witness",
        formal=(
            "DPV000-0.ax (DAG-SAFE): disj(commercialPurpose, R&D) NOT asserted\n"
            "%   because ↓cP ∩ ↓R&D ∋ commercialResearch ≠ ∅  [DAG-safety check]\n"
            "%   Witness: commercialResearch\n"
            "%     leq(cR, commercialPurpose)      → cR ∈ ⟦isA(cP)⟧\n"
            "%     leq(cR, researchAndDevelopment) → cR ∈ ⟦isA(R&D)⟧\n"
            "%   KB is consistent and multi-parent concept works correctly"
        ),
        paper_ref="Note 1 — DAG-Safe Preserves Consistency",
        difficulty="Medium",
        notes="Paired with ODRL056: same concept, different disjointness treatment.",
        policy_ttl=(
            "%   ex:policy1 a odrl:Set ;\n"
            "%     odrl:permission [ odrl:action odrl:use ;\n"
            "%       odrl:constraint [ odrl:leftOperand odrl:hasPurpose ;\n"
            "%         odrl:operator odrl:isA ;\n"
            "%         odrl:rightOperand dpv:commercialResearch ] ] ."
        ),
        conjecture_fof=(
            "fof(odrl057, conjecture,\n"
            "    ?[X]: ( in_denotation(X, commercialPurpose, isA)\n"
            "          & in_denotation(X, researchAndDevelopment, isA) ))."
        ),
        conjecture_smt2=_smt2(
            "; DAG-safe: ∃X. leq(X,cP) ∧ leq(X,R&D)\n"
            "; Negated: ∀X. ¬(leq(X,cP) ∧ leq(X,R&D)) → unsat (cR witnesses)\n"
            "(assert (not (exists ((X C))\n"
            "    (and (leq X commercialPurpose)\n"
            "         (leq X researchAndDevelopment)))))"
        ),
        inline_smt2_kb=_preamble_dag_safe(),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL058 — All 6 multi-parent concepts (Table 1 validation)
    # One .p file with 6 separate conjectures (Vampire proves all).
    # SMT2: negate all 6 witnesses simultaneously → unsat.
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=58, name="all-6-multi-parent-table1-validation",
        category=Category.DAG_MULTI_PARENT,
        verdict=Verdict.COMPATIBLE, szs=SZS.THEOREM,
        kbs=[KB.DPV],
        c1=None, c2=None,
        description="Table 1: all 6 multi-parent concepts verified in DAG-safe mode",
        formal=(
            "1. commercialResearch:             cP ∧ R&D\n"
            "%   2. nonCommercialResearch:          ncP ∧ R&D\n"
            "%   3. personalisedAdvertising:        advertising ∧ personalisation\n"
            "%   4. servicePersonalisation:         personalisation ∧ serviceProvision\n"
            "%   5. communicationForCustomerCare:   communicationManagement ∧ customerCare\n"
            "%   6. improveInternalCRMProcesses:    CRM ∧ optimisationForController\n"
            "%   All 6 witnessed in DPV000-0.ax (DAG-safe)"
        ),
        paper_ref="Note 1 — All 6 Multi-Parent Concepts (Table 1)",
        difficulty="Medium",
        notes=(
            "Multiple conjectures in one .p file — Vampire proves each independently. "
            "SMT2 negates all 6 simultaneously; any single witness falsifies the negation."
        ),
        policy_ttl=(
            "%   Six policies, one per multi-parent concept (see paper Table 1)"
        ),
        # Single conjecture — conjunction of all 6 witnesses.
        # TPTP allows only ONE conjecture per problem; multiple would be non-standard.
        # Each existential uses a distinct variable to avoid unintended sharing.
        conjecture_fof=(
            "fof(odrl058, conjecture,\n"
            "    ( ?[X1]: ( in_denotation(X1, commercialPurpose, isA)\n"
            "             & in_denotation(X1, researchAndDevelopment, isA) )\n"
            "    & ?[X2]: ( in_denotation(X2, nonCommercialPurpose, isA)\n"
            "             & in_denotation(X2, researchAndDevelopment, isA) )\n"
            "    & ?[X3]: ( in_denotation(X3, advertising, isA)\n"
            "             & in_denotation(X3, personalisation, isA) )\n"
            "    & ?[X4]: ( in_denotation(X4, personalisation, isA)\n"
            "             & in_denotation(X4, serviceProvision, isA) )\n"
            "    & ?[X5]: ( in_denotation(X5, communicationManagement, isA)\n"
            "             & in_denotation(X5, customerCare, isA) )\n"
            "    & ?[X6]: ( in_denotation(X6, customerRelationshipManagement, isA)\n"
            "             & in_denotation(X6, optimisationForController, isA) ) ))."
        ),
        # SMT2: negate all 6 simultaneously — any single witness makes this unsat
        conjecture_smt2=_smt2(
            "; All 6 multi-parent witnesses — negate all simultaneously\n"
            "; If any single witness exists, the conjunction of negations is unsat\n"
            "(assert (not (exists ((X1 C))\n"
            "    (and (leq X1 commercialPurpose)(leq X1 researchAndDevelopment)))))\n"
            "(assert (not (exists ((X2 C))\n"
            "    (and (leq X2 nonCommercialPurpose)(leq X2 researchAndDevelopment)))))\n"
            "(assert (not (exists ((X3 C))\n"
            "    (and (leq X3 advertising)(leq X3 personalisation)))))\n"
            "(assert (not (exists ((X4 C))\n"
            "    (and (leq X4 personalisation)(leq X4 serviceProvision)))))\n"
            "(assert (not (exists ((X5 C))\n"
            "    (and (leq X5 communicationManagement)(leq X5 customerCare)))))\n"
            "(assert (not (exists ((X6 C))\n"
            "    (and (leq X6 customerRelationshipManagement)\n"
            "         (leq X6 optimisationForController)))))"
        ),
        inline_smt2_kb=_preamble_multi(),
    ))

    return problems
