"""Category H: LogicalOr — odrl:or connective (disjunctive constraints).

ODRL 440–451 (12 benchmarks).

Tests ODRL's odrl:or LogicalConstraint where at least one constraint
within a policy must be satisfied.  This BREAKS the per-axis
decomposition that works for implicit AND, because satisfying ANY one
axis-constraint is sufficient — the axes become COUPLED.

ODRL Turtle pattern:
    odrl:permission [
      odrl:action odrl:use ;
      odrl:constraint [
        a odrl:LogicalConstraint ;
        odrl:or (
          [ odrl:leftOperand oax:absoluteSizeWidth ;
            odrl:operator odrl:lteq ;
            odrl:rightOperand "600"^^xsd:decimal ]
          [ odrl:leftOperand oax:absoluteSizeHeight ;
            odrl:operator odrl:lteq ;
            odrl:rightOperand "400"^^xsd:decimal ]
        )
      ]
    ] .

Satisfaction: ω ⊨ or(c₁, c₂, ..., cₙ)  iff  ∃i: ω ⊨ cᵢ

Key difference from AND:
  AND: ∃(x,y): c₁ᴬ(x) ∧ c₂ᴬ(y) ∧ c₁ᴮ(x) ∧ c₂ᴮ(y)
  OR:  ∃(x,y): (c₁ᴬ(x) ∨ c₂ᴬ(y)) ∧ (c₁ᴮ(x) ∧ c₂ᴮ(y))

With OR, a single compatible axis-arm can rescue an otherwise-
conflicting policy pair.  Conflict requires ALL OR-arms to fail.

Benchmark patterns:
  - OR(A) × AND(B):  Compatible / Conflict
  - AND(A) × OR(B):  Compatible / Conflict (symmetric)
  - OR(A) × OR(B):   Compatible (extremely permissive)
  - Subsumption:      AND ⊆ OR (easy) / OR ⊄ AND (typical)
  - Mixed ops + open boundaries with OR
"""

from .models import (Benchmark, Category, Connective, Constraint,
                     Op, SZS, Verdict)


def _make_or_policy_ttl(b: Benchmark) -> str:
    """TTL snippet showing odrl:or / implicit AND as appropriate."""
    AXIS_TO_IRI = {
        "width": "oax:absoluteSizeWidth",
        "height": "oax:absoluteSizeHeight",
        "depth": "oax:absoluteSizeDepth",
    }

    def _iri(c):
        return c.axis_iri if c.axis_iri else AXIS_TO_IRI.get(
            c.axis, f"odrl:{c.axis}")

    def _gather(b_, policy):
        """Return list of (constraint, IRI) for a policy."""
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
            # Implicit AND
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
            # LogicalConstraint with odrl:or / odrl:xone
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


def logical_or_benchmarks() -> list[Benchmark]:
    """Category H: LogicalOr — odrl:or connective (12 benchmarks)."""
    benchmarks = []

    # ------------------------------------------------------------------
    # 440: OR(A) × AND(B) — Compatible (height arm rescues)
    # ------------------------------------------------------------------
    # A(OR): width ≤ 400 OR height ≤ 800
    # B(AND): width ≥ 600 AND height ≥ 200
    # width arm: ≤400 ∩ ≥600 = ∅, height arm: ≤800 ∩ ≥200 ≠ ∅
    # Witness: (600, 300) — A via height (300 ≤ 800), B via both.
    benchmarks.append(Benchmark(
        number=440, name="or-a-and-b-compatible",
        category=Category.LOGICAL_OR,
        c1=Constraint("width", Op.LTEQ, 400),
        c2=Constraint("width", Op.GTEQ, 600),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="OR(A)×AND(B): height arm rescues width conflict",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        connective_a=Connective.OR,
        c1_ax2=Constraint("height", Op.LTEQ, 800),
        c2_ax2=Constraint("height", Op.GTEQ, 200),
        domain2_lo=0, domain2_lo_open=True,
        needs_density=True,
        notes="Width arm conflicts but height arm ≤800 overlaps ≥200. "
              "Witness: (600, 300). With AND(A), this would be Conflict.",
    ))

    # ------------------------------------------------------------------
    # 441: OR(A) × AND(B) — Conflict (both OR-arms fail)
    # ------------------------------------------------------------------
    # A(OR): width ≤ 400 OR height ≤ 100
    # B(AND): width ≥ 800 AND height ≥ 200
    benchmarks.append(Benchmark(
        number=441, name="or-a-and-b-conflict",
        category=Category.LOGICAL_OR,
        c1=Constraint("width", Op.LTEQ, 400),
        c2=Constraint("width", Op.GTEQ, 800),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="OR(A)×AND(B): both OR-arms fail → Conflict",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        connective_a=Connective.OR,
        c1_ax2=Constraint("height", Op.LTEQ, 100),
        c2_ax2=Constraint("height", Op.GTEQ, 200),
        domain2_lo=0, domain2_lo_open=True,
        notes="Width arm: ≤400 ∩ ≥800 = ∅. Height arm: ≤100 ∩ ≥200 = ∅. "
              "Every OR-disjunct individually conflicts with B's AND.",
    ))

    # ------------------------------------------------------------------
    # 442: AND(A) × OR(B) — Compatible (B's height arm saves it)
    # ------------------------------------------------------------------
    # A(AND): width ≤ 800 AND height ≤ 600
    # B(OR):  width ≥ 1000 OR height ≥ 200
    benchmarks.append(Benchmark(
        number=442, name="and-a-or-b-compatible",
        category=Category.LOGICAL_OR,
        c1=Constraint("width", Op.LTEQ, 800),
        c2=Constraint("width", Op.GTEQ, 1000),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="AND(A)×OR(B): B's height arm saves width mismatch",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        connective_b=Connective.OR,
        c1_ax2=Constraint("height", Op.LTEQ, 600),
        c2_ax2=Constraint("height", Op.GTEQ, 200),
        domain2_lo=0, domain2_lo_open=True,
        needs_density=True,
        notes="Witness: (400, 300). A: w≤800 ✓, h≤600 ✓. "
              "B(OR): w≥1000? No, but h≥200 ✓.",
    ))

    # ------------------------------------------------------------------
    # 443: AND(A) × OR(B) — Conflict
    # ------------------------------------------------------------------
    # A(AND): width ≤ 400 AND height ≤ 100
    # B(OR):  width ≥ 800 OR height ≥ 200
    # For any point in A: w≤400 (so w≥800 fails), h≤100 (so h≥200 fails).
    benchmarks.append(Benchmark(
        number=443, name="and-a-or-b-conflict",
        category=Category.LOGICAL_OR,
        c1=Constraint("width", Op.LTEQ, 400),
        c2=Constraint("width", Op.GTEQ, 800),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="AND(A)×OR(B): A is too small for either OR-arm of B",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        connective_b=Connective.OR,
        c1_ax2=Constraint("height", Op.LTEQ, 100),
        c2_ax2=Constraint("height", Op.GTEQ, 200),
        domain2_lo=0, domain2_lo_open=True,
        notes="A's box (0,400]×(0,100] fails both OR-arms of B: "
              "w≤400 → w≱800; h≤100 → h≱200.",
    ))

    # ------------------------------------------------------------------
    # 444: OR(A) × OR(B) — Compatible (cross-combination works)
    # ------------------------------------------------------------------
    # A(OR): width ≤ 400 OR height ≤ 600
    # B(OR): width ≥ 300 OR height ≥ 500
    # Witness: (300, 550) — A: w≤400 ✓. B: h≥500 ✓.
    benchmarks.append(Benchmark(
        number=444, name="or-a-or-b-compatible",
        category=Category.LOGICAL_OR,
        c1=Constraint("width", Op.LTEQ, 400),
        c2=Constraint("width", Op.GTEQ, 300),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="OR(A)×OR(B): cross-combination compatible",
        difficulty="Medium",
        domain_lo=0, domain_lo_open=True,
        connective_a=Connective.OR,
        connective_b=Connective.OR,
        c1_ax2=Constraint("height", Op.LTEQ, 600),
        c2_ax2=Constraint("height", Op.GTEQ, 500),
        domain2_lo=0, domain2_lo_open=True,
        needs_density=True,
        notes="OR×OR is extremely permissive — cross-terms rescue conflicts. "
              "Witness: (300, 550). A-width arm + B-height arm.",
    ))

    # ------------------------------------------------------------------
    # 445: 3-axis OR(A) × AND(B) — Conflict (all 3 OR-arms fail)
    # ------------------------------------------------------------------
    benchmarks.append(Benchmark(
        number=445, name="3axis-or-a-and-b-conflict",
        category=Category.LOGICAL_OR,
        c1=Constraint("width", Op.LTEQ, 200),
        c2=Constraint("width", Op.GTEQ, 400),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="3-axis OR(A)×AND(B): all 3 OR-arms fail → Conflict",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        connective_a=Connective.OR,
        c1_ax2=Constraint("height", Op.LTEQ, 100),
        c2_ax2=Constraint("height", Op.GTEQ, 200),
        domain2_lo=0, domain2_lo_open=True,
        c1_ax3=Constraint("depth", Op.LTEQ, 50),
        c2_ax3=Constraint("depth", Op.GTEQ, 100),
        domain3_lo=0, domain3_lo_open=True,
        notes="3-way OR: (w≤200 | h≤100 | d≤50) vs AND(w≥400, h≥200, d≥100). "
              "Each arm individually disjoint from B.",
    ))

    # ------------------------------------------------------------------
    # 446: 3-axis OR(A) × AND(B) — Compatible (one arm saves it)
    # ------------------------------------------------------------------
    benchmarks.append(Benchmark(
        number=446, name="3axis-or-a-and-b-compatible",
        category=Category.LOGICAL_OR,
        c1=Constraint("width", Op.LTEQ, 200),
        c2=Constraint("width", Op.GTEQ, 400),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="3-axis OR(A)×AND(B): depth arm rescues → Compatible",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        connective_a=Connective.OR,
        needs_density=True,
        c1_ax2=Constraint("height", Op.LTEQ, 100),
        c2_ax2=Constraint("height", Op.GTEQ, 200),
        domain2_lo=0, domain2_lo_open=True,
        # depth arm: ≤200 overlaps ≥100
        c1_ax3=Constraint("depth", Op.LTEQ, 200),
        c2_ax3=Constraint("depth", Op.GTEQ, 100),
        domain3_lo=0, domain3_lo_open=True,
        notes="Width and height arms conflict, but depth arm (≤200 ∩ ≥100) "
              "is compatible. Witness: (400, 200, 150).",
    ))

    # ------------------------------------------------------------------
    # 447: Subsumption AND ⊆ OR (easy direction)
    # ------------------------------------------------------------------
    # A(AND): width ≤ 600 AND height ≤ 400
    # B(OR):  width ≤ 800 OR height ≤ 600
    # If w≤600 → w≤800 → B satisfied. Always true. SUBSUMES.
    benchmarks.append(Benchmark(
        number=447, name="and-subsumes-or",
        category=Category.LOGICAL_OR,
        c1=Constraint("width", Op.LTEQ, 600),
        c2=Constraint("width", Op.LTEQ, 800),
        verdict=Verdict.SUBSUMES, szs=SZS.THEOREM,
        description="AND ⊆ OR: every AND-point satisfies at least one OR-arm",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        connective_b=Connective.OR,
        c1_ax2=Constraint("height", Op.LTEQ, 400),
        c2_ax2=Constraint("height", Op.LTEQ, 600),
        domain2_lo=0, domain2_lo_open=True,
        notes="AND(w≤600, h≤400) ⊆ OR(w≤800, h≤600). "
              "Every A-point has w≤600 ⟹ w≤800, so B's first arm always holds.",
    ))

    # ------------------------------------------------------------------
    # 448: Subsumption OR ⊄ AND (refuted)
    # ------------------------------------------------------------------
    # A(OR):  width ≤ 800 OR height ≤ 600
    # B(AND): width ≤ 600 AND height ≤ 400
    # Counterexample: (700, 500) — A: w≤800 ✓ (OR). B: w≤600? No.
    benchmarks.append(Benchmark(
        number=448, name="or-not-subsumes-and",
        category=Category.LOGICAL_OR,
        c1=Constraint("width", Op.LTEQ, 800),
        c2=Constraint("width", Op.LTEQ, 600),
        verdict=Verdict.REFUTED, szs=SZS.COUNTERSATISFIABLE,
        description="OR ⊄ AND: OR is wider than AND → Refuted",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        connective_a=Connective.OR,
        needs_density=True,
        c1_ax2=Constraint("height", Op.LTEQ, 600),
        c2_ax2=Constraint("height", Op.LTEQ, 400),
        domain2_lo=0, domain2_lo_open=True,
        notes="Counterexample: (700, 500) ∈ OR(w≤800, h≤600) via width arm, "
              "but ∉ AND(w≤600, h≤400) since 700 > 600.",
    ))

    # ------------------------------------------------------------------
    # 449: 3-axis OR(A) × OR(B) — Compatible
    # ------------------------------------------------------------------
    benchmarks.append(Benchmark(
        number=449, name="3axis-or-a-or-b-compatible",
        category=Category.LOGICAL_OR,
        c1=Constraint("width", Op.LTEQ, 200),
        c2=Constraint("width", Op.GTEQ, 400),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="3-axis OR×OR: cross-combination → Compatible",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        connective_a=Connective.OR,
        connective_b=Connective.OR,
        needs_density=True,
        c1_ax2=Constraint("height", Op.LTEQ, 100),
        c2_ax2=Constraint("height", Op.GTEQ, 200),
        domain2_lo=0, domain2_lo_open=True,
        c1_ax3=Constraint("depth", Op.LTEQ, 800),
        c2_ax3=Constraint("depth", Op.GTEQ, 300),
        domain3_lo=0, domain3_lo_open=True,
        notes="Width and height arms all conflict pairwise, but "
              "A's depth arm (≤800) × B's depth arm (≥300): witness (400, 200, 500).",
    ))

    # ------------------------------------------------------------------
    # 450: 2-axis OR(A) × AND(B) with open boundaries + density
    # ------------------------------------------------------------------
    # A(OR): width < 600 OR height > 200
    # B(AND): width > 400 AND height < 800
    benchmarks.append(Benchmark(
        number=450, name="or-open-boundary-compatible",
        category=Category.LOGICAL_OR,
        c1=Constraint("width", Op.LT, 600),
        c2=Constraint("width", Op.GT, 400),
        verdict=Verdict.COMPATIBLE, szs=SZS.COUNTERSATISFIABLE,
        description="OR(A)×AND(B) with open boundaries → Compatible",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        connective_a=Connective.OR,
        needs_density=True,
        c1_ax2=Constraint("height", Op.GT, 200),
        c2_ax2=Constraint("height", Op.LT, 800),
        domain2_lo=0, domain2_lo_open=True,
        notes="A(OR): w<600 | h>200. B(AND): w>400 & h<800. "
              "Width arm: (400,600) overlap with density. "
              "Height arm: (200,800) overlap. Witness: (500, 500).",
    ))

    # ------------------------------------------------------------------
    # 451: 3-axis mixed-ops OR(A) × AND(B)
    # ------------------------------------------------------------------
    benchmarks.append(Benchmark(
        number=451, name="or-mixed-ops-conflict",
        category=Category.LOGICAL_OR,
        # A(OR): width = 600 OR height < 200 OR depth > 100
        c1=Constraint("width", Op.EQ, 600),
        c2=Constraint("width", Op.GT, 800),
        verdict=Verdict.CONFLICT, szs=SZS.THEOREM,
        description="3-axis mixed-ops OR(A)×AND(B): all OR-arms fail",
        difficulty="Hard",
        domain_lo=0, domain_lo_open=True,
        connective_a=Connective.OR,
        # B(AND): width > 800 AND height ≥ 400 AND depth ≤ 50
        c1_ax2=Constraint("height", Op.LT, 200),
        c2_ax2=Constraint("height", Op.GTEQ, 400),
        domain2_lo=0, domain2_lo_open=True,
        c1_ax3=Constraint("depth", Op.GT, 100),
        c2_ax3=Constraint("depth", Op.LTEQ, 50),
        domain3_lo=0, domain3_lo_open=True,
        notes="A(OR): w=600 | h<200 | d>100. B(AND): w>800 & h≥400 & d≤50. "
              "w=600 ∩ w>800: ∅. h<200 ∩ h≥400: ∅. d>100 ∩ d≤50: ∅.",
    ))

    # Generate policy TTL
    for b_ in benchmarks:
        b_.policy_ttl = _make_or_policy_ttl(b_)

    return benchmarks
