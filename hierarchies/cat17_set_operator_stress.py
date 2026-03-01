"""
cat17_set_operator_stress.py
Category 17: Set Operator Stress — ODRL200–205
Deep isNoneOf/isAllOf/isAnyOf combinations.
"""
from .models import Category, KBProblem, SZS

_CAT  = Category.COMBINED
_GEO  = "Axioms/Layer0-DomainKB/GEO000-0.ax"
_ODRL = "Axioms/Layer1-ODRLCore/ODRL000-0.ax"

def _cl(lid, elems):
    d = " | ".join(f"G = {e}" for e in elems)
    return f"fof(list_{lid}_closed, axiom,\n    ![G]: (in_value_list(G, {lid}) => ({d})))."

def set_operator_stress() -> list[KBProblem]:
    return [

        KBProblem(
            number=200, name="isNoneOf-x-isNoneOf-double-complement",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL],
            inline_axioms=(
                "fof(l200a, axiom, in_value_list(westernEurope, noneListA200)).\n" +
                _cl("noneListA200", ["westernEurope"]) + "\n"
                "fof(l200b, axiom, in_value_list(easternEurope, noneListB200)).\n" +
                _cl("noneListB200", ["easternEurope"])
            ),
            conjecture_fof=(
                "fof(odrl200, conjecture,\n"
                "    ?[X]: ( in_denotation_set(X, noneListA200, isNoneOf)\n"
                "          & in_denotation_set(X, noneListB200, isNoneOf) ))."
            ),
            description="isNoneOf({wE}) ∩ isNoneOf({eE}) ≠ ∅, witness=europe",
            difficulty="Very Hard",
        ),

        KBProblem(
            number=201, name="isNoneOf-x-isAllOf-complement-meets-intersection",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL],
            inline_axioms=(
                "fof(l201a, axiom, in_value_list(easternEurope, noneList201)).\n" +
                _cl("noneList201", ["easternEurope"]) + "\n"
                "fof(l201b1,axiom, in_value_list(europe,        allList201)).\n"
                "fof(l201b2,axiom, in_value_list(westernEurope, allList201)).\n" +
                _cl("allList201", ["europe", "westernEurope"])
            ),
            conjecture_fof=(
                "fof(odrl201, conjecture,\n"
                "    ?[X]: ( in_denotation_set(X, noneList201, isNoneOf)\n"
                "          & in_denotation_set(X, allList201,  isAllOf) ))."
            ),
            description="isNoneOf({eE}) ∩ isAllOf({europe,wE})=↓wE, witness=germany",
            difficulty="Very Hard",
        ),

        KBProblem(
            number=202, name="isNoneOf-large-exclusion-nearly-empty",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL],
            inline_axioms=(
                "fof(l202_1,axiom, in_value_list(westernEurope, noneList202)).\n"
                "fof(l202_2,axiom, in_value_list(easternEurope, noneList202)).\n" +
                _cl("noneList202", ["westernEurope", "easternEurope"])
            ),
            conjecture_fof=(
                "fof(odrl202, conjecture,\n"
                "    ![X]: ( in_denotation_set(X, noneList202, isNoneOf)\n"
                "        => X = europe ))."
            ),
            description="isNoneOf({wE,eE})={europe}: exhaustive check over 24 concepts",
            difficulty="Extreme",
        ),

        KBProblem(
            number=203, name="3way-set-operators-isAnyOf-isNoneOf-isAllOf",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL],
            inline_axioms=(
                "fof(l203a1,axiom, in_value_list(germany,       anyList203)).\n"
                "fof(l203a2,axiom, in_value_list(france,        anyList203)).\n" +
                _cl("anyList203", ["germany", "france"]) + "\n"
                "fof(l203b, axiom, in_value_list(westernEurope, noneList203)).\n" +
                _cl("noneList203", ["westernEurope"]) + "\n"
                "fof(l203c1,axiom, in_value_list(europe,        allList203)).\n"
                "fof(l203c2,axiom, in_value_list(germany,       allList203)).\n" +
                _cl("allList203", ["europe", "germany"])
            ),
            conjecture_fof=(
                "fof(odrl203, conjecture,\n"
                "    ( ![X]: ~( in_denotation_set(X, anyList203,  isAnyOf)\n"
                "             & in_denotation_set(X, noneList203, isNoneOf) )\n"
                "    & ?[Y]: ( in_denotation_set(Y,  anyList203,  isAnyOf)\n"
                "            & in_denotation_set(Y,  allList203,  isAllOf) )\n"
                "    & ![Z]: ~( in_denotation_set(Z, noneList203, isNoneOf)\n"
                "             & in_denotation_set(Z, allList203,  isAllOf) ) ))."
            ),
            description="3-way isAnyOf × isNoneOf × isAllOf non-transitive",
            difficulty="Extreme",
        ),

        KBProblem(
            number=204, name="isNoneOf-x-isPartOf-universal-conflict",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL],
            inline_axioms=(
                "fof(l204, axiom, in_value_list(europe, noneList204)).\n" +
                _cl("noneList204", ["europe"])
            ),
            conjecture_fof=(
                "fof(odrl204, conjecture,\n"
                "    ![X]: ~( in_denotation_set(X, noneList204, isNoneOf)\n"
                "           & in_denotation(X, germany, isPartOf) ))."
            ),
            description="isNoneOf({europe}) ∩ isPartOf(de)=∅: ↓de ⊆ ↓europe",
            difficulty="Very Hard",
        ),

        KBProblem(
            number=205, name="isAnyOf5-x-isNoneOf2-large-union-vs-complement",
            variant=1, category=_CAT, szs=SZS.THEOREM,
            kbs=[_GEO, _ODRL],
            inline_axioms=(
                "fof(l205a1,axiom, in_value_list(germany,      anyList205)).\n"
                "fof(l205a2,axiom, in_value_list(france,       anyList205)).\n"
                "fof(l205a3,axiom, in_value_list(italy,        anyList205)).\n"
                "fof(l205a4,axiom, in_value_list(spain,        anyList205)).\n"
                "fof(l205a5,axiom, in_value_list(netherlands,  anyList205)).\n" +
                _cl("anyList205", ["germany","france","italy","spain","netherlands"]) + "\n"
                "fof(l205b1,axiom, in_value_list(westernEurope, noneList205)).\n"
                "fof(l205b2,axiom, in_value_list(easternEurope, noneList205)).\n" +
                _cl("noneList205", ["westernEurope","easternEurope"])
            ),
            conjecture_fof=(
                "fof(odrl205, conjecture,\n"
                "    ?[X]: ( in_denotation_set(X, anyList205,  isAnyOf)\n"
                "          & in_denotation_set(X, noneList205, isNoneOf) ))."
            ),
            description="isAnyOf(5) ∩ isNoneOf(2): all union members ≤ wE → Compatible (italy/spain/nl may not be in GEO)",
            difficulty="Extreme",
        ),
    ]