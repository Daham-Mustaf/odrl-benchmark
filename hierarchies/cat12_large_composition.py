"""
cat12_large_composition.py
Category 12: Large-Scale Composition — ODRL130–132
Multi-operand AND / 5-way existential witnesses.
"""
from .models import Category, KBProblem, SZS

_CAT  = Category.LARGE_COMPOSITION
_GEO  = "Axioms/Layer0-DomainKB/GEO000-0.ax"
_DPV  = "Axioms/Layer0-DomainKB/DPV000-0.ax"
_LANG = "Axioms/Layer0-DomainKB/LANG000-0.ax"
_ODRL = "Axioms/Layer1-ODRLCore/ODRL000-0.ax"

def large_composition() -> list[KBProblem]:
    return [

        KBProblem(
            number=130, name="three-operand-AND-composition",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _DPV, _LANG, _ODRL], inline_axioms="",
            conjecture_fof=(
                "fof(odrl130, conjecture,\n"
                "    ( ?[X]: ( in_denotation(X, europe, isPartOf)\n"
                "            & in_denotation(X, germany, eq) )\n"
                "    & ?[Y]: ( in_denotation(Y, researchAndDevelopment, isA)\n"
                "            & in_denotation(Y, academicResearch, isA) )\n"
                "    & ?[Z]: ( in_denotation(Z, en, isPartOf)\n"
                "            & in_denotation(Z, enGB, eq) ) ))."
            ),
            description="3-operand AND: spatial+purpose+language all Compatible",
            difficulty="Medium",
        ),

        KBProblem(
            number=131, name="three-operand-AND-one-conflict",
            variant=1, category=_CAT, szs=SZS.COUNTER_SATISFIABLE,
            kbs=[_GEO, _DPV, _LANG, _ODRL], inline_axioms="",
            conjecture_fof=(
                "fof(odrl131, conjecture,\n"
                "    ?[X]: ( in_denotation(X, westernEurope, isPartOf)\n"
                "          & in_denotation(X, easternEurope, isPartOf) ))."
            ),
                "fof(odrl131, conjecture,\n"
                "    ![X]: ~( in_denotation(X, westernEurope, isPartOf)\n"
                "           & in_denotation(X, easternEurope, isPartOf) ))."
            ),
            description="3-operand AND: spatial Conflict → composed Conflict (Thm 2)",
            difficulty="Hard",
        ),

        KBProblem(
            number=132, name="five-way-existential-witness",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL], inline_axioms="",
            conjecture_fof=(
                "fof(odrl132, conjecture,\n"
                "    ( ?[X1]: ( in_denotation(X1, europe, isPartOf)\n"
                "             & in_denotation(X1, germany, eq) )\n"
                "    & ?[X2]: ( in_denotation(X2, westernEurope, isPartOf)\n"
                "             & in_denotation(X2, france, eq) )\n"
                "    & ?[X3]: ( in_denotation(X3, europe, hasPart)\n"
                "             & in_denotation(X3, germany, hasPart) )\n"
                "    & ?[X4]: ( in_denotation(X4, westernEurope, isPartOf)\n"
                "             & in_denotation(X4, bavaria, isPartOf) )\n"
                "    & ?[X5]: ( in_denotation(X5, europe, isPartOf)\n"
                "             & in_denotation(X5, poland, eq) ) ))."
            ),
            description="5 independent Compatible pairs — prover finds 5 witnesses",
            difficulty="Hard",
        ),
    ]