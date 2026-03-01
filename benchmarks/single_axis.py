"""Category A: Single-axis interval conflict/compatible/subsumption.

ODRL 300–314 (15 benchmarks).
"""

from .models import Benchmark, Category, Constraint, Op, SZS, Verdict


def _make_size_policy_ttl(c1: Constraint, c2: Constraint) -> str:
    """ODRL policy snippet for single-axis size constraints."""
    return f"""\
%   @prefix odrl: <http://www.w3.org/ns/odrl/2/> .
%   @prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
%   @prefix ex:   <https://example.org/> .
%
%   ex:policyA a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSize{c1.axis.title()} ;
%         odrl:operator odrl:{c1.op.value} ;
%         odrl:rightOperand "{c1.value}"^^xsd:decimal ;
%         odrl:unit <http://dbpedia.org/resource/Pixel> ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSize{c2.axis.title()} ;
%         odrl:operator odrl:{c2.op.value} ;
%         odrl:rightOperand "{c2.value}"^^xsd:decimal ;
%         odrl:unit <http://dbpedia.org/resource/Pixel> ] ] ."""


def single_axis_benchmarks() -> list[Benchmark]:
    """Category A: Single-axis interval conflict/compatible/subsumption."""
    benchmarks = []

    # --- Conflict benchmarks ---

    benchmarks.append(Benchmark(
        number=300, name="lteq-gteq-conflict",
        category=Category.SINGLE_AXIS,
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.GTEQ, 800),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="width ≤ 600 vs width ≥ 800: disjoint intervals",
        difficulty="Easy",
        domain_lo=0, domain_lo_open=True,
    ))

    benchmarks.append(Benchmark(
        number=301, name="eq-eq-conflict",
        category=Category.SINGLE_AXIS,
        c1=Constraint("width", Op.EQ, 600),
        c2=Constraint("width", Op.EQ, 800),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="width = 600 vs width = 800: distinct points",
        difficulty="Easy",
        domain_lo=0, domain_lo_open=True,
    ))

    benchmarks.append(Benchmark(
        number=302, name="lt-gteq-boundary-conflict",
        category=Category.SINGLE_AXIS,
        c1=Constraint("width", Op.LT, 600),
        c2=Constraint("width", Op.GTEQ, 600),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="width < 600 vs width ≥ 600: open/closed boundary",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        needs_density=True,
        notes="Tests open/closed boundary — requires Section A predicates",
    ))

    benchmarks.append(Benchmark(
        number=303, name="gt-lteq-boundary-conflict",
        category=Category.SINGLE_AXIS,
        c1=Constraint("width", Op.GT, 600),
        c2=Constraint("width", Op.LTEQ, 600),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="width > 600 vs width ≤ 600: mirror boundary",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        needs_density=True,
    ))

    # --- Compatible benchmarks ---

    benchmarks.append(Benchmark(
        number=304, name="lteq-gteq-compatible",
        category=Category.SINGLE_AXIS,
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.GTEQ, 200),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="width ≤ 600 vs width ≥ 200: overlapping intervals",
        difficulty="Easy",
        domain_lo=0, domain_lo_open=True,
    ))

    benchmarks.append(Benchmark(
        number=305, name="lteq-gteq-touch-compatible",
        category=Category.SINGLE_AXIS,
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.GTEQ, 600),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="width ≤ 600 vs width ≥ 600: touching at 600",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        notes="Witness: x = 600. Tests closed-closed boundary.",
    ))

    benchmarks.append(Benchmark(
        number=306, name="eq-eq-same-compatible",
        category=Category.SINGLE_AXIS,
        c1=Constraint("width", Op.EQ, 600),
        c2=Constraint("width", Op.EQ, 600),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="width = 600 vs width = 600: identical points",
        difficulty="Easy",
        domain_lo=0, domain_lo_open=True,
    ))

    benchmarks.append(Benchmark(
        number=307, name="eq-lteq-compatible",
        category=Category.SINGLE_AXIS,
        c1=Constraint("width", Op.EQ, 400),
        c2=Constraint("width", Op.LTEQ, 600),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="width = 400 vs width ≤ 600: point inside interval",
        difficulty="Easy",
        domain_lo=0, domain_lo_open=True,
    ))

    benchmarks.append(Benchmark(
        number=308, name="gt-lt-open-compatible",
        category=Category.SINGLE_AXIS,
        c1=Constraint("width", Op.GT, 200),
        c2=Constraint("width", Op.LT, 800),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="width > 200 vs width < 800: open overlap",
        difficulty="Easy",
        domain_lo=0, domain_lo_open=True,
        needs_density=True,
    ))

    # --- Subsumption benchmarks ---

    benchmarks.append(Benchmark(
        number=309, name="lteq-subsumes-lteq",
        category=Category.SINGLE_AXIS,
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.LTEQ, 1200),
        verdict=Verdict.SUBSUMES, szs=SZS.THEOREM,
        description="(0,600] ⊆ (0,1200]: tighter bound subsumes wider",
        difficulty="Easy",
        domain_lo=0, domain_lo_open=True,
    ))

    benchmarks.append(Benchmark(
        number=310, name="lteq-not-subsumes-lteq",
        category=Category.SINGLE_AXIS,
        c1=Constraint("width", Op.LTEQ, 1200),
        c2=Constraint("width", Op.LTEQ, 600),
        verdict=Verdict.REFUTED, szs=SZS.COUNTERSATISFIABLE,
        description="(0,1200] ⊄ (0,600]: wider does not subsume tighter",
        difficulty="Easy",
        domain_lo=0, domain_lo_open=True,
    ))

    benchmarks.append(Benchmark(
        number=311, name="gteq-subsumes-gteq",
        category=Category.SINGLE_AXIS,
        c1=Constraint("width", Op.GTEQ, 800),
        c2=Constraint("width", Op.GTEQ, 400),
        verdict=Verdict.SUBSUMES, szs=SZS.THEOREM,
        description="[800,∞) ⊆ [400,∞): higher lower-bound subsumes",
        difficulty="Easy",
        domain_lo=0, domain_lo_open=True,
    ))

    benchmarks.append(Benchmark(
        number=312, name="eq-subsumes-lteq",
        category=Category.SINGLE_AXIS,
        c1=Constraint("width", Op.EQ, 400),
        c2=Constraint("width", Op.LTEQ, 600),
        verdict=Verdict.SUBSUMES, szs=SZS.THEOREM,
        description="{400} ⊆ (0,600]: point inside interval",
        difficulty="Easy",
        domain_lo=0, domain_lo_open=True,
    ))

    # --- BSB running example ---

    benchmarks.append(Benchmark(
        number=313, name="bsb-width-conflict",
        category=Category.SINGLE_AXIS,
        c1=Constraint("width", Op.LTEQ, 600,
                       axis_iri="oax:absoluteSizeWidth"),
        c2=Constraint("width", Op.GTEQ, 1200,
                       axis_iri="oax:absoluteSizeWidth"),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="BSB running example: width ≤ 600 vs width ≥ 1200",
        difficulty="Easy",
        domain_lo=0, domain_lo_open=True,
    ))

    benchmarks.append(Benchmark(
        number=314, name="bsb-height-compatible",
        category=Category.SINGLE_AXIS,
        c1=Constraint("height", Op.LTEQ, 600,
                       axis_iri="oax:absoluteSizeHeight"),
        c2=Constraint("height", Op.GTEQ, 400,
                       axis_iri="oax:absoluteSizeHeight"),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="BSB running example: height ≤ 600 vs height ≥ 400",
        difficulty="Easy",
        domain_lo=0, domain_lo_open=True,
    ))

    # Generate policy TTL for all
    for b in benchmarks:
        b.policy_ttl = _make_size_policy_ttl(b.c1, b.c2)

    return benchmarks
