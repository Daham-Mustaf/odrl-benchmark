"""Category E: Cross-domain aggregation.

ODRL 380–391 (12 benchmarks).

Tests def:cross-domain: aggregating verdicts from DIFFERENT leftOperand
families using the same Kleene conjunction as box-level aggregation.

Key paper claim: box_verdict serves BOTH within-domain (e.g. width × height)
and cross-domain (e.g. spatial × temporal × count) aggregation because
K_3 conjunction is associative, commutative, and domain-agnostic.

Axis semantics (heterogeneous domains):
  - Axis 1 (X) : spatial — absoluteSizeWidth, pixels, domain (0, ∞)
  - Axis 2 (Y) : temporal — dateTime as ordinal day, domain [0, ∞)
  - Axis 3 (Z) : count — number of permitted uses, domain [0, ∞)
  - Axis 4 (W) : financial — payAmount in EUR cents, domain [0, ∞)

Note: Temporal values use ordinal encoding (days since epoch).
  2024-01-01 = 0, 2024-06-30 = 181, 2024-12-31 = 365, 2025-06-30 = 546
"""

from .models import Benchmark, Category, Constraint, Op, SZS, Verdict


def _make_cross_domain_policy_ttl(b: Benchmark) -> str:
    """ODRL policy snippet for cross-domain constraints."""
    c1s, c2s = b.c1, b.c2           # spatial
    c1t, c2t = b.c1_ax2, b.c2_ax2   # temporal
    c1c, c2c = b.c1_ax3, b.c2_ax3   # count
    c1f, c2f = b.c1_ax4, b.c2_ax4   # financial

    # Build constraint blocks, skipping None axes
    def _constraint_block(c, prefix=""):
        blocks = []
        if c is None:
            return blocks
        ax = c.axis
        if ax == "width":
            blocks.append(f"%{prefix}       odrl:constraint [")
            blocks.append(f"%{prefix}         odrl:leftOperand oax:absoluteSizeWidth ;")
            blocks.append(f"%{prefix}         odrl:operator odrl:{c.op.value} ;")
            blocks.append(f"%{prefix}         odrl:rightOperand \"{c.value}\"^^xsd:decimal ;")
            blocks.append(f"%{prefix}         odrl:unit <http://dbpedia.org/resource/Pixel> ]")
        elif ax == "dateTime":
            blocks.append(f"%{prefix}       odrl:constraint [")
            blocks.append(f"%{prefix}         odrl:leftOperand odrl:dateTime ;")
            blocks.append(f"%{prefix}         odrl:operator odrl:{c.op.value} ;")
            blocks.append(f"%{prefix}         odrl:rightOperand \"{int(c.value)}\"^^xsd:integer ]")
        elif ax == "count":
            blocks.append(f"%{prefix}       odrl:constraint [")
            blocks.append(f"%{prefix}         odrl:leftOperand odrl:count ;")
            blocks.append(f"%{prefix}         odrl:operator odrl:{c.op.value} ;")
            blocks.append(f"%{prefix}         odrl:rightOperand \"{int(c.value)}\"^^xsd:integer ]")
        elif ax == "payAmount":
            blocks.append(f"%{prefix}       odrl:constraint [")
            blocks.append(f"%{prefix}         odrl:leftOperand odrl:payAmount ;")
            blocks.append(f"%{prefix}         odrl:operator odrl:{c.op.value} ;")
            blocks.append(f"%{prefix}         odrl:rightOperand \"{c.value}\"^^xsd:decimal ;")
            blocks.append(f"%{prefix}         odrl:unit <http://dbpedia.org/resource/Euro> ]")
        return blocks

    lines = []
    lines.append("%   @prefix odrl: <http://www.w3.org/ns/odrl/2/> .")
    lines.append("%   @prefix oax:  <http://w3id.org/odrl/spatial-axis#> .")
    lines.append("%   @prefix ex:   <https://example.org/> .")
    lines.append("%")
    lines.append("%   ex:policyA a odrl:Set ;")
    lines.append("%     odrl:permission [")
    lines.append("%       odrl:action odrl:use ;")
    for c in [c1s, c1t, c1c, c1f]:
        for bl in _constraint_block(c, "  "):
            lines.append(bl)
    lines.append("%     ] .")
    lines.append("%")
    lines.append("%   ex:policyB a odrl:Set ;")
    lines.append("%     odrl:permission [")
    lines.append("%       odrl:action odrl:use ;")
    for c in [c2s, c2t, c2c, c2f]:
        for bl in _constraint_block(c, "  "):
            lines.append(bl)
    lines.append("%     ] .")
    return "\n".join(lines)


def cross_domain_benchmarks() -> list[Benchmark]:
    """Category E: Cross-domain aggregation (spatial × temporal × count × financial)."""
    benchmarks = []

    # ------------------------------------------------------------------
    # 2-domain: spatial × temporal
    # ------------------------------------------------------------------

    # Spatial compatible, temporal compatible → Compatible
    benchmarks.append(Benchmark(
        number=380, name="spatial-temporal-compatible",
        category=Category.CROSS_DOMAIN,
        # width: ≤800 vs ≥200 → Compatible
        c1=Constraint("width", Op.LTEQ, 800),
        c2=Constraint("width", Op.GTEQ, 200),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="Spatial compatible × temporal compatible → Compatible",
        difficulty="Easy",
        domain_lo=0, domain_lo_open=True,
        # dateTime: ≤365 vs ≥181 → Compatible (both within 2024)
        c1_ax2=Constraint("dateTime", Op.LTEQ, 365),
        c2_ax2=Constraint("dateTime", Op.GTEQ, 181),
        domain2_lo=0, domain2_lo_open=False,  # dateTime: [0, ∞)
        notes="Spatial (pixels) × temporal (ordinal days). Different domains, same algebra.",
    ))

    # Spatial compatible, temporal conflict → Conflict
    benchmarks.append(Benchmark(
        number=381, name="temporal-kills-spatial",
        category=Category.CROSS_DOMAIN,
        c1=Constraint("width", Op.LTEQ, 800),
        c2=Constraint("width", Op.GTEQ, 200),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="Temporal conflict kills spatial compatibility",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        # dateTime: ≤181 vs ≥365 → Conflict (H1 vs H2)
        c1_ax2=Constraint("dateTime", Op.LTEQ, 181),
        c2_ax2=Constraint("dateTime", Op.GTEQ, 365),
        domain2_lo=0, domain2_lo_open=False,
        notes="Shows cross-domain Kleene: one bad domain kills the whole policy.",
    ))

    # Spatial conflict, temporal compatible → Conflict
    benchmarks.append(Benchmark(
        number=382, name="spatial-kills-temporal",
        category=Category.CROSS_DOMAIN,
        # width: ≤400 vs ≥800 → Conflict
        c1=Constraint("width", Op.LTEQ, 400),
        c2=Constraint("width", Op.GTEQ, 800),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="Spatial conflict kills temporal compatibility",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("dateTime", Op.LTEQ, 365),
        c2_ax2=Constraint("dateTime", Op.GTEQ, 181),
        domain2_lo=0, domain2_lo_open=False,
        notes="Symmetric to ODRL381: conflict source doesn't matter.",
    ))

    # ------------------------------------------------------------------
    # 3-domain: spatial × temporal × count
    # ------------------------------------------------------------------

    benchmarks.append(Benchmark(
        number=383, name="three-domain-compatible",
        category=Category.CROSS_DOMAIN,
        c1=Constraint("width", Op.LTEQ, 800),
        c2=Constraint("width", Op.GTEQ, 200),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="Spatial × temporal × count all compatible",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("dateTime", Op.LTEQ, 365),
        c2_ax2=Constraint("dateTime", Op.GTEQ, 181),
        domain2_lo=0, domain2_lo_open=False,
        c1_ax3=Constraint("count", Op.LTEQ, 100),
        c2_ax3=Constraint("count", Op.GTEQ, 10),
        domain3_lo=0, domain3_lo_open=False,
    ))

    # Count conflict kills the other two
    benchmarks.append(Benchmark(
        number=384, name="count-kills-all",
        category=Category.CROSS_DOMAIN,
        c1=Constraint("width", Op.LTEQ, 800),
        c2=Constraint("width", Op.GTEQ, 200),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="Count conflict kills spatial+temporal compatibility",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("dateTime", Op.LTEQ, 365),
        c2_ax2=Constraint("dateTime", Op.GTEQ, 181),
        domain2_lo=0, domain2_lo_open=False,
        # count: ≤5 vs ≥50 → Conflict
        c1_ax3=Constraint("count", Op.LTEQ, 5),
        c2_ax3=Constraint("count", Op.GTEQ, 50),
        domain3_lo=0, domain3_lo_open=False,
        notes="Usage count conflict: ≤5 uses vs ≥50 uses.",
    ))

    # ------------------------------------------------------------------
    # 4-domain: spatial × temporal × count × financial
    # ------------------------------------------------------------------

    benchmarks.append(Benchmark(
        number=385, name="four-domain-compatible",
        category=Category.CROSS_DOMAIN,
        c1=Constraint("width", Op.LTEQ, 800),
        c2=Constraint("width", Op.GTEQ, 200),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="All 4 domains compatible",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("dateTime", Op.LTEQ, 365),
        c2_ax2=Constraint("dateTime", Op.GTEQ, 181),
        domain2_lo=0, domain2_lo_open=False,
        c1_ax3=Constraint("count", Op.LTEQ, 100),
        c2_ax3=Constraint("count", Op.GTEQ, 10),
        domain3_lo=0, domain3_lo_open=False,
        c1_ax4=Constraint("payAmount", Op.LTEQ, 5000),
        c2_ax4=Constraint("payAmount", Op.GTEQ, 1000),
        domain4_lo=0, domain4_lo_open=False,
        notes="Full heterogeneous composition: pixels × days × uses × EUR cents.",
    ))

    # Financial conflict kills all 3 compatible domains
    benchmarks.append(Benchmark(
        number=386, name="financial-kills-all",
        category=Category.CROSS_DOMAIN,
        c1=Constraint("width", Op.LTEQ, 800),
        c2=Constraint("width", Op.GTEQ, 200),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="Payment conflict kills 3 compatible domains",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("dateTime", Op.LTEQ, 365),
        c2_ax2=Constraint("dateTime", Op.GTEQ, 181),
        domain2_lo=0, domain2_lo_open=False,
        c1_ax3=Constraint("count", Op.LTEQ, 100),
        c2_ax3=Constraint("count", Op.GTEQ, 10),
        domain3_lo=0, domain3_lo_open=False,
        # payAmount: ≤1000 vs ≥5000 → Conflict
        c1_ax4=Constraint("payAmount", Op.LTEQ, 1000),
        c2_ax4=Constraint("payAmount", Op.GTEQ, 5000),
        domain4_lo=0, domain4_lo_open=False,
        notes="Provider caps at €10, consumer requires ≥€50. Incompatible.",
    ))

    # ------------------------------------------------------------------
    # Cross-domain subsumption
    # ------------------------------------------------------------------

    # Spatial ⊆ spatial AND temporal ⊆ temporal → Subsumes
    benchmarks.append(Benchmark(
        number=387, name="cross-domain-subsumption",
        category=Category.CROSS_DOMAIN,
        # width: ≤600 ⊆ ≤1200
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.LTEQ, 1200),
        verdict=Verdict.SUBSUMES, szs=SZS.THEOREM,
        description="Spatial + temporal: tighter box subsumes wider",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        # dateTime: ≤181 ⊆ ≤365
        c1_ax2=Constraint("dateTime", Op.LTEQ, 181),
        c2_ax2=Constraint("dateTime", Op.LTEQ, 365),
        domain2_lo=0, domain2_lo_open=False,
    ))

    # Temporal axis breaks cross-domain subsumption → Refuted
    benchmarks.append(Benchmark(
        number=388, name="temporal-breaks-subsumption",
        category=Category.CROSS_DOMAIN,
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.LTEQ, 1200),
        verdict=Verdict.REFUTED, szs=SZS.COUNTERSATISFIABLE,
        description="Temporal axis breaks cross-domain subsumption",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        # dateTime: ≤365 ⊄ ≤181 (A has wider window)
        c1_ax2=Constraint("dateTime", Op.LTEQ, 365),
        c2_ax2=Constraint("dateTime", Op.LTEQ, 181),
        domain2_lo=0, domain2_lo_open=False,
        notes="Counterexample: (1, 300). Width OK but date 300 > 181.",
    ))

    # ------------------------------------------------------------------
    # Open boundaries across domains
    # ------------------------------------------------------------------

    # Temporal with strict operators + density
    benchmarks.append(Benchmark(
        number=389, name="open-temporal-compatible",
        category=Category.CROSS_DOMAIN,
        c1=Constraint("width", Op.LTEQ, 800),
        c2=Constraint("width", Op.GTEQ, 200),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="Open temporal intervals + spatial overlap → Compatible",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        # dateTime: > 100 vs < 300 → Compatible (open overlap)
        c1_ax2=Constraint("dateTime", Op.GT, 100),
        c2_ax2=Constraint("dateTime", Op.LT, 300),
        domain2_lo=0, domain2_lo_open=False,
        needs_density=True,
    ))

    # Open temporal boundary conflict
    benchmarks.append(Benchmark(
        number=390, name="open-temporal-conflict",
        category=Category.CROSS_DOMAIN,
        c1=Constraint("width", Op.LTEQ, 800),
        c2=Constraint("width", Op.GTEQ, 200),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="Open/closed temporal boundary conflict kills spatial",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        # dateTime: < 181 vs ≥ 181 → Conflict (open/closed)
        c1_ax2=Constraint("dateTime", Op.LT, 181),
        c2_ax2=Constraint("dateTime", Op.GTEQ, 181),
        domain2_lo=0, domain2_lo_open=False,
        needs_density=True,
        notes="Temporal open/closed boundary: <June30 vs ≥June30.",
    ))

    # ------------------------------------------------------------------
    # Realistic Datenraum Kultur scenario
    # ------------------------------------------------------------------

    benchmarks.append(Benchmark(
        number=391, name="drk-image-policy-conflict",
        category=Category.CROSS_DOMAIN,
        # Spatial: museum allows ≤600px, researcher needs ≥1200px
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.GTEQ, 1200),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="DRK scenario: museum thumbnail vs researcher high-res → Conflict",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        # Temporal: museum allows until day 365, researcher needs from day 181
        c1_ax2=Constraint("dateTime", Op.LTEQ, 365),
        c2_ax2=Constraint("dateTime", Op.GTEQ, 181),
        domain2_lo=0, domain2_lo_open=False,
        # Count: museum allows ≤10 uses, researcher needs ≥5
        c1_ax3=Constraint("count", Op.LTEQ, 10),
        c2_ax3=Constraint("count", Op.GTEQ, 5),
        domain3_lo=0, domain3_lo_open=False,
        notes="Datenraum Kultur: spatial conflict dominates despite temporal+count compatibility.",
    ))

    # Generate policy TTL
    for b_ in benchmarks:
        b_.policy_ttl = _make_cross_domain_policy_ttl(b_)

    return benchmarks
