"""
cat18_combined_complexity.py
Category 18: Combined Complexity — ODRL210–215
Multi-hop + N-way + set ops + DAG simultaneously.
"""
from .models import Category, KBProblem, SZS

_CAT        = Category.COMBINED
_GEO        = "Axioms/Layer0-DomainKB/GEO000-0.ax"
_ISO        = "Axioms/Layer0-DomainKB/ISO3166-0.ax"
_LANG       = "Axioms/Layer0-DomainKB/LANG000-0.ax"
_ALIGN_DATA = "Axioms/Alignment/ALIGN-GEO-ISO.ax"
_ODRL       = "Axioms/Layer1-ODRLCore/ODRL000-0.ax"
_ALIGN_TH   = "Axioms/Layer1-ODRLCore/ALIGN000-0.ax"

_SYNTH = """\
fof(synth_root, axiom, concept(euZone)).
fof(synth_c1,   axiom, concept(zoneWest)).
fof(synth_c2,   axiom, concept(zoneEast)).
fof(synth_leq1, axiom, leq(zoneWest, euZone)).
fof(synth_leq2, axiom, leq(zoneEast, euZone)).
fof(synth_refl1,axiom, leq(euZone,   euZone)).
fof(synth_refl2,axiom, leq(zoneWest, zoneWest)).
fof(synth_refl3,axiom, leq(zoneEast, zoneEast)).
fof(synth_una,  axiom, $distinct(euZone, zoneWest, zoneEast))."""
_ALIGN_IS = """\
fof(align_is_1, axiom, align(europe, euZone)).
fof(align_is_2, axiom, align(dE, zoneWest)).
fof(align_is_3, axiom, align(pL, zoneEast))."""
_COMP = """\
fof(comp_root, axiom, concept(complianceScope)).
fof(comp_c1,   axiom, concept(gdprFull)).
fof(comp_c2,   axiom, concept(gdprPartial)).
fof(comp_leq1, axiom, leq(gdprFull,    complianceScope)).
fof(comp_leq2, axiom, leq(gdprPartial, complianceScope)).
fof(comp_refl1,axiom, leq(complianceScope, complianceScope)).
fof(comp_refl2,axiom, leq(gdprFull,    gdprFull)).
fof(comp_refl3,axiom, leq(gdprPartial, gdprPartial)).
fof(comp_una,  axiom, $distinct(complianceScope, gdprFull, gdprPartial))."""
_ALIGN_SC = """\
fof(align_sc_1, axiom, align(euZone,   complianceScope)).
fof(align_sc_2, axiom, align(zoneWest, gdprFull)).
fof(align_sc_3, axiom, align(zoneEast, gdprPartial))."""
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
_4KB = _SYNTH + "\n" + _ALIGN_IS + "\n" + _COMP + "\n" + _ALIGN_SC
_2HOP_INC = [_GEO, _ISO, _ALIGN_DATA, _ODRL, _ALIGN_TH]

def _cl(lid, elems):
    d = " | ".join(f"G = {e}" for e in elems)
    return f"fof(list_{lid}_closed, axiom,\n    ![G]: (in_value_list(G, {lid}) => ({d})))."

def combined_complexity() -> list[KBProblem]:
    return [
        KBProblem(
            number=210, name="multihop-setops-isAnyOf-aligned-kb",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=_2HOP_INC,
            inline_axioms=(
                _SYNTH + "\n" + _ALIGN_IS + "\n"
                "fof(l210_1,axiom, in_value_list(zoneWest, anyList210)).\n"
                "fof(l210_2,axiom, in_value_list(zoneEast, anyList210)).\n" +
                _cl("anyList210", ["zoneWest","zoneEast"])
            ),
            conjecture_fof=(
                "fof(odrl210, conjecture,\n"
                "    ?[X]: ( in_denotation_set(X, anyList210, isAnyOf)\n"
                "          & in_denotation(X, euZone, isPartOf) ))."
            ),
            description="Multi-hop + set ops: isAnyOf in aligned KB",
            difficulty="Extreme",
        ),
        KBProblem(
            number=211, name="3hop-isNoneOf-complement-4th-dataspace",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=_2HOP_INC,
            inline_axioms=(
                _4KB + "\n"
                "fof(l211, axiom, in_value_list(gdprFull, noneList211)).\n" +
                _cl("noneList211", ["gdprFull"])
            ),
            conjecture_fof=(
                "fof(odrl211, conjecture,\n"
                "    ?[X]: ( in_denotation_set(X, noneList211, isNoneOf)\n"
                "          & in_denotation(X, gdprPartial, isPartOf) ))."
            ),
            description="3-hop + isNoneOf: complement in 4th dataspace",
            difficulty="Extreme",
        ),
        KBProblem(
            number=212, name="full-monty-nway-dag-setops-multidim",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL],
            inline_axioms=(
                _DPV_SAFE + "\n"
                "fof(l212a1,axiom, in_value_list(germany,       anyList212)).\n"
                "fof(l212a2,axiom, in_value_list(france,        anyList212)).\n" +
                _cl("anyList212", ["germany","france"]) + "\n"
                "fof(l212b, axiom, in_value_list(easternEurope, noneList212)).\n" +
                _cl("noneList212", ["easternEurope"])
            ),
            conjecture_fof=(
                "fof(odrl212, conjecture,\n"
                "    ( ?[Xs,Xp]: ( in_denotation_set(Xs, anyList212,  isAnyOf)\n"
                "                & in_denotation_set(Xs, noneList212, isNoneOf)\n"
                "                & in_denotation(Xp, commercialPurpose,     isA)\n"
                "                & in_denotation(Xp, researchAndDevelopment,isA) )\n"
                "    & ?[Ys,Yp]: ( in_denotation_set(Ys, anyList212,  isAnyOf)\n"
                "                & in_denotation(Ys, westernEurope,  isPartOf)\n"
                "                & in_denotation(Yp, commercialPurpose,  isA)\n"
                "                & in_denotation(Yp, commercialResearch, isA) )\n"
                "    & ?[Zs,Zp]: ( in_denotation_set(Zs, noneList212, isNoneOf)\n"
                "                & in_denotation(Zs, westernEurope,  isPartOf)\n"
                "                & in_denotation(Zp, researchAndDevelopment,isA)\n"
                "                & in_denotation(Zp, commercialResearch,   isA) ) ))."
            ),
            description="The Full Monty: n-way + DAG + isAnyOf + isNoneOf + multi-dim",
            difficulty="Extreme",
        ),
        KBProblem(
            number=213, name="3hop-nway-dag-cross-dataspace-triple",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=_2HOP_INC,
            inline_axioms=_DPV_SAFE + "\n" + _4KB,
            conjecture_fof=(
                "fof(odrl213, conjecture,\n"
                "    ( ?[Xp,Xs]: ( in_denotation(Xp, commercialPurpose,     isA)\n"
                "               & in_denotation(Xp, researchAndDevelopment, isA)\n"
                "               & in_denotation(Xs, complianceScope,        isPartOf)\n"
                "               & in_denotation(Xs, gdprFull,               isPartOf) )\n"
                "    & ?[Yp,Ys]: ( in_denotation(Yp, commercialPurpose,     isA)\n"
                "               & in_denotation(Yp, commercialResearch,     isA)\n"
                "               & in_denotation(Ys, complianceScope,        isPartOf)\n"
                "               & in_denotation(Ys, gdprFull,               eq) )\n"
                "    & ?[Zp,Zs]: ( in_denotation(Zp, researchAndDevelopment,isA)\n"
                "               & in_denotation(Zp, commercialResearch,     isA)\n"
                "               & in_denotation(Zs, gdprFull,               isPartOf)\n"
                "               & in_denotation(Zs, gdprFull,               eq) ) ))."
            ),
            description="3-hop + n-way + DAG: 3 policies across 4 dataspaces",
            difficulty="Extreme",
        ),
        KBProblem(
            number=214, name="runtime-alignment-setops-fullstack",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ISO, _ALIGN_DATA, _ODRL, _ALIGN_TH,
                      "Axioms/Layer1-ODRLCore/RUNTIME000-0.ax"],
            inline_axioms=_SYNTH + "\n" + _ALIGN_IS + "\nfof(odrl214_ctx, axiom, assigns(omega214, zoneWest)).",
            conjecture_fof=(
                "fof(odrl214, conjecture,\n"
                "    ( ?[X]: ( in_denotation(X, euZone,   isPartOf)\n"
                "            & in_denotation(X, zoneWest, eq) )\n"
                "    & satisfies(omega214, euZone, isPartOf) ))."
            ),
            description="Full stack: runtime + alignment + denotation in 3-KB context",
            difficulty="Extreme",
        ),
        KBProblem(
            number=215, name="ultimate-4kbs-3policies-3operands-setops-dag",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ISO, _ALIGN_DATA, _ODRL, _ALIGN_TH, _LANG],
            inline_axioms=(
                _DPV_SAFE + "\n" + _4KB + "\n"
                "fof(l215, axiom, in_value_list(gdprFull, anyList215)).\n" +
                _cl("anyList215", ["gdprFull"])
            ),
            conjecture_fof=(
                "fof(odrl215, conjecture,\n"
                "    ( ?[Xs,Xp,Xl]: ( in_denotation_set(Xs, anyList215,  isAnyOf)\n"
                "                   & in_denotation(Xs, complianceScope, isPartOf)\n"
                "                   & in_denotation(Xp, commercialPurpose,     isA)\n"
                "                   & in_denotation(Xp, researchAndDevelopment,isA)\n"
                "                   & in_denotation(Xl, en,   isPartOf)\n"
                "                   & in_denotation(Xl, enGB, eq) )\n"
                "    & ?[Ys,Yp,Yl]: ( in_denotation_set(Ys, anyList215,  isAnyOf)\n"
                "                   & in_denotation(Ys, gdprFull,        eq)\n"
                "                   & in_denotation(Yp, commercialPurpose,   isA)\n"
                "                   & in_denotation(Yp, commercialResearch,  isA)\n"
                "                   & in_denotation(Yl, en, isPartOf)\n"
                "                   & in_denotation(Yl, en, isPartOf) )\n"
                "    & ?[Zs,Zp,Zl]: ( in_denotation(Zs, complianceScope,      isPartOf)\n"
                "                   & in_denotation(Zs, gdprFull,              eq)\n"
                "                   & in_denotation(Zp, researchAndDevelopment,isA)\n"
                "                   & in_denotation(Zp, commercialResearch,    isA)\n"
                "                   & in_denotation(Zl, enGB, eq)\n"
                "                   & in_denotation(Zl, en,   isPartOf) ) ))."
            ),
            description="Ultimate: 4 KBs × 3 policies × 3 operands × set ops × DAG",
            difficulty="Extreme",
        ),
    ]