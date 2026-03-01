"""Category F: Policy quality — difficulty ladder from trivial to stress-test.

ODRL 400–415 (16 benchmarks).

Designed to expose prover performance scaling.  Each benchmark increases
one or more difficulty parameters:

  Difficulty drivers:
    D1  Number of distinct named constants  (3 → 12+)
    D2  Number of axes                      (1 → 4)
    D3  Open/closed boundary mix            (all closed → all open)
    D4  Density axiom requirement           (no → yes, all axes)
    D5  Verdict type complexity             (conflict → subsumption w/ De Morgan)
    D6  Near-miss numerical margins         (gap=200 → gap=0.5)
    D7  Operator variety                    (single op → all 5 O_δ)

Rating scale:
    Trivial    — 1 axis, 2–3 constants, closed
    Easy       — 1–2 axes, 4–5 constants
    Medium     — 2–3 axes, 5–7 constants, some open
    Hard       — 3–4 axes, 8–9 constants, density, near-miss
    Very Hard  — 4 axes, 10–12 constants, all open, density,
                         De Morgan subsumption, gap < 1
"""

from .models import Benchmark, Category, Constraint, Op, SZS, Verdict


def _make_pq_policy_ttl(b: Benchmark) -> str:
    """Minimal TTL for policy quality benchmarks."""
    lines = [
        "%   @prefix odrl: <http://www.w3.org/ns/odrl/2/> .",
        "%   @prefix oax:  <http://w3id.org/odrl/spatial-axis#> .",
        "%   @prefix ex:   <https://example.org/> .",
    ]

    # Map axis names to proper ontology IRIs
    AXIS_TO_IRI = {
        "width": "oax:absoluteSizeWidth",
        "height": "oax:absoluteSizeHeight",
        "depth": "oax:absoluteSizeDepth",
        "resolution": "odrl:resolution",
        "dateTime": "odrl:dateTime",
        "count": "odrl:count",
        "payAmount": "odrl:payAmount",
    }

    def _axis_label(c):
        return c.axis_iri if c.axis_iri else AXIS_TO_IRI.get(c.axis, f"oax:{c.axis}")

    axes_a = [b.c1]
    axes_b = [b.c2]
    if b.c1_ax2:
        axes_a.append(b.c1_ax2); axes_b.append(b.c2_ax2)
    if b.c1_ax3:
        axes_a.append(b.c1_ax3); axes_b.append(b.c2_ax3)
    if b.c1_ax4:
        axes_a.append(b.c1_ax4); axes_b.append(b.c2_ax4)

    for label, axes in [("policyA", axes_a), ("policyB", axes_b)]:
        lines.append(f"%")
        lines.append(f"%   ex:{label} a odrl:Set ;")
        lines.append(f"%     odrl:permission [")
        lines.append(f"%       odrl:action odrl:use ;")
        for c in axes:
            lines.append(f"%       odrl:constraint [")
            lines.append(f"%         odrl:leftOperand {_axis_label(c)} ;")
            lines.append(f"%         odrl:operator odrl:{c.op.value} ;")
            lines.append(f"%         odrl:rightOperand \"{c.value}\"^^xsd:decimal ] ;")
        lines.append(f"%     ] .")

    return "\n".join(lines)


def policy_quality_benchmarks() -> list[Benchmark]:
    """Category F: Policy quality — graduated difficulty ladder."""
    benchmarks = []

    # ==================================================================
    # ★☆☆☆☆  TRIVIAL — warm-up, baseline timing
    # D1=3, D2=1, D3=closed, D4=no, D6=gap=200, D7=1 op pair
    # ==================================================================

    benchmarks.append(Benchmark(
        number=400, name="trivial-conflict",
        category=Category.POLICY_QUALITY,
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.GTEQ, 800),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="★☆☆☆☆ Trivial: 1 axis, 3 constants, gap=200",
        difficulty="Trivial",
        domain_lo=0, domain_lo_open=True,
    ))

    benchmarks.append(Benchmark(
        number=401, name="trivial-compatible",
        category=Category.POLICY_QUALITY,
        c1=Constraint("width", Op.LTEQ, 800),
        c2=Constraint("width", Op.GTEQ, 200),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="★☆☆☆☆ Trivial: 1 axis, 3 constants, wide overlap",
        difficulty="Trivial",
        domain_lo=0, domain_lo_open=True,
    ))

    # ==================================================================
    # ★★☆☆☆  EASY — introduce second axis, subsumption
    # D1=4–5, D2=1–2, D5=subsumption
    # ==================================================================

    benchmarks.append(Benchmark(
        number=402, name="easy-2axis-conflict",
        category=Category.POLICY_QUALITY,
        c1=Constraint("width", Op.LTEQ, 400),
        c2=Constraint("width", Op.GTEQ, 800),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="★★☆☆☆ Easy: 2 axes, 5 constants, closed intervals",
        difficulty="Easy",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("height", Op.LTEQ, 600),
        c2_ax2=Constraint("height", Op.GTEQ, 200),
        domain2_lo=0, domain2_lo_open=True,
    ))

    benchmarks.append(Benchmark(
        number=403, name="easy-subsumption",
        category=Category.POLICY_QUALITY,
        c1=Constraint("width", Op.LTEQ, 400),
        c2=Constraint("width", Op.LTEQ, 800),
        verdict=Verdict.SUBSUMES, szs=SZS.THEOREM,
        description="★★☆☆☆ Easy: 1 axis, simple subsumption",
        difficulty="Easy",
        domain_lo=0, domain_lo_open=True,
    ))

    # ==================================================================
    # ★★★☆☆  MEDIUM — open boundaries, density, mixed ops, near-miss
    # D1=5–7, D2=2–3, D3=mixed, D4=yes, D6=gap≤1, D7=3 ops
    # ==================================================================

    benchmarks.append(Benchmark(
        number=404, name="medium-open-boundary",
        category=Category.POLICY_QUALITY,
        # width: <600 vs ≥600 → Conflict (open/closed at same point)
        c1=Constraint("width", Op.LT, 600),
        c2=Constraint("width", Op.GTEQ, 600),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="★★★☆☆ Medium: 2 axes, open/closed boundary, density",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        needs_density=True,
        c1_ax2=Constraint("height", Op.LTEQ, 800),
        c2_ax2=Constraint("height", Op.GTEQ, 200),
        domain2_lo=0, domain2_lo_open=True,
    ))

    benchmarks.append(Benchmark(
        number=405, name="medium-3axis-mixed-ops",
        category=Category.POLICY_QUALITY,
        c1=Constraint("width", Op.EQ, 600),
        c2=Constraint("width", Op.LTEQ, 800),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="★★★☆☆ Medium: 3 axes, 7 constants, mixed ops (eq/gteq/lteq)",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("height", Op.GTEQ, 200),
        c2_ax2=Constraint("height", Op.LTEQ, 400),
        domain2_lo=0, domain2_lo_open=True,
        c1_ax3=Constraint("depth", Op.LTEQ, 32),
        c2_ax3=Constraint("depth", Op.GTEQ, 16),
        domain3_lo=0, domain3_lo_open=True,
    ))

    benchmarks.append(Benchmark(
        number=406, name="medium-near-miss-gap1",
        category=Category.POLICY_QUALITY,
        # width: ≤599 vs ≥601 → Conflict (gap=2, but small)
        c1=Constraint("width", Op.LTEQ, 599),
        c2=Constraint("width", Op.GTEQ, 601),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="★★★☆☆ Medium: 2 axes, near-miss gap=2 on both axes",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("height", Op.LTEQ, 399),
        c2_ax2=Constraint("height", Op.GTEQ, 401),
        domain2_lo=0, domain2_lo_open=True,
    ))

    benchmarks.append(Benchmark(
        number=407, name="medium-2axis-subsumption",
        category=Category.POLICY_QUALITY,
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.LTEQ, 1200),
        verdict=Verdict.SUBSUMES, szs=SZS.THEOREM,
        description="★★★☆☆ Medium: 2-axis subsumption with De Morgan",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("height", Op.LTEQ, 400),
        c2_ax2=Constraint("height", Op.LTEQ, 800),
        domain2_lo=0, domain2_lo_open=True,
    ))

    # ==================================================================
    # ★★★★☆  HARD — 4 axes, many constants, density, near-miss
    # D1=8–9, D2=3–4, D3=mixed, D4=yes, D5=all verdicts, D6=gap=1
    # ==================================================================

    benchmarks.append(Benchmark(
        number=408, name="hard-4axis-near-miss",
        category=Category.POLICY_QUALITY,
        # gap=1 on width, 3 other axes compatible
        c1=Constraint("width", Op.LTEQ, 599),
        c2=Constraint("width", Op.GTEQ, 601),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="★★★★☆ Hard: 4 axes, 9 constants, gap=1 on width",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("height", Op.LTEQ, 1080),
        c2_ax2=Constraint("height", Op.GTEQ, 480),
        domain2_lo=0, domain2_lo_open=True,
        c1_ax3=Constraint("depth", Op.LTEQ, 32),
        c2_ax3=Constraint("depth", Op.GTEQ, 8),
        domain3_lo=0, domain3_lo_open=True,
        c1_ax4=Constraint("resolution", Op.LTEQ, 300),
        c2_ax4=Constraint("resolution", Op.GTEQ, 72),
        domain4_lo=0, domain4_lo_open=True,
    ))

    benchmarks.append(Benchmark(
        number=409, name="hard-all-open-4axis",
        category=Category.POLICY_QUALITY,
        c1=Constraint("width", Op.GT, 200),
        c2=Constraint("width", Op.LT, 800),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="★★★★☆ Hard: 4 axes, all open intervals, density on all axes",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        needs_density=True,
        c1_ax2=Constraint("height", Op.GT, 100),
        c2_ax2=Constraint("height", Op.LT, 500),
        domain2_lo=0, domain2_lo_open=True,
        c1_ax3=Constraint("depth", Op.GT, 8),
        c2_ax3=Constraint("depth", Op.LT, 32),
        domain3_lo=0, domain3_lo_open=True,
        c1_ax4=Constraint("resolution", Op.GT, 72),
        c2_ax4=Constraint("resolution", Op.LT, 300),
        domain4_lo=0, domain4_lo_open=True,
    ))

    benchmarks.append(Benchmark(
        number=410, name="hard-4axis-subsumption",
        category=Category.POLICY_QUALITY,
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.LTEQ, 1920),
        verdict=Verdict.SUBSUMES, szs=SZS.THEOREM,
        description="★★★★☆ Hard: 4-axis De Morgan subsumption, 8 constants",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("height", Op.LTEQ, 400),
        c2_ax2=Constraint("height", Op.LTEQ, 1080),
        domain2_lo=0, domain2_lo_open=True,
        c1_ax3=Constraint("depth", Op.LTEQ, 16),
        c2_ax3=Constraint("depth", Op.LTEQ, 48),
        domain3_lo=0, domain3_lo_open=True,
        c1_ax4=Constraint("resolution", Op.LTEQ, 150),
        c2_ax4=Constraint("resolution", Op.LTEQ, 600),
        domain4_lo=0, domain4_lo_open=True,
        notes="4-way De Morgan: (or not-w not-h not-d not-r). All branches unsat.",
    ))

    benchmarks.append(Benchmark(
        number=411, name="hard-all-ops-3axis",
        category=Category.POLICY_QUALITY,
        # All 5 operators + density + near-miss
        # width: =600 vs =601 → Conflict (distinct points, gap=1)
        c1=Constraint("width", Op.EQ, 600),
        c2=Constraint("width", Op.EQ, 601),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="★★★★☆ Hard: all 5 ops, gap=1, density, 3 axes",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        needs_density=True,
        # height: >300 vs <500 → Compatible (open)
        c1_ax2=Constraint("height", Op.GT, 300),
        c2_ax2=Constraint("height", Op.LT, 500),
        domain2_lo=0, domain2_lo_open=True,
        # depth: ≥16 vs ≤32 → Compatible (closed)
        c1_ax3=Constraint("depth", Op.GTEQ, 16),
        c2_ax3=Constraint("depth", Op.LTEQ, 32),
        domain3_lo=0, domain3_lo_open=True,
        notes="All 5 O_delta operators: eq*2, gt, lt, gteq, lteq. Gap=1 kills box.",
    ))

    # ==================================================================
    # ★★★★★  VERY HARD — maximum parameters, stress-test
    # D1=10–12, D2=4, D3=all open, D4=yes, D5=De Morgan, D6=gap<1, D7=all 5
    # ==================================================================

    # 412: 12 distinct constants, all open, density, gap=0.5 on every axis
    benchmarks.append(Benchmark(
        number=412, name="vhard-12-constants-fractional-gap",
        category=Category.POLICY_QUALITY,
        # width: <599.5 vs >=600 → Conflict (gap=0.5)
        c1=Constraint("width", Op.LT, 599.5),
        c2=Constraint("width", Op.GTEQ, 600),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="★★★★★ Very Hard: 12 constants, all open, fractional gap=0.5",
        difficulty="Very Hard",
        # different domain_lo per axis → maximises distinct constants
        domain_lo=1, domain_lo_open=True,
        needs_density=True,
        # height: >479.5 vs <480 → Conflict (gap=0.5, both open)
        c1_ax2=Constraint("height", Op.GT, 479.5),
        c2_ax2=Constraint("height", Op.LT, 480),
        domain2_lo=2, domain2_lo_open=True,
        # depth: >15.5 vs <16 → Conflict (gap=0.5)
        c1_ax3=Constraint("depth", Op.GT, 15.5),
        c2_ax3=Constraint("depth", Op.LT, 16),
        domain3_lo=3, domain3_lo_open=True,
        # resolution: <71.5 vs >=72 → Conflict (gap=0.5)
        c1_ax4=Constraint("resolution", Op.LT, 71.5),
        c2_ax4=Constraint("resolution", Op.GTEQ, 72),
        domain4_lo=4, domain4_lo_open=True,
        notes="12 distinct values → C(12,2)=66 ordering axioms. "
              "All 4 axes conflict with gap=0.5.",
    ))

    # 413: 12 distinct constants, razor-thin compatible overlap=0.5
    benchmarks.append(Benchmark(
        number=413, name="vhard-12-constants-razor-overlap",
        category=Category.POLICY_QUALITY,
        # width: <=600.5 vs >=600 → Compatible (overlap=0.5)
        c1=Constraint("width", Op.LTEQ, 600.5),
        c2=Constraint("width", Op.GTEQ, 600),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="★★★★★ Very Hard: 12 constants, razor-thin 4D overlap=0.5",
        difficulty="Very Hard",
        domain_lo=1, domain_lo_open=True,
        needs_density=True,
        # height: <=480.5 vs >=480 → Compatible (overlap=0.5)
        c1_ax2=Constraint("height", Op.LTEQ, 480.5),
        c2_ax2=Constraint("height", Op.GTEQ, 480),
        domain2_lo=2, domain2_lo_open=True,
        # depth: <=16.5 vs >=16 → Compatible (overlap=0.5)
        c1_ax3=Constraint("depth", Op.LTEQ, 16.5),
        c2_ax3=Constraint("depth", Op.GTEQ, 16),
        domain3_lo=3, domain3_lo_open=True,
        # resolution: <=72.5 vs >=72 → Compatible (overlap=0.5)
        c1_ax4=Constraint("resolution", Op.LTEQ, 72.5),
        c2_ax4=Constraint("resolution", Op.GTEQ, 72),
        domain4_lo=4, domain4_lo_open=True,
        notes="12 distinct values → 66 ordering axioms. "
              "Each axis overlaps by exactly 0.5. "
              "Witness: (600.25, 480.25, 16.25, 72.25).",
    ))

    # 414: All 5 operators, 4-axis De Morgan refutation
    benchmarks.append(Benchmark(
        number=414, name="vhard-all-ops-refuted",
        category=Category.POLICY_QUALITY,
        # A: width =600, height >300, depth >=16, resolution <300
        # B: width <=1920, height <1080, depth <=48, resolution >=72
        # A not-subset B because resolution: <300 not-subset >=72 (res=50)
        c1=Constraint("width", Op.EQ, 600),
        c2=Constraint("width", Op.LTEQ, 1920),
        verdict=Verdict.REFUTED, szs=SZS.COUNTERSATISFIABLE,
        description="★★★★★ Very Hard: all 5 ops, 4-axis De Morgan refutation",
        difficulty="Very Hard",
        domain_lo=1, domain_lo_open=True,
        needs_density=True,
        c1_ax2=Constraint("height", Op.GT, 300),
        c2_ax2=Constraint("height", Op.LT, 1080),
        domain2_lo=2, domain2_lo_open=True,
        c1_ax3=Constraint("depth", Op.GTEQ, 16),
        c2_ax3=Constraint("depth", Op.LTEQ, 48),
        domain3_lo=3, domain3_lo_open=True,
        c1_ax4=Constraint("resolution", Op.LT, 300),
        c2_ax4=Constraint("resolution", Op.GTEQ, 72),
        domain4_lo=4, domain4_lo_open=True,
        notes="All 5 ops (eq, gt, gteq, lt, lteq). "
              "De Morgan: (or not-w not-h not-d not-r). "
              "Counterexample: (600, 301, 16, 50) — res 50 < 72.",
    ))

    # 415: 12 distinct constants, tight 4-axis De Morgan subsumption
    benchmarks.append(Benchmark(
        number=415, name="vhard-12-constants-tight-subsumption",
        category=Category.POLICY_QUALITY,
        # Each axis: A subset B by margin=1 (fractional bounds)
        c1=Constraint("width", Op.LTEQ, 599.5),
        c2=Constraint("width", Op.LTEQ, 600.5),
        verdict=Verdict.SUBSUMES, szs=SZS.THEOREM,
        description="★★★★★ Very Hard: 12 constants, 4-axis tight subsumption (margin=1)",
        difficulty="Very Hard",
        domain_lo=1, domain_lo_open=True,
        c1_ax2=Constraint("height", Op.LTEQ, 479.5),
        c2_ax2=Constraint("height", Op.LTEQ, 480.5),
        domain2_lo=2, domain2_lo_open=True,
        c1_ax3=Constraint("depth", Op.LTEQ, 15.5),
        c2_ax3=Constraint("depth", Op.LTEQ, 16.5),
        domain3_lo=3, domain3_lo_open=True,
        c1_ax4=Constraint("resolution", Op.LTEQ, 71.5),
        c2_ax4=Constraint("resolution", Op.LTEQ, 72.5),
        domain4_lo=4, domain4_lo_open=True,
        notes="A subset B by margin=1 on each axis. 66 ordering axioms. "
              "4-way De Morgan: all 4 disjuncts must be proven unsatisfiable.",
    ))

    # 416: 4D single-point witness — hardest existential
    benchmarks.append(Benchmark(
        number=416, name="vhard-single-point-4d",
        category=Category.POLICY_QUALITY,
        # All 4 axes touch at exactly one point
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.GTEQ, 600),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="★★★★★ Very Hard: 4D single-point witness (600,480,16,72)",
        difficulty="Very Hard",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("height", Op.LTEQ, 480),
        c2_ax2=Constraint("height", Op.GTEQ, 480),
        domain2_lo=0, domain2_lo_open=True,
        c1_ax3=Constraint("depth", Op.LTEQ, 16),
        c2_ax3=Constraint("depth", Op.GTEQ, 16),
        domain3_lo=0, domain3_lo_open=True,
        c1_ax4=Constraint("resolution", Op.LTEQ, 72),
        c2_ax4=Constraint("resolution", Op.GTEQ, 72),
        domain4_lo=0, domain4_lo_open=True,
        notes="Box intersection is the single point (600,480,16,72). "
              "Prover must find the unique 4D witness.",
    ))

    # Generate policy TTL
    for b_ in benchmarks:
        b_.policy_ttl = _make_pq_policy_ttl(b_)

    return benchmarks
