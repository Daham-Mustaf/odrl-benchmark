"""
cat11_quantifier_stress.py
Category 11: Quantifier Stress — ODRL120–123
∀∃ and ∃∀ alternation patterns.
"""
from .models import Category, KBProblem, SZS

_CAT  = Category.QUANTIFIER_STRESS
_GEO  = "Axioms/Layer0-DomainKB/GEO000-0.ax"
_ODRL = "Axioms/Layer1-ODRLCore/ODRL000-0.ax"

def quantifier_stress() -> list[KBProblem]:
    return [

        KBProblem(
            number=120, name="universal-all-descendant-pairs-conflict",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL], inline_axioms="",
            conjecture_fof=(
                "fof(odrl120, conjecture,\n"
                "    ![G1,G2,X]: (\n"
                "        (leq(G1, westernEurope) & leq(G2, easternEurope))\n"
                "      => ~( in_denotation(X, G1, isPartOf)\n"
                "          & in_denotation(X, G2, isPartOf) )))."
            ),
            description="∀G1∈↓wE, ∀G2∈↓eE: overlap=∅ (universal conflict)",
            difficulty="Hard",
        ),

        KBProblem(
            number=121, name="existential-common-ancestor-three-countries",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL], inline_axioms="",
            conjecture_fof=(
                "fof(odrl121, conjecture,\n"
                "    ?[X]: ( in_denotation(X, germany, hasPart)\n"
                "          & in_denotation(X, france, hasPart)\n"
                "          & in_denotation(X, italy, hasPart) ))."
            ),
            description="∃X ancestor of {de,fr,it}: witness=europe",
            difficulty="Hard",
        ),

        KBProblem(
            number=122, name="subsumption-chain-denotation",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL], inline_axioms="",
            conjecture_fof=(
                "fof(odrl122, conjecture,\n"
                "    ![X]: ( in_denotation(X, bavaria, isPartOf)\n"
                "        => in_denotation(X, europe, isPartOf) ))."
            ),
            description="↓bavaria ⊆ ↓europe via 3-hop leq chain",
            difficulty="Medium",
        ),

        KBProblem(
            number=123, name="forall-exists-every-descendant-has-ancestor",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL], inline_axioms="",
            conjecture_fof=(
                "fof(odrl123, conjecture,\n"
                "    ![G]: ( leq(G, westernEurope)\n"
                "        => ?[X]: in_denotation(X, G, hasPart) ))."
            ),
            description="∀G≤wE: ∃X in hasPart(G), witness=westernEurope",
            difficulty="Hard",
        ),
    ]