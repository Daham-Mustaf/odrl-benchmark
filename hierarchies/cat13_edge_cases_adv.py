"""
cat13_edge_cases_adv.py
Category 13: Edge Cases & Adversarial — ODRL140–145
Degenerate, pathological, and boundary cases.
"""
from .models import Category, KBProblem, SZS

_CAT  = Category.EDGE_CASES
_GEO  = "Axioms/Layer0-DomainKB/GEO000-0.ax"
_ODRL = "Axioms/Layer1-ODRLCore/ODRL000-0.ax"

_MINIMAL_KB = """\
fof(min_root, axiom, concept(universe)).
fof(min_refl, axiom, leq(universe, universe))."""

def edge_cases_adv() -> list[KBProblem]:
    return [

        KBProblem(
            number=140, name="tautological-self-conflict-eq-neq",
            variant=1, category=_CAT, szs=SZS.COUNTER_SATISFIABLE,
            kbs=[_GEO, _ODRL], inline_axioms="",
            conjecture_fof=(
                "fof(odrl140, conjecture,\n"
                "    ?[X]: ( in_denotation(X, germany, eq)\n"
                "          & in_denotation(X, germany, neq) ))."
            ),
                "fof(odrl140, conjecture,\n"
                "    ![X]: ~( in_denotation(X, germany, eq)\n"
                "           & in_denotation(X, germany, neq) ))."
            ),
            description="eq(de) ∩ neq(de)=∅: tautological self-conflict",
            difficulty="Easy",
        ),

        KBProblem(
            number=141, name="single-concept-kb-degenerate",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_ODRL], inline_axioms=_MINIMAL_KB,
            conjecture_fof=(
                "fof(odrl141, conjecture,\n"
                "    ?[X]: ( in_denotation(X, universe, isPartOf)\n"
                "          & in_denotation(X, universe, eq) ))."
            ),
            description="Degenerate single-concept KB: trivially Compatible",
            difficulty="Easy",
        ),

        KBProblem(
            number=142, name="root-level-conflict-large-kb",
            variant=1, category=_CAT, szs=SZS.COUNTER_SATISFIABLE,
            kbs=[_GEO, _ODRL], inline_axioms="",
            conjecture_fof=(
                "fof(odrl142, conjecture,\n"
                "    ?[X]: ( in_denotation(X, europe, eq)\n"
                "          & in_denotation(X, europe, neq) ))."
            ),
                "fof(odrl142, conjecture,\n"
                "    ![X]: ~( in_denotation(X, europe, eq)\n"
                "           & in_denotation(X, europe, neq) ))."
            ),
            description="eq(europe) ∩ neq(europe)=∅ with full 24-concept GEO KB",
            difficulty="Easy",
        ),

        KBProblem(
            number=143, name="reflexivity-every-concept-in-own-isPartOf",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL], inline_axioms="",
            conjecture_fof=(
                "fof(odrl143, conjecture,\n"
                "    ![G]: ( concept(G)\n"
                "        => in_denotation(G, G, isPartOf) ))."
            ),
            description="∀G: concept(G) → G ∈ ⟦isPartOf(G)⟧ (reflexivity)",
            difficulty="Easy",
        ),

        KBProblem(
            number=144, name="bidirectional-conflict-disj-symm",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL], inline_axioms="",
            conjecture_fof=(
                "fof(odrl144, conjecture,\n"
                "    ( ![X]: ~( in_denotation(X, westernEurope, isPartOf)\n"
                "             & in_denotation(X, easternEurope, isPartOf) )\n"
                "    & ![Y]: ~( in_denotation(Y, easternEurope, isPartOf)\n"
                "             & in_denotation(Y, westernEurope, isPartOf) ) ))."
            ),
            description="Bidirectional conflict: disj(wE,eE) ∧ disj(eE,wE) (symmetry)",
            difficulty="Medium",
        ),

        KBProblem(
            number=145, name="non-existent-concept-unknown",
            variant=1, category=_CAT, szs=SZS.COUNTER_SATISFIABLE,
            kbs=[_GEO, _ODRL], inline_axioms="",
            conjecture_fof=(
                "fof(odrl145, conjecture,\n"
                "    ?[X]: in_denotation(X, phantomConcept, isPartOf))."
            ),
            description="phantomConcept not in KB → no axiom fires → Unknown/CounterSat",
            difficulty="Medium",
        ),
    ]