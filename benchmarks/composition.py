"""Category D: Composition — 4-axis implicit AND conjunction.

ODRL 360–371 (12 benchmarks).

ODRL constraint connective: implicit AND (multiple odrl:constraint
on one odrl:Permission).  This is the standard ODRL pattern where
ALL constraints must be satisfied simultaneously:

    odrl:permission [
      odrl:constraint [ ... width  ≤ 800  ... ] ;   ← implicit
      odrl:constraint [ ... height ≤ 600  ... ] ;   ← conjunction
      odrl:constraint [ ... depth  ≤ 32   ... ] ;   ← (AND)
      odrl:constraint [ ... res    ≤ 300  ... ] ;
    ] .

Because AND × AND = AND, the conflict check decomposes per-axis:
  ∃(x,y,z,w): [c₁ᴬ(x) ∧ c₂ᴬ(y) ∧ c₃ᴬ(z) ∧ c₄ᴬ(w)]
             ∧ [c₁ᴮ(x) ∧ c₂ᴮ(y) ∧ c₃ᴮ(z) ∧ c₄ᴮ(w)]

Each axis is independent ⟹ box model ⟹ Kleene conjunction applies.

For odrl:or and odrl:xone (LogicalConstraint), see Category H
(LogicalOr) and Category I (LogicalXone), where axes are COUPLED
and the per-axis decomposition does NOT apply.

Tests nested Kleene conjunction at depth 4:
  box_verdict(V1, box_verdict(V2, box_verdict(V3, V4)))

Axes model a realistic image-constraint policy:
  - width      (X) : oax:absoluteSizeWidth,  domain (0, ∞)
  - height     (Y) : oax:absoluteSizeHeight, domain (0, ∞)
  - depth      (Z) : oax:absoluteSizeDepth,  domain (0, ∞)
  - resolution (W) : odrl:resolution,        domain (0, ∞)

Key properties exercised:
  - Associativity: conflict position in a 4-chain doesn't matter
  - Scaling: more named constants → larger ordering chain → harder
  - Mixed operators: different O_δ operators across axes
  - 4D subsumption and refutation with De Morgan disjunction
"""

from .models import Benchmark, Category, Constraint, Op, SZS, Verdict


def _make_composition_policy_ttl(b: Benchmark) -> str:
    """ODRL policy snippet for 4-axis constraints."""
    c1w, c2w = b.c1, b.c2
    c1h, c2h = b.c1_ax2, b.c2_ax2
    c1d, c2d = b.c1_ax3, b.c2_ax3
    c1r, c2r = b.c1_ax4, b.c2_ax4
    return f"""\
%   @prefix odrl: <http://www.w3.org/ns/odrl/2/> .
%   @prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
%   @prefix ex:   <https://example.org/> .
%
%   ex:policyA a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeWidth ;
%         odrl:operator odrl:{c1w.op.value} ;
%         odrl:rightOperand "{c1w.value}"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:{c1h.op.value} ;
%         odrl:rightOperand "{c1h.value}"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeDepth ;
%         odrl:operator odrl:{c1d.op.value} ;
%         odrl:rightOperand "{c1d.value}"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand odrl:resolution ;
%         odrl:operator odrl:{c1r.op.value} ;
%         odrl:rightOperand "{c1r.value}"^^xsd:decimal ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeWidth ;
%         odrl:operator odrl:{c2w.op.value} ;
%         odrl:rightOperand "{c2w.value}"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:{c2h.op.value} ;
%         odrl:rightOperand "{c2h.value}"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeDepth ;
%         odrl:operator odrl:{c2d.op.value} ;
%         odrl:rightOperand "{c2d.value}"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand odrl:resolution ;
%         odrl:operator odrl:{c2r.op.value} ;
%         odrl:rightOperand "{c2r.value}"^^xsd:decimal ] ] ."""


def composition_benchmarks() -> list[Benchmark]:
    """Category D: 4-axis composition (width × height × depth × resolution)."""
    benchmarks = []

    # ------------------------------------------------------------------
    # All compatible: 4-way Kleene conjunction = compatible
    # ------------------------------------------------------------------

    benchmarks.append(Benchmark(
        number=360, name="all-four-compatible",
        category=Category.COMPOSITION,
        c1=Constraint("width", Op.LTEQ, 800),
        c2=Constraint("width", Op.GTEQ, 200),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="All 4 axes compatible → box Compatible",
        difficulty="Easy",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("height", Op.LTEQ, 600),
        c2_ax2=Constraint("height", Op.GTEQ, 100),
        domain2_lo=0, domain2_lo_open=True,
        c1_ax3=Constraint("depth", Op.LTEQ, 32),
        c2_ax3=Constraint("depth", Op.GTEQ, 8),
        domain3_lo=0, domain3_lo_open=True,
        c1_ax4=Constraint("resolution", Op.LTEQ, 300),
        c2_ax4=Constraint("resolution", Op.GTEQ, 72),
        domain4_lo=0, domain4_lo_open=True,
        notes="Kleene: o ⊗ o ⊗ o ⊗ o = o.  Witness exists in 4D intersection.",
    ))

    # ------------------------------------------------------------------
    # Conflict at each position: tests associativity
    # ------------------------------------------------------------------

    # Conflict on axis 1 only
    benchmarks.append(Benchmark(
        number=361, name="conflict-at-axis-1",
        category=Category.COMPOSITION,
        c1=Constraint("width", Op.LTEQ, 400),
        c2=Constraint("width", Op.GTEQ, 800),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="Conflict on axis 1 of 4 → box Conflict",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("height", Op.LTEQ, 600),
        c2_ax2=Constraint("height", Op.GTEQ, 100),
        domain2_lo=0, domain2_lo_open=True,
        c1_ax3=Constraint("depth", Op.LTEQ, 32),
        c2_ax3=Constraint("depth", Op.GTEQ, 8),
        domain3_lo=0, domain3_lo_open=True,
        c1_ax4=Constraint("resolution", Op.LTEQ, 300),
        c2_ax4=Constraint("resolution", Op.GTEQ, 72),
        domain4_lo=0, domain4_lo_open=True,
    ))

    # Conflict on axis 4 only (deepest position in nesting)
    benchmarks.append(Benchmark(
        number=362, name="conflict-at-axis-4",
        category=Category.COMPOSITION,
        c1=Constraint("width", Op.LTEQ, 800),
        c2=Constraint("width", Op.GTEQ, 200),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="Conflict on axis 4 of 4 → box Conflict",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("height", Op.LTEQ, 600),
        c2_ax2=Constraint("height", Op.GTEQ, 100),
        domain2_lo=0, domain2_lo_open=True,
        c1_ax3=Constraint("depth", Op.LTEQ, 32),
        c2_ax3=Constraint("depth", Op.GTEQ, 8),
        domain3_lo=0, domain3_lo_open=True,
        c1_ax4=Constraint("resolution", Op.LTEQ, 72),
        c2_ax4=Constraint("resolution", Op.GTEQ, 300),
        domain4_lo=0, domain4_lo_open=True,
        notes="Conflict in deepest nesting position: box_verdict(o, box_verdict(o, box_verdict(o, C))).",
    ))

    # Conflict on axis 2 only (middle position)
    benchmarks.append(Benchmark(
        number=363, name="conflict-at-axis-2",
        category=Category.COMPOSITION,
        c1=Constraint("width", Op.LTEQ, 800),
        c2=Constraint("width", Op.GTEQ, 200),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="Conflict on axis 2 of 4 → box Conflict",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("height", Op.LTEQ, 300),
        c2_ax2=Constraint("height", Op.GTEQ, 600),
        domain2_lo=0, domain2_lo_open=True,
        c1_ax3=Constraint("depth", Op.LTEQ, 32),
        c2_ax3=Constraint("depth", Op.GTEQ, 8),
        domain3_lo=0, domain3_lo_open=True,
        c1_ax4=Constraint("resolution", Op.LTEQ, 300),
        c2_ax4=Constraint("resolution", Op.GTEQ, 72),
        domain4_lo=0, domain4_lo_open=True,
    ))

    # ------------------------------------------------------------------
    # Mixed operators: each axis uses a different O_δ pair
    # ------------------------------------------------------------------

    # All 5 operators represented: eq, lt, lteq, gt, gteq
    benchmarks.append(Benchmark(
        number=364, name="mixed-ops-compatible",
        category=Category.COMPOSITION,
        # width: = 600 vs ≤ 800 → Compatible (point inside)
        c1=Constraint("width", Op.EQ, 600),
        c2=Constraint("width", Op.LTEQ, 800),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="All 5 operator types across 4 axes → Compatible",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        # height: > 100 vs < 500 → Compatible (open overlap, needs density)
        c1_ax2=Constraint("height", Op.GT, 100),
        c2_ax2=Constraint("height", Op.LT, 500),
        domain2_lo=0, domain2_lo_open=True,
        # depth: ≥ 8 vs ≤ 32 → Compatible
        c1_ax3=Constraint("depth", Op.GTEQ, 8),
        c2_ax3=Constraint("depth", Op.LTEQ, 32),
        domain3_lo=0, domain3_lo_open=True,
        # resolution: ≤ 300 vs ≥ 150 → Compatible
        c1_ax4=Constraint("resolution", Op.LTEQ, 300),
        c2_ax4=Constraint("resolution", Op.GTEQ, 150),
        domain4_lo=0, domain4_lo_open=True,
        needs_density=True,
        notes="Exercises all 5 ODRL operators: eq, lt, lteq, gt, gteq.",
    ))

    benchmarks.append(Benchmark(
        number=365, name="mixed-ops-conflict",
        category=Category.COMPOSITION,
        # width: = 600 vs = 800 → Conflict (distinct points)
        c1=Constraint("width", Op.EQ, 600),
        c2=Constraint("width", Op.EQ, 800),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="eq vs eq conflict + mixed operators elsewhere → Conflict",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        # height: > 100 vs < 500 → Compatible
        c1_ax2=Constraint("height", Op.GT, 100),
        c2_ax2=Constraint("height", Op.LT, 500),
        domain2_lo=0, domain2_lo_open=True,
        # depth: ≥ 8 vs ≤ 32 → Compatible
        c1_ax3=Constraint("depth", Op.GTEQ, 8),
        c2_ax3=Constraint("depth", Op.LTEQ, 32),
        domain3_lo=0, domain3_lo_open=True,
        # resolution: ≤ 300 vs ≥ 150 → Compatible
        c1_ax4=Constraint("resolution", Op.LTEQ, 300),
        c2_ax4=Constraint("resolution", Op.GTEQ, 150),
        domain4_lo=0, domain4_lo_open=True,
        needs_density=True,
    ))

    # ------------------------------------------------------------------
    # Many constants: stress the ordering chain
    # ------------------------------------------------------------------

    # 8 distinct values → C(8,2) = 28 ordering axioms
    benchmarks.append(Benchmark(
        number=366, name="many-constants-compatible",
        category=Category.COMPOSITION,
        c1=Constraint("width", Op.LTEQ, 1920),
        c2=Constraint("width", Op.GTEQ, 640),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="8 distinct values, 28 ordering axioms → Compatible",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("height", Op.LTEQ, 1080),
        c2_ax2=Constraint("height", Op.GTEQ, 480),
        domain2_lo=0, domain2_lo_open=True,
        c1_ax3=Constraint("depth", Op.LTEQ, 48),
        c2_ax3=Constraint("depth", Op.GTEQ, 16),
        domain3_lo=0, domain3_lo_open=True,
        c1_ax4=Constraint("resolution", Op.LTEQ, 600),
        c2_ax4=Constraint("resolution", Op.GTEQ, 150),
        domain4_lo=0, domain4_lo_open=True,
        notes="Realistic HD image values. Tests prover with larger constant set.",
    ))

    benchmarks.append(Benchmark(
        number=367, name="many-constants-conflict",
        category=Category.COMPOSITION,
        # width: ≤640 vs ≥1920 → Conflict (SD vs 4K)
        c1=Constraint("width", Op.LTEQ, 640),
        c2=Constraint("width", Op.GTEQ, 1920),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="SD vs 4K width conflict, other 3 axes compatible",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("height", Op.LTEQ, 1080),
        c2_ax2=Constraint("height", Op.GTEQ, 480),
        domain2_lo=0, domain2_lo_open=True,
        c1_ax3=Constraint("depth", Op.LTEQ, 48),
        c2_ax3=Constraint("depth", Op.GTEQ, 16),
        domain3_lo=0, domain3_lo_open=True,
        c1_ax4=Constraint("resolution", Op.LTEQ, 600),
        c2_ax4=Constraint("resolution", Op.GTEQ, 150),
        domain4_lo=0, domain4_lo_open=True,
        notes="Same 8 constants as ODRL366, but width now conflicts.",
    ))

    # ------------------------------------------------------------------
    # 4D subsumption
    # ------------------------------------------------------------------

    benchmarks.append(Benchmark(
        number=368, name="full-4d-subsumption",
        category=Category.COMPOSITION,
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.LTEQ, 1200),
        verdict=Verdict.SUBSUMES, szs=SZS.THEOREM,
        description="All 4 axes: box A ⊆ box B → Subsumes",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("height", Op.LTEQ, 400),
        c2_ax2=Constraint("height", Op.LTEQ, 800),
        domain2_lo=0, domain2_lo_open=True,
        c1_ax3=Constraint("depth", Op.LTEQ, 16),
        c2_ax3=Constraint("depth", Op.LTEQ, 32),
        domain3_lo=0, domain3_lo_open=True,
        c1_ax4=Constraint("resolution", Op.LTEQ, 150),
        c2_ax4=Constraint("resolution", Op.LTEQ, 300),
        domain4_lo=0, domain4_lo_open=True,
        notes="4D containment: every smaller bound ⊆ every larger bound.",
    ))

    benchmarks.append(Benchmark(
        number=369, name="axis-4-breaks-subsumption",
        category=Category.COMPOSITION,
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.LTEQ, 1200),
        verdict=Verdict.REFUTED, szs=SZS.COUNTERSATISFIABLE,
        description="Resolution axis breaks 4D subsumption → Refuted",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("height", Op.LTEQ, 400),
        c2_ax2=Constraint("height", Op.LTEQ, 800),
        domain2_lo=0, domain2_lo_open=True,
        c1_ax3=Constraint("depth", Op.LTEQ, 16),
        c2_ax3=Constraint("depth", Op.LTEQ, 32),
        domain3_lo=0, domain3_lo_open=True,
        # resolution: ≤300 ⊄ ≤150 (A wider than B on axis 4)
        c1_ax4=Constraint("resolution", Op.LTEQ, 300),
        c2_ax4=Constraint("resolution", Op.LTEQ, 150),
        domain4_lo=0, domain4_lo_open=True,
        notes="Counterexample: (1, 1, 1, 200) ∈ A but ∉ B (De Morgan disjunction).",
    ))

    # ------------------------------------------------------------------
    # Open boundaries across all 4 axes
    # ------------------------------------------------------------------

    benchmarks.append(Benchmark(
        number=370, name="all-open-4d-compatible",
        category=Category.COMPOSITION,
        c1=Constraint("width", Op.GT, 200),
        c2=Constraint("width", Op.LT, 800),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="All 4 axes open overlap → Compatible (density needed)",
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
        notes="Density axioms needed on all 4 axes for existential witness.",
    ))

    benchmarks.append(Benchmark(
        number=371, name="open-close-mismatch-4d-conflict",
        category=Category.COMPOSITION,
        # width: <600 vs ≥600 → Conflict
        c1=Constraint("width", Op.LT, 600),
        c2=Constraint("width", Op.GTEQ, 600),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="Open/closed mismatch on axis 1, 3 compatible → Conflict",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        needs_density=True,
        c1_ax2=Constraint("height", Op.LTEQ, 800),
        c2_ax2=Constraint("height", Op.GTEQ, 200),
        domain2_lo=0, domain2_lo_open=True,
        c1_ax3=Constraint("depth", Op.LTEQ, 32),
        c2_ax3=Constraint("depth", Op.GTEQ, 8),
        domain3_lo=0, domain3_lo_open=True,
        c1_ax4=Constraint("resolution", Op.LTEQ, 300),
        c2_ax4=Constraint("resolution", Op.GTEQ, 150),
        domain4_lo=0, domain4_lo_open=True,
        notes="Tests that open/closed boundary conflict propagates through 4D box.",
    ))

    # Generate policy TTL
    for b_ in benchmarks:
        b_.policy_ttl = _make_composition_policy_ttl(b_)

    return benchmarks
