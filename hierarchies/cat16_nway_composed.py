"""
cat16_nway_composed.py
Category 16: N-Way Composed Policies — ODRL170–175
N-way × multi-operand (spatial + purpose).
"""
from .models import Category, KBProblem, SZS

_CAT  = Category.N_WAY_COMPOSED
_GEO  = "Axioms/Layer0-DomainKB/GEO000-0.ax"
_ODRL = "Axioms/Layer1-ODRLCore/ODRL000-0.ax"

_DPV_SAFE = """\
fof(dpv_s_root, axiom, concept(purpose)).
fof(dpv_s_c1,   axiom, concept(commercialPurpose)).
fof(dpv_s_c2,   axiom, concept(researchAndDevelopment)).
fof(dpv_s_c3,   axiom, concept(commercialResearch)).
fof(dpv_s_c4,   axiom, concept(academicResearch)).
fof(dpv_s_c5,   axiom, concept(serviceProvision)).
fof(dpv_s_leq1, axiom, leq(commercialPurpose, purpose)).
fof(dpv_s_leq2, axiom, leq(researchAndDevelopment, purpose)).
fof(dpv_s_leq3, axiom, leq(serviceProvision, purpose)).
fof(dpv_s_leq4, axiom, leq(commercialResearch, commercialPurpose)).
fof(dpv_s_leq5, axiom, leq(commercialResearch, researchAndDevelopment)).
fof(dpv_s_leq6, axiom, leq(academicResearch, researchAndDevelopment)).
fof(dpv_s_refl1,axiom, leq(purpose, purpose)).
fof(dpv_s_refl2,axiom, leq(commercialPurpose, commercialPurpose)).
fof(dpv_s_refl3,axiom, leq(researchAndDevelopment, researchAndDevelopment)).
fof(dpv_s_refl4,axiom, leq(commercialResearch, commercialResearch)).
fof(dpv_s_refl5,axiom, leq(academicResearch, academicResearch)).
fof(dpv_s_refl6,axiom, leq(serviceProvision, serviceProvision)).
fof(dpv_s_disj1,axiom, disjoint(commercialPurpose, serviceProvision)).
fof(dpv_s_disj2,axiom, disjoint(researchAndDevelopment, serviceProvision)).
fof(dpv_s_una,  axiom, $distinct(purpose, commercialPurpose, researchAndDevelopment,
              commercialResearch, academicResearch, serviceProvision))."""

def nway_composed() -> list[KBProblem]:
    return [

        KBProblem(
            number=170, name="3policy-all-compatible-spatial-purpose",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL], inline_axioms=_DPV_SAFE,
            conjecture_fof=(
                "fof(odrl170, conjecture,\n"
                "    ( ?[Xs,Xp]: ( in_denotation(Xs, europe,                isPartOf)\n"
                "                & in_denotation(Xs, germany,               eq)\n"
                "                & in_denotation(Xp, researchAndDevelopment,isA)\n"
                "                & in_denotation(Xp, academicResearch,      isA) )\n"
                "    & ?[Ys,Yp]: ( in_denotation(Ys, europe,                isPartOf)\n"
                "                & in_denotation(Ys, westernEurope,         isPartOf)\n"
                "                & in_denotation(Yp, researchAndDevelopment,isA)\n"
                "                & in_denotation(Yp, researchAndDevelopment,isA) )\n"
                "    & ?[Zs,Zp]: ( in_denotation(Zs, germany,               eq)\n"
                "                & in_denotation(Zs, westernEurope,         isPartOf)\n"
                "                & in_denotation(Zp, academicResearch,      isA)\n"
                "                & in_denotation(Zp, researchAndDevelopment,isA) ) ))."
            ),
            description="3-way multi-dim: all 3 pairs Compatible on spatial+purpose",
            difficulty="Very Hard",
        ),

        KBProblem(
            number=171, name="non-transitive-one-dimension",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL], inline_axioms=_DPV_SAFE,
            conjecture_fof=(
                "fof(odrl171, conjecture,\n"
                "    ( ?[Xs,Xp]: ( in_denotation(Xs, westernEurope,          isPartOf)\n"
                "                & in_denotation(Xs, europe,                 isPartOf)\n"
                "                & in_denotation(Xp, researchAndDevelopment, isA)\n"
                "                & in_denotation(Xp, academicResearch,       isA) )\n"
                "    & ?[Ys,Yp]: ( in_denotation(Ys, europe,                 isPartOf)\n"
                "                & in_denotation(Ys, easternEurope,          isPartOf)\n"
                "                & in_denotation(Yp, academicResearch,       isA)\n"
                "                & in_denotation(Yp, commercialResearch,     isA) )\n"
                "    & ![Zs]:    ~( in_denotation(Zs, westernEurope,          isPartOf)\n"
                "               &  in_denotation(Zs, easternEurope,          isPartOf) ) ))."
            ),
            description="Non-transitive in multi-dim: spatial conflict breaks transitivity",
            difficulty="Very Hard",
        ),

        KBProblem(
            number=172, name="3policy-mutual-exclusion-spatial-suffices",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL], inline_axioms=_DPV_SAFE,
            conjecture_fof=(
                "fof(odrl172, conjecture,\n"
                "    ( ![X]: ~( in_denotation(X, germany, isPartOf)\n"
                "             & in_denotation(X, france,  isPartOf) )\n"
                "    & ![Y]: ~( in_denotation(Y, germany, isPartOf)\n"
                "             & in_denotation(Y, poland,  isPartOf) )\n"
                "    & ![Z]: ~( in_denotation(Z, france,  isPartOf)\n"
                "             & in_denotation(Z, poland,  isPartOf) ) ))."
            ),
            description="3-way mutual exclusion: spatial conflict suffices (Thm 2)",
            difficulty="Very Hard",
        ),

        KBProblem(
            number=173, name="3operands-3policies-max-complexity",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL], inline_axioms=_DPV_SAFE,
            conjecture_fof=(
                "fof(odrl173, conjecture,\n"
                "    ( ?[Xs,Xp]: ( in_denotation(Xs, europe,                 isPartOf)\n"
                "               & in_denotation(Xs, germany,                 eq)\n"
                "               & in_denotation(Xp, researchAndDevelopment,  isA)\n"
                "               & in_denotation(Xp, academicResearch,        isA) )\n"
                "    & ?[Ys,Yp]: ( in_denotation(Ys, europe,                 isPartOf)\n"
                "               & in_denotation(Ys, westernEurope,           isPartOf)\n"
                "               & in_denotation(Yp, researchAndDevelopment,  isA)\n"
                "               & in_denotation(Yp, researchAndDevelopment,  isA) )\n"
                "    & ?[Zs,Zp]: ( in_denotation(Zs, germany,                eq)\n"
                "               & in_denotation(Zs, westernEurope,           isPartOf)\n"
                "               & in_denotation(Zp, academicResearch,        isA)\n"
                "               & in_denotation(Zp, researchAndDevelopment,  isA) ) ))."
            ),
            description="3 operands × 3 policies = 9 pairwise checks, all Compatible",
            difficulty="Very Hard",
        ),

        KBProblem(
            number=174, name="4policy-spoiler-spatial-dimension",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL], inline_axioms=_DPV_SAFE,
            conjecture_fof=(
                "fof(odrl174, conjecture,\n"
                "    ( ?[Xs,Xp]: ( in_denotation(Xs, europe,                isPartOf)\n"
                "                & in_denotation(Xs, easternEurope,         isPartOf)\n"
                "                & in_denotation(Xp, researchAndDevelopment,isA)\n"
                "                & in_denotation(Xp, researchAndDevelopment,isA) )\n"
                "    & ![Ys]:   ~( in_denotation(Ys, westernEurope,         isPartOf)\n"
                "               & in_denotation(Ys, easternEurope,         isPartOf) )\n"
                "    & ![Zs]:   ~( in_denotation(Zs, germany,               eq)\n"
                "               & in_denotation(Zs, easternEurope,         isPartOf) ) ))."
            ),
            description="4-policy spoiler: D conflicts B,C on spatial, Compatible with A",
            difficulty="Very Hard",
        ),

        KBProblem(
            number=175, name="dag-multiparent-3way-composed",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL], inline_axioms=_DPV_SAFE,
            conjecture_fof=(
                "fof(odrl175, conjecture,\n"
                "    ( ?[Xp,Xs]: ( in_denotation(Xp, commercialPurpose,      isA)\n"
                "                & in_denotation(Xp, researchAndDevelopment, isA)\n"
                "                & in_denotation(Xs, germany,                isPartOf)\n"
                "                & in_denotation(Xs, europe,                 isPartOf) )\n"
                "    & ?[Yp,Ys]: ( in_denotation(Yp, commercialPurpose,      isA)\n"
                "                & in_denotation(Yp, commercialResearch,     isA)\n"
                "                & in_denotation(Ys, germany,                isPartOf)\n"
                "                & in_denotation(Ys, germany,                eq) )\n"
                "    & ?[Zp,Zs]: ( in_denotation(Zp, researchAndDevelopment, isA)\n"
                "                & in_denotation(Zp, commercialResearch,     isA)\n"
                "                & in_denotation(Zs, europe,                 isPartOf)\n"
                "                & in_denotation(Zs, germany,                eq) ) ))."
            ),
            description="DAG multi-parent in 3-way: cR witnesses all pairs",
            difficulty="Very Hard",
        ),
    ]