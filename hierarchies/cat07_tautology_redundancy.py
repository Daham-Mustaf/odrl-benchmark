"""
hierarchies/cat07_tautology_redundancy.py
Category 7: Tautology / Redundancy / Refinement Conflict — ODRL060-069.

Sub-groups:
  6A Tautology Detection  (060-062)  — is ⟦c⟧ = C?
  6B Redundancy Detection (063-065)  — is c1 ⊆ c2 under conjunction?
  6C Refinement Conflict  (066-069)  — partial overlap (c1 ⊄ c2 ∧ c2 ⊄ c1 ∧ c1∩c2 ≠ ∅)

SMT2 encoding notes:
  Tautology uses concept/1 predicate with closed-world closure axiom.
  ∀X.concept(X)⇒leq(X,G) is expressed as: negate the existential,
  ∃X.concept(X)∧¬leq(X,G) → expect unsat (Theorem) or sat (CounterSat).

  Partial-overlap uses three simultaneous existentials:
    X: c1 ∧ c2    (intersection non-empty)
    Y: c1 ∧ ¬c2   (c1 not subsumed by c2)
    Z: c2 ∧ ¬c1   (c2 not subsumed by c1)
  All three must hold — negate the conjunction → expect unsat.
"""
from .models import (
    Category, Constraint, KB, KBProblem, Op, SZS, Verdict
)
from .kb_smt2 import geo_full_smt2_preamble, GEO_CONCEPTS

_GEO_PREAMBLE = None


def _preamble() -> str:
    global _GEO_PREAMBLE
    if _GEO_PREAMBLE is None:
        _GEO_PREAMBLE = "(set-logic UF)\n\n" + geo_full_smt2_preamble()
    return _GEO_PREAMBLE


def _ground_fof_conjunction(template: str, concepts: list[str]) -> str:
    """
    Ground conjunction: template.format(c) for each c in concepts.
    template uses {} as placeholder.  Returns multi-line FOF.
    """
    atoms = [template.format(c) for c in concepts]
    # 4 atoms per line
    chunks = []
    for i in range(0, len(atoms), 4):
        chunks.append(" & ".join(atoms[i:i+4]))
    return "( " + "\n    & ".join(chunks) + " )"


def _ground_smt2_conjunction(template: str, concepts: list[str]) -> str:
    """SMT2 (and t1 t2 ...) over all concepts."""
    terms = [template.format(c) for c in concepts]
    return "(and\n    " + "\n    ".join(terms) + ")"


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


def _ttl_single(policy, rule, op, val):
    return (
        f"%   ex:{policy} a odrl:Set ;\n"
        f"%     odrl:{rule} [ odrl:action odrl:use ;\n"
        f"%       odrl:constraint [ odrl:leftOperand odrl:spatial ;\n"
        f"%         odrl:operator odrl:{op} ; odrl:rightOperand geo:{val} ] ] ."
    )


def tautology_redundancy() -> list[KBProblem]:
    problems = []

    # ══════════════════════════════════════════════════════════════════════
    # 6A: TAUTOLOGY DETECTION (060-062)
    # Ground encoding: no concept/1 predicate — enumerate all 26 KB concepts
    # directly as a conjunction. This is sound and complete for any prover,
    # because the KB is finite and all constants are named.
    # ══════════════════════════════════════════════════════════════════════

    # ──────────────────────────────────────────────────────────────────────
    # ODRL060 — Tautological: isPartOf(europe) = C
    # Every concept in GEO KB satisfies leq(X, europe) via transitivity.
    # Ground encoding: prove in_denotation(c, europe, isPartOf) for all 26.
    # ──────────────────────────────────────────────────────────────────────
    fof_ground_060 = _ground_fof_conjunction(
        "in_denotation({}, europe, isPartOf)", GEO_CONCEPTS
    )
    smt2_ground_060 = _ground_smt2_conjunction("(leq {} europe)", GEO_CONCEPTS)

    problems.append(KBProblem(
        number=60, name="tautology-isPartOf-europe",
        category=Category.SPATIAL,
        verdict=Verdict.TAUTOLOGICAL, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=None, c2=None,
        description="Tautology: isPartOf(europe) = C (root covers all concepts)",
        formal=(
            "⟦isPartOf(europe)⟧ = {X ∈ C | leq(X, europe)} = C\n"
            "%   europe is the root of GEO KB (26 concepts, no world above)\n"
            "%   Ground encoding: prove leq(c, europe) for each of the 26 named concepts\n"
            "%   Chain: country → sub-region → europe by transitivity"
        ),
        paper_ref="Tautology Detection",
        difficulty="Easy",
        notes=(
            "Ground conjunction over all 26 GEO concepts. "
            "No concept/1 predicate: open-world quantification is unsound for tautology."
        ),
        policy_ttl=(
            "%   c: [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:europe ] ."
        ),
        conjecture_fof=f"fof(odrl060, conjecture,\n    {fof_ground_060}).",
        # SMT2: negate the conjunction — if any one fails → sat; all succeed → unsat
        conjecture_smt2=(
            f"; Tautology: negate ground conjunction → unsat (all 26 concepts ≤ europe)\n"
            f"(assert (not\n    {smt2_ground_060}))\n"
            f"(check-sat)\n(exit)"
        ),
        inline_smt2_kb=_preamble(),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL061 — Non-Tautological: isPartOf(westernEurope) ⊂ C
    # Counterexample: poland (leq(poland, easternEurope), ¬leq(poland, wE))
    # Ground encoding: prove ¬in_denotation(poland, westernEurope, isPartOf)
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=61, name="non-tautology-isPartOf-westernEurope",
        category=Category.SPATIAL,
        verdict=Verdict.CONSISTENT, szs=SZS.COUNTERSATISFIABLE,
        kbs=[KB.GEO],
        c1=None, c2=None,
        description="Non-tautological: isPartOf(westernEurope) ⊂ C",
        formal=(
            "⟦isPartOf(wE)⟧ = ↓wE = {wE, austria, belgium, france, germany,\n"
            "%   liechtenstein, luxembourg, monaco, netherlands, switzerland}  (10 of 26)\n"
            "%   Counterexample: poland → leq(poland, easternEurope), ¬leq(poland, wE)"
        ),
        paper_ref="Tautology Detection",
        difficulty="Easy",
        notes="Ground witness: poland not in ↓wE. Vampire skipped (CounterSat → Z3 only).",
        policy_ttl=(
            "%   c: [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:westernEurope ] ."
        ),
        # Provide ground counterexample witness directly
        conjecture_fof=(
            "fof(odrl061, conjecture,\n"
            "    ~in_denotation(poland, westernEurope, isPartOf))."
        ),
        conjecture_smt2=(
            "; Non-tautological: poland ∉ ↓wE → ¬leq(poland, westernEurope) → sat\n"
            "(assert (not (leq poland westernEurope)))\n"
            "(check-sat)\n(exit)"
        ),
        inline_smt2_kb=_preamble(),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL062 — Non-Tautological: hasPart(europe) = {europe} ≠ C
    # Counterexample: germany — leq(europe, germany) is not derivable.
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=62, name="non-tautology-hasPart-europe",
        category=Category.SPATIAL,
        verdict=Verdict.CONSISTENT, szs=SZS.COUNTERSATISFIABLE,
        kbs=[KB.GEO],
        c1=None, c2=None,
        description="Non-tautological: hasPart(europe) = {europe} ≠ C",
        formal=(
            "⟦hasPart(europe)⟧ = {X ∈ C | leq(europe, X)} = {europe}  [only via reflexivity]\n"
            "%   europe is maximal (root) — no leq(europe, X) except X=europe\n"
            "%   Counterexample: germany — leq(europe, germany) not in KB"
        ),
        paper_ref="Tautology Detection (hasPart root)",
        difficulty="Easy",
        notes=(
            "Contrast with ODRL060: hasPart at root has smallest denotation (1 element). "
            "isPartOf at root has largest (all 26). Vampire skipped (CounterSat → Z3 only)."
        ),
        policy_ttl=(
            "%   c: [ odrl:operator odrl:hasPart ; odrl:rightOperand geo:europe ] ."
        ),
        conjecture_fof=(
            "fof(odrl062, conjecture,\n"
            "    ~in_denotation(germany, europe, hasPart))."
        ),
        conjecture_smt2=(
            "; Non-tautological: germany ∉ hasPart(europe) → ¬leq(europe,germany) → sat\n"
            "(assert (not (leq europe germany)))\n"
            "(check-sat)\n(exit)"
        ),
        inline_smt2_kb=_preamble(),
    ))

    # ══════════════════════════════════════════════════════════════════════
    # 6B: REDUNDANCY DETECTION (063-065)
    # ══════════════════════════════════════════════════════════════════════

    # ──────────────────────────────────────────────────────────────────────
    # ODRL063 — Redundant: isPartOf(europe) redundant in ∧ with isPartOf(germany)
    # isPartOf(germany) ⊆ isPartOf(europe) → europe constraint adds nothing
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=63, name="redundancy-isPartOf-germany-implies-isPartOf-europe",
        category=Category.SPATIAL,
        verdict=Verdict.DERIVABLE, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.IS_PART_OF, "germany"),
        c2=Constraint("spatial", Op.IS_PART_OF, "europe"),
        description="Redundancy: isPartOf(europe) redundant under ∧ with isPartOf(germany)",
        formal=(
            "⟦isPartOf(germany)⟧ ⊆ ⟦isPartOf(europe)⟧\n"
            "%   Chain: leq(X,germany) → leq(germany,wE) → leq(wE,europe) → leq(X,europe)\n"
            "%   → the europe constraint adds no restriction under conjunction\n"
            "%   The STRICTER constraint makes the WEAKER one redundant"
        ),
        paper_ref="Redundancy Detection (intra-rule ∧)",
        difficulty="Medium",
        policy_ttl=(
            "%   ex:rule a odrl:Permission ; odrl:action odrl:use ;\n"
            "%     odrl:constraint [ odrl:operator odrl:isPartOf ;"
            " odrl:rightOperand geo:germany ] ;\n"
            "%     odrl:constraint [ odrl:operator odrl:isPartOf ;"
            " odrl:rightOperand geo:europe ] ."
        ),
        conjecture_fof=(
            "fof(odrl063, conjecture,\n"
            "    ![X]: ( in_denotation(X, germany, isPartOf)\n"
            "          => in_denotation(X, europe, isPartOf) ))."
        ),
        conjecture_smt2=_smt2(
            "; Redundant: ∀X.leq(X,germany) → leq(X,europe)\n"
            "; Negated: ∃X.leq(X,germany) ∧ ¬leq(X,europe)\n"
            "(assert (exists ((X C))\n"
            "    (and (leq X germany)(not (leq X europe)))))"
        ),
        inline_smt2_kb=_preamble(),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL064 — Redundant: isAnyOf({germany,france}) ⊆ isPartOf(westernEurope)
    # ↓germany ∪ ↓france ⊆ ↓wE because de ≤ wE and fr ≤ wE
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=64, name="redundancy-isAnyOf-de-fr-subset-isPartOf-wE",
        category=Category.SPATIAL,
        verdict=Verdict.DERIVABLE, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=None, c2=None,
        description="Redundancy: isAnyOf({germany,france}) ⊆ isPartOf(westernEurope)",
        formal=(
            "⟦isAnyOf({de,fr})⟧ = ↓germany ∪ ↓france\n"
            "%   leq(germany,wE) → ↓germany ⊆ ↓wE\n"
            "%   leq(france,wE)  → ↓france  ⊆ ↓wE\n"
            "%   → isAnyOf({de,fr}) ⊆ isPartOf(wE) → wE constraint redundant"
        ),
        paper_ref="Redundancy Detection (set-valued)",
        difficulty="Medium",
        policy_ttl=(
            "%   ex:rule a odrl:Permission ;\n"
            "%     odrl:constraint [ odrl:operator odrl:isAnyOf ;\n"
            "%       odrl:rightOperand ( geo:germany geo:france ) ] ;\n"
            "%     odrl:constraint [ odrl:operator odrl:isPartOf ;\n"
            "%       odrl:rightOperand geo:westernEurope ] ."
        ),
        inline_axioms=_fof_list_axioms("anyList064", ["germany", "france"]),
        conjecture_fof=(
            "fof(odrl064, conjecture,\n"
            "    ![X]: ( in_denotation_set(X, anyList064, isAnyOf)\n"
            "          => in_denotation(X, westernEurope, isPartOf) ))."
        ),
        conjecture_smt2=_smt2(
            "; Redundant: ∀X.(leq(X,de) ∨ leq(X,fr)) → leq(X,wE)\n"
            "; Negated: ∃X.(leq(X,de) ∨ leq(X,fr)) ∧ ¬leq(X,wE)\n"
            "(assert (exists ((X C))\n"
            "    (and (or (leq X germany)(leq X france))\n"
            "         (not (leq X westernEurope)))))"
        ),
        inline_smt2_kb=_preamble(),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL065 — Non-Redundant: isPartOf(europe) ⊄ neq(germany)
    # germany witnesses: germany ∈ ⟦isPartOf(europe)⟧ but germany ∉ ⟦neq(germany)⟧
    # neq genuinely restricts the rule
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=65, name="non-redundant-isPartOf-europe-neq-germany",
        category=Category.SPATIAL,
        verdict=Verdict.REFUTED, szs=SZS.COUNTERSATISFIABLE,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.IS_PART_OF, "europe"),
        c2=Constraint("spatial", Op.NEQ, "germany"),
        description="Non-redundant: isPartOf(europe) ⊄ neq(germany)",
        formal=(
            "⟦isPartOf(europe)⟧ ⊄ ⟦neq(germany)⟧\n"
            "%   Counterexample: germany\n"
            "%     leq(germany, europe)  → germany ∈ ⟦isPartOf(europe)⟧\n"
            "%     germany = germany     → germany ∉ ⟦neq(germany)⟧\n"
            "%   → neq(germany) genuinely restricts (removes germany from scope)"
        ),
        paper_ref="Redundancy Refuted",
        difficulty="Medium",
        notes="flip_conj: find X ∈ isPartOf(europe) but X ∉ neq(germany). germany witnesses.",
        policy_ttl=(
            "%   ex:rule a odrl:Permission ;\n"
            "%     odrl:constraint [ odrl:operator odrl:isPartOf ;"
            " odrl:rightOperand geo:europe ] ;\n"
            "%     odrl:constraint [ odrl:operator odrl:neq ;"
            " odrl:rightOperand geo:germany ] ."
        ),
        conjecture_fof=(
            "fof(odrl065, conjecture,\n"
            "    ?[X]: ( in_denotation(X, europe, isPartOf)\n"
            "          & ~in_denotation(X, germany, neq) ))."
        ),
        conjecture_smt2=_smt2(
            "; Non-redundant: ∃X.leq(X,europe) ∧ X=germany → sat\n"
            "(assert (exists ((X C))\n"
            "    (and (leq X europe)(= X germany))))"
        ),
        inline_smt2_kb=_preamble(),
    ))

    # ══════════════════════════════════════════════════════════════════════
    # 6C: REFINEMENT CONFLICT / PARTIAL OVERLAP (066-069)
    # Pattern: X∈(c1∩c2) ∧ Y∈(c1\c2) ∧ Z∈(c2\c1)
    # All three hold → partial overlap (modification conflict)
    # ══════════════════════════════════════════════════════════════════════

    # ──────────────────────────────────────────────────────────────────────
    # ODRL066 — Partial overlap: hasPart(germany) vs isPartOf(westernEurope)
    # hasPart(de) = {de, wE, europe}  (ancestors of germany)
    # isPartOf(wE) = ↓wE               (10 western concepts)
    # Intersection = {germany, westernEurope}  ≠ ∅
    # hasPart(de) \ isPartOf(wE) = {europe}         → c1 ⊄ c2
    # isPartOf(wE) \ hasPart(de) = {austria, ...}   → c2 ⊄ c1
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=66, name="partial-overlap-hasPart-germany-isPartOf-wE",
        category=Category.SPATIAL,
        verdict=Verdict.COMPATIBLE, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.HAS_PART, "germany"),
        c2=Constraint("spatial", Op.IS_PART_OF, "westernEurope"),
        description="Partial overlap: hasPart(germany) ∩≠ isPartOf(westernEurope)",
        formal=(
            "⟦hasPart(germany)⟧  = {X | leq(germany,X)} = {germany, wE, europe}\n"
            "%   ⟦isPartOf(wE)⟧    = ↓wE = {wE, austria, belgium, france, de, ...}\n"
            "%   X=germany: leq(germany,germany) ∧ leq(germany,wE)    ✓  [intersection]\n"
            "%   Y=europe:  leq(germany,europe)  ∧ ¬leq(europe,wE)    ✓  [c1 only]\n"
            "%   Z=france:  leq(france,wE)       ∧ ¬leq(germany,france) ✓  [c2 only]"
        ),
        paper_ref="Refinement Conflict (hasPart vs isPartOf)",
        difficulty="Hard",
        policy_ttl=(
            _ttl_single("policyA", "permission", "hasPart", "germany") + "\n%\n" +
            _ttl_single("policyB", "prohibition", "isPartOf", "westernEurope")
        ),
        conjecture_fof=(
            "fof(odrl066, conjecture,\n"
            "    ( ?[X]: ( in_denotation(X, germany, hasPart)\n"
            "           & in_denotation(X, westernEurope, isPartOf) )\n"
            "    & ?[Y]: ( in_denotation(Y, germany, hasPart)\n"
            "           & ~in_denotation(Y, westernEurope, isPartOf) )\n"
            "    & ?[Z]: ( in_denotation(Z, westernEurope, isPartOf)\n"
            "           & ~in_denotation(Z, germany, hasPart) ) ))."
        ),
        conjecture_smt2=_smt2(
            "; Partial overlap: negate all three witnesses simultaneously → unsat\n"
            "; X ∈ hasPart(de) ∩ isPartOf(wE)  [germany: leq(de,de) ∧ leq(de,wE)]\n"
            "; Y ∈ hasPart(de) \\ isPartOf(wE)  [europe:  leq(de,eu) ∧ ¬leq(eu,wE)]\n"
            "; Z ∈ isPartOf(wE) \\ hasPart(de)  [france:  leq(fr,wE) ∧ ¬leq(de,fr)]\n"
            "(assert (not (exists ((X C))\n"
            "    (and (leq germany X)(leq X westernEurope)))))\n"
            "(assert (not (exists ((Y C))\n"
            "    (and (leq germany Y)(not (leq Y westernEurope))))))\n"
            "(assert (not (exists ((Z C))\n"
            "    (and (leq Z westernEurope)(not (leq germany Z))))))"
        ),
        inline_smt2_kb=_preamble(),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL067 — Partial overlap: neq(germany) vs isPartOf(westernEurope)
    # neq(de) = C \ {germany}   (25 concepts)
    # isPartOf(wE) = ↓wE        (10 concepts)
    # Intersection = ↓wE \ {germany} = {wE, austria, belgium, france, ...} (9)
    # neq(de) \ isPartOf(wE) = {poland, eE, nE, sE, europe, ...}   → c1 ⊄ c2
    # isPartOf(wE) \ neq(de) = {germany}                            → c2 ⊄ c1
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=67, name="partial-overlap-neq-germany-isPartOf-wE",
        category=Category.SPATIAL,
        verdict=Verdict.COMPATIBLE, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.NEQ, "germany"),
        c2=Constraint("spatial", Op.IS_PART_OF, "westernEurope"),
        description="Partial overlap: neq(germany) ∩≠ isPartOf(westernEurope)",
        formal=(
            "⟦neq(germany)⟧  = C \\ {germany}  (25 concepts)\n"
            "%   ⟦isPartOf(wE)⟧ = ↓wE            (10 concepts)\n"
            "%   X=france:   france≠germany ∧ leq(france,wE)   ✓  [intersection]\n"
            "%   Y=poland:   poland≠germany ∧ ¬leq(poland,wE)  ✓  [c1 only]\n"
            "%   Z=germany:  leq(germany,wE) ∧ germany=germany  ✓  [c2 only]"
        ),
        paper_ref="Refinement Conflict (neq vs isPartOf)",
        difficulty="Hard",
        policy_ttl=(
            _ttl_single("policyA", "permission", "neq", "germany") + "\n%\n" +
            _ttl_single("policyB", "prohibition", "isPartOf", "westernEurope")
        ),
        conjecture_fof=(
            "fof(odrl067, conjecture,\n"
            "    ( ?[X]: ( in_denotation(X, germany, neq)\n"
            "           & in_denotation(X, westernEurope, isPartOf) )\n"
            "    & ?[Y]: ( in_denotation(Y, germany, neq)\n"
            "           & ~in_denotation(Y, westernEurope, isPartOf) )\n"
            "    & ?[Z]: ( in_denotation(Z, westernEurope, isPartOf)\n"
            "           & ~in_denotation(Z, germany, neq) ) ))."
        ),
        conjecture_smt2=_smt2(
            "; X=france: france≠germany ∧ leq(france,wE)\n"
            "; Y=poland: poland≠germany ∧ ¬leq(poland,wE)\n"
            "; Z=germany: leq(germany,wE) ∧ germany=germany\n"
            "(assert (not (exists ((X C))\n"
            "    (and (not (= X germany))(leq X westernEurope)))))\n"
            "(assert (not (exists ((Y C))\n"
            "    (and (not (= Y germany))(not (leq Y westernEurope))))))\n"
            "(assert (not (exists ((Z C))\n"
            "    (and (leq Z westernEurope)(= Z germany)))))"
        ),
        inline_smt2_kb=_preamble(),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL068 — Partial overlap: isNoneOf({easternEurope}) vs hasPart(poland)
    # isNoneOf({eE}) = C \ ↓eE   (21 non-eastern concepts, including europe)
    # hasPart(poland)= {X | leq(poland,X)} = {poland, eE, europe}
    # Intersection = {europe}    (europe ∉ ↓eE, leq(poland,europe) ✓)
    # isNoneOf({eE}) \ hasPart(pl) = {wE,nE,sE,france,...}    → c1 ⊄ c2
    # hasPart(pl) \ isNoneOf({eE}) = {poland, eE}  (both ≤ eE) → c2 ⊄ c1
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=68, name="partial-overlap-isNoneOf-eE-hasPart-poland",
        category=Category.SPATIAL,
        verdict=Verdict.COMPATIBLE, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=None, c2=None,
        description="Partial overlap: isNoneOf({eE}) ∩≠ hasPart(poland)",
        formal=(
            "⟦isNoneOf({eE})⟧   = C \\ ↓eE = {europe, wE, nE, sE, france, ...}\n"
            "%   ⟦hasPart(poland)⟧ = {X | leq(poland,X)} = {poland, eE, europe}\n"
            "%   X=europe: ¬leq(europe,eE) ∧ leq(poland,europe)  ✓  [intersection]\n"
            "%   Y=france: ¬leq(france,eE) ∧ ¬leq(poland,france)  ✓  [c1 only]\n"
            "%   Z=poland: leq(poland,poland) ∧ leq(poland,eE) → poland ≤ eE → not in isNoneOf ✓ [c2 only]"
        ),
        paper_ref="Refinement Conflict (isNoneOf vs hasPart)",
        difficulty="Very Hard",
        policy_ttl=(
            _ttl_single("policyA", "permission", "isNoneOf", "easternEurope") + "\n%\n" +
            _ttl_single("policyB", "prohibition", "hasPart", "poland")
        ),
        inline_axioms=_fof_list_axioms("excl068", ["easternEurope"]),
        conjecture_fof=(
            "fof(odrl068, conjecture,\n"
            "    ( ?[X]: ( in_denotation_set(X, excl068, isNoneOf)\n"
            "           & in_denotation(X, poland, hasPart) )\n"
            "    & ?[Y]: ( in_denotation_set(Y, excl068, isNoneOf)\n"
            "           & ~in_denotation(Y, poland, hasPart) )\n"
            "    & ?[Z]: ( in_denotation(Z, poland, hasPart)\n"
            "           & ~in_denotation_set(Z, excl068, isNoneOf) ) ))."
        ),
        conjecture_smt2=_smt2(
            "; X=europe: ¬leq(europe,eE) ∧ leq(poland,europe)\n"
            "; Y=france: ¬leq(france,eE) ∧ ¬leq(poland,france)\n"
            "; Z=poland: leq(poland,poland) ∧ leq(poland,eE)\n"
            "(assert (not (exists ((X C))\n"
            "    (and (not (leq X easternEurope))(leq poland X)))))\n"
            "(assert (not (exists ((Y C))\n"
            "    (and (not (leq Y easternEurope))(not (leq poland Y))))))\n"
            "(assert (not (exists ((Z C))\n"
            "    (and (leq poland Z)(leq Z easternEurope)))))"
        ),
        inline_smt2_kb=_preamble(),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL069 — NOT partial overlap: eq(germany) ⊆ isPartOf(wE)
    # Three-part test FAILS at part 2: no Y ∈ eq(de) \ isPartOf(wE)
    # because germany ≤ wE directly → full subsumption, not partial overlap.
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=69, name="not-partial-overlap-eq-germany-isPartOf-wE",
        category=Category.SPATIAL,
        verdict=Verdict.SUBSUMES, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.EQ, "germany"),
        c2=Constraint("spatial", Op.IS_PART_OF, "westernEurope"),
        description="NOT partial overlap: eq(germany) ⊆ isPartOf(wE) — full subsumption",
        formal=(
            "Three-part test fails at part 2:\n"
            "%   X: eq(de) ∩ isPartOf(wE) → germany ✓  (de=de ∧ leq(de,wE))\n"
            "%   Y: eq(de) \\ isPartOf(wE) → NO WITNESS  (de ≤ wE directly)\n"
            "%   Z: isPartOf(wE) \\ eq(de)  → france ✓\n"
            "%   → Not partial overlap; this is FULL SUBSUMPTION (cf. ODRL034)"
        ),
        paper_ref="Refinement Conflict Refuted",
        difficulty="Medium",
        notes="flip_conj proves the missing witness Y doesn't exist.",
        policy_ttl=(
            _ttl_single("policyA", "permission", "eq", "germany") + "\n%\n" +
            _ttl_single("policyB", "prohibition", "isPartOf", "westernEurope")
        ),
        conjecture_fof=(
            "% NOT partial overlap — prove part 2 witness cannot exist\n"
            "fof(odrl069, conjecture,\n"
            "    ~( ?[Y]: ( in_denotation(Y, germany, eq)\n"
            "            & ~in_denotation(Y, westernEurope, isPartOf) ) ))."
        ),
        conjecture_smt2=_smt2(
            "; NOT partial overlap: no Y satisfies eq(germany) ∧ ¬isPartOf(wE)\n"
            "; = ¬∃Y. Y=germany ∧ ¬leq(Y,wE)\n"
            "; Negated: ∃Y. Y=germany ∧ ¬leq(Y,wE) → unsat (leq(germany,wE) holds)\n"
            "(assert (exists ((Y C))\n"
            "    (and (= Y germany)(not (leq Y westernEurope)))))"
        ),
        inline_smt2_kb=_preamble(),
    ))

    return problems