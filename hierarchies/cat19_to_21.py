"""
cat19_adversarial_operators.py
Category 19: Adversarial Operator Patterns — ODRL220–225
Boundary/degenerate set operator combinations.
"""
from .models import Category, KBProblem, SZS

_GEO  = "Axioms/Layer0-DomainKB/GEO000-0.ax"
_ODRL = "Axioms/Layer1-ODRLCore/ODRL000-0.ax"

def _cl(lid, elems):
    d = " | ".join(f"G = {e}" for e in elems)
    return f"fof(list_{lid}_closed, axiom,\n    ![G]: (in_value_list(G, {lid}) => ({d})))."

def adversarial_operators() -> list[KBProblem]:
    _CAT = Category.ADVERSARIAL
    return [

        KBProblem(
            number=220, name="isAllOf-singleton-equals-isPartOf",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL],
            inline_axioms=(
                "fof(l220, axiom, in_value_list(germany, allList220)).\n" +
                _cl("allList220", ["germany"])
            ),
            conjecture_fof=(
                "fof(odrl220, conjecture,\n"
                "    ![X]: ( in_denotation_set(X, allList220, isAllOf)\n"
                "        <=> in_denotation(X, germany, isPartOf) ))."
            ),
            description="isAllOf({de}) ≡ isPartOf(de): singleton biconditional",
            difficulty="Very Hard",
        ),

        KBProblem(
            number=221, name="isAnyOf-singleton-equals-isPartOf",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL],
            inline_axioms=(
                "fof(l221, axiom, in_value_list(germany, anyList221)).\n" +
                _cl("anyList221", ["germany"])
            ),
            conjecture_fof=(
                "fof(odrl221, conjecture,\n"
                "    ![X]: ( in_denotation_set(X, anyList221, isAnyOf)\n"
                "        <=> in_denotation(X, germany, isPartOf) ))."
            ),
            description="isAnyOf({de}) ≡ isPartOf(de): singleton biconditional",
            difficulty="Very Hard",
        ),

        KBProblem(
            number=222, name="isNoneOf-root-complement-empty",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL],
            inline_axioms=(
                "fof(l222, axiom, in_value_list(europe, noneList222)).\n" +
                _cl("noneList222", ["europe"])
            ),
            conjecture_fof=(
                "fof(odrl222, conjecture,\n"
                "    ![X]: ( concept(X)\n"
                "        => ~in_denotation_set(X, noneList222, isNoneOf) ))."
            ),
            description="isNoneOf({europe})=∅: root complement is empty (24-concept check)",
            difficulty="Very Hard",
        ),

        KBProblem(
            number=223, name="isAllOf-subsumes-isAnyOf-same-list",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL],
            inline_axioms=(
                "fof(l223_1,axiom, in_value_list(westernEurope, sharedList223)).\n"
                "fof(l223_2,axiom, in_value_list(europe,        sharedList223)).\n" +
                _cl("sharedList223", ["westernEurope","europe"])
            ),
            conjecture_fof=(
                "fof(odrl223, conjecture,\n"
                "    ![X]: ( in_denotation_set(X, sharedList223, isAllOf)\n"
                "        => in_denotation_set(X, sharedList223, isAnyOf) ))."
            ),
            description="isAllOf(L) ⊆ isAnyOf(L): intersection ⊆ union (same list)",
            difficulty="Very Hard",
        ),

        KBProblem(
            number=224, name="isAnyOf-isNoneOf-same-list-self-annihilation",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL],
            inline_axioms=(
                "fof(l224a, axiom, in_value_list(germany, anyList224)).\n" +
                _cl("anyList224", ["germany"]) + "\n"
                "fof(l224b, axiom, in_value_list(germany, noneList224)).\n" +
                _cl("noneList224", ["germany"])
            ),
            conjecture_fof=(
                "fof(odrl224, conjecture,\n"
                "    ![X]: ~( in_denotation_set(X, anyList224,  isAnyOf)\n"
                "           & in_denotation_set(X, noneList224, isNoneOf) ))."
            ),
            description="Self-annihilation: isAnyOf({de}) ∩ isNoneOf({de})=∅",
            difficulty="Very Hard",
        ),

        KBProblem(
            number=225, name="isNoneOf-isAllOf-dont-partition-C",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL],
            inline_axioms=(
                "fof(l225_1,axiom, in_value_list(westernEurope, sharedList225)).\n"
                "fof(l225_2,axiom, in_value_list(easternEurope, sharedList225)).\n" +
                _cl("sharedList225", ["westernEurope","easternEurope"])
            ),
            conjecture_fof=(
                "fof(odrl225, conjecture,\n"
                "    ?[X]: ( concept(X)\n"
                "          & ~in_denotation_set(X, sharedList225, isNoneOf)\n"
                "          & ~in_denotation_set(X, sharedList225, isAllOf) ))."
            ),
            description="isNoneOf and isAllOf don't partition C: ∃X in neither",
            difficulty="Extreme",
        ),
    ]


# ===========================================================================
"""
cat20_xone.py
Category 20: XONE / Symmetric Difference — ODRL230–237
Negative denotation reasoning via contradiction chains.
"""

_ISO        = "Axioms/Layer0-DomainKB/ISO3166-0.ax"
_ALIGN_DATA = "Axioms/Alignment/ALIGN-GEO-ISO.ax"
_ALIGN_TH   = "Axioms/Layer1-ODRLCore/ALIGN000-0.ax"

_DPV_SAFE_XONE = """\
fof(dpv_xone_c1, axiom, concept(commercialPurpose)).
fof(dpv_xone_c2, axiom, concept(researchAndDevelopment)).
fof(dpv_xone_c3, axiom, concept(commercialResearch)).
fof(dpv_xone_c4, axiom, concept(academicResearch)).
fof(dpv_xone_leq1,axiom, leq(commercialResearch, commercialPurpose)).
fof(dpv_xone_leq2,axiom, leq(commercialResearch, researchAndDevelopment)).
fof(dpv_xone_leq3,axiom, leq(academicResearch,   researchAndDevelopment)).
fof(dpv_xone_refl1,axiom,leq(commercialPurpose, commercialPurpose)).
fof(dpv_xone_refl2,axiom,leq(researchAndDevelopment,researchAndDevelopment)).
fof(dpv_xone_refl3,axiom,leq(commercialResearch, commercialResearch)).
fof(dpv_xone_refl4,axiom,leq(academicResearch,   academicResearch)).
fof(dpv_xone_una, axiom, $distinct(commercialPurpose,researchAndDevelopment,
    commercialResearch,academicResearch))."""

_SYNTH_XONE = """\
fof(sx_root, axiom, concept(euZone)).
fof(sx_c1,   axiom, concept(zoneWest)).
fof(sx_c2,   axiom, concept(zoneEast)).
fof(sx_leq1, axiom, leq(zoneWest, euZone)).
fof(sx_leq2, axiom, leq(zoneEast, euZone)).
fof(sx_refl1,axiom, leq(euZone,   euZone)).
fof(sx_refl2,axiom, leq(zoneWest, zoneWest)).
fof(sx_refl3,axiom, leq(zoneEast, zoneEast)).
fof(sx_una,  axiom, $distinct(euZone, zoneWest, zoneEast))."""
_ALIGN_XONE = """\
fof(ax_1, axiom, align(europe, euZone)).
fof(ax_2, axiom, align(dE, zoneWest)).
fof(ax_3, axiom, align(pL, zoneEast))."""

def _cl20(lid, elems):
    d = " | ".join(f"G = {e}" for e in elems)
    return f"fof(list_{lid}_closed, axiom,\n    ![G]: (in_value_list(G, {lid}) => ({d})))."

def xone() -> list[KBProblem]:
    _CAT = Category.XONE_SYMM_SYMM
    _INC2 = [_GEO, _ISO, _ALIGN_DATA, _ODRL, _ALIGN_TH]
    return [
        KBProblem(
            number=230, name="xone-basic-disjoint-siblings",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL], inline_axioms="",
            conjecture_fof=(
                "fof(odrl230, conjecture,\n"
                "    ?[X]: ( ( in_denotation(X, germany, isPartOf)\n"
                "            & ~in_denotation(X, france,  isPartOf) )\n"
                "          | ( ~in_denotation(X, germany, isPartOf)\n"
                "            & in_denotation(X, france,  isPartOf) ) ))."
            ),
            description="XONE: ↓de △ ↓fr ≠ ∅ via sibling disjointness",
            difficulty="Very Hard",
        ),
        KBProblem(
            number=231, name="xone-derived-disjointness",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL], inline_axioms="",
            conjecture_fof=(
                "fof(odrl231, conjecture,\n"
                "    ?[X]: ( ( in_denotation(X, germany, isPartOf)\n"
                "            & ~in_denotation(X, poland, isPartOf) )\n"
                "          | ( ~in_denotation(X, germany, isPartOf)\n"
                "            & in_denotation(X, poland, isPartOf) ) ))."
            ),
            description="XONE via derived disjointness: de⊥pl (wE⊥eE chain)",
            difficulty="Very Hard",
        ),
        KBProblem(
            number=232, name="xone-3way-mutual-exclusion",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL], inline_axioms="",
            conjecture_fof=(
                "fof(odrl232, conjecture,\n"
                "    ?[X]: ( ( in_denotation(X, germany, isPartOf)\n"
                "            & ~in_denotation(X, france,  isPartOf)\n"
                "            & ~in_denotation(X, poland,  isPartOf) )\n"
                "          | ( ~in_denotation(X, germany, isPartOf)\n"
                "            & in_denotation(X, france,  isPartOf)\n"
                "            & ~in_denotation(X, poland,  isPartOf) )\n"
                "          | ( ~in_denotation(X, germany, isPartOf)\n"
                "            & ~in_denotation(X, france,  isPartOf)\n"
                "            & in_denotation(X, poland,  isPartOf) ) ))."
            ),
            description="3-way XONE: exactly one of {↓de,↓fr,↓pl}",
            difficulty="Extreme",
        ),
        KBProblem(
            number=233, name="xone-failure-dag-safe-blocks-proof",
            variant=1, category=_CAT, szs=SZS.COUNTER_SATISFIABLE,
            kbs=[_ODRL], inline_axioms=_DPV_SAFE_XONE,
            conjecture_fof=(
                "fof(odrl233, conjecture,\n"
                "    ?[X]: ( ( in_denotation(X, commercialPurpose,     isA)\n"
                "            & ~in_denotation(X, researchAndDevelopment,isA) )\n"
                "          | ( ~in_denotation(X, commercialPurpose,     isA)\n"
                "            & in_denotation(X, researchAndDevelopment, isA) ) ))."
            ),
            description="XONE failure: DAG-safe suppresses cP⊥R&D → unprovable",
            difficulty="Very Hard",
        ),
        KBProblem(
            number=234, name="xone-isNoneOf-set-negation",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL],
            inline_axioms=(
                "fof(l234_1,axiom, in_value_list(westernEurope, noneList234)).\n" +
                _cl20("noneList234", ["westernEurope"])
            ),
            conjecture_fof=(
                "fof(odrl234, conjecture,\n"
                "    ?[X]: ( ( in_denotation_set(X, noneList234, isNoneOf)\n"
                "            & ~in_denotation(X, easternEurope, isPartOf) )\n"
                "          | ( ~in_denotation_set(X, noneList234, isNoneOf)\n"
                "            & in_denotation(X, easternEurope, isPartOf) ) ))."
            ),
            description="XONE + isNoneOf: complement × isPartOf, witness=europe",
            difficulty="Extreme",
        ),
        KBProblem(
            number=235, name="xone-2hop-alignment",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=_INC2,
            inline_axioms=_SYNTH_XONE + "\n" + _ALIGN_XONE,
            conjecture_fof=(
                "fof(odrl235, conjecture,\n"
                "    ?[X]: ( ( in_denotation(X, zoneWest, isPartOf)\n"
                "            & ~in_denotation(X, zoneEast, isPartOf) )\n"
                "          | ( ~in_denotation(X, zoneWest, isPartOf)\n"
                "            & in_denotation(X, zoneEast, isPartOf) ) ))."
            ),
            description="XONE via 2-hop alignment: zoneWest △ zoneEast",
            difficulty="Extreme",
        ),
        KBProblem(
            number=236, name="xone-all-pairs-matrix-3concepts",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL], inline_axioms="",
            conjecture_fof=(
                "fof(odrl236, conjecture,\n"
                "    ( ?[X1]: ( ( in_denotation(X1, germany, isPartOf)\n"
                "               & ~in_denotation(X1, france,  isPartOf) )\n"
                "             | ( ~in_denotation(X1, germany, isPartOf)\n"
                "               & in_denotation(X1, france,  isPartOf) ) )\n"
                "    & ?[X2]: ( ( in_denotation(X2, germany, isPartOf)\n"
                "               & ~in_denotation(X2, poland, isPartOf) )\n"
                "             | ( ~in_denotation(X2, germany, isPartOf)\n"
                "               & in_denotation(X2, poland, isPartOf) ) )\n"
                "    & ?[X3]: ( ( in_denotation(X3, france,  isPartOf)\n"
                "               & ~in_denotation(X3, poland, isPartOf) )\n"
                "             | ( ~in_denotation(X3, france,  isPartOf)\n"
                "               & in_denotation(X3, poland, isPartOf) ) ) ))."
            ),
            description="XONE all-pairs matrix: C(3,2)=3 pairwise symmetric diffs",
            difficulty="Extreme",
        ),
        KBProblem(
            number=237, name="xone-multidim-spatial-purpose",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL], inline_axioms=_DPV_SAFE_XONE,
            conjecture_fof=(
                "fof(odrl237, conjecture,\n"
                "    ( ?[Xs]: ( ( in_denotation(Xs, germany, isPartOf)\n"
                "               & ~in_denotation(Xs, france,  isPartOf) )\n"
                "             | ( ~in_denotation(Xs, germany, isPartOf)\n"
                "               & in_denotation(Xs, france,  isPartOf) ) )\n"
                "    & ?[Xp]: ( in_denotation(Xp, researchAndDevelopment, isA)\n"
                "             & in_denotation(Xp, academicResearch,       isA) ) ))."
            ),
            description="XONE multi-dim: spatial(de△fr) × purpose(R&D∩acR)",
            difficulty="Extreme",
        ),
    ]


# ===========================================================================
"""
cat21_operator_monotonicity.py
Category 21: Operator Monotonicity — ODRL250–254
Meta-properties: monotone, anti-monotone, non-monotone operators.
"""

def _cl21(lid, elems):
    d = " | ".join(f"G = {e}" for e in elems)
    return f"fof(list_{lid}_closed, axiom,\n    ![G]: (in_value_list(G, {lid}) => ({d})))."

def operator_monotonicity() -> list[KBProblem]:
    _CAT = Category.MONOTONICITY
    _GEO2  = "Axioms/Layer0-DomainKB/GEO000-0.ax"
    _ODRL2 = "Axioms/Layer1-ODRLCore/ODRL000-0.ax"
    return [
        KBProblem(
            number=250, name="isPartOf-monotone-universal",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO2, _ODRL2], inline_axioms="",
            conjecture_fof=(
                "fof(odrl250, conjecture,\n"
                "    ![A,B,X]: (\n"
                "        (leq(A, B) & in_denotation(X, A, isPartOf))\n"
                "      => in_denotation(X, B, isPartOf) ))."
            ),
            description="isPartOf monotone: leq(A,B) → ↓A ⊆ ↓B (universal)",
            difficulty="Hard",
        ),
        KBProblem(
            number=251, name="hasPart-anti-monotone-universal",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO2, _ODRL2], inline_axioms="",
            conjecture_fof=(
                "fof(odrl251, conjecture,\n"
                "    ![A,B,X]: (\n"
                "        (leq(A, B) & in_denotation(X, B, hasPart))\n"
                "      => in_denotation(X, A, hasPart) ))."
            ),
            description="hasPart anti-monotone: leq(A,B) → ↑B ⊆ ↑A (universal)",
            difficulty="Hard",
        ),
        KBProblem(
            number=252, name="isNoneOf-anti-monotone-concrete",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO2, _ODRL2],
            inline_axioms=(
                "fof(l252a, axiom, in_value_list(westernEurope, noneListWE252)).\n" +
                _cl21("noneListWE252", ["westernEurope"]) + "\n"
                "fof(l252b, axiom, in_value_list(germany, noneListDE252)).\n" +
                _cl21("noneListDE252", ["germany"])
            ),
            conjecture_fof=(
                "fof(odrl252, conjecture,\n"
                "    ![X]: (\n"
                "        in_denotation_set(X, noneListWE252, isNoneOf)\n"
                "      => in_denotation_set(X, noneListDE252, isNoneOf) ))."
            ),
            description="isNoneOf anti-monotone: de≤wE → isNoneOf({wE}) ⊆ isNoneOf({de})",
            difficulty="Very Hard",
        ),
        KBProblem(
            number=253, name="eq-non-monotone-counterexample",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO2, _ODRL2], inline_axioms="",
            conjecture_fof=(
                "fof(odrl253, conjecture,\n"
                "    ?[X]: ( in_denotation(X, bavaria, eq)\n"
                "          & ~in_denotation(X, germany, eq) ))."
            ),
            description="eq non-monotone: bav∈eq(bav) ∧ bav∉eq(de) despite bav≤de",
            difficulty="Medium",
        ),
        KBProblem(
            number=254, name="neq-non-monotone-counterexample",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO2, _ODRL2], inline_axioms="",
            conjecture_fof=(
                "fof(odrl254, conjecture,\n"
                "    ?[X]: ( in_denotation(X, bavaria, neq)\n"
                "          & ~in_denotation(X, germany, neq) ))."
            ),
            description="neq non-monotone: de∈neq(bav) ∧ de∉neq(de) despite bav≤de",
            difficulty="Medium",
        ),
    ]