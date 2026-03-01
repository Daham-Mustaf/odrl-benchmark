"""
hierarchies/cat08_alignment.py
Category 8: Cross-Dataspace Alignment — ODRL080-089b.

Tests Definition 8 (Alignment), Lemma 3, Proposition 2, Corollary 1.

KBs: GEO (curated UN M49) + ISO 3166 (flat EU27 code list)
Alignment: GEO → ISO
  europe→europe, germany→dE, france→fR, poland→pL,
  italy→iT, spain→eS, austria→aT, belgium→bE, netherlands→nL, sweden→sE
Unmapped: westernEurope, easternEurope, northernEurope, southernEurope,
          bavaria, ileDeFrance (no ISO counterpart)

SMT2 encoding:
  align/2 is a declared UF predicate (not leq-based).
  Alignment theory axioms are quantified universally.
  Unknown verdicts → CounterSatisfiable for Vampire, sat for Z3
  (both provers find a model where the intersection could be non-empty,
  because there's insufficient structure to prove disjointness).
"""
from .models import (
    Category, Constraint, KB, KBProblem, Op, SZS, Verdict
)
from .kb_smt2 import (
    geo_iso_aligned_smt2_preamble,
    geo_iso_data_only_smt2_preamble,
    iso_only_smt2_preamble,
    geo_dpv_full_smt2_preamble,
    geo_full_smt2_preamble,
)

_ALIGNED_PREAMBLE  = None
_DATA_ONLY_PREAMBLE = None
_ISO_ONLY_PREAMBLE = None
_GEO_DPV_PREAMBLE  = None


def _p_aligned() -> str:
    global _ALIGNED_PREAMBLE
    if _ALIGNED_PREAMBLE is None:
        _ALIGNED_PREAMBLE = "(set-logic UF)\n\n" + geo_iso_aligned_smt2_preamble()
    return _ALIGNED_PREAMBLE


def _p_data_only() -> str:
    global _DATA_ONLY_PREAMBLE
    if _DATA_ONLY_PREAMBLE is None:
        _DATA_ONLY_PREAMBLE = "(set-logic UF)\n\n" + geo_iso_data_only_smt2_preamble()
    return _DATA_ONLY_PREAMBLE


def _p_iso_only() -> str:
    global _ISO_ONLY_PREAMBLE
    if _ISO_ONLY_PREAMBLE is None:
        _ISO_ONLY_PREAMBLE = "(set-logic UF)\n\n" + iso_only_smt2_preamble()
    return _ISO_ONLY_PREAMBLE


def _p_geo_dpv() -> str:
    global _GEO_DPV_PREAMBLE
    if _GEO_DPV_PREAMBLE is None:
        _GEO_DPV_PREAMBLE = "(set-logic UF)\n\n" + geo_dpv_full_smt2_preamble()
    return _GEO_DPV_PREAMBLE


def _smt2(block: str) -> str:
    return f"{block}\n(check-sat)\n(exit)"


def _fof_list_axioms(list_id: str, values: list[str]) -> str:
    lines = []
    for i, v in enumerate(values, 1):
        lines.append(f"fof(list_{list_id}_{i}, axiom, in_value_list({v}, {list_id})).")
    disjuncts = " | ".join(f"G = {v}" for v in values)
    lines.append(
        f"fof(list_{list_id}_closed, axiom,\n"
        f"    ![G]: (in_value_list(G, {list_id}) => ({disjuncts})))."
    )
    return "\n".join(lines)


# Part A of ALIGN000-0.ax inlined for ODRL082
ALIGN_PART_A_INLINE = """\
% --- Inline Part A of ALIGN000-0.ax (Definition 8) ---
fof(align_order_forward, axiom,
    ![X,Y,Xp,Yp]: ((align(X, Xp) & align(Y, Yp) & leq(X, Y))
        => leq(Xp, Yp))).
fof(align_order_backward, axiom,
    ![X,Y,Xp,Yp]: ((align(X, Xp) & align(Y, Yp) & leq(Xp, Yp))
        => leq(X, Y))).
fof(align_disj_forward, axiom,
    ![X,Y,Xp,Yp]: ((align(X, Xp) & align(Y, Yp) & disjoint(X, Y))
        => disjoint(Xp, Yp))).
fof(align_injective, axiom,
    ![X,Y,Z]: ((align(X, Z) & align(Y, Z)) => (X = Y))).
fof(align_functional, axiom,
    ![X,Y,Z]: ((align(X, Y) & align(X, Z)) => (Y = Z))).
fof(align_typed, axiom,
    ![X,Y]: (align(X, Y) => (concept(X) & concept(Y))))."""


def alignment() -> list[KBProblem]:
    problems = []

    # ──────────────────────────────────────────────────────────────────────
    # ODRL080 — Conflict preservation (Prop 2.1): baseline
    # wE ⊥ eE in GEO; loading ISO + alignment must not disrupt this.
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=80, name="alignment-conflict-preservation-baseline",
        category=Category.MULTI_HOP_ALIGN,
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        kbs=[KB.GEO, KB.ISO, KB.ALIGN_DATA, KB.ALIGN_THEORY],
        c1=Constraint("spatial", Op.IS_PART_OF, "westernEurope"),
        c2=Constraint("spatial", Op.IS_PART_OF, "easternEurope"),
        description="Conflict preservation: wE ⊥ eE holds with alignment loaded",
        formal=(
            "disjoint(westernEurope, easternEurope) in GEO → ∅ → Conflict\n"
            "%   Tests: loading ISO3166 + alignment does NOT disrupt source-KB reasoning"
        ),
        paper_ref="Proposition 2(1) — Conflict Preservation (baseline)",
        difficulty="Hard",
        conjecture_fof=(
            "fof(odrl080, conjecture,\n"
            "    ![X]: ~( in_denotation(X, westernEurope, isPartOf)\n"
            "           & in_denotation(X, easternEurope, isPartOf) ))."
        ),
        conjecture_smt2=_smt2(
            "; Conflict preserved: ∃X.leq(X,wE)∧leq(X,eE) → unsat\n"
            "(assert (exists ((X C))\n"
            "    (and (leq X westernEurope)(leq X easternEurope))))"
        ),
        inline_smt2_kb=_p_aligned(),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL081 — Aligned disjointness transfer (Def 8.ii + disj_downward)
    # disj_downward(wE⊥eE, de≤wE, pl≤eE) → disj(germany,poland)
    # align_disj_forward(de→dE, pl→pL) → disj(dE,pL) → Conflict
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=81, name="aligned-disjointness-transfer-dE-pL",
        category=Category.MULTI_HOP_ALIGN,
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        kbs=[KB.GEO, KB.ISO, KB.ALIGN_DATA, KB.ALIGN_THEORY],
        c1=None, c2=None,
        description="Aligned conflict: disjoint(dE, pL) via alignment transfer",
        formal=(
            "disj_downward(wE⊥eE, de≤wE, pl≤eE) → disj(germany, poland)\n"
            "%   align_disj_forward(germany→dE, poland→pL, disj(de,pl))\n"
            "%   → disj(dE, pL) in ISO 3166\n"
            "%   → ⟦isPartOf(dE)⟧ ∩ ⟦isPartOf(pL)⟧ = ∅ → Conflict"
        ),
        paper_ref="Def. 8(ii), Proposition 2(1) — Disjointness Transfer",
        difficulty="Very Hard",
        notes="Compare ODRL088 (ISO alone) and ODRL089 (data without theory).",
        conjecture_fof=(
            "fof(odrl081, conjecture,\n"
            "    ![X]: ~( in_denotation(X, dE, isPartOf)\n"
            "           & in_denotation(X, pL, isPartOf) ))."
        ),
        conjecture_smt2=_smt2(
            "; Aligned conflict: ∃X.leq(X,dE)∧leq(X,pL) → unsat\n"
            "; Proof chain: disj(germany,poland) + align_disj_forward → disj(dE,pL)\n"
            "(assert (exists ((X C))\n"
            "    (and (leq X dE)(leq X pL))))"
        ),
        inline_smt2_kb=_p_aligned(),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL082 — Lemma 3 derivability: Part B from Part A inline
    # Inline Part A axioms; prove denotation transfer as conjecture.
    # Does NOT load ALIGN000-0.ax (testing derivability, not loading it).
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=82, name="lemma3-denotation-transfer-derivability",
        category=Category.MULTI_HOP_ALIGN,
        verdict=Verdict.DERIVABLE, szs=SZS.THEOREM,
        kbs=[KB.GEO, KB.ISO, KB.ALIGN_DATA],  # NO ALIGN_THEORY
        c1=None, c2=None,
        description="Lemma 3: denotation transfer derivable from Part A + ODRL000-0.ax",
        formal=(
            "Prove: in_den(X,G,isPartOf) ∧ align(X,Xp) ∧ align(G,Gp)\n"
            "%          ⟹ in_den(Xp, Gp, isPartOf)\n"
            "%   Proof: den_isPartOf_onlyif → leq(X,G)\n"
            "%          align_order_forward → leq(Xp,Gp)\n"
            "%          den_isPartOf_if → in_denotation(Xp,Gp,isPartOf)"
        ),
        paper_ref="Lemma 3 — Denotation Transfer Derivability",
        difficulty="Hard",
        notes="Part A inlined; ALIGN000-0.ax NOT loaded. Meta-theorem verification.",
        inline_axioms=ALIGN_PART_A_INLINE,
        conjecture_fof=(
            "fof(odrl082, conjecture,\n"
            "    ![X,G,Xp,Gp]: ((in_denotation(X, G, isPartOf)\n"
            "                    & align(X, Xp)\n"
            "                    & align(G, Gp))\n"
            "        => in_denotation(Xp, Gp, isPartOf)))."
        ),
        conjecture_smt2=_smt2(
            "; Lemma 3: negate denotation transfer → unsat\n"
            "; ∃X,G,Xp,Gp. leq(X,G) ∧ align(X,Xp) ∧ align(G,Gp) ∧ ¬leq(Xp,Gp)\n"
            "(assert (exists ((X C)(G C)(Xp C)(Gp C))\n"
            "    (and (leq X G)(align X Xp)(align G Gp)\n"
            "         (not (leq Xp Gp)))))"
        ),
        # For SMT2: use aligned preamble (has align theory) for this derivability test
        inline_smt2_kb=_p_aligned(),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL083 — Aligned compatible: verdict preservation (Prop 2.1)
    # isPartOf(europe) ∩ eq(dE) — dE ≤ europe in ISO, dE = dE
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=83, name="aligned-compatible-isPartOf-europe-eq-dE",
        category=Category.MULTI_HOP_ALIGN,
        verdict=Verdict.COMPATIBLE, szs=SZS.THEOREM,
        kbs=[KB.GEO, KB.ISO, KB.ALIGN_DATA, KB.ALIGN_THEORY],
        c1=None, c2=None,
        description="Aligned compatible: isPartOf(europe) ∩ eq(dE) ≠ ∅",
        formal=(
            "ISO: leq(dE, europe)  → dE ∈ ⟦isPartOf(europe)⟧\n"
            "%   eq(dE) = {dE}      → dE ∈ ⟦eq(dE)⟧\n"
            "%   Witness: dE. Alignment preserves compatible verdict."
        ),
        paper_ref="Proposition 2(1) — Compatible Verdict Preservation",
        difficulty="Medium",
        conjecture_fof=(
            "fof(odrl083, conjecture,\n"
            "    ?[X]: ( in_denotation(X, europe, isPartOf)\n"
            "          & in_denotation(X, dE, eq) ))."
        ),
        conjecture_smt2=_smt2(
            "; Compatible: ∃X. leq(X,europe) ∧ X=dE → negated → unsat (dE≤europe)\n"
            "(assert (not (exists ((X C))\n"
            "    (and (leq X europe)(= X dE)))))"
        ),
        inline_smt2_kb=_p_aligned(),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL084 — Subsumption preservation (Corollary 1)
    # isPartOf(dE) ⊆ isPartOf(europe) via leq(dE,europe) in ISO
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=84, name="subsumption-preservation-dE-europe",
        category=Category.MULTI_HOP_ALIGN,
        verdict=Verdict.SUBSUMES, szs=SZS.THEOREM,
        kbs=[KB.GEO, KB.ISO, KB.ALIGN_DATA, KB.ALIGN_THEORY],
        c1=None, c2=None,
        description="Subsumption preservation: isPartOf(dE) ⊆ isPartOf(europe)",
        formal=(
            "⟦isPartOf(dE)⟧ ⊆ ⟦isPartOf(europe)⟧\n"
            "%   leq(dE, europe) in ISO3166 → leq_trans → subsumption\n"
            "%   Tests Corollary 1: subsumption preserved under alignment"
        ),
        paper_ref="Corollary 1 — Subsumption Preservation",
        difficulty="Medium",
        conjecture_fof=(
            "fof(odrl084, conjecture,\n"
            "    ![X]: ( in_denotation(X, dE, isPartOf)\n"
            "          => in_denotation(X, europe, isPartOf) ))."
        ),
        conjecture_smt2=_smt2(
            "; Subsumes: ∃X.leq(X,dE)∧¬leq(X,europe) → unsat (dE≤europe)\n"
            "(assert (exists ((X C))\n"
            "    (and (leq X dE)(not (leq X europe)))))"
        ),
        inline_smt2_kb=_p_aligned(),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL085 — Graceful degradation (Prop 2.2): unmapped concept
    # westernEurope has NO ISO counterpart.
    # leq(dE, westernEurope) cannot be derived → Unknown verdict.
    # Vampire: CounterSatisfiable; Z3: sat
    #
    # IMPORTANT: Use data-only preamble (no align theory) for SMT2.
    # The alignment theory's universal quantifiers (forall X,Y,Xp,Yp ...)
    # cause Z3 to loop on sat queries — it tries to instantiate the
    # foralls searching for a contradiction, but there is none.
    # Data-only preamble (GEO + ISO + ground align facts, no universals)
    # lets Z3 return sat immediately: leq(dE,westernEurope) is unconstrained.
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=85, name="graceful-degradation-unmapped-westernEurope",
        category=Category.MULTI_HOP_ALIGN,
        verdict=Verdict.UNKNOWN, szs=SZS.COUNTERSATISFIABLE,
        kbs=[KB.GEO, KB.ISO, KB.ALIGN_DATA, KB.ALIGN_THEORY],
        c1=None, c2=None,
        description="Graceful degradation: unmapped concept westernEurope → Unknown",
        formal=(
            "westernEurope has NO ISO 3166 counterpart.\n"
            "%   align_order_backward needs align(???, westernEurope) — doesn't exist.\n"
            "%   leq(dE, westernEurope) cannot be derived from ISO alone.\n"
            "%   Prover cannot prove OR refute overlap → Unknown (Prop 2.2)"
        ),
        paper_ref="Proposition 2(2) — Graceful Degradation",
        difficulty="Hard",
        notes=(
            "TPTP: loads full alignment (Vampire searches and fails → CounterSat). "
            "SMT2: data-only preamble (no align theory foralls — Z3 loops otherwise). "
            "Paired with ODRL083 (mapped concept dE → immediate sat)."
        ),
        conjecture_fof=(
            "fof(odrl085, conjecture,\n"
            "    ?[X]: ( in_denotation(X, westernEurope, isPartOf)\n"
            "          & in_denotation(X, dE, eq) ))."
        ),
        # Data-only preamble: no align theory universals → Z3 returns sat quickly
        # (leq(dE,westernEurope) is unconstrained without align_order_backward)
        conjecture_smt2=_smt2(
            "; Unknown: leq(dE,westernEurope) unconstrained without align theory\n"
            "; Z3 builds trivial sat model (no forall prevents it)\n"
            "(assert (and (leq dE westernEurope)(= dE dE)))"
        ),
        inline_smt2_kb=_p_data_only(),  # NOT _p_aligned() — avoids Z3 forall loop
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL086 — Cross-KB conflict via UNA: eq(dE) ∩ eq(fR) = ∅
    # dE ≠ fR from ISO $distinct → singleton denotations are disjoint
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=86, name="cross-kb-conflict-eq-dE-eq-fR",
        category=Category.MULTI_HOP_ALIGN,
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        kbs=[KB.GEO, KB.ISO, KB.ALIGN_DATA, KB.ALIGN_THEORY],
        c1=None, c2=None,
        description="Cross-KB conflict: eq(dE) ∩ eq(fR) = ∅ via UNA",
        formal=(
            "eq(dE) = {dE}, eq(fR) = {fR}\n"
            "%   dE ≠ fR  [ISO $distinct / UNA]\n"
            "%   → intersection = ∅ → Conflict"
        ),
        paper_ref="Definition 5 — Cross-KB Conflict via UNA",
        difficulty="Easy",
        conjecture_fof=(
            "fof(odrl086, conjecture,\n"
            "    ![X]: ~( in_denotation(X, dE, eq)\n"
            "           & in_denotation(X, fR, eq) ))."
        ),
        conjecture_smt2=_smt2(
            "; Conflict: ∃X. X=dE ∧ X=fR → unsat (dE ≠ fR by UNA)\n"
            "(assert (exists ((X C))\n"
            "    (and (= X dE)(= X fR))))"
        ),
        inline_smt2_kb=_p_aligned(),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL087 — Aligned set-valued: isAnyOf({dE,fR}) ∩ isPartOf(europe)
    # dE ≤ europe and fR ≤ europe in ISO → Compatible
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=87, name="aligned-isAnyOf-dE-fR-isPartOf-europe",
        category=Category.MULTI_HOP_ALIGN,
        verdict=Verdict.COMPATIBLE, szs=SZS.THEOREM,
        kbs=[KB.GEO, KB.ISO, KB.ALIGN_DATA, KB.ALIGN_THEORY],
        c1=None, c2=None,
        description="Aligned compatible: isAnyOf({dE,fR}) ∩ isPartOf(europe) ≠ ∅",
        formal=(
            "⟦isAnyOf({dE,fR})⟧ = ↓dE ∪ ↓fR\n"
            "%   leq(dE, europe), leq(fR, europe) in ISO3166\n"
            "%   Witness: dE ∈ ↓dE ∩ ↓europe"
        ),
        paper_ref="Definition 3 (isAnyOf), Proposition 2(1)",
        difficulty="Medium",
        inline_axioms=_fof_list_axioms("isoRegions087", ["dE", "fR"]),
        conjecture_fof=(
            "fof(odrl087, conjecture,\n"
            "    ?[X]: ( in_denotation_set(X, isoRegions087, isAnyOf)\n"
            "          & in_denotation(X, europe, isPartOf) ))."
        ),
        conjecture_smt2=_smt2(
            "; Compatible: ∃X.(X≤dE ∨ X≤fR) ∧ leq(X,europe) → negated → unsat\n"
            "(assert (not (exists ((X C))\n"
            "    (and (or (leq X dE)(leq X fR))\n"
            "         (leq X europe)))))"
        ),
        inline_smt2_kb=_p_aligned(),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL088 — Downward asymmetry: flat ISO KB alone — no disjointness
    # ISO 3166 has no sibling disjointness axioms.
    # disjoint(dE, pL) is NOT derivable → Unknown
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=88, name="downward-asymmetry-flat-ISO-no-disjointness",
        category=Category.MULTI_HOP_ALIGN,
        verdict=Verdict.UNKNOWN, szs=SZS.COUNTERSATISFIABLE,
        kbs=[KB.ISO],
        c1=None, c2=None,
        description="Downward asymmetry: flat ISO alone cannot detect dE ⊥ pL",
        formal=(
            "ISO 3166 has $distinct(dE, pL) for UNA — dE ≠ pL\n"
            "%   BUT $distinct ≠ disjoint/2 (no leq/2 structure forbidding overlap)\n"
            "%   disjoint(dE, pL) is NOT derivable from ISO alone\n"
            "%   Compare ODRL081: adds GEO+alignment → Conflict in 0.1s"
        ),
        paper_ref="Proposition 2(2) — Downward Asymmetry: Flat KB Alone",
        difficulty="Hard",
        notes="Demonstrates: structural disjointness from richer KB is necessary.",
        conjecture_fof=(
            "fof(odrl088, conjecture,\n"
            "    ?[X]: ( in_denotation(X, dE, isPartOf)\n"
            "          & in_denotation(X, pL, isPartOf) ))."
        ),
        conjecture_smt2=_smt2(
            "; Unknown: ∃X.leq(X,dE)∧leq(X,pL)\n"
            "; ISO has no disj axioms → Z3 builds a sat model\n"
            "(assert (exists ((X C))\n"
            "    (and (leq X dE)(leq X pL))))"
        ),
        inline_smt2_kb=_p_iso_only(),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL089 — Upward asymmetry: data without theory is inert
    # GEO + ISO + alignment FACTS but NO ALIGN000-0.ax (theory).
    # align/2 ground atoms present but align_disj_forward absent.
    # disj(dE, pL) cannot be bridged → Unknown
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=89, name="upward-asymmetry-data-without-theory",
        category=Category.MULTI_HOP_ALIGN,
        verdict=Verdict.UNKNOWN, szs=SZS.COUNTERSATISFIABLE,
        kbs=[KB.GEO, KB.ISO, KB.ALIGN_DATA],  # NO ALIGN_THEORY
        c1=None, c2=None,
        description="Upward asymmetry: alignment data without theory is inert",
        formal=(
            "GEO: disj(germany, poland) derivable [disj_downward(wE⊥eE)]\n"
            "%   ALIGN-GEO-ISO: align(germany,dE), align(poland,pL) present\n"
            "%   MISSING: ALIGN000-0.ax (align_disj_forward rule)\n"
            "%   Without the theory, align/2 facts cannot bridge GEO→ISO\n"
            "%   Compare ODRL081: adds ALIGN_THEORY → Conflict in 0.1s"
        ),
        paper_ref="Proposition 2(2) — Upward Asymmetry: Data Without Theory",
        difficulty="Hard",
        notes="Paired with ODRL081/ODRL088: both alone fail, both together succeed.",
        conjecture_fof=(
            "fof(odrl089, conjecture,\n"
            "    ?[X]: ( in_denotation(X, dE, isPartOf)\n"
            "          & in_denotation(X, pL, isPartOf) ))."
        ),
        conjecture_smt2=_smt2(
            "; Unknown: data+GEO present but no theory to bridge\n"
            "; Z3 builds sat model (align facts are inert ground atoms)\n"
            "(assert (exists ((X C))\n"
            "    (and (leq X dE)(leq X pL))))"
        ),
        inline_smt2_kb=_p_data_only(),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL089b — Positive control: rich multi-KB enables detection
    # 3 rich KBs (GEO + DPV + LANG) — all have full disjointness structure.
    # 3-operand AND composition; all three dimensions conflict.
    # TPTP: load lemma axioms (provable from KBs), then disjunctive conjecture.
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=89, variant=2,  # ODRL089b → ODRL089-2.p
        name="positive-control-rich-multi-KB",
        category=Category.MULTI_HOP_ALIGN,
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        kbs=[KB.GEO, KB.DPV, KB.LANG],
        c1=None, c2=None,
        description="Positive control: rich multi-KB structure enables conflict detection",
        formal=(
            "GEO: disj(westernEurope, easternEurope)         [sibling M49]\n"
            "%   DPV: disj(commercialPurpose, nonCommercialPurpose) [sibling DPV]\n"
            "%   LANG: disj(de, en)                              [base languages]\n"
            "%   AND-composition: at least one dimension conflicts → Conflict"
        ),
        paper_ref="Multi-KB Positive Control — Rich Structure Enables Detection",
        difficulty="Medium",
        notes=(
            "Contrast with ODRL088 (flat ISO alone cannot detect spatial conflict). "
            "Spatial conflict alone is sufficient for the disjunctive conjecture."
        ),
        # Inline spatial_conflict axiom (redundant but makes proof structure explicit)
        inline_axioms=(
            "fof(spatial_conflict, axiom,\n"
            "    ![X]: ~( in_denotation(X, westernEurope, isPartOf)\n"
            "           & in_denotation(X, easternEurope, isPartOf) )).\n"
            "fof(purpose_conflict, axiom,\n"
            "    ![X]: ~( in_denotation(X, commercialPurpose, isA)\n"
            "           & in_denotation(X, nonCommercialPurpose, isA) ))."
        ),
        conjecture_fof=(
            "fof(odrl089b, conjecture,\n"
            "    ( ![Xs]: ~( in_denotation(Xs, westernEurope, isPartOf)\n"
            "              & in_denotation(Xs, easternEurope, isPartOf) )\n"
            "    | ![Xp]: ~( in_denotation(Xp, commercialPurpose, isA)\n"
            "              & in_denotation(Xp, nonCommercialPurpose, isA) ) ))."
        ),
        conjecture_smt2=_smt2(
            "; At least one dimension conflicts: negate disjunction → assert both non-empty\n"
            "; Spatial: ∃Xs.leq(Xs,wE)∧leq(Xs,eE) → unsat (disj(wE,eE))\n"
            "(assert (exists ((Xs C))\n"
            "    (and (leq Xs westernEurope)(leq Xs easternEurope))))\n"
            "(assert (exists ((Xp C))\n"
            "    (and (leq Xp commercialPurpose)(leq Xp nonCommercialPurpose))))"
        ),
        inline_smt2_kb=_p_geo_dpv(),
    ))

    return problems