"""Category G: Boundary — open/closed endpoint semantics.

ODRL 420–435 (16 benchmarks).

Systematically tests the 10 distinct operator pairs at the SAME value v,
which is where open/closed boundary semantics determine the verdict.

The 10 operator pairs at value v (with expected 1D verdict):
  ──────────────────────────────────────────────────────────
  Pair  Op_A    Op_B    Boundary     Verdict      Density?
  ──────────────────────────────────────────────────────────
   P1   ≤v      ≥v      closed/closed  Compatible   no
   P2   ≤v      >v      closed/open    Conflict     no
   P3   <v      ≥v      open/closed    Conflict     no
   P4   <v      >v      open/open      Conflict     no
   P5   =v      ≤v      point ∈ ray    Compatible   no
   P6   =v      ≥v      point ∈ ray    Compatible   no
   P7   =v      <v      point ∉ open   Conflict     no
   P8   =v      >v      point ∉ open   Conflict     no
   P9   <v      ≤v      nested rays    Compatible   yes
   P10  >v      ≥v      nested rays    Compatible   yes
  ──────────────────────────────────────────────────────────

Plus multi-axis boundary interactions where individual axis
boundary types combine via Kleene conjunction.

All benchmarks use v=600 as the shared boundary point
(oax:absoluteSizeWidth in pixels).
"""

from .models import Benchmark, Category, Constraint, Op, SZS, Verdict


def _make_boundary_policy_ttl(b: Benchmark) -> str:
    """TTL snippet for boundary benchmarks."""
    AXIS_TO_IRI = {
        "width": "oax:absoluteSizeWidth",
        "height": "oax:absoluteSizeHeight",
        "depth": "oax:absoluteSizeDepth",
    }

    def _iri(c):
        return c.axis_iri if c.axis_iri else AXIS_TO_IRI.get(c.axis, f"oax:{c.axis}")

    axes_a = [b.c1]
    axes_b = [b.c2]
    if b.c1_ax2:
        axes_a.append(b.c1_ax2); axes_b.append(b.c2_ax2)
    if b.c1_ax3:
        axes_a.append(b.c1_ax3); axes_b.append(b.c2_ax3)

    lines = [
        "%   @prefix odrl: <http://www.w3.org/ns/odrl/2/> .",
        "%   @prefix oax:  <http://w3id.org/odrl/spatial-axis#> .",
        "%   @prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .",
        "%   @prefix ex:   <https://example.org/> .",
    ]

    for label, axes in [("policyA", axes_a), ("policyB", axes_b)]:
        lines.append(f"%")
        lines.append(f"%   ex:{label} a odrl:Set ;")
        lines.append(f"%     odrl:permission [")
        lines.append(f"%       odrl:action odrl:use ;")
        for c in axes:
            lines.append(f"%       odrl:constraint [")
            lines.append(f"%         odrl:leftOperand {_iri(c)} ;")
            lines.append(f"%         odrl:operator odrl:{c.op.value} ;")
            lines.append(f"%         odrl:rightOperand \"{c.value}\"^^xsd:decimal ] ;")
        lines.append(f"%     ] .")

    return "\n".join(lines)


def boundary_benchmarks() -> list[Benchmark]:
    """Category G: Boundary — all 10 operator pairs at the same value."""
    benchmarks = []
    V = 600  # shared boundary point

    # ==================================================================
    # Single-axis: the 10 operator pairs at v=600
    # ==================================================================

    # P1: ≤v ∧ ≥v → Compatible (closed/closed touch)
    benchmarks.append(Benchmark(
        number=420, name="P1-closed-closed-touch",
        category=Category.BOUNDARY,
        c1=Constraint("width", Op.LTEQ, V),
        c2=Constraint("width", Op.GTEQ, V),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="P1: ≤v ∧ ≥v → touch at v=600 → Compatible",
        difficulty="Easy",
        domain_lo=0, domain_lo_open=True,
        notes="Witness: X=600. The simplest boundary case.",
    ))

    # P2: ≤v ∧ >v → Conflict (closed/open mismatch)
    benchmarks.append(Benchmark(
        number=421, name="P2-closed-open-mismatch",
        category=Category.BOUNDARY,
        c1=Constraint("width", Op.LTEQ, V),
        c2=Constraint("width", Op.GT, V),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="P2: ≤v ∧ >v → gap at v=600 → Conflict",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        notes="(0,600] ∩ (600,∞) = ∅. The >v excludes the only touch point.",
    ))

    # P3: <v ∧ ≥v → Conflict (open/closed mismatch)
    benchmarks.append(Benchmark(
        number=422, name="P3-open-closed-mismatch",
        category=Category.BOUNDARY,
        c1=Constraint("width", Op.LT, V),
        c2=Constraint("width", Op.GTEQ, V),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="P3: <v ∧ ≥v → gap at v=600 → Conflict",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        notes="(0,600) ∩ [600,∞) = ∅. Symmetric to P2.",
    ))

    # P4: <v ∧ >v → Conflict (both open, double gap)
    benchmarks.append(Benchmark(
        number=423, name="P4-both-open-gap",
        category=Category.BOUNDARY,
        c1=Constraint("width", Op.LT, V),
        c2=Constraint("width", Op.GT, V),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="P4: <v ∧ >v → double gap at v=600 → Conflict",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        notes="(0,600) ∩ (600,∞) = ∅. Neither side includes v.",
    ))

    # P5: =v ∧ ≤v → Compatible (point inside closed ray)
    benchmarks.append(Benchmark(
        number=424, name="P5-eq-inside-lteq",
        category=Category.BOUNDARY,
        c1=Constraint("width", Op.EQ, V),
        c2=Constraint("width", Op.LTEQ, V),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="P5: =v ∧ ≤v → v ∈ (0,v] → Compatible",
        difficulty="Easy",
        domain_lo=0, domain_lo_open=True,
        notes="Witness: X=600. Point sits on the closed endpoint.",
    ))

    # P6: =v ∧ ≥v → Compatible (point inside closed ray)
    benchmarks.append(Benchmark(
        number=425, name="P6-eq-inside-gteq",
        category=Category.BOUNDARY,
        c1=Constraint("width", Op.EQ, V),
        c2=Constraint("width", Op.GTEQ, V),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="P6: =v ∧ ≥v → v ∈ [v,∞) → Compatible",
        difficulty="Easy",
        domain_lo=0, domain_lo_open=True,
        notes="Witness: X=600. Symmetric to P5.",
    ))

    # P7: =v ∧ <v → Conflict (point excluded by strict)
    benchmarks.append(Benchmark(
        number=426, name="P7-eq-excluded-by-lt",
        category=Category.BOUNDARY,
        c1=Constraint("width", Op.EQ, V),
        c2=Constraint("width", Op.LT, V),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="P7: =v ∧ <v → v ∉ (0,v) → Conflict",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        notes="{600} ∩ (0,600) = ∅. The strict < excludes the point.",
    ))

    # P8: =v ∧ >v → Conflict (point excluded by strict)
    benchmarks.append(Benchmark(
        number=427, name="P8-eq-excluded-by-gt",
        category=Category.BOUNDARY,
        c1=Constraint("width", Op.EQ, V),
        c2=Constraint("width", Op.GT, V),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="P8: =v ∧ >v → v ∉ (v,∞) → Conflict",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        notes="{600} ∩ (600,∞) = ∅. Symmetric to P7.",
    ))

    # P9: <v ∧ ≤v → Compatible (open ray nested in closed ray)
    benchmarks.append(Benchmark(
        number=428, name="P9-lt-inside-lteq",
        category=Category.BOUNDARY,
        c1=Constraint("width", Op.LT, V),
        c2=Constraint("width", Op.LTEQ, V),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="P9: <v ∧ ≤v → (0,v) ∩ (0,v] ≠ ∅ → Compatible",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        needs_density=True,
        notes="(0,600) ⊂ (0,600]. Needs density to produce witness in open interval.",
    ))

    # P10: >v ∧ ≥v → Compatible (open ray nested in closed ray)
    benchmarks.append(Benchmark(
        number=429, name="P10-gt-inside-gteq",
        category=Category.BOUNDARY,
        c1=Constraint("width", Op.GT, V),
        c2=Constraint("width", Op.GTEQ, V),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="P10: >v ∧ ≥v → (v,∞) ∩ [v,∞) ≠ ∅ → Compatible",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        needs_density=True,
        notes="(600,∞) ⊂ [600,∞). Needs density for witness.",
    ))

    # ==================================================================
    # Multi-axis boundary interactions
    # ==================================================================

    # 2-axis: both axes touch → Compatible (single point in R²)
    benchmarks.append(Benchmark(
        number=430, name="2axis-double-touch",
        category=Category.BOUNDARY,
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.GTEQ, 600),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="2 axes both touch → single point (600,400) → Compatible",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("height", Op.LTEQ, 400),
        c2_ax2=Constraint("height", Op.GTEQ, 400),
        domain2_lo=0, domain2_lo_open=True,
        notes="Witness: (600, 400). 2D single-point intersection.",
    ))

    # 2-axis: axis 1 touches, axis 2 has open gap → Conflict
    benchmarks.append(Benchmark(
        number=431, name="2axis-touch-plus-open-gap",
        category=Category.BOUNDARY,
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.GTEQ, 600),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="Axis 1 touches but axis 2 open gap → Conflict",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        # height: <400 vs ≥400 → P3 Conflict
        c1_ax2=Constraint("height", Op.LT, 400),
        c2_ax2=Constraint("height", Op.GTEQ, 400),
        domain2_lo=0, domain2_lo_open=True,
        notes="Width compatible at boundary, but height open/closed gap kills the box.",
    ))

    # 3-axis: mixed boundary types — all 3 touch but middle axis open
    benchmarks.append(Benchmark(
        number=432, name="3axis-mixed-boundary",
        category=Category.BOUNDARY,
        # width: ≤600 vs ≥600 → P1 touch Compatible
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.GTEQ, 600),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="3 axes: touch × open-gap × touch → Conflict",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        # height: ≤400 vs >400 → P2 Conflict (closed/open mismatch)
        c1_ax2=Constraint("height", Op.LTEQ, 400),
        c2_ax2=Constraint("height", Op.GT, 400),
        domain2_lo=0, domain2_lo_open=True,
        # depth: ≤200 vs ≥200 → P1 touch Compatible
        c1_ax3=Constraint("depth", Op.LTEQ, 200),
        c2_ax3=Constraint("depth", Op.GTEQ, 200),
        domain3_lo=0, domain3_lo_open=True,
        notes="Kleene: compatible ⊗ conflict ⊗ compatible = conflict. "
              "Middle axis P2 mismatch kills 3D box despite both edges touching.",
    ))

    # 2-axis boundary subsumption: ≤v subsumes <v (at boundary)
    benchmarks.append(Benchmark(
        number=433, name="boundary-subsumption-strict-inside-nonstrict",
        category=Category.BOUNDARY,
        # A: <600 ⊆ B: ≤600 ? Yes — (0,600) ⊆ (0,600]
        c1=Constraint("width", Op.LT, 600),
        c2=Constraint("width", Op.LTEQ, 600),
        verdict=Verdict.SUBSUMES, szs=SZS.THEOREM,
        description="<v ⊆ ≤v → strict ray inside non-strict → Subsumes",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        # height: ≤400 ⊆ ≤800
        c1_ax2=Constraint("height", Op.LTEQ, 400),
        c2_ax2=Constraint("height", Op.LTEQ, 800),
        domain2_lo=0, domain2_lo_open=True,
        notes="(0,600) ⊆ (0,600] is true. De Morgan: (or X>600 Y>800) — "
              "if X<600 then X≤600 always; if Y≤400 then Y≤800 always.",
    ))

    # 2-axis boundary refutation: ≤v does NOT subsume <v (direction reversed)
    benchmarks.append(Benchmark(
        number=434, name="boundary-refuted-nonstrict-exceeds-strict",
        category=Category.BOUNDARY,
        # A: ≤600 ⊆ B: <600 ? No — 600 ∈ A but 600 ∉ B
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.LT, 600),
        verdict=Verdict.REFUTED, szs=SZS.COUNTERSATISFIABLE,
        description="≤v ⊄ <v → endpoint 600 ∈ A, ∉ B → Refuted",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        needs_density=True,
        c1_ax2=Constraint("height", Op.LTEQ, 400),
        c2_ax2=Constraint("height", Op.LTEQ, 800),
        domain2_lo=0, domain2_lo_open=True,
        notes="Counterexample: (600, 1). Width 600 ≤ 600 but 600 ≮ 600. "
              "De Morgan disjunction: (or (not (< x 600)) (not (<= y 800))).",
    ))

    # 3-axis: all three at boundary, all compatible by different pair types
    benchmarks.append(Benchmark(
        number=435, name="3axis-all-boundary-compatible",
        category=Category.BOUNDARY,
        # width: =600 ∧ ≤600 → P5 Compatible
        c1=Constraint("width", Op.EQ, 600),
        c2=Constraint("width", Op.LTEQ, 600),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="3 axes: P5 × P1 × P6 — all boundary compatible",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        # height: ≤400 ∧ ≥400 → P1 touch Compatible
        c1_ax2=Constraint("height", Op.LTEQ, 400),
        c2_ax2=Constraint("height", Op.GTEQ, 400),
        domain2_lo=0, domain2_lo_open=True,
        # depth: =200 ∧ ≥200 → P6 Compatible
        c1_ax3=Constraint("depth", Op.EQ, 200),
        c2_ax3=Constraint("depth", Op.GTEQ, 200),
        domain3_lo=0, domain3_lo_open=True,
        notes="Witness: (600, 400, 200). Three different boundary-compatible "
              "pair types (P5, P1, P6) all hold simultaneously.",
    ))

    # Generate policy TTL
    for b_ in benchmarks:
        b_.policy_ttl = _make_boundary_policy_ttl(b_)

    return benchmarks
