"""
hierarchies/cat10_nested_set_ops.py
Category 10: Nested Set Operators — ODRL110–114
isAllOf (∩), isAnyOf (∪), isNoneOf (complement) interactions.
"""
from .models import Category, Constraint, KB, KBProblem, Op, SZS, Verdict

_CAT  = Category.NESTED_SET
_GEO  = KB.GEO
_ODRL = KB.GEO  # no separate ODRL KB — GEO includes axioms


def _closure(list_id: str, elements: list[str]) -> str:
    disj = " | ".join(f"G = {e}" for e in elements)
    return (f"fof(list_{list_id}_closed, axiom,\n"
            f"    ![G]: (in_value_list(G, {list_id}) => ({disj}))).")


def nested_set_ops() -> list[KBProblem]:
    return [
        KBProblem(
            number=110, name="isAllOf-empty-disjoint-members",
            variant=1, category=_CAT,
            verdict=Verdict.CONFLICT,
            szs=SZS.THEOREM,
            kbs=[_GEO],
            c1=None, c2=None,
            inline_axioms=(
                "fof(list_110_1, axiom, in_value_list(westernEurope, list110)).\n"
                "fof(list_110_2, axiom, in_value_list(easternEurope, list110)).\n" +
                _closure("list110", ["westernEurope", "easternEurope"])
            ),
            conjecture_fof=(
                "fof(odrl110, conjecture,\n"
                "    ![X]: ~in_denotation_set(X, list110, isAllOf))."
            ),
            conjecture_smt2=(
                "(assert (exists ((X Region))\n"
                "  (in_denotation_set X list110 isAllOf)))\n"
                "(check-sat)\n(exit)"
            ),
            description="isAllOf({wE,eE})=∅: disjoint members → empty denotation",
            difficulty="Hard",
        ),
        KBProblem(
            number=111, name="isAnyOf-union-compatible-isPartOf",
            variant=1, category=_CAT,
            verdict=Verdict.COMPATIBLE,
            szs=SZS.THEOREM,
            kbs=[_GEO],
            c1=None, c2=None,
            inline_axioms=(
                "fof(list_111_1, axiom, in_value_list(germany, list111)).\n"
                "fof(list_111_2, axiom, in_value_list(france, list111)).\n" +
                _closure("list111", ["germany", "france"])
            ),
            conjecture_fof=(
                "fof(odrl111, conjecture,\n"
                "    ?[X]: ( in_denotation_set(X, list111, isAnyOf)\n"
                "          & in_denotation(X, westernEurope, isPartOf) ))."
            ),
            conjecture_smt2=(
                "(assert (not (exists ((X Region))\n"
                "  (and (in_denotation_set X list111 isAnyOf)\n"
                "       (in_denotation X westernEurope isPartOf)))))\n"
                "(check-sat)\n(exit)"
            ),
            description="isAnyOf({de,fr}) ∩ isPartOf(wE) ≠ ∅, witness=germany",
            difficulty="Easy",
        ),
        KBProblem(
            number=112, name="isNoneOf-conflict-subsumed-isPartOf",
            variant=1, category=_CAT,
            verdict=Verdict.CONFLICT,
            szs=SZS.THEOREM,
            kbs=[_GEO],
            c1=None, c2=None,
            inline_axioms=(
                "fof(list_112_1, axiom, in_value_list(westernEurope, list112)).\n" +
                _closure("list112", ["westernEurope"])
            ),
            conjecture_fof=(
                "fof(odrl112, conjecture,\n"
                "    ![X]: ~( in_denotation_set(X, list112, isNoneOf)\n"
                "           & in_denotation(X, germany, isPartOf) ))."
            ),
            conjecture_smt2=(
                "(assert (exists ((X Region))\n"
                "  (and (in_denotation_set X list112 isNoneOf)\n"
                "       (in_denotation X germany isPartOf))))\n"
                "(check-sat)\n(exit)"
            ),
            description="isNoneOf({wE}) ∩ isPartOf(de)=∅: de≤wE → conflict",
            difficulty="Hard",
        ),
        KBProblem(
            number=113, name="isAnyOf-isNoneOf-partial-overlap",
            variant=1, category=_CAT,
            verdict=Verdict.COMPATIBLE,
            szs=SZS.THEOREM,
            kbs=[_GEO],
            c1=None, c2=None,
            inline_axioms=(
                "fof(list_113a_1, axiom, in_value_list(germany, anyList113)).\n"
                "fof(list_113a_2, axiom, in_value_list(poland, anyList113)).\n" +
                _closure("anyList113", ["germany", "poland"]) + "\n" +
                "fof(list_113b_1, axiom, in_value_list(easternEurope, noneList113)).\n" +
                _closure("noneList113", ["easternEurope"])
            ),
            conjecture_fof=(
                "fof(odrl113, conjecture,\n"
                "    ?[X]: ( in_denotation_set(X, anyList113, isAnyOf)\n"
                "          & in_denotation_set(X, noneList113, isNoneOf) ))."
            ),
            conjecture_smt2=(
                "(assert (not (exists ((X Region))\n"
                "  (and (in_denotation_set X anyList113 isAnyOf)\n"
                "       (in_denotation_set X noneList113 isNoneOf)))))\n"
                "(check-sat)\n(exit)"
            ),
            description="isAnyOf({de,pl}) ∩ isNoneOf({eE}): partial overlap, witness=germany",
            difficulty="Medium",
        ),
        KBProblem(
            number=114, name="isAllOf-compatible-members-nonempty",
            variant=1, category=_CAT,
            verdict=Verdict.COMPATIBLE,
            szs=SZS.THEOREM,
            kbs=[_GEO],
            c1=None, c2=None,
            inline_axioms=(
                "fof(list_114_1, axiom, in_value_list(westernEurope, list114)).\n"
                "fof(list_114_2, axiom, in_value_list(europe, list114)).\n" +
                _closure("list114", ["westernEurope", "europe"])
            ),
            conjecture_fof=(
                "fof(odrl114, conjecture,\n"
                "    ?[X]: in_denotation_set(X, list114, isAllOf))."
            ),
            conjecture_smt2=(
                "(assert (not (exists ((X Region))\n"
                "  (in_denotation_set X list114 isAllOf))))\n"
                "(check-sat)\n(exit)"
            ),
            description="isAllOf({wE,europe})≠∅: wE≤europe → ↓wE is the intersection",
            difficulty="Easy",
        ),
    ]
