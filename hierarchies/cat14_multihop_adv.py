"""
cat14_multihop_adv.py
Category 14: Multi-Hop Alignment — ODRL150–159
2-hop and 3-hop alignment conflict detection + Proposition 2(2) witness-loss.
"""
from .models import Category, KBProblem, SZS

_CAT        = Category.MULTI_HOP_ALIGN
_GEO        = "Axioms/Layer0-DomainKB/GEO000-0.ax"
_ISO        = "Axioms/Layer0-DomainKB/ISO3166-0.ax"
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

_ALIGN_ISO_SYNTH = """\
fof(align_iso_synth_1, axiom, align(europe, euZone)).
fof(align_iso_synth_2, axiom, align(dE, zoneWest)).
fof(align_iso_synth_3, axiom, align(pL, zoneEast))."""

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

_ALIGN_SYNTH_COMP = """\
fof(align_synth_comp_1, axiom, align(euZone,   complianceScope)).
fof(align_synth_comp_2, axiom, align(zoneWest, gdprFull)).
fof(align_synth_comp_3, axiom, align(zoneEast, gdprPartial))."""

_WIT_SRC = """\
fof(wit_src_c1,   axiom, concept(witA)).
fof(wit_src_c2,   axiom, concept(witB)).
fof(wit_src_c3,   axiom, concept(witC)).
fof(wit_src_leq1, axiom, leq(witA, witB)).
fof(wit_src_leq2, axiom, leq(witA, witC)).
fof(wit_src_refl1,axiom, leq(witA, witA)).
fof(wit_src_refl2,axiom, leq(witB, witB)).
fof(wit_src_refl3,axiom, leq(witC, witC)).
fof(wit_src_una,  axiom, $distinct(witA, witB, witC))."""

_WIT_TGT_PARTIAL = """\
fof(wit_tgt_c1,   axiom, concept(tgtB)).
fof(wit_tgt_c2,   axiom, concept(tgtC)).
fof(wit_tgt_refl1,axiom, leq(tgtB, tgtB)).
fof(wit_tgt_refl2,axiom, leq(tgtC, tgtC)).
fof(wit_tgt_una,  axiom, $distinct(tgtB, tgtC))."""

_WIT_TGT_FULL = """\
fof(wit_full_c1,   axiom, concept(tgtA)).
fof(wit_full_c2,   axiom, concept(tgtB)).
fof(wit_full_c3,   axiom, concept(tgtC)).
fof(wit_full_leq1, axiom, leq(tgtA, tgtB)).
fof(wit_full_leq2, axiom, leq(tgtA, tgtC)).
fof(wit_full_refl1,axiom, leq(tgtA, tgtA)).
fof(wit_full_refl2,axiom, leq(tgtB, tgtB)).
fof(wit_full_refl3,axiom, leq(tgtC, tgtC)).
fof(wit_full_una,  axiom, $distinct(tgtA, tgtB, tgtC))."""

_2HOP_INC = [_GEO, _ISO, _ALIGN_DATA, _ODRL, _ALIGN_TH]
_3HOP_INC = _2HOP_INC  # same includes, different inline KBs

def multihop_adv() -> list[KBProblem]:
    return [

        # ── 2-hop ─────────────────────────────────────────────────────
        KBProblem(
            number=150, name="2hop-alignment-conflict",
            variant=1, category=_CAT, szs=SZS.COUNTER_SATISFIABLE,
            kbs=_2HOP_INC,
            inline_axioms=_SYNTH + "\n" + _ALIGN_ISO_SYNTH,
            conjecture_fof=(
                "fof(odrl150, conjecture,\n"
                "    ?[X]: ( in_denotation(X, zoneWest, isPartOf)\n"
                "          & in_denotation(X, zoneEast, isPartOf) ))."
            ),
                "fof(odrl150, conjecture,\n"
                "    ![X]: ~( in_denotation(X, zoneWest, isPartOf)\n"
                "           & in_denotation(X, zoneEast, isPartOf) ))."
            ),
            description="2-hop GEO→ISO→SYNTH: derives disj(zoneWest,zoneEast)",
            difficulty="Very Hard",
        ),

        KBProblem(
            number=151, name="2hop-alignment-compatible",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=_2HOP_INC,
            inline_axioms=_SYNTH + "\n" + _ALIGN_ISO_SYNTH,
            conjecture_fof=(
                "fof(odrl151, conjecture,\n"
                "    ?[X]: ( in_denotation(X, euZone, isPartOf)\n"
                "          & in_denotation(X, zoneWest, eq) ))."
            ),
            description="2-hop compatible: isPartOf(euZone) ∩ eq(zoneWest) ≠ ∅",
            difficulty="Medium",
        ),

        KBProblem(
            number=152, name="2hop-ablation-SYNTH-alone-unknown",
            variant=1, category=_CAT, szs=SZS.COUNTER_SATISFIABLE,
            kbs=[_ODRL],
            inline_axioms=_SYNTH,
            conjecture_fof=(
                "fof(odrl152, conjecture,\n"
                "    ?[X]: ( in_denotation(X, zoneWest, isPartOf)\n"
                "          & in_denotation(X, zoneEast, isPartOf) ))."
            ),
            description="Ablation: SYNTH alone → no disjointness → Unknown",
            difficulty="Hard",
        ),

        KBProblem(
            number=153, name="2hop-intermediate-hop1",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=_2HOP_INC, inline_axioms="",
            conjecture_fof="fof(odrl153, conjecture, disjoint(dE, pL)).",
            description="Hop 1 intermediate: derives disjoint(dE, pL)",
            difficulty="Medium",
        ),

        # ── 3-hop ─────────────────────────────────────────────────────
        KBProblem(
            number=154, name="3hop-alignment-conflict",
            variant=1, category=_CAT, szs=SZS.COUNTER_SATISFIABLE,
            kbs=_3HOP_INC,
            inline_axioms=_SYNTH + "\n" + _ALIGN_ISO_SYNTH + "\n" + _COMP + "\n" + _ALIGN_SYNTH_COMP,
            conjecture_fof=(
                "fof(odrl154, conjecture,\n"
                "    ?[X]: ( in_denotation(X, gdprFull, isPartOf)\n"
                "          & in_denotation(X, gdprPartial, isPartOf) ))."
            ),
                "fof(odrl154, conjecture,\n"
                "    ![X]: ~( in_denotation(X, gdprFull, isPartOf)\n"
                "           & in_denotation(X, gdprPartial, isPartOf) ))."
            ),
            description="3-hop GEO→ISO→SYNTH→COMP: derives disj(gdprFull,gdprPartial)",
            difficulty="Very Hard",
        ),

        KBProblem(
            number=155, name="3hop-alignment-compatible",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=_3HOP_INC,
            inline_axioms=_SYNTH + "\n" + _ALIGN_ISO_SYNTH + "\n" + _COMP + "\n" + _ALIGN_SYNTH_COMP,
            conjecture_fof=(
                "fof(odrl155, conjecture,\n"
                "    ?[X]: ( in_denotation(X, complianceScope, isPartOf)\n"
                "          & in_denotation(X, gdprFull, eq) ))."
            ),
            description="3-hop compatible: isPartOf(compScope) ∩ eq(gdprFull) ≠ ∅",
            difficulty="Medium",
        ),

        KBProblem(
            number=156, name="3hop-ablation-COMP-alone-unknown",
            variant=1, category=_CAT, szs=SZS.COUNTER_SATISFIABLE,
            kbs=[_ODRL],
            inline_axioms=_COMP,
            conjecture_fof=(
                "fof(odrl156, conjecture,\n"
                "    ?[X]: ( in_denotation(X, gdprFull, isPartOf)\n"
                "          & in_denotation(X, gdprPartial, isPartOf) ))."
            ),
            description="Ablation: COMP alone → no disjointness → Unknown",
            difficulty="Hard",
        ),

        KBProblem(
            number=157, name="3hop-intermediate-hop2",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=_3HOP_INC,
            inline_axioms=_SYNTH + "\n" + _ALIGN_ISO_SYNTH,
            conjecture_fof="fof(odrl157, conjecture, disjoint(zoneWest, zoneEast)).",
            description="Hop 2 intermediate: derives disjoint(zoneWest, zoneEast)",
            difficulty="Hard",
        ),

        # ── Proposition 2(2) witness loss ─────────────────────────────
        KBProblem(
            number=158, name="prop2-baseline-compatible-source",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_ODRL],
            inline_axioms=_WIT_SRC,
            conjecture_fof=(
                "fof(odrl158, conjecture,\n"
                "    ?[X]: ( in_denotation(X, witB, isA)\n"
                "          & in_denotation(X, witC, isA) ))."
            ),
            description="Prop 2(2) baseline: witA witnesses isA(witB)∩isA(witC)≠∅",
            difficulty="Easy",
        ),

        KBProblem(
            number=159, name="prop2-bug-fabricated-conflict-partial-align",
            variant=1, category=_CAT, szs=SZS.COUNTER_SATISFIABLE,
            kbs=[_ODRL],
            inline_axioms=_WIT_TGT_PARTIAL,
            conjecture_fof=(
                "fof(odrl159, conjecture,\n"
                "    ?[X]: ( in_denotation(X, tgtB, isA)\n"
                "          & in_denotation(X, tgtC, isA) ))."
            ),
                "fof(odrl159, conjecture,\n"
                "    ![X]: ~( in_denotation(X, tgtB, isA)\n"
                "           & in_denotation(X, tgtC, isA) ))."
            ),
            description="Prop 2(2) BUG: partial alignment loses witA → fabricated Conflict",
            difficulty="Very Hard",
        ),

        KBProblem(
            number=158, name="prop2-fix-downward-closed-alignment",
            variant=2, category=_CAT, szs=SZS.THEOREM,
            kbs=[_ODRL],
            inline_axioms=_WIT_TGT_FULL,
            conjecture_fof=(
                "fof(odrl158b, conjecture,\n"
                "    ?[X]: ( in_denotation(X, tgtB, isA)\n"
                "          & in_denotation(X, tgtC, isA) ))."
            ),
            description="Prop 2(2) FIX: downward-closed alignment preserves Compatible",
            difficulty="Hard",
        ),
    ]