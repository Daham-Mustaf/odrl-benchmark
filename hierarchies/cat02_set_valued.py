"""
hierarchies/cat02_set_valued.py
Category 2: Set-valued operator coverage — ODRL020-025.

Tests isAnyOf, isNoneOf, isAllOf against the GEO KB.
All conjectures are prover-friendly (Theorem for Vampire, unsat for Z3).

SMT2 encoding: set-valued operators are inlined directly — no list predicates:
  isAnyOf({v1,v2})  → (or  (leq X v1) (leq X v2))
  isNoneOf({v1,v2}) → (and (not (leq X v1)) (not (leq X v2)))
  isAllOf({v1,v2})  → (and (leq X v1) (leq X v2))

TPTP encoding: uses in_denotation_set/3 + in_value_list/2 + closure axiom
  (matches existing ODRL000-0.ax semantics exactly).

Paper references: Definition 3 (Set-Valued Denotation), Definition 5.

Problems:
  ODRL020  Compatible: isAnyOf({wE,nE}) ∩ eq(germany)
  ODRL021  Compatible: isNoneOf({eE,sE}) ∩ isPartOf(wE)
  ODRL022  Conflict:   isNoneOf({europe}) ∩ isPartOf(wE)   [transitivity]
  ODRL023  Conflict:   isAllOf({wE,eE}) ∩ eq(germany)       [empty isAllOf]
  ODRL024  Compatible: isAnyOf({france,germany}) ∩ isNoneOf({eE})
  ODRL025  Conflict:   isAnyOf({germany,france}) ∩ isNoneOf({wE})
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


def _smt2(assert_block: str) -> str:
    return f"{assert_block}\n(check-sat)\n(exit)"


# ==========================================================================
# SMT2 denotation helpers for set-valued operators
# ==========================================================================

def _smt2_is_any_of(var: str, values: list[str]) -> str:
    """X ∈ ⟦isAnyOf(L)⟧  ↔  ∃v∈L: leq(X,v)"""
    if len(values) == 1:
        return f"(leq {var} {values[0]})"
    clauses = " ".join(f"(leq {var} {v})" for v in values)
    return f"(or {clauses})"


def _smt2_is_none_of(var: str, values: list[str]) -> str:
    """X ∈ ⟦isNoneOf(L)⟧  ↔  ∀v∈L: ¬leq(X,v)"""
    if len(values) == 1:
        return f"(not (leq {var} {values[0]}))"
    clauses = " ".join(f"(not (leq {var} {v}))" for v in values)
    return f"(and {clauses})"


def _smt2_is_all_of(var: str, values: list[str]) -> str:
    """X ∈ ⟦isAllOf(L)⟧  ↔  ∀v∈L: leq(X,v)"""
    if len(values) == 1:
        return f"(leq {var} {values[0]})"
    clauses = " ".join(f"(leq {var} {v})" for v in values)
    return f"(and {clauses})"


# ==========================================================================
# TPTP list axiom helpers
# ==========================================================================

def _fof_list_axioms(list_id: str, values: list[str]) -> str:
    """
    Generate TPTP in_value_list membership facts + closure axiom.
    Mirrors generate_list_closure() from gen_spatial_suite.py.
    """
    lines = []
    for i, v in enumerate(values, 1):
        lines.append(
            f"fof(list_{list_id}_{i}, axiom, in_value_list({v}, {list_id}))."
        )
    # Closure: ∀G. in_value_list(G, list_id) ⇒ (G = v1 ∨ ... ∨ G = vn)
    disjuncts = " | ".join(f"G = {v}" for v in values)
    lines.append(
        f"fof(list_{list_id}_closed, axiom,\n"
        f"    ![G]: (in_value_list(G, {list_id}) => ({disjuncts})))."
    )
    return "\n".join(lines)


# ==========================================================================
# TTL helpers
# ==========================================================================

def _ttl_set(policy: str, rule_type: str, operand: str,
             operator: str, values: list[str]) -> str:
    val_str = "( " + " ".join(f"geo:{v}" for v in values) + " )"
    return (
        f"%   ex:{policy} a odrl:Set ;\n"
        f"%     odrl:{rule_type} [\n"
        f"%       odrl:action odrl:use ;\n"
        f"%       odrl:constraint [\n"
        f"%         odrl:leftOperand odrl:{operand} ;\n"
        f"%         odrl:operator odrl:{operator} ;\n"
        f"%         odrl:rightOperand {val_str} ] ] ."
    )


def _ttl_single(policy: str, rule_type: str, operand: str,
                operator: str, value: str) -> str:
    return (
        f"%   ex:{policy} a odrl:Set ;\n"
        f"%     odrl:{rule_type} [\n"
        f"%       odrl:action odrl:use ;\n"
        f"%       odrl:constraint [\n"
        f"%         odrl:leftOperand odrl:{operand} ;\n"
        f"%         odrl:operator odrl:{operator} ;\n"
        f"%         odrl:rightOperand geo:{value} ] ] ."
    )


# ==========================================================================
# Problem definitions
# ==========================================================================

def set_valued() -> list[KBProblem]:
    problems = []

    # ──────────────────────────────────────────────────────────────────────
    # ODRL020 — Compatible: isAnyOf({westernEurope, northernEurope}) ∩ eq(germany)
    # ⟦isAnyOf({wE,nE})⟧ = ↓wE ∪ ↓nE  ∋ germany (since leq(germany, wE))
    # Witness: germany
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=20, name="isAnyOf-wE-nE-eq-germany-compatible",
        category=Category.SPATIAL,
        verdict=Verdict.COMPATIBLE, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.IS_ANY_OF, "", values=["westernEurope", "northernEurope"],
                      list_id="regions020"),
        c2=Constraint("spatial", Op.EQ, "germany"),
        description="Compatible: isAnyOf({wE,nE}) ∩ eq(germany) ≠ ∅",
        formal=(
            "⟦isAnyOf({wE,nE})⟧ = ↓wE ∪ ↓nE\n"
            "%   germany ∈ ↓wE  [leq(germany, westernEurope)]\n"
            "%   Witness: germany"
        ),
        paper_ref="Definition 3 (isAnyOf), Definition 5",
        difficulty="Medium",
        policy_ttl=(
            _ttl_set("policyA", "permission", "spatial", "isAnyOf",
                     ["westernEurope", "northernEurope"]) + "\n%\n" +
            _ttl_single("policyB", "prohibition", "spatial", "eq", "germany")
        ),
        inline_axioms=_fof_list_axioms("regions020",
                                        ["westernEurope", "northernEurope"]),
        conjecture_fof=(
            "fof(odrl020, conjecture,\n"
            "    ?[X]: ( in_denotation_set(X, regions020, isAnyOf)\n"
            "          & in_denotation(X, germany, eq) ))."
        ),
        conjecture_smt2=_smt2(
            "; Compatible: ∃X. (X≤wE ∨ X≤nE) ∧ X=germany\n"
            "; Negated: ∀X. ¬((X≤wE ∨ X≤nE) ∧ X=germany)\n"
            "(assert (not (exists ((X C))\n"
            f"    (and {_smt2_is_any_of('X', ['westernEurope','northernEurope'])}\n"
            "         (= X germany)))))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL021 — Compatible: isNoneOf({eE,sE}) ∩ isPartOf(wE)
    # Witness: germany — leq(germany,wE) ∧ ¬leq(germany,eE) ∧ ¬leq(germany,sE)
    # (disjoint(wE,eE) + disjoint(wE,sE) prevent leq into other branches)
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=21, name="isNoneOf-eE-sE-isPartOf-wE-compatible",
        category=Category.SPATIAL,
        verdict=Verdict.COMPATIBLE, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.IS_NONE_OF, "", values=["easternEurope", "southernEurope"],
                      list_id="excluded021"),
        c2=Constraint("spatial", Op.IS_PART_OF, "westernEurope"),
        description="Compatible: isNoneOf({eE,sE}) ∩ isPartOf(wE) ≠ ∅",
        formal=(
            "⟦isNoneOf({eE,sE})⟧ = C \\ (↓eE ∪ ↓sE)\n"
            "%   Witness: germany\n"
            "%     leq(germany, westernEurope)  → germany ∈ isPartOf(wE)\n"
            "%     disj(wE,eE) → ¬leq(germany,eE) → germany ∉ ↓eE\n"
            "%     disj(wE,sE) → ¬leq(germany,sE) → germany ∉ ↓sE"
        ),
        paper_ref="Definition 3 (isNoneOf), Definition 5",
        difficulty="Hard",
        policy_ttl=(
            _ttl_set("policyA", "permission", "spatial", "isNoneOf",
                     ["easternEurope", "southernEurope"]) + "\n%\n" +
            _ttl_single("policyB", "prohibition", "spatial", "isPartOf", "westernEurope")
        ),
        inline_axioms=_fof_list_axioms("excluded021",
                                        ["easternEurope", "southernEurope"]),
        conjecture_fof=(
            "fof(odrl021, conjecture,\n"
            "    ?[X]: ( in_denotation_set(X, excluded021, isNoneOf)\n"
            "          & in_denotation(X, westernEurope, isPartOf) ))."
        ),
        conjecture_smt2=_smt2(
            "; Compatible: ∃X. ¬(X≤eE) ∧ ¬(X≤sE) ∧ leq(X,wE)\n"
            "; Negated: ∀X. ¬(¬(X≤eE) ∧ ¬(X≤sE) ∧ leq(X,wE))\n"
            "(assert (not (exists ((X C))\n"
            f"    (and {_smt2_is_none_of('X', ['easternEurope','southernEurope'])}\n"
            "         (leq X westernEurope)))))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL022 — Conflict: isNoneOf({europe}) ∩ isPartOf(wE)
    # ∀x: leq(x,wE) → leq(x,europe) [leq_trans via wE≤europe]
    # → every element of isPartOf(wE) is excluded by isNoneOf({europe}) → ∅
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=22, name="isNoneOf-europe-isPartOf-wE-conflict",
        category=Category.SPATIAL,
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.IS_NONE_OF, "", values=["europe"],
                      list_id="excluded022"),
        c2=Constraint("spatial", Op.IS_PART_OF, "westernEurope"),
        description="Conflict: isNoneOf({europe}) ∩ isPartOf(wE) = ∅",
        formal=(
            "∀X: leq(X, westernEurope) → leq(X, europe)  [leq_trans: wE ≤ europe]\n"
            "%   → every X ∈ ⟦isPartOf(wE)⟧ satisfies leq(X,europe)\n"
            "%   → X is excluded by isNoneOf({europe})\n"
            "%   → intersection = ∅  →  Conflict"
        ),
        paper_ref="Definition 3 (isNoneOf), Definition 5",
        difficulty="Very Hard",
        notes="Requires leq_trans to establish that wE ⊆ ↓europe, then contradiction.",
        policy_ttl=(
            _ttl_set("policyA", "permission", "spatial", "isNoneOf", ["europe"]) + "\n%\n" +
            _ttl_single("policyB", "prohibition", "spatial", "isPartOf", "westernEurope")
        ),
        inline_axioms=_fof_list_axioms("excluded022", ["europe"]),
        conjecture_fof=(
            "fof(odrl022, conjecture,\n"
            "    ![X]: ~( in_denotation_set(X, excluded022, isNoneOf)\n"
            "           & in_denotation(X, westernEurope, isPartOf) ))."
        ),
        conjecture_smt2=_smt2(
            "; Conflict: ∀X. ¬(¬leq(X,europe) ∧ leq(X,wE))\n"
            "; Negated: ∃X. ¬leq(X,europe) ∧ leq(X,westernEurope)\n"
            "(assert (exists ((X C))\n"
            f"    (and {_smt2_is_none_of('X', ['europe'])}\n"
            "         (leq X westernEurope))))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL023 — Conflict: isAllOf({wE,eE}) ∩ eq(germany)
    # disjoint(wE,eE) → ⟦isAllOf({wE,eE})⟧ = ∅ (nothing can be ≤ both)
    # Empty set ∩ anything = ∅ → Conflict
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=23, name="isAllOf-wE-eE-eq-germany-conflict",
        category=Category.SPATIAL,
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.IS_ALL_OF, "", values=["westernEurope", "easternEurope"],
                      list_id="allRegions023"),
        c2=Constraint("spatial", Op.EQ, "germany"),
        description="Conflict: isAllOf({wE,eE}) ∩ eq(germany) = ∅ [empty isAllOf]",
        formal=(
            "⟦isAllOf({wE,eE})⟧ = {X | leq(X,wE) ∧ leq(X,eE)}\n"
            "%   disjoint(wE,eE) → disj_downward → ∀X: leq(X,wE) ∧ leq(X,eE) → disj(X,X)\n"
            "%   disj_irrefl → contradiction → ⟦isAllOf⟧ = ∅\n"
            "%   ∅ ∩ {germany} = ∅  →  Conflict"
        ),
        paper_ref="Definition 3 (isAllOf), Definition 5",
        difficulty="Hard",
        notes="isAllOf requires membership in ALL listed closures. Disjoint pair → empty.",
        policy_ttl=(
            _ttl_set("policyA", "permission", "spatial", "isAllOf",
                     ["westernEurope", "easternEurope"]) + "\n%\n" +
            _ttl_single("policyB", "prohibition", "spatial", "eq", "germany")
        ),
        inline_axioms=_fof_list_axioms("allRegions023",
                                        ["westernEurope", "easternEurope"]),
        conjecture_fof=(
            "fof(odrl023, conjecture,\n"
            "    ![X]: ~( in_denotation_set(X, allRegions023, isAllOf)\n"
            "           & in_denotation(X, germany, eq) ))."
        ),
        conjecture_smt2=_smt2(
            "; Conflict: ∀X. ¬(leq(X,wE) ∧ leq(X,eE) ∧ X=germany)\n"
            "; Negated: ∃X. leq(X,wE) ∧ leq(X,eE) ∧ X=germany\n"
            "(assert (exists ((X C))\n"
            f"    (and {_smt2_is_all_of('X', ['westernEurope','easternEurope'])}\n"
            "         (= X germany))))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL024 — Compatible: isAnyOf({france,germany}) ∩ isNoneOf({eE})
    # Witness: france — leq(france,wE) so france∈isAnyOf, and
    # disj(wE,eE) → ¬leq(france,eE) so france∈isNoneOf({eE})
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=24, name="isAnyOf-fr-de-isNoneOf-eE-compatible",
        category=Category.SPATIAL,
        verdict=Verdict.COMPATIBLE, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.IS_ANY_OF, "", values=["france", "germany"],
                      list_id="anyList024"),
        c2=Constraint("spatial", Op.IS_NONE_OF, "", values=["easternEurope"],
                      list_id="noneList024"),
        description="Compatible: isAnyOf({france,germany}) ∩ isNoneOf({eE}) ≠ ∅",
        formal=(
            "⟦isAnyOf({fr,de})⟧  = ↓france ∪ ↓germany\n"
            "%   ⟦isNoneOf({eE})⟧ = C \\ ↓eE\n"
            "%   Witness: france\n"
            "%     leq(france, westernEurope) → france ∈ isAnyOf\n"
            "%     disj(wE,eE) + disj_downward → ¬leq(france,eE) → france ∈ isNoneOf"
        ),
        paper_ref="Definition 3 (isAnyOf/isNoneOf), Definition 5",
        difficulty="Hard",
        policy_ttl=(
            _ttl_set("policyA", "permission", "spatial", "isAnyOf",
                     ["france", "germany"]) + "\n%\n" +
            _ttl_set("policyB", "prohibition", "spatial", "isNoneOf",
                     ["easternEurope"])
        ),
        inline_axioms=(
            _fof_list_axioms("anyList024", ["france", "germany"]) + "\n" +
            _fof_list_axioms("noneList024", ["easternEurope"])
        ),
        conjecture_fof=(
            "fof(odrl024, conjecture,\n"
            "    ?[X]: ( in_denotation_set(X, anyList024, isAnyOf)\n"
            "          & in_denotation_set(X, noneList024, isNoneOf) ))."
        ),
        conjecture_smt2=_smt2(
            "; Compatible: ∃X. (X≤france ∨ X≤germany) ∧ ¬leq(X,eE)\n"
            "; Negated: ∀X. ¬((X≤france ∨ X≤germany) ∧ ¬leq(X,eE))\n"
            "(assert (not (exists ((X C))\n"
            f"    (and {_smt2_is_any_of('X', ['france','germany'])}\n"
            f"         {_smt2_is_none_of('X', ['easternEurope'])}))))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL025 — Conflict: isAnyOf({germany,france}) ∩ isNoneOf({wE})
    # leq(germany,wE) ∧ leq(france,wE) → both excluded by isNoneOf({wE}) → ∅
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=25, name="isAnyOf-de-fr-isNoneOf-wE-conflict",
        category=Category.SPATIAL,
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.IS_ANY_OF, "", values=["germany", "france"],
                      list_id="anyList025"),
        c2=Constraint("spatial", Op.IS_NONE_OF, "", values=["westernEurope"],
                      list_id="noneList025"),
        description="Conflict: isAnyOf({germany,france}) ∩ isNoneOf({wE}) = ∅",
        formal=(
            "⟦isAnyOf({de,fr})⟧  = ↓germany ∪ ↓france\n"
            "%   ⟦isNoneOf({wE})⟧ = C \\ ↓wE\n"
            "%   leq(germany, westernEurope) → germany ∈ ↓wE → excluded\n"
            "%   leq(france,  westernEurope) → france  ∈ ↓wE → excluded\n"
            "%   All elements of isAnyOf are excluded → ∅ → Conflict"
        ),
        paper_ref="Definition 3 (isAnyOf/isNoneOf), Definition 5",
        difficulty="Hard",
        policy_ttl=(
            _ttl_set("policyA", "permission", "spatial", "isAnyOf",
                     ["germany", "france"]) + "\n%\n" +
            _ttl_set("policyB", "prohibition", "spatial", "isNoneOf",
                     ["westernEurope"])
        ),
        inline_axioms=(
            _fof_list_axioms("anyList025", ["germany", "france"]) + "\n" +
            _fof_list_axioms("noneList025", ["westernEurope"])
        ),
        conjecture_fof=(
            "fof(odrl025, conjecture,\n"
            "    ![X]: ~( in_denotation_set(X, anyList025, isAnyOf)\n"
            "           & in_denotation_set(X, noneList025, isNoneOf) ))."
        ),
        conjecture_smt2=_smt2(
            "; Conflict: ∀X. ¬((X≤de ∨ X≤fr) ∧ ¬leq(X,wE))\n"
            "; Negated: ∃X. (X≤de ∨ X≤fr) ∧ ¬leq(X,wE)\n"
            "(assert (exists ((X C))\n"
            f"    (and {_smt2_is_any_of('X', ['germany','france'])}\n"
            f"         {_smt2_is_none_of('X', ['westernEurope'])})))"
        ),
    ))

    # Inject shared GEO preamble
    preamble = _preamble()
    for prob in problems:
        prob.inline_smt2_kb = preamble

    return problems
