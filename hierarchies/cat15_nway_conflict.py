"""
cat15_nway_conflict.py
Category 15: N-Way Policy Conflicts — ODRL160–165
3–4 policies simultaneously; non-transitive compatibility.
"""
from .models import Category, KBProblem, SZS

_CAT  = Category.N_WAY_CONFLICT
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

def nway_conflict() -> list[KBProblem]:
    return [

        KBProblem(
            number=160, name="3policy-mutual-exclusion",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL], inline_axioms="",
            conjecture_fof=(
                "fof(odrl160, conjecture,\n"
                "    ( ![X]: ~( in_denotation(X, germany,       isPartOf)\n"
                "             & in_denotation(X, france,        isPartOf) )\n"
                "    & ![Y]: ~( in_denotation(Y, germany,       isPartOf)\n"
                "             & in_denotation(Y, poland,        isPartOf) )\n"
                "    & ![Z]: ~( in_denotation(Z, france,        isPartOf)\n"
                "             & in_denotation(Z, poland,        isPartOf) ) ))."
            ),
            description="3-policy mutual exclusion: all C(3,2)=3 pairs conflict",
            difficulty="Hard",
        ),

        KBProblem(
            number=161, name="3policy-common-witness",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL], inline_axioms="",
            conjecture_fof=(
                "fof(odrl161, conjecture,\n"
                "    ?[X]: ( in_denotation(X, europe,        isPartOf)\n"
                "          & in_denotation(X, westernEurope, isPartOf)\n"
                "          & in_denotation(X, germany,       eq) ))."
            ),
            description="3-policy 3-way ∃: witness=germany ∈ ↓europe∩↓wE∩{de}",
            difficulty="Medium",
        ),

        KBProblem(
            number=162, name="non-transitive-compatibility",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL], inline_axioms="",
            conjecture_fof=(
                "fof(odrl162, conjecture,\n"
                "    ( ?[X]: ( in_denotation(X, westernEurope, isPartOf)\n"
                "            & in_denotation(X, europe,        isPartOf) )\n"
                "    & ?[Y]: ( in_denotation(Y, europe,        isPartOf)\n"
                "            & in_denotation(Y, easternEurope, isPartOf) )\n"
                "    & ![Z]: ~( in_denotation(Z, westernEurope, isPartOf)\n"
                "             & in_denotation(Z, easternEurope, isPartOf) ) ))."
            ),
            description="Non-transitive: A~B, B~C but A⊥C (key N-way insight)",
            difficulty="Hard",
        ),

        KBProblem(
            number=163, name="multidim-3way-spatial-purpose",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL], inline_axioms=_DPV_SAFE,
            conjecture_fof=(
                "fof(odrl163, conjecture,\n"
                "    ( ?[Xs,Xp]: ( in_denotation(Xs, europe,                 isPartOf)\n"
                "               & in_denotation(Xs, germany,                 isPartOf)\n"
                "               & in_denotation(Xp, researchAndDevelopment,  isA)\n"
                "               & in_denotation(Xp, academicResearch,        isA) )\n"
                "    & ?[Ys,Yp]: ( in_denotation(Ys, europe,                 isPartOf)\n"
                "               & in_denotation(Ys, france,                  isPartOf)\n"
                "               & in_denotation(Yp, researchAndDevelopment,  isA)\n"
                "               & in_denotation(Yp, commercialPurpose,       isA) )\n"
                "    & ![Z]:     ~( in_denotation(Z,  germany,                isPartOf)\n"
                "               &  in_denotation(Z,  france,                  isPartOf) ) ))."
            ),
            description="Multi-dim 3-way: A~B, A~C (spatial+purpose), B⊥C (spatial)",
            difficulty="Very Hard",
        ),

        KBProblem(
            number=164, name="4policy-subsumption-chain",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL], inline_axioms="",
            conjecture_fof=(
                "fof(odrl164, conjecture,\n"
                "    ?[X]: ( in_denotation(X, europe,        isPartOf)\n"
                "          & in_denotation(X, westernEurope, isPartOf)\n"
                "          & in_denotation(X, germany,       isPartOf)\n"
                "          & in_denotation(X, bavaria,       eq) ))."
            ),
            description="4-way ∃: all 4 policies share witness=bavaria",
            difficulty="Medium",
        ),

        KBProblem(
            number=165, name="4policy-one-spoiler",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL], inline_axioms="",
            conjecture_fof=(
                "fof(odrl165, conjecture,\n"
                "    ( ?[X]: ( in_denotation(X, europe,        isPartOf)\n"
                "            & in_denotation(X, easternEurope, isPartOf) )\n"
                "    & ![Y]: ~( in_denotation(Y, westernEurope, isPartOf)\n"
                "             & in_denotation(Y, easternEurope, isPartOf) )\n"
                "    & ![Z]: ~( in_denotation(Z, germany,       eq)\n"
                "             & in_denotation(Z, easternEurope, isPartOf) ) ))."
            ),
            description="4-policy spoiler D: Compatible(A,D) ∧ Conflict(B,D) ∧ Conflict(C,D)",
            difficulty="Hard",
        ),
    ]