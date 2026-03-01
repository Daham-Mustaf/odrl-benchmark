"""
hierarchies/cat03_subsumption.py
Category 3: Constraint Subsumption — ODRL030-037.

Tests Definition 7: c1 ⊑ c2 iff ⟦c1⟧ ⊆ ⟦c2⟧.
Mixed cross-operator subsumption (eq ⊑ isPartOf, isPartOf ⊑ neq, etc.)
and refutation (counterexample witnesses).

SMT2 encoding for subsumption:
  Subsumes: ∀X. φ(X,c1) → φ(X,c2)
  Negated:  ∃X. φ(X,c1) ∧ ¬φ(X,c2)   ← what we assert for unsat check

SMT2 encoding for refuted:
  Refuted:  ∃X. φ(X,c1) ∧ ¬φ(X,c2)   ← sat check (witness exists)
  Negated:  we assert this directly, expect sat

Paper references: Definition 7 (Constraint Subsumption), Lemma 2.

Problems:
  ODRL030  Confirmed: isPartOf(germany) ⊆ isPartOf(europe)
  ODRL031  Refuted:   isPartOf(europe) ⊄ isPartOf(germany)   [france witness]
  ODRL032  Confirmed: eq(germany) ⊆ isPartOf(europe)
  ODRL033  Confirmed: isA(germany) ≡ isPartOf(germany)        [tautology]
  ODRL034  Confirmed: eq(germany) ⊆ isPartOf(westernEurope)   [redundancy]
  ODRL035  Conflict:  conflict propagation c1⊑c2 ∧ conflict(c2,c3) → conflict(c1,c3)
  ODRL036  Confirmed: isPartOf(germany) ⊆ neq(france)
  ODRL037  Refuted:   neq(germany) ⊄ isPartOf(westernEurope)  [poland witness]
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


def _ttl_constraint(label: str, operator: str, value: str) -> str:
    return (
        f"%   {label}: [\n"
        f"%     odrl:leftOperand odrl:spatial ;\n"
        f"%     odrl:operator    odrl:{operator} ;\n"
        f"%     odrl:rightOperand geo:{value} ] ."
    )


def _ttl_sub(c1_op, c1_val, c2_op, c2_val) -> str:
    return (
        _ttl_constraint("c1", c1_op, c1_val) + "\n%\n" +
        _ttl_constraint("c2", c2_op, c2_val)
    )


def subsumption() -> list[KBProblem]:
    problems = []

    # ──────────────────────────────────────────────────────────────────────
    # ODRL030 — Confirmed: isPartOf(germany) ⊆ isPartOf(europe)
    # leq(X,germany) → leq(germany,westernEurope) → leq(wE,europe) → leq(X,europe)
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=30, name="isPartOf-germany-subsumes-isPartOf-europe",
        category=Category.SPATIAL,
        verdict=Verdict.SUBSUMES, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.IS_PART_OF, "germany"),
        c2=Constraint("spatial", Op.IS_PART_OF, "europe"),
        description="Subsumption confirmed: isPartOf(germany) ⊆ isPartOf(europe)",
        formal=(
            "∀X: leq(X,germany) → leq(X,westernEurope) → leq(X,europe)  [leq_trans×2]\n"
            "%   ⟦isPartOf(germany)⟧ ⊆ ⟦isPartOf(europe)⟧"
        ),
        paper_ref="Definition 7 (Constraint Subsumption)",
        difficulty="Easy",
        policy_ttl=_ttl_sub("isPartOf", "germany", "isPartOf", "europe"),
        conjecture_fof=(
            "fof(odrl030, conjecture,\n"
            "    ![X]: ( in_denotation(X, germany, isPartOf)\n"
            "          => in_denotation(X, europe, isPartOf) ))."
        ),
        conjecture_smt2=_smt2(
            "; Subsumes: ∀X. leq(X,germany) → leq(X,europe)\n"
            "; Negated:  ∃X. leq(X,germany) ∧ ¬leq(X,europe)\n"
            "(assert (exists ((X C))\n"
            "    (and (leq X germany)\n"
            "         (not (leq X europe)))))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL031 — Refuted: isPartOf(europe) ⊄ isPartOf(germany)
    # Counterexample: france ∈ ⟦isPartOf(europe)⟧ but france ∉ ⟦isPartOf(germany)⟧
    # (leq(france,europe) holds but leq(france,germany) does not)
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=31, name="isPartOf-europe-not-subsumes-isPartOf-germany",
        category=Category.SPATIAL,
        verdict=Verdict.REFUTED, szs=SZS.COUNTERSATISFIABLE,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.IS_PART_OF, "europe"),
        c2=Constraint("spatial", Op.IS_PART_OF, "germany"),
        description="Subsumption refuted: isPartOf(europe) ⊄ isPartOf(germany)",
        formal=(
            "Counterexample: france\n"
            "%   leq(france, westernEurope) → leq(france, europe)  → france ∈ ⟦c1⟧\n"
            "%   leq(france, germany) is NOT derivable              → france ∉ ⟦c2⟧\n"
            "%   (france and germany are distinct siblings under wE)"
        ),
        paper_ref="Definition 7",
        difficulty="Medium",
        notes="Paired with ODRL030: subsumption is strictly one-directional.",
        policy_ttl=_ttl_sub("isPartOf", "europe", "isPartOf", "germany"),
        conjecture_fof=(
            "fof(odrl031, conjecture,\n"
            "    ![X]: ( in_denotation(X, europe, isPartOf)\n"
            "          => in_denotation(X, germany, isPartOf) ))."
        ),
        conjecture_smt2=_smt2(
            "; Refuted: ∃X. leq(X,europe) ∧ ¬leq(X,germany)  — expect sat (france)\n"
            "; For Z3 sat-check: assert the witness condition directly\n"
            "(assert (exists ((X C))\n"
            "    (and (leq X europe)\n"
            "         (not (leq X germany)))))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL032 — Confirmed: eq(germany) ⊆ isPartOf(europe)
    # ⟦eq(germany)⟧ = {germany}, and leq(germany,europe) → germany ∈ isPartOf(europe)
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=32, name="eq-germany-subsumes-isPartOf-europe",
        category=Category.SPATIAL,
        verdict=Verdict.SUBSUMES, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.EQ, "germany"),
        c2=Constraint("spatial", Op.IS_PART_OF, "europe"),
        description="Cross-operator subsumption: eq(germany) ⊆ isPartOf(europe)",
        formal=(
            "⟦eq(germany)⟧ = {germany}\n"
            "%   leq(germany, westernEurope) ∧ leq(westernEurope, europe)  [leq_trans]\n"
            "%   → germany ∈ ⟦isPartOf(europe)⟧\n"
            "%   → ⟦eq(germany)⟧ ⊆ ⟦isPartOf(europe)⟧"
        ),
        paper_ref="Definition 7",
        difficulty="Easy",
        notes="'Exactly germany' is a refinement of 'anywhere in europe'.",
        policy_ttl=_ttl_sub("eq", "germany", "isPartOf", "europe"),
        conjecture_fof=(
            "fof(odrl032, conjecture,\n"
            "    ![X]: ( in_denotation(X, germany, eq)\n"
            "          => in_denotation(X, europe, isPartOf) ))."
        ),
        conjecture_smt2=_smt2(
            "; Subsumes: ∀X. X=germany → leq(X,europe)\n"
            "; Negated:  ∃X. X=germany ∧ ¬leq(X,europe)\n"
            "(assert (exists ((X C))\n"
            "    (and (= X germany)\n"
            "         (not (leq X europe)))))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL033 — Tautology: isA(germany) ≡ isPartOf(germany)
    # ODRL000-0.ax defines isA and isPartOf with identical denotation rules
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=33, name="isA-isPartOf-tautological-equivalence",
        category=Category.SPATIAL,
        verdict=Verdict.SUBSUMES, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.IS_A, "germany"),
        c2=Constraint("spatial", Op.IS_PART_OF, "germany"),
        description="Tautological equivalence: isA(germany) ≡ isPartOf(germany)",
        formal=(
            "den_isA_if/onlyif and den_isPartOf_if/onlyif in ODRL000-0.ax\n"
            "%   both reduce to leq(X, germany)\n"
            "%   → ⟦isA(germany)⟧ = ⟦isPartOf(germany)⟧  (biconditional)"
        ),
        paper_ref="Definition 3 (isA = isPartOf), Definition 7",
        difficulty="Trivial",
        notes="isA is a semantic alias for isPartOf in ODRL000-0.ax.",
        policy_ttl=_ttl_sub("isA", "germany", "isPartOf", "germany"),
        conjecture_fof=(
            "fof(odrl033, conjecture,\n"
            "    ![X]: ( in_denotation(X, germany, isA)\n"
            "          => in_denotation(X, germany, isPartOf) ))."
        ),
        conjecture_smt2=_smt2(
            "; isA and isPartOf both reduce to leq(X,germany) — identical\n"
            "; Negated: ∃X. leq(X,germany) ∧ ¬leq(X,germany)  — always unsat\n"
            "(assert (exists ((X C))\n"
            "    (and (leq X germany)\n"
            "         (not (leq X germany)))))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL034 — Redundancy: eq(germany) ⊆ isPartOf(westernEurope)
    # In a conjunction constraint [eq(germany) ∧ isPartOf(wE)],
    # the isPartOf(wE) is redundant because eq(germany) already implies it.
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=34, name="eq-germany-subsumes-isPartOf-wE-redundancy",
        category=Category.SPATIAL,
        verdict=Verdict.SUBSUMES, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.EQ, "germany"),
        c2=Constraint("spatial", Op.IS_PART_OF, "westernEurope"),
        description="Redundancy: eq(germany) ⊆ isPartOf(westernEurope)",
        formal=(
            "⟦eq(germany)⟧ = {germany}\n"
            "%   leq(germany, westernEurope)  [direct edge in GEO]\n"
            "%   → germany ∈ ⟦isPartOf(westernEurope)⟧\n"
            "%   → isPartOf(wE) is redundant in ∧-conjunction with eq(germany)"
        ),
        paper_ref="Definition 7, policy simplification",
        difficulty="Easy",
        notes="The stricter eq constraint makes the weaker isPartOf constraint redundant.",
        policy_ttl=_ttl_sub("eq", "germany", "isPartOf", "westernEurope"),
        conjecture_fof=(
            "fof(odrl034, conjecture,\n"
            "    ![X]: ( in_denotation(X, germany, eq)\n"
            "          => in_denotation(X, westernEurope, isPartOf) ))."
        ),
        conjecture_smt2=_smt2(
            "; Subsumes: ∀X. X=germany → leq(X,westernEurope)\n"
            "; Negated:  ∃X. X=germany ∧ ¬leq(X,westernEurope)\n"
            "(assert (exists ((X C))\n"
            "    (and (= X germany)\n"
            "         (not (leq X westernEurope)))))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL035 — Conflict propagation: c1⊑c2 ∧ conflict(c2,c3) → conflict(c1,c3)
    # c1=isPartOf(germany), c2=isPartOf(wE), c3=isPartOf(eE)
    # ODRL030: c1⊑c2; ODRL013: conflict(c2,c3) → conflict(c1,c3) [Lemma 2]
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=35, name="conflict-propagation-via-subsumption",
        category=Category.SPATIAL,
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.IS_PART_OF, "germany"),
        c2=Constraint("spatial", Op.IS_PART_OF, "easternEurope"),
        description="Conflict propagation: c1⊑c2 ∧ conflict(c2,c3) → conflict(c1,c3)",
        formal=(
            "ODRL030: isPartOf(germany) ⊆ isPartOf(westernEurope)  [c1⊑c2]\n"
            "%   ODRL013: conflict(isPartOf(wE), isPartOf(eE))       [c2 conflict c3]\n"
            "%   Lemma 2: c1⊑c2 ∧ conflict(c2,c3) → conflict(c1,c3)\n"
            "%   → isPartOf(germany) ∩ isPartOf(easternEurope) = ∅"
        ),
        paper_ref="Lemma 2 (Conflict Propagation)",
        difficulty="Medium",
        notes="Combines ODRL030 (subsumption) and ODRL013 (conflict) in one proof.",
        policy_ttl=_ttl_sub("isPartOf", "germany", "isPartOf", "easternEurope"),
        conjecture_fof=(
            "fof(odrl035, conjecture,\n"
            "    ![X]: ~( in_denotation(X, germany, isPartOf)\n"
            "           & in_denotation(X, easternEurope, isPartOf) ))."
        ),
        conjecture_smt2=_smt2(
            "; Conflict: ∀X. ¬(leq(X,germany) ∧ leq(X,easternEurope))\n"
            "; Negated:  ∃X. leq(X,germany) ∧ leq(X,easternEurope)\n"
            "(assert (exists ((X C))\n"
            "    (and (leq X germany)\n"
            "         (leq X easternEurope))))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL036 — Confirmed: isPartOf(germany) ⊆ neq(france)
    # germany ≠ france [UNA] → {germany} ⊆ C\{france}
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=36, name="isPartOf-germany-subsumes-neq-france",
        category=Category.SPATIAL,
        verdict=Verdict.SUBSUMES, szs=SZS.THEOREM,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.IS_PART_OF, "germany"),
        c2=Constraint("spatial", Op.NEQ, "france"),
        description="Cross-operator subsumption: isPartOf(germany) ⊆ neq(france)",
        formal=(
            "∀X: leq(X,germany) → X ≠ france\n"
            "%   Proof: leq(X,germany) ∧ X=france → leq(france,germany)\n"
            "%   But disj(wE,wE_other) → disj(france,germany)  [siblings]\n"
            "%   disj_order_consistency: leq(france,germany) → ¬disj(france,germany)\n"
            "%   Contradiction → X ≠ france"
        ),
        paper_ref="Definition 7",
        difficulty="Medium",
        policy_ttl=_ttl_sub("isPartOf", "germany", "neq", "france"),
        conjecture_fof=(
            "fof(odrl036, conjecture,\n"
            "    ![X]: ( in_denotation(X, germany, isPartOf)\n"
            "          => in_denotation(X, france, neq) ))."
        ),
        conjecture_smt2=_smt2(
            "; Subsumes: ∀X. leq(X,germany) → X≠france\n"
            "; Negated:  ∃X. leq(X,germany) ∧ X=france\n"
            "(assert (exists ((X C))\n"
            "    (and (leq X germany)\n"
            "         (= X france))))"
        ),
    ))

    # ──────────────────────────────────────────────────────────────────────
    # ODRL037 — Refuted: neq(germany) ⊄ isPartOf(westernEurope)
    # Counterexample: poland ∈ ⟦neq(germany)⟧ but poland ∉ ⟦isPartOf(wE)⟧
    # (poland is in easternEurope, not westernEurope)
    # ──────────────────────────────────────────────────────────────────────
    problems.append(KBProblem(
        number=37, name="neq-germany-not-subsumes-isPartOf-wE",
        category=Category.SPATIAL,
        verdict=Verdict.REFUTED, szs=SZS.COUNTERSATISFIABLE,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.NEQ, "germany"),
        c2=Constraint("spatial", Op.IS_PART_OF, "westernEurope"),
        description="Subsumption refuted: neq(germany) ⊄ isPartOf(westernEurope)",
        formal=(
            "Counterexample: poland\n"
            "%   poland ≠ germany  [UNA]           → poland ∈ ⟦neq(germany)⟧\n"
            "%   ¬leq(poland,wE)  [GEO axiom]      → poland ∉ ⟦isPartOf(wE)⟧"
        ),
        paper_ref="Definition 7",
        difficulty="Medium",
        notes="Paired with ODRL036: neq is much broader than isPartOf.",
        policy_ttl=_ttl_sub("neq", "germany", "isPartOf", "westernEurope"),
        conjecture_fof=(
            "fof(odrl037, conjecture,\n"
            "    ![X]: ( in_denotation(X, germany, neq)\n"
            "          => in_denotation(X, westernEurope, isPartOf) ))."
        ),
        conjecture_smt2=_smt2(
            "; Refuted: ∃X. X≠germany ∧ ¬leq(X,wE)  — expect sat (poland)\n"
            "(assert (exists ((X C))\n"
            "    (and (not (= X germany))\n"
            "         (not (leq X westernEurope)))))"
        ),
    ))
    # ODRL038 — Unknown: ungrounded concept → Unknown verdict
    # concept 'unknownRegion' is in domain C but has no hierarchy facts
    problems.append(KBProblem(
        number=38, name="ungrounded-concept-yields-unknown",
        category=Category.SPATIAL,
        verdict=Verdict.UNKNOWN, szs=SZS.COUNTERSATISFIABLE,
        kbs=[KB.GEO],
        c1=Constraint("spatial", Op.IS_PART_OF, "europe"),
        c2=Constraint("spatial", Op.IS_PART_OF, "unknownRegion"),
        description="Unknown: unknownRegion not in hierarchy → verdict Unknown",
        formal=(
            "γ(unknownRegion) = ⊥  (not grounded)\n"
            "%   ⟦isPartOf(unknownRegion)⟧ = ⊤\n"
            "%   verdict_of(⊤, classical_set) = Unknown"
        ),
        paper_ref="Definition 3 (grounding), Definition 5 (Unknown verdict)",
        difficulty="Trivial",
        notes="Demonstrates open-world semantics: missing concept → Unknown, not Conflict.",
        conjecture_fof=(
            "fof(odrl038, conjecture,\n"
            "    ![X]: ~( in_denotation(X, europe, isPartOf)\n"
            "           & in_denotation(X, unknownRegion, isPartOf) ))."
        ),
        conjecture_smt2=_smt2(
            "; Unknown: unknownRegion has no leq facts → sat (free assignment)\n"
            "(assert (exists ((X C))\n"
            "    (and (leq X europe)\n"
            "         (leq X unknownRegion))))"
        ),
    ))

    preamble = _preamble()
    for prob in problems:
        prob.inline_smt2_kb = preamble

    return problems
