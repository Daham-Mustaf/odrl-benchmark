"""Category C: Three-axis (width × height × depth) box intersection.

ODRL 340–351 (12 benchmarks).

Tests nested Kleene conjunction:
  box_verdict(V1, box_verdict(V2, V3))

Key property: associativity + commutativity of K_3 ∧ means the
position of the conflicting axis doesn't matter — any single
Conflict kills the entire box.

Axis semantics (all from oax: spatial-axis profile):
  - width  (axis 1, X) : oax:absoluteSizeWidth,  domain (0, ∞)
  - height (axis 2, Y) : oax:absoluteSizeHeight, domain (0, ∞)
  - depth  (axis 3, Z) : oax:absoluteSizeDepth,  domain (0, ∞)
    (physical depth for 3D assets, e.g. sculpture, point cloud)
"""

from .models import Benchmark, Category, Constraint, Op, SZS, Verdict


def _make_box3d_policy_ttl(b: Benchmark) -> str:
    """ODRL policy snippet for 3-axis constraints."""
    c1w, c2w = b.c1, b.c2
    c1h, c2h = b.c1_ax2, b.c2_ax2
    c1d, c2d = b.c1_ax3, b.c2_ax3
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
%         odrl:unit <http://dbpedia.org/resource/Pixel> ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSize{c1d.axis.title()} ;
%         odrl:operator odrl:{c1d.op.value} ;
%         odrl:rightOperand "{c1d.value}"^^xsd:decimal ] ] .
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
%         odrl:unit <http://dbpedia.org/resource/Pixel> ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSize{c2d.axis.title()} ;
%         odrl:operator odrl:{c2d.op.value} ;
%         odrl:rightOperand "{c2d.value}"^^xsd:decimal ] ] ."""


def box_3d_benchmarks() -> list[Benchmark]:
    """Category C: Three-axis (width × height × depth) box intersection."""
    benchmarks = []

    # ------------------------------------------------------------------
    # Conflict family: any single axis Conflict ⟹ box Conflict
    # Tests associativity: box_verdict(V1, box_verdict(V2, V3))
    # ------------------------------------------------------------------

    # C × C × C → Conflict  (all three disjoint)
    benchmarks.append(Benchmark(
        number=340, name="all-three-conflict",
        category=Category.BOX_3D,
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.GTEQ, 800),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="All three axes conflict → box Conflict",
        difficulty="Easy",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("height", Op.LTEQ, 300),
        c2_ax2=Constraint("height", Op.GTEQ, 500),
        domain2_lo=0, domain2_lo_open=True,
        c1_ax3=Constraint("depth", Op.LTEQ, 8),
        c2_ax3=Constraint("depth", Op.GTEQ, 24),
        domain3_lo=0, domain3_lo_open=True,
    ))

    # C × o × o → Conflict  (only axis 1 conflicts)
    benchmarks.append(Benchmark(
        number=341, name="first-axis-conflict",
        category=Category.BOX_3D,
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.GTEQ, 1200),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="Width conflict, height+depth compatible → Conflict",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("height", Op.LTEQ, 800),
        c2_ax2=Constraint("height", Op.GTEQ, 200),
        domain2_lo=0, domain2_lo_open=True,
        c1_ax3=Constraint("depth", Op.LTEQ, 32),
        c2_ax3=Constraint("depth", Op.GTEQ, 8),
        domain3_lo=0, domain3_lo_open=True,
        notes="Kleene: conflict ⊗ compatible ⊗ compatible = conflict.",
    ))

    # o × C × o → Conflict  (only axis 2 conflicts)
    benchmarks.append(Benchmark(
        number=342, name="second-axis-conflict",
        category=Category.BOX_3D,
        c1=Constraint("width", Op.LTEQ, 800),
        c2=Constraint("width", Op.GTEQ, 200),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="Height conflict, width+depth compatible → Conflict",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("height", Op.LTEQ, 300),
        c2_ax2=Constraint("height", Op.GTEQ, 500),
        domain2_lo=0, domain2_lo_open=True,
        c1_ax3=Constraint("depth", Op.LTEQ, 32),
        c2_ax3=Constraint("depth", Op.GTEQ, 8),
        domain3_lo=0, domain3_lo_open=True,
        notes="Tests commutativity: conflict position shouldn't matter.",
    ))

    # o × o × C → Conflict  (only axis 3 conflicts)
    benchmarks.append(Benchmark(
        number=343, name="third-axis-conflict",
        category=Category.BOX_3D,
        c1=Constraint("width", Op.LTEQ, 800),
        c2=Constraint("width", Op.GTEQ, 200),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="Depth conflict, width+height compatible → Conflict",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("height", Op.LTEQ, 600),
        c2_ax2=Constraint("height", Op.GTEQ, 100),
        domain2_lo=0, domain2_lo_open=True,
        c1_ax3=Constraint("depth", Op.LTEQ, 8),
        c2_ax3=Constraint("depth", Op.GTEQ, 24),
        domain3_lo=0, domain3_lo_open=True,
        notes="Tests associativity: conflict in last position.",
    ))

    # C × C × o → Conflict  (two axes conflict)
    benchmarks.append(Benchmark(
        number=344, name="two-of-three-conflict",
        category=Category.BOX_3D,
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.GTEQ, 800),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="Width+height conflict, depth compatible → Conflict",
        difficulty="Easy",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("height", Op.LTEQ, 300),
        c2_ax2=Constraint("height", Op.GTEQ, 500),
        domain2_lo=0, domain2_lo_open=True,
        c1_ax3=Constraint("depth", Op.LTEQ, 32),
        c2_ax3=Constraint("depth", Op.GTEQ, 8),
        domain3_lo=0, domain3_lo_open=True,
    ))

    # ------------------------------------------------------------------
    # Compatible family: all three axes compatible ⟹ box Compatible
    # ------------------------------------------------------------------

    # o × o × o → Compatible  (all overlap)
    benchmarks.append(Benchmark(
        number=345, name="all-three-compatible",
        category=Category.BOX_3D,
        c1=Constraint("width", Op.LTEQ, 800),
        c2=Constraint("width", Op.GTEQ, 200),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="All three axes compatible → box Compatible",
        difficulty="Easy",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("height", Op.LTEQ, 600),
        c2_ax2=Constraint("height", Op.GTEQ, 100),
        domain2_lo=0, domain2_lo_open=True,
        c1_ax3=Constraint("depth", Op.LTEQ, 32),
        c2_ax3=Constraint("depth", Op.GTEQ, 8),
        domain3_lo=0, domain3_lo_open=True,
        notes="Kleene: compatible ⊗ compatible ⊗ compatible = compatible.",
    ))

    # Touch × Touch × Touch → Compatible  (single-point witness)
    benchmarks.append(Benchmark(
        number=346, name="triple-touch",
        category=Category.BOX_3D,
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.GTEQ, 600),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="All three axes touch → single-point Compatible",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("height", Op.LTEQ, 400),
        c2_ax2=Constraint("height", Op.GTEQ, 400),
        domain2_lo=0, domain2_lo_open=True,
        c1_ax3=Constraint("depth", Op.LTEQ, 16),
        c2_ax3=Constraint("depth", Op.GTEQ, 16),
        domain3_lo=0, domain3_lo_open=True,
        notes="Witness: (600, 400, 16). Intersection is a single point in R³.",
    ))

    # ------------------------------------------------------------------
    # Boundary + density
    # ------------------------------------------------------------------

    # Open overlap on all 3 axes → Compatible (needs density)
    benchmarks.append(Benchmark(
        number=347, name="all-open-compatible",
        category=Category.BOX_3D,
        c1=Constraint("width", Op.GT, 200),
        c2=Constraint("width", Op.LT, 800),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="All three axes open overlap → Compatible",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        needs_density=True,
        c1_ax2=Constraint("height", Op.GT, 100),
        c2_ax2=Constraint("height", Op.LT, 500),
        domain2_lo=0, domain2_lo_open=True,
        c1_ax3=Constraint("depth", Op.GT, 8),
        c2_ax3=Constraint("depth", Op.LT, 32),
        domain3_lo=0, domain3_lo_open=True,
    ))

    # Open boundary conflict on axis 3, compatible on 1+2
    benchmarks.append(Benchmark(
        number=348, name="open-depth-conflict",
        category=Category.BOX_3D,
        c1=Constraint("width", Op.LTEQ, 800),
        c2=Constraint("width", Op.GTEQ, 200),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="Depth open/closed boundary conflict kills 3D box",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        needs_density=True,
        c1_ax2=Constraint("height", Op.LTEQ, 600),
        c2_ax2=Constraint("height", Op.GTEQ, 100),
        domain2_lo=0, domain2_lo_open=True,
        c1_ax3=Constraint("depth", Op.LT, 16),
        c2_ax3=Constraint("depth", Op.GTEQ, 16),
        domain3_lo=0, domain3_lo_open=True,
        notes="Tests that open-boundary conflict on axis 3 kills the box.",
    ))

    # ------------------------------------------------------------------
    # Subsumption family (3-axis)
    # ------------------------------------------------------------------

    # All 3 axes subsumed → Subsumes
    benchmarks.append(Benchmark(
        number=349, name="full-subsumption",
        category=Category.BOX_3D,
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.LTEQ, 1200),
        verdict=Verdict.SUBSUMES, szs=SZS.THEOREM,
        description="All 3 axes: box A ⊆ box B → Subsumes",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("height", Op.LTEQ, 400),
        c2_ax2=Constraint("height", Op.LTEQ, 800),
        domain2_lo=0, domain2_lo_open=True,
        c1_ax3=Constraint("depth", Op.LTEQ, 16),
        c2_ax3=Constraint("depth", Op.LTEQ, 32),
        domain3_lo=0, domain3_lo_open=True,
        notes="(0,600]×(0,400]×(0,16] ⊆ (0,1200]×(0,800]×(0,32].",
    ))

    # Axis 1+2 subsumed, axis 3 breaks it → Refuted
    benchmarks.append(Benchmark(
        number=350, name="depth-breaks-subsumption",
        category=Category.BOX_3D,
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.LTEQ, 1200),
        verdict=Verdict.REFUTED, szs=SZS.COUNTERSATISFIABLE,
        description="Depth axis breaks subsumption → Refuted",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        c1_ax2=Constraint("height", Op.LTEQ, 400),
        c2_ax2=Constraint("height", Op.LTEQ, 800),
        domain2_lo=0, domain2_lo_open=True,
        # depth: ≤32 ⊄ ≤16  (A wider than B on axis 3)
        c1_ax3=Constraint("depth", Op.LTEQ, 32),
        c2_ax3=Constraint("depth", Op.LTEQ, 16),
        domain3_lo=0, domain3_lo_open=True,
        notes="Counterexample: (1, 1, 24) ∈ A but ∉ B.",
    ))

    # ------------------------------------------------------------------
    # BSB-style running example (3-axis)
    # ------------------------------------------------------------------

    benchmarks.append(Benchmark(
        number=351, name="bsb-3d-conflict",
        category=Category.BOX_3D,
        # Width: ≤600 vs ≥1200 → Conflict
        c1=Constraint("width", Op.LTEQ, 600,
                       axis_iri="oax:absoluteSizeWidth"),
        c2=Constraint("width", Op.GTEQ, 1200,
                       axis_iri="oax:absoluteSizeWidth"),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="BSB 3D: width conflict × height compat × depth compat → Conflict",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        # Height: ≤600 vs ≥400 → Compatible
        c1_ax2=Constraint("height", Op.LTEQ, 600,
                           axis_iri="oax:absoluteSizeHeight"),
        c2_ax2=Constraint("height", Op.GTEQ, 400,
                           axis_iri="oax:absoluteSizeHeight"),
        domain2_lo=0, domain2_lo_open=True,
        # Depth: ≤32 vs ≥8 → Compatible
        c1_ax3=Constraint("depth", Op.LTEQ, 32,
                           axis_iri="oax:colourDepthBits"),
        c2_ax3=Constraint("depth", Op.GTEQ, 8,
                           axis_iri="oax:colourDepthBits"),
        domain3_lo=0, domain3_lo_open=True,
        notes="Extended BSB example. One conflict axis dominates.",
    ))

    # Generate policy TTL
    for b_ in benchmarks:
        b_.policy_ttl = _make_box3d_policy_ttl(b_)

    return benchmarks
