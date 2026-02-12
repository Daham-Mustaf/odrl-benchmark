# TPTP-ODRL Benchmark Suite

**Grounding ODRL Constraints: Knowledge-Based Conflict Detection Across Dataspaces**

Mustafa, D. & Sutcliffe, G.

---

## 1. Motivation

The W3C Open Digital Rights Language (ODRL) defines set-based operators (`isA`, `isPartOf`, `hasPart`, `isAnyOf`, `isAllOf`, `isNoneOf`) whose evaluation requires external domain knowledge. The specification leaves this knowledge unspecified. Without it, every cross-dataspace policy comparison returns **Unknown**.

This benchmark suite formalises a denotational semantics for ODRL constraints, parameterised by domain knowledge bases, that enables automated conflict detection. Each constraint maps to a *denotation* (the set of KB concepts satisfying it); conflict detection reduces to intersection testing under a three-valued verdict: **Conflict**, **Compatible**, or **Unknown**.

154 problems are encoded in both TPTP (Vampire) and SMT-LIB2 (Z3). Both provers agree on all 154 verdicts.

---

## 2. Architecture: Four-Layer Stack

```
Layer 0   Domain KBs          GEO000-0.ax, DPV000-0.ax, ...   Domain facts
Layer 1   ODRL Core           ODRL000-0.ax                     Constraint structure
Layer 2   Grounding Bridge    GROUND000-1.ax                   Denotation semantics
Layer 3   Problems            ODRL0xx-1.p / .smt2              Conjectures
```

A higher layer never modifies a lower one.

### Layer 0 — Domain Knowledge Bases (16 axiom files)

**Production KBs** (six families, two per operand for cross-standard alignment):

| File | Domain | |C| | Source | Relation |
|------|--------|:---:|--------|----------|
| GEO000-0.ax | Spatial | 4 | GeoNames | `partOf` (mereological) |
| GEO001-0.ax | Spatial | 3 | ISO 3166 | `partOf` (mereological) |
| DPV000-0.ax | Purpose | 10 | W3C DPV v2.2 | `subClassOf` (taxonomic DAG) |
| DPV001-0.ax | Purpose | 6 | GDPR-derived | `subClassOf` (taxonomic) |
| LNG000-0.ax | Language | 10 | BCP 47 | `subClassOf` (taxonomic) |
| LNG001-0.ax | Language | 6 | ISO 639-3 | `subClassOf` (taxonomic) |
| NOM000-0.ax | Channel | 4 | Delivery channels | `=` (nominal/identity) |

**Auxiliary axiom files** (UNA and negative facts):

| File | Content |
|------|---------|
| GEO002-0.ax | UNA + negative `partOf` |
| DPV002-0.ax | Same-level UNA (leaf≠leaf, parent≠parent) |
| DPV003-0.ax | Cross-level UNA (leaf≠parent) |
| LNG002-0.ax | UNA for BCP 47 concepts |

**Structural KBs** (adversarial edge cases):

| File | |C| | Structure | Tests |
|------|:---:|-----------|-------|
| CHN000-0.ax | 5 | Depth-5 linear chain A⊑B⊑C⊑D⊑E | Transitive closure depth |
| DIA000-0.ax | 4 | Diamond DAG: X⊑A, X⊑B, A⊑C, B⊑C | Multiple inheritance |
| SNG000-0.ax | 1 | Single concept + domain closure | Degenerate complements |
| NMS000-0.ax | 6 | Two taxonomies overlapping on one concept | Near-miss boundaries |

### Layer 1 — ODRL Core (ODRL000-0.ax)

Structural vocabulary independent of any domain: constraint structure (`has_operand`, `has_operator`, `has_value`), operator classification (`set_operator(isA)`, etc.), operand typing (`mereological(spatial)`, `taxonomic(purpose)`), and scope predicates (`same_operand`). No existential quantifiers.

### Layer 2 — Grounding Bridge (GROUND000-1.ax)

Encodes denotation semantics via the `in_denotation(X, C)` predicate. Each operator has **bidirectional** rules:

- **If-direction:** KB fact → denotation membership (proves compatibility)
- **Only-if direction:** denotation membership → KB fact (proves conflict)

Without only-if rules, provers trivially satisfy all implications by setting `in_denotation := true` for all inputs (open-world frame problem). This bidirectional pattern was discovered when ODRL013-1 unexpectedly returned CounterSatisfiable.

---

## 3. Operator Encodings

### 3.1 Fully Bidirectional (Layer 2)

| Operator | Denotation | Domain |
|----------|-----------|--------|
| `eq` | `{x \| x = v}` | All |
| `neq` | `C \ {v}` | All |
| `isA` | `{x \| x ≤ v}` (downward closure) | Taxonomic |
| `isPartOf` | `{x \| x ≤ v}` (downward closure) | Mereological |
| `hasPart` | `{x \| v ≤ x}` (upward closure) | Mereological |

Both if and only-if rules live in GROUND000-1.ax. `neq` requires UNA axioms to prove its complement non-empty.

### 3.2 Asymmetric (per-problem grounding)

| Operator | Layer 2 | Per-problem | Hard direction | Issue |
|----------|:-------:|:-----------:|----------------|-------|
| `isAnyOf` | if ✓ | only-if | only-if | ∃ Skolem explosion |
| `isAllOf` | only-if ✓ | if | if | ∀ in antecedent |
| `isNoneOf` | only-if ✓ | if | if | ¬ in antecedent |

The hard directions involve existentials, universals in antecedents, or negation in antecedents. Per-problem grounding with concrete values keeps the fragment within EPR.

### 3.3 Nominal Domain

Under identity (`≤ = =`), `isA` degenerates to `eq`, `isPartOf` degenerates to `eq`, and `isAllOf` requires all values to coincide (yields ∅ otherwise). The operator's semantics is determined by the KB relation, not the operator name.

---

## 4. Verdict Encoding

| Verdict | Conjecture | Vampire SZS | Z3 SMT |
|---------|-----------|:-----------:|:------:|
| Compatible | `∃x(denot(x,c₁) ∧ denot(x,c₂))` | Theorem | unsat |
| Conflict | `¬∃x(denot(x,c₁) ∧ denot(x,c₂))` | Theorem | unsat |
| Unknown | either | CounterSatisfiable | sat |

All problems are in the **EPR fragment** (function-free, finite constants, universally quantified implications). Decidable; typical proof times 0.002–0.022s.

---

## 5. Benchmark Suite (154 Problems)

### 5.1 Single-KB Reasoning (90 problems)

| Category | Range | n | Tests |
|----------|-------|:-:|-------|
| Spatial (GeoNames) | 010–015 | 6 | Mereological `partOf`, transitivity, open-world gaps |
| Purpose (W3C DPV) | 020–029 | 10 | All operators over taxonomic DAG |
| Adversarial | 040–045 | 7 | Boundary conditions, reflexivity exploits |
| Language (BCP 47) | 050–056 | 7 | Taxonomic subsumption, dialect chains |
| Neq | 090–096 | 7 | Complement denotation; \|C\|=1 collapse (095) |
| HasPart | 100–106 | 7 | Upward closure, inverse of `isPartOf` |
| IsAnyOf | 110–118 | 9 | Union across taxonomic, mereological, nominal |
| IsAllOf | 120–128 | 9 | Intersection; DAG multi-parent required |
| IsNoneOf | 130–139 | 10 | Exclusion; double negation edge cases |
| Nominal | 140–147 | 8 | Identity-only KB; operator degeneration |
| Operator pairs | 150–161 | 12 | Cross-operator interactions (neq∧isA, hasPart∧isNoneOf, etc.) |
| Adversarial deep | 170–181 | 12 | Chain-5, diamond DAG, single-concept, near-miss |

### 5.2 Logical Composition (21 problems)

| Category | Range | n | Tests |
|----------|-------|:-:|-------|
| Conjunction (and) | 030–033, 200–201 | 6 | Multi-operand; single Conflict blocks all |
| Disjunction (or) | 080–084, 202–203 | 7 | One Compatible resolves; nested spatial∧or(purpose) |
| Exclusive (xone) | 085–088, 204–207 | 8 | **Key finding:** requires strictly stronger KB axioms |

XONE asymmetry: ODRL085 (nonCommRes) → Compatible (explicit `¬⊑` axiom exists). ODRL086 (commRes) → Unknown (no `¬⊑` axiom). Structurally symmetric problems, different verdicts.

### 5.3 Cross-KB Alignment (23 problems)

| Category | Range | n | Tests |
|----------|-------|:-:|-------|
| Alignment (original) | 057–066 | 13 | Three KB pairs, total/partial/empty alignment |
| Alignment (adversarial) | 190–199 | 10 | Unmapped witnesses, triple degradation, cross-operator |

No false Conflict in any of the 23 tests. Degradation tests use paired checks: both compat and conflict conjectures return CounterSatisfiable, confirming genuine indeterminacy.

### 5.4 Runtime Soundness (6 problems)

| Range | n | Tests |
|-------|:-:|-------|
| 070–075 | 6 | Witness extraction, pointwise rejection, exhaustive finite-model check |

### 5.5 Verdict Distribution

| Verdict | Count |
|---------|:-----:|
| Compatible (Theorem) | 68 |
| Conflict (Theorem) | 48 |
| Unknown (CounterSatisfiable) | 38 |
| **Total** | **154** |

### 5.6 Dual-Prover Agreement

All 154 problems: Vampire SZS status = Z3 SMT result. 100% concordance.

Both provers use complete decision procedures for the EPR fragment, so agreement reflects encoding correctness rather than heuristic coincidence.

---

## 6. Key Design Decisions

**Why bidirectional denotation rules?** Sufficient conditions alone allow `in_denotation := true` everywhere in open-world FOL. Necessary conditions constrain witness properties, enabling conflict proofs.

**Why no domain closure?** `![X]: (X = a | X = b | ...)` forces every variable (including policy names, operators, constraint IDs) to be a spatial/purpose constant. Open-world is the correct choice.

**Why per-problem grounding for set operators?** The hard directions of `isAnyOf`, `isAllOf`, `isNoneOf` involve existentials or universals that cause Skolem explosion or search-space blowup. Grounding to concrete values keeps the fragment decidable.

**Why cross-level UNA?** Same-level UNA (leaf≠leaf) is insufficient. Without `commercialResearch ≠ commercialPurpose`, Z3 can collapse child and parent, eliminating witnesses that should exist. Fixed in DPV003-0.ax.

**Why open-world for `xone`?** Exclusive disjunction requires *provable non-overlap* of the other branch. Without explicit `¬⊑` axioms, open-world semantics correctly produces Unknown even when positive evidence satisfies exactly one branch.

---

## 7. Running the Benchmarks

### TPTP (Vampire)
```bash
# Single problem
cd Problems/ODRL
vampire KBGrounding/Spatial/ODRL012-1.p

# All 154 problems
for f in KBGrounding/*/*.p; do
    result=$(vampire --time_limit 10 "$f" 2>&1 | grep "SZS status")
    echo "$(basename $f): $result"
done
```

### SMT-LIB (Z3)
```bash
# Single problem
z3 Problems/ODRL/SMT-LIB/Spatial/ODRL012-1.smt2

# Generate all + validate (original 62)
python3 generate_smtlib.py --run

# Extension benchmarks (92)
python3 generate_smtlib_ext.py --run
```

---

## 8. File Map

```
tptp-odrl/
├── README.md
├── generate_smtlib.py              Original 62 problems (SMT-LIB)
├── generate_smtlib_ext.py          Extension 92 problems (SMT-LIB)
├── Problems/ODRL/
│   ├── Axioms/
│   │   ├── Layer0-DomainKB/
│   │   │   ├── GEO000-0.ax … GEO002-0.ax
│   │   │   ├── DPV000-0.ax … DPV003-0.ax
│   │   │   ├── LNG000-0.ax … LNG002-0.ax
│   │   │   ├── NOM000-0.ax
│   │   │   ├── CHN000-0.ax, DIA000-0.ax
│   │   │   ├── SNG000-0.ax, NMS000-0.ax
│   │   │   └── *.md (per-KB documentation)
│   │   ├── Layer1-ODRLCore/
│   │   │   └── ODRL000-0.ax
│   │   └── Layer2-Grounding/
│   │       └── GROUND000-1.ax
│   ├── KBGrounding/
│   │   ├── Spatial/           ODRL010–015     (6)
│   │   ├── Purpose/           ODRL020–029     (10)
│   │   ├── CrossDataspace/    ODRL030–033,055–056  (6)
│   │   ├── Adversarial/       ODRL040–045     (7)
│   │   ├── Language/          ODRL050–056     (7)
│   │   ├── Alignment/         ODRL057–066     (13)
│   │   ├── Runtime/           ODRL070–075     (6)
│   │   ├── LogicalOr/         ODRL080–084     (5)
│   │   └── LogicalXone/       ODRL085–088     (4)
│   └── SMT-LIB/
│       └── KBGrounding/       All 154 .smt2 files
│           ├── Spatial/
│           ├── Purpose/
│           ├── CrossDataspace/
│           ├── Neq/           ODRL090–096
│           ├── HasPart/       ODRL100–106
│           ├── IsAnyOf/       ODRL110–118
│           ├── IsAllOf/       ODRL120–128
│           ├── IsNoneOf/      ODRL130–139
│           ├── Nominal/       ODRL140–147
│           ├── OperatorPairs/ ODRL150–161
│           ├── AdvDeep/       ODRL170–181
│           ├── AlignAdv/      ODRL190–199
│           └── CompDeep/      ODRL200–207
└── Solutions/                 Saved Vampire proofs
```

**Note:** Extension problems (090–207) currently have SMT-LIB files only. TPTP `.p` files for these require additional `.ax` axiom files (CHN, DIA, SNG, NMS, extended grounding rules) — generation in progress.

---

## 9. ODRL Semantic Extension Note

The suite extends ODRL's flat operators to hierarchical (transitive closure) semantics:

| Operator | W3C ODRL | This suite |
|----------|----------|------------|
| `isA` | Direct subsumption | Transitive closure |
| `isPartOf` | Direct containment | Transitive closure |
| `isAnyOf` | Flat set membership | Union of downward closures |
| `isAllOf` | Member of all values | Intersection of downward closures |
| `isNoneOf` | Not member of any | Exclusion from all downward closures |

This extension is necessary for KB-parameterised reasoning (a concept three levels deep must still satisfy `isA` on its grandparent). The flat variant would use `GROUND000-0.ax` (not yet implemented).

---

## 10. Prover Details

**Vampire 5.0.0** (CASC mode, automatic EPR detection). Typical: 0.002–0.022s, 8MB.

**Z3 4.15.4.0** (Logic: UF, single sort Entity). Typical: 0.05–0.21s. ~3–10× slower than Vampire on EPR.

**Translation notes:** SMT-LIB has no `include()` mechanism — all axioms are inlined. The generator splits grounding rules into taxonomic-only and mereological-only variants per problem. Undeclared functions cause SMT-LIB parse errors (harmless in TPTP).

---

## 11. Version History

| Version | Changes | Problems |
|---------|---------|----------|
| 0.1–0.2 | eq, isPartOf, isA; bidirectional discovery | 010–015 |
| 0.3–0.5 | isAnyOf, isAllOf, isNoneOf (Skolem fix) | 020–029 |
| 0.6 | Cross-dataspace conjunction | 030–033 |
| 0.7 | SMT-LIB parallel encoding | 62 .smt2 |
| 0.8 | neq, hasPart operators | 090–106 |
| 0.9 | Set operators across all domains; nominal | 110–147 |
| 1.0 | Operator pairs, structural KBs, cross-level UNA | 150–181 |
| 1.1 | Adversarial alignment, deep composition | 190–207 |
| **1.2** | **DPV cross-level UNA fix; ODRL199 dedup fix** | **154/154 passing** |