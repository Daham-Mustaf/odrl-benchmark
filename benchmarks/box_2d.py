"""Category B: Two-axis (width × height) box intersection.

ODRL 320–330 (11 benchmarks).

Tests thm:projection: box conflict/compatible is determined by
per-axis verdicts aggregated via Kleene conjunction (def:box-verdict).

Kleene truth table exercised:
  Conflict × Conflict   → Conflict   (Rule 1)
  Conflict × Compatible → Conflict   (Rule 1 — key case!)
  Compatible × Conflict → Conflict   (Rule 1 — commutative)
  Compatible × Compatible → Compatible (Rule 2)
"""

from .models import Benchmark, Category, Constraint, Op, SZS, Verdict


def _make_box2d_policy_ttl(b: Benchmark) -> str:
    """ODRL policy snippet for 2-axis (width × height) constraints."""
    c1w, c2w = b.c1, b.c2
    c1h, c2h = b.c1_ax2, b.c2_ax2
    return f"""\
%   @prefix odrl: <http://www.w3.org/ns/odrl/2/> .
%   @prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
%   @prefix ex:   <https://example.org/> .
%
%   ex:policyA a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSize{c1w.axis.title()} ;
%         odrl:operator odrl:{c1w.op.value} ;
%         odrl:rightOperand "{c1w.value}"^^xsd:decimal ;
%         odrl:unit <http://dbpedia.org/resource/Pixel> ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSize{c1h.axis.title()} ;
%         odrl:operator odrl:{c1h.op.value} ;
%         odrl:rightOperand "{c1h.value}"^^xsd:decimal ;
%         odrl:unit <http://dbpedia.org/resource/Pixel> ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSize{c2w.axis.title()} ;
%         odrl:operator odrl:{c2w.op.value} ;
%         odrl:rightOperand "{c2w.value}"^^xsd:decimal ;
%         odrl:unit <http://dbpedia.org/resource/Pixel> ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSize{c2h.axis.title()} ;
%         odrl:operator odrl:{c2h.op.value} ;
%         odrl:rightOperand "{c2h.value}"^^xsd:decimal ;
%         odrl:unit <http://dbpedia.org/resource/Pixel> ] ] ."""


def box_2d_benchmarks() -> list[Benchmark]:
    """Category B: Two-axis (width × height) box intersection."""
    benchmarks = []

    # --- BSB Running Example (from the paper) ---

    benchmarks.append(Benchmark(
        number=320, name="bsb-box-conflict",
        category=Category.BOX_2D,
        # Width: ≤600 vs ≥1200 → Conflict
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.GTEQ, 1200),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="BSB: width conflict × height compatible → box Conflict",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        # Height: ≤600 vs ≥400 → Compatible
        c1_ax2=Constraint("height", Op.LTEQ, 600),
        c2_ax2=Constraint("height", Op.GTEQ, 400),
        domain2_lo=0, domain2_lo_open=True,
        notes="Paper running example. Kleene Rule 1: conflict ⊗ compatible = conflict.",
    ))

    # --- Conflict × Conflict → Conflict (both axes disjoint) ---

    benchmarks.append(Benchmark(
        number=321, name="both-conflict",
        category=Category.BOX_2D,
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.GTEQ, 800),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="Both axes conflict → box Conflict",
        difficulty="Easy",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("height", Op.LTEQ, 300),
        c2_ax2=Constraint("height", Op.GTEQ, 500),
        domain2_lo=0, domain2_lo_open=True,
    ))

    # --- Compatible × Conflict → Conflict (swapped from BSB) ---

    benchmarks.append(Benchmark(
        number=322, name="compat-then-conflict",
        category=Category.BOX_2D,
        # Width: ≤800 vs ≥200 → Compatible
        c1=Constraint("width", Op.LTEQ, 800),
        c2=Constraint("width", Op.GTEQ, 200),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="Width compatible, height conflict → box Conflict",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        # Height: ≤300 vs ≥500 → Conflict
        c1_ax2=Constraint("height", Op.LTEQ, 300),
        c2_ax2=Constraint("height", Op.GTEQ, 500),
        domain2_lo=0, domain2_lo_open=True,
        notes="Kleene Rule 1: compatible ⊗ conflict = conflict (commutativity).",
    ))

    # --- Compatible × Compatible → Compatible ---

    benchmarks.append(Benchmark(
        number=323, name="both-compatible",
        category=Category.BOX_2D,
        c1=Constraint("width", Op.LTEQ, 800),
        c2=Constraint("width", Op.GTEQ, 200),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="Both axes compatible → box Compatible",
        difficulty="Easy",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("height", Op.LTEQ, 600),
        c2_ax2=Constraint("height", Op.GTEQ, 100),
        domain2_lo=0, domain2_lo_open=True,
        notes="Kleene Rule 2: compatible ⊗ compatible = compatible.",
    ))

    benchmarks.append(Benchmark(
        number=324, name="both-compatible-eq",
        category=Category.BOX_2D,
        # Width: =600 vs ≤800 → Compatible (point inside)
        c1=Constraint("width", Op.EQ, 600),
        c2=Constraint("width", Op.LTEQ, 800),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="Width eq+lteq, height overlap → box Compatible",
        difficulty="Easy",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("height", Op.GTEQ, 200),
        c2_ax2=Constraint("height", Op.LTEQ, 600),
        domain2_lo=0, domain2_lo_open=True,
    ))

    # --- Boundary cases: touching at a single point ---

    benchmarks.append(Benchmark(
        number=325, name="touch-both-axes",
        category=Category.BOX_2D,
        # Width: ≤600 vs ≥600 → Compatible (touch at 600)
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.GTEQ, 600),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="Both axes touch → single-point box Compatible",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        # Height: ≤400 vs ≥400 → Compatible (touch at 400)
        c1_ax2=Constraint("height", Op.LTEQ, 400),
        c2_ax2=Constraint("height", Op.GTEQ, 400),
        domain2_lo=0, domain2_lo_open=True,
        notes="Witness: (600, 400). Box intersection is a single point.",
    ))

    benchmarks.append(Benchmark(
        number=326, name="touch-one-conflict-other",
        category=Category.BOX_2D,
        # Width: ≤600 vs ≥600 → Compatible (touch)
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.GTEQ, 600),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="Width touches, height conflicts → box Conflict",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        # Height: ≤300 vs ≥500 → Conflict
        c1_ax2=Constraint("height", Op.LTEQ, 300),
        c2_ax2=Constraint("height", Op.GTEQ, 500),
        domain2_lo=0, domain2_lo_open=True,
    ))

    # --- Open boundary + density ---

    benchmarks.append(Benchmark(
        number=327, name="open-open-compatible",
        category=Category.BOX_2D,
        # Width: >200 vs <800 → Compatible (open overlap)
        c1=Constraint("width", Op.GT, 200),
        c2=Constraint("width", Op.LT, 800),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="Both axes open intervals, overlapping → Compatible",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        needs_density=True,
        # Height: >100 vs <500 → Compatible
        c1_ax2=Constraint("height", Op.GT, 100),
        c2_ax2=Constraint("height", Op.LT, 500),
        domain2_lo=0, domain2_lo_open=True,
    ))

    benchmarks.append(Benchmark(
        number=328, name="open-boundary-conflict",
        category=Category.BOX_2D,
        # Width: <600 vs ≥600 → Conflict (open/closed)
        c1=Constraint("width", Op.LT, 600),
        c2=Constraint("width", Op.GTEQ, 600),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="Width open/closed boundary conflict × height compatible",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        needs_density=True,
        # Height: ≤800 vs ≥200 → Compatible
        c1_ax2=Constraint("height", Op.LTEQ, 800),
        c2_ax2=Constraint("height", Op.GTEQ, 200),
        domain2_lo=0, domain2_lo_open=True,
        notes="Tests that open-boundary conflict on one axis kills the box.",
    ))

    # --- Asymmetric: narrow strip ---

    benchmarks.append(Benchmark(
        number=329, name="narrow-strip-compatible",
        category=Category.BOX_2D,
        # Width: ≥500 vs ≤510 → Compatible (narrow: [500,510])
        c1=Constraint("width", Op.GTEQ, 500),
        c2=Constraint("width", Op.LTEQ, 510),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="Narrow width strip × wide height → Compatible",
        difficulty="Easy",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("height", Op.GTEQ, 100),
        c2_ax2=Constraint("height", Op.LTEQ, 900),
        domain2_lo=0, domain2_lo_open=True,
    ))

    benchmarks.append(Benchmark(
        number=330, name="near-miss-conflict",
        category=Category.BOX_2D,
        # Width: ≤599 vs ≥601 → Conflict (gap of 1)
        c1=Constraint("width", Op.LTEQ, 599),
        c2=Constraint("width", Op.GTEQ, 601),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="Width near-miss (gap=1) × height compatible → Conflict",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("height", Op.LTEQ, 800),
        c2_ax2=Constraint("height", Op.GTEQ, 200),
        domain2_lo=0, domain2_lo_open=True,
        notes="Tests that even a tiny gap on one axis causes box Conflict.",
    ))

    # Generate policy TTL for all
    for b_ in benchmarks:
        b_.policy_ttl = _make_box2d_policy_ttl(b_)

    return benchmarks
