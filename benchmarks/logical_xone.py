"""Category I: LogicalXone — odrl:xone connective (exclusive-or constraints).

ODRL 460–469 (10 benchmarks).

Tests ODRL's odrl:xone LogicalConstraint where EXACTLY ONE constraint
within a policy must hold.  This creates "L-shaped" or "donut-shaped"
feasibility regions — the complement of the "both-hold" and
"neither-holds" zones.

ODRL Turtle pattern:
    odrl:permission [
      odrl:action odrl:use ;
      odrl:constraint [
        a odrl:LogicalConstraint ;
        odrl:xone (
          [ odrl:leftOperand oax:absoluteSizeWidth ;
            odrl:operator odrl:lteq ;
            odrl:rightOperand "600"^^xsd:decimal ]
          [ odrl:leftOperand oax:absoluteSizeHeight ;
            odrl:operator odrl:lteq ;
            odrl:rightOperand "400"^^xsd:decimal ]
        )
      ]
    ] .

Satisfaction (n=2):
  ω ⊨ xone(c₁, c₂)  iff  (c₁ ∧ ¬c₂) ∨ (¬c₁ ∧ c₂)

FOF encoding (n=2):
  (c₁(X) & ~(c₂(Y))) | (~(c₁(X)) & c₂(Y))

For n=3:
  (c₁ & ~c₂ & ~c₃) | (~c₁ & c₂ & ~c₃) | (~c₁ & ~c₂ & c₃)

The XONE region is the symmetric difference of the individual
constraint regions, which for 2-axis spatial constraints forms
an L-shape:

  h ∞ ┌─────────┐
      │ NEITHER  │  ← w>600, h>400 (xone=false)
  400 ├─────┬───┘
      │BOTH │ ✓  │  ← w>600, h≤400 (arm 2 only)
      │     │    │
  200 │(xone│    │
      │=fals│    │
    0 └─────┴────┘
      0   600    ∞
      ↑ w≤600, h≤400 = both hold → xone=false
      ✓ = w≤600, h>400 (arm 1 only)
"""

from .models import (Benchmark, Category, Connective, Constraint,
                     Op, SZS, Verdict)


def _make_xone_policy_ttl(b: Benchmark) -> str:
    """TTL snippet showing odrl:xone / implicit AND as appropriate."""
    AXIS_TO_IRI = {
        "width": "oax:absoluteSizeWidth",
        "height": "oax:absoluteSizeHeight",
        "depth": "oax:absoluteSizeDepth",
    }

    def _iri(c):
        return c.axis_iri if c.axis_iri else AXIS_TO_IRI.get(
            c.axis, f"odrl:{c.axis}")

    def _gather(b_, policy):
        if policy == "A":
            cs = [b_.c1]
            if b_.c1_ax2: cs.append(b_.c1_ax2)
            if b_.c1_ax3: cs.append(b_.c1_ax3)
        else:
            cs = [b_.c2]
            if b_.c2_ax2: cs.append(b_.c2_ax2)
            if b_.c2_ax3: cs.append(b_.c2_ax3)
        return cs

    def _format_policy(label, cs, connective):
        out = []
        conn = connective
        if conn is None or conn == Connective.AND:
            out.append(f"%   ex:{label} a odrl:Set ;")
            out.append(f"%     odrl:permission [")
            out.append(f"%       odrl:action odrl:use ;")
            for c in cs:
                out.append(f"%       odrl:constraint [")
                out.append(f"%         odrl:leftOperand {_iri(c)} ;")
                out.append(f"%         odrl:operator odrl:{c.op.value} ;")
                out.append(f"%         odrl:rightOperand \"{c.value}\"^^xsd:decimal ] ;")
            out.append(f"%     ] .")
        else:
            out.append(f"%   ex:{label} a odrl:Set ;")
            out.append(f"%     odrl:permission [")
            out.append(f"%       odrl:action odrl:use ;")
            out.append(f"%       odrl:constraint [")
            out.append(f"%         a odrl:LogicalConstraint ;")
            out.append(f"%         odrl:{conn.value} (")
            for c in cs:
                out.append(f"%           [ odrl:leftOperand {_iri(c)} ;")
                out.append(f"%             odrl:operator odrl:{c.op.value} ;")
                out.append(f"%             odrl:rightOperand \"{c.value}\"^^xsd:decimal ]")
            out.append(f"%         )")
            out.append(f"%       ]")
            out.append(f"%     ] .")
        return out

    lines = [
        "%   @prefix odrl: <http://www.w3.org/ns/odrl/2/> .",
        "%   @prefix oax:  <http://w3id.org/odrl/spatial-axis#> .",
        "%   @prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .",
        "%   @prefix ex:   <https://example.org/> .",
        "%",
    ]
    lines += _format_policy("policyA", _gather(b, "A"), b.connective_a)
    lines.append("%")
    lines += _format_policy("policyB", _gather(b, "B"), b.connective_b)

    return "\n".join(lines)


def logical_xone_benchmarks() -> list[Benchmark]:
    """Category I: LogicalXone — odrl:xone connective (10 benchmarks)."""
    benchmarks = []

    # ==================================================================
    # XONE(A) × AND(B) — 2-axis
    # ==================================================================

    # 460: XONE(A) × AND(B) — Compatible (B hits XONE arm 1)
    # A(XONE): width ≤ 600 XONE height ≤ 400
    #   Region 1: w≤600 & h>400  (arm 1 only)
    #   Region 2: w>600 & h≤400  (arm 2 only)
    # B(AND): width ≤ 400 AND height ≥ 500
    # B region: w ∈ (0,400], h ∈ [500,∞)
    # B ∩ XONE region 1: w ∈ (0,400], h ≥ 500 → ≠ ∅
    # Witness: (300, 600) — A: w≤600 ✓, h≤400? No → exactly one ✓.
    benchmarks.append(Benchmark(
        number=460, name="xone-a-and-b-compatible",
        category=Category.LOGICAL_XONE,
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.LTEQ, 400),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="XONE(A)×AND(B): B hits XONE arm 1 → Compatible",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        connective_a=Connective.XONE,
        c1_ax2=Constraint("height", Op.LTEQ, 400),
        c2_ax2=Constraint("height", Op.GTEQ, 500),
        domain2_lo=0, domain2_lo_open=True,
        notes="XONE region 1: w≤600 & h>400. B: w≤400 & h≥500. "
              "Overlap → witness (300, 600).",
    ))

    # 461: XONE(A) × AND(B) — Conflict (B falls in "both-hold" zone)
    # A(XONE): width ≤ 600 XONE height ≤ 400
    # B(AND): width ≤ 400 AND height ≤ 200
    # B region: w ∈ (0,400], h ∈ (0,200]
    # For all B points: w≤600 ✓ AND h≤400 ✓ → BOTH hold → XONE = false
    benchmarks.append(Benchmark(
        number=461, name="xone-a-and-b-conflict-both-hold",
        category=Category.LOGICAL_XONE,
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.LTEQ, 400),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="XONE(A)×AND(B): B in both-hold zone → Conflict",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        connective_a=Connective.XONE,
        c1_ax2=Constraint("height", Op.LTEQ, 400),
        c2_ax2=Constraint("height", Op.LTEQ, 200),
        domain2_lo=0, domain2_lo_open=True,
        notes="Every point in B (w≤400, h≤200) satisfies BOTH XONE arms "
              "(w≤600 ✓, h≤400 ✓) → XONE=false → Conflict.",
    ))

    # ==================================================================
    # AND(A) × XONE(B) — 2-axis
    # ==================================================================

    # 462: AND(A) × XONE(B) — Compatible (A hits XONE arm 2)
    # A(AND): width ≥ 800 AND height ≤ 200
    # B(XONE): width ≤ 600 XONE height ≤ 400
    # A region: w ≥ 800, h ∈ (0,200]
    # XONE arm 2: w>600 & h≤400 → w≥800 ✓, h≤200 ⊆ h≤400 ✓
    benchmarks.append(Benchmark(
        number=462, name="and-a-xone-b-compatible",
        category=Category.LOGICAL_XONE,
        c1=Constraint("width", Op.GTEQ, 800),
        c2=Constraint("width", Op.LTEQ, 600),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="AND(A)×XONE(B): A hits XONE arm 2 → Compatible",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        connective_b=Connective.XONE,
        c1_ax2=Constraint("height", Op.LTEQ, 200),
        c2_ax2=Constraint("height", Op.LTEQ, 400),
        domain2_lo=0, domain2_lo_open=True,
        notes="A: w≥800, h≤200. XONE arm 2: w>600 (✓) & h≤400 (✓) & w≤600 (✗). "
              "Exactly one arm holds. Witness: (900, 100).",
    ))

    # 463: AND(A) × XONE(B) — Conflict (A in both-hold zone of XONE)
    # A(AND): width ≤ 400 AND height ≤ 200
    # B(XONE): width ≤ 600 XONE height ≤ 400
    benchmarks.append(Benchmark(
        number=463, name="and-a-xone-b-conflict",
        category=Category.LOGICAL_XONE,
        c1=Constraint("width", Op.LTEQ, 400),
        c2=Constraint("width", Op.LTEQ, 600),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="AND(A)×XONE(B): A in XONE both-hold zone → Conflict",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        connective_b=Connective.XONE,
        c1_ax2=Constraint("height", Op.LTEQ, 200),
        c2_ax2=Constraint("height", Op.LTEQ, 400),
        domain2_lo=0, domain2_lo_open=True,
        notes="A: w≤400, h≤200 → B-XONE: w≤600 ✓, h≤400 ✓ → both hold → "
              "XONE=false. Symmetric to ODRL461.",
    ))

    # ==================================================================
    # XONE(A) × XONE(B) — 2-axis
    # ==================================================================

    # 464: XONE(A) × XONE(B) — Compatible (regions overlap)
    # A(XONE): width ≤ 400 XONE height ≤ 300
    #   A arm 1: w≤400 & h>300
    #   A arm 2: w>400 & h≤300
    # B(XONE): width ≤ 600 XONE height ≤ 500
    #   B arm 1: w≤600 & h>500
    #   B arm 2: w>600 & h≤500
    # A arm 1 ∩ B arm 1: w≤400 & h>500 → (200, 600) ✓
    benchmarks.append(Benchmark(
        number=464, name="xone-a-xone-b-compatible",
        category=Category.LOGICAL_XONE,
        c1=Constraint("width", Op.LTEQ, 400),
        c2=Constraint("width", Op.LTEQ, 600),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="XONE(A)×XONE(B): arm 1 regions overlap → Compatible",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        connective_a=Connective.XONE,
        connective_b=Connective.XONE,
        c1_ax2=Constraint("height", Op.LTEQ, 300),
        c2_ax2=Constraint("height", Op.LTEQ, 500),
        domain2_lo=0, domain2_lo_open=True,
        notes="A-arm1 (w≤400, h>300) ∩ B-arm1 (w≤600, h>500): "
              "w≤400 & h>500. Witness: (200, 600).",
    ))

    # ==================================================================
    # 3-axis XONE
    # ==================================================================

    # 465: 3-axis XONE(A) × AND(B) — Conflict
    # A(XONE): w≤600 XONE h≤400 XONE d≤200
    # 3-way XONE: exactly ONE of the three holds.
    # B(AND): w≤400 AND h≤200 AND d≤100
    # B region: all three XONE arms hold → XONE=false
    benchmarks.append(Benchmark(
        number=465, name="3axis-xone-a-and-b-conflict",
        category=Category.LOGICAL_XONE,
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.LTEQ, 400),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="3-axis XONE(A)×AND(B): B in all-hold zone → Conflict",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        connective_a=Connective.XONE,
        c1_ax2=Constraint("height", Op.LTEQ, 400),
        c2_ax2=Constraint("height", Op.LTEQ, 200),
        domain2_lo=0, domain2_lo_open=True,
        c1_ax3=Constraint("depth", Op.LTEQ, 200),
        c2_ax3=Constraint("depth", Op.LTEQ, 100),
        domain3_lo=0, domain3_lo_open=True,
        notes="B (w≤400, h≤200, d≤100) ⊂ all three XONE arms "
              "(w≤600 ✓, h≤400 ✓, d≤200 ✓) → three hold → XONE=false.",
    ))

    # 466: 3-axis XONE(A) × AND(B) — Compatible
    # A(XONE): w≤600 XONE h≤400 XONE d≤200
    # B(AND): w≤400 AND h ≥ 500 AND d ≥ 300
    # B region: w≤400 (arm 1 ✓), h≥500 → h≤400 (✗), d≥300 → d≤200 (✗)
    # Exactly one arm holds → XONE=true
    benchmarks.append(Benchmark(
        number=466, name="3axis-xone-a-and-b-compatible",
        category=Category.LOGICAL_XONE,
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.LTEQ, 400),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="3-axis XONE(A)×AND(B): exactly arm 1 holds → Compatible",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        connective_a=Connective.XONE,
        c1_ax2=Constraint("height", Op.LTEQ, 400),
        c2_ax2=Constraint("height", Op.GTEQ, 500),
        domain2_lo=0, domain2_lo_open=True,
        c1_ax3=Constraint("depth", Op.LTEQ, 200),
        c2_ax3=Constraint("depth", Op.GTEQ, 300),
        domain3_lo=0, domain3_lo_open=True,
        notes="B: w≤400 → arm1 ✓; h≥500 → arm2 ✗; d≥300 → arm3 ✗. "
              "Exactly one holds. Witness: (300, 600, 400).",
    ))

    # ==================================================================
    # Subsumption with XONE
    # ==================================================================

    # 467: AND ⊆ XONE — Subsumes
    # A(AND): width ≥ 800 AND height ≤ 200
    # B(XONE): width ≤ 600 XONE height ≤ 400
    # For all A: w≥800 → w≤600 FALSE; h≤200 → h≤400 TRUE.
    # Exactly one arm → XONE=true. SUBSUMES.
    benchmarks.append(Benchmark(
        number=467, name="and-subsumes-xone",
        category=Category.LOGICAL_XONE,
        c1=Constraint("width", Op.GTEQ, 800),
        c2=Constraint("width", Op.LTEQ, 600),
        verdict=Verdict.SUBSUMES, szs=SZS.THEOREM,
        description="AND ⊆ XONE: A-region falls in exactly-one XONE arm",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        connective_b=Connective.XONE,
        c1_ax2=Constraint("height", Op.LTEQ, 200),
        c2_ax2=Constraint("height", Op.LTEQ, 400),
        domain2_lo=0, domain2_lo_open=True,
        notes="A: w≥800, h≤200. For XONE: w≤600 FALSE, h≤400 TRUE → "
              "exactly one arm. All A-points satisfy B-XONE.",
    ))

    # 468: AND ⊄ XONE — Refuted
    # A(AND): width ≤ 400 AND height ≤ 200
    # B(XONE): width ≤ 600 XONE height ≤ 400
    # Counterexample: (300, 100) ∈ A → w≤600 ✓, h≤400 ✓ → both → XONE=false
    benchmarks.append(Benchmark(
        number=468, name="and-not-subsumes-xone-both-hold",
        category=Category.LOGICAL_XONE,
        c1=Constraint("width", Op.LTEQ, 400),
        c2=Constraint("width", Op.LTEQ, 600),
        verdict=Verdict.REFUTED, szs=SZS.COUNTERSATISFIABLE,
        description="AND ⊄ XONE: A falls in both-hold zone → Refuted",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        connective_b=Connective.XONE,
        needs_density=True,
        c1_ax2=Constraint("height", Op.LTEQ, 200),
        c2_ax2=Constraint("height", Op.LTEQ, 400),
        domain2_lo=0, domain2_lo_open=True,
        notes="Counterexample: (300, 100) ∈ AND(w≤400, h≤200). "
              "XONE: w≤600 ✓, h≤400 ✓ → both hold → XONE=false.",
    ))

    # ==================================================================
    # Cross-connective: XONE × OR
    # ==================================================================

    # 469: XONE(A) × OR(B) — Compatible
    # A(XONE): width ≤ 600 XONE height ≤ 400
    # B(OR):   width ≥ 800 OR height ≥ 200
    # XONE arm 1: w≤600 & h>400. B(OR): h≥200? h>400 ✓. → Compatible.
    benchmarks.append(Benchmark(
        number=469, name="xone-a-or-b-compatible",
        category=Category.LOGICAL_XONE,
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.GTEQ, 800),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="XONE(A)×OR(B): XONE arm 1 meets OR height arm",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        connective_a=Connective.XONE,
        connective_b=Connective.OR,
        c1_ax2=Constraint("height", Op.LTEQ, 400),
        c2_ax2=Constraint("height", Op.GTEQ, 200),
        domain2_lo=0, domain2_lo_open=True,
        notes="XONE arm 1: w≤600 & h>400. B(OR): h≥200 is satisfied "
              "since h>400. Witness: (400, 500).",
    ))

    # Generate policy TTL
    for b_ in benchmarks:
        b_.policy_ttl = _make_xone_policy_ttl(b_)

    return benchmarks
