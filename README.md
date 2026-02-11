# TPTP-ODRL Benchmark Suite

**Grounding ODRL Constraints: Knowledge-Based Conflict Detection Across Dataspaces**
Mustafa, D. & Sutcliffe, G. · DEXA 2026

---

## 1. Motivation

The W3C Open Digital Rights Language (ODRL) is the standard policy language for data sharing in European dataspaces (IDSA, Gaia-X, Eclipse Dataspace Connector). ODRL constraints compare an operand (e.g., `spatial`, `purpose`) against a value using an operator (e.g., `eq`, `isPartOf`, `isA`, `isAnyOf`, `isAllOf`, `isNoneOf`).

**The problem:** ODRL's set-based operators (`isA`, `isPartOf`, `isAnyOf`, `isAllOf`, `isNoneOf`) require domain knowledge to evaluate. For example, does `spatial isPartOf europe` conflict with `spatial eq bavaria`? The answer depends on knowing that `partOf(bavaria, germany)` and `partOf(germany, europe)` — facts external to ODRL itself.

**Our contribution:** A denotational semantics for ODRL constraints, parameterised by domain knowledge bases (KBs), that enables automated conflict detection. This benchmark suite formalises the framework in first-order logic (FOL) and validates it using the Vampire theorem prover.

---

## 2. Architecture: Four-Layer Stack

The encoding separates concerns into four layers, frozen bottom-up. A higher layer never modifies a lower one.

```
Layer 0   Domain KBs          GEO000-0.ax, DPV000-0.ax     Domain facts
Layer 1   ODRL Core           ODRL000-0.ax                  Constraint structure
Layer 2   Grounding Bridge    GROUND000-1.ax                Denotation semantics
Layer 3   Problems            ODRL0xx-1.p                   Conjectures
```

### Layer 0 — Domain Knowledge Bases

Two KBs demonstrate two distinct relation types.

**GEO000-0.ax — GeoNames Spatial (mereological)**

4 concepts, reflexive + transitive `partOf/2`:

```
europe
├── france          partOf(france, europe)
└── germany         partOf(germany, europe)
    └── bavaria     partOf(bavaria, germany)
```

Negative facts for conflict detection: `~partOf(germany, france)`, `~partOf(france, germany)`.

Transitivity derives `partOf(bavaria, europe)` — validated by ODRL010-1.

**DPV000-0.ax — W3C Data Privacy Vocabulary (taxonomic)**

10 concepts from the official DPV v2.2 purpose taxonomy, modelled as a DAG (not a tree) with reflexive + transitive `subClassOf/2`:

```
purpose
├── commercialPurpose
│   └── commercialResearch ←──┐
├── nonCommercialPurpose      │ (multi-parent)
│   └── nonCommercialResearch ←──┐
├── researchAndDevelopment    │   │
│   ├── academicResearch      │   │
│   ├── scientificResearch    │   │
│   ├── commercialResearch ───┘   │
│   └── nonCommercialResearch ────┘
└── marketing
    ├── advertising
    └── directMarketing
```

Critical DPV fact: `scientificResearch ⊑ researchAndDevelopment` but **NOT** `⊑ nonCommercialPurpose`. This is verified from the official W3C DPV specification and is the basis for several Unknown-verdict tests (ODRL021-1, ODRL027-1).

The DAG structure means `commercialResearch` has two parents (`researchAndDevelopment` AND `commercialPurpose`), which is essential for testing `isAllOf` (ODRL026-1).

Disjointness axioms assert cross-branch separation, e.g., `~subClassOf(advertising, nonCommercialPurpose)`.

### Layer 1 — ODRL Core (ODRL000-0.ax)

Encodes the structural vocabulary of ODRL constraints, independent of any domain:

- **Constraint structure:** `constraint(C)`, `has_operand(C, L)`, `has_operator(C, Op)`, `has_value(C, V)`
- **Policy types:** `permission(P)`, `prohibition(P)`, `obligation(P)` with reverse typing axioms
- **Operator classification:** `comparison_operator(eq)`, `set_operator(isA)`, `set_operator(isAnyOf)`, etc.
- **Operand typing:** `mereological(spatial)`, `taxonomic(purpose)`, `taxonomic(language)` — guards that prevent cross-domain pollution
- **Scope predicate:** `same_operand(C1, C2)` for pairing constraints that share an operand

Design constraint: **no existential quantifiers** in Layer 1 (avoids Skolemisation issues in the axiom layer).

### Layer 2 — Grounding Bridge (GROUND000-1.ax)

This is the central contribution. It encodes the paper's Definition 3 (Denotation) as FOL axioms, connecting ODRL constraint structure (Layer 1) to domain knowledge (Layer 0) via the `in_denotation(X, C)` predicate.

Each operator has **bidirectional** rules where possible:

- **If-direction** (sufficient condition): domain fact → membership in denotation
- **Only-if direction** (necessary condition): membership in denotation → domain fact

The only-if direction is critical. Without it, the prover can trivially satisfy all implications by setting `in_denotation(X, C) := true` for all inputs (open-world frame problem). This was discovered when ODRL013-1 unexpectedly returned CounterSatisfiable before the only-if rules were added.

**Current version: 0.5.0** — supports six operators across two domain types.

---

## 3. Operator Encodings

### 3.1 Simple Operators (full bidirectional in Layer 2)

These operators have clean per-value rules in both directions. No per-problem encoding needed.

**eq — Exact match (all domains)**

```
⟦l eq v⟧ = { x | x = v }
```

```tptp
% If: X = V → in_denotation(X, C)
fof(denotation_eq, axiom,
    ![C,L,V,X]: ((has_operand(C,L) & has_operator(C,eq) & has_value(C,V) & X = V)
        => in_denotation(X, C))).

% Only-if: in_denotation(X, C) → X = V
fof(denotation_eq_only, axiom,
    ![C,L,V,X]: ((in_denotation(X,C) & has_operand(C,L) & has_operator(C,eq) & has_value(C,V))
        => X = V)).
```

**isPartOf — Mereological containment**

```
⟦l isPartOf v⟧ = { x | partOf(x, v) }
```

Guards: requires `mereological(L)`. Relies on Layer 0 transitivity for chain reasoning (e.g., `bavaria → germany → europe`).

**isA — Taxonomic subsumption**

```
⟦l isA v⟧ = { x | subClassOf(x, v) }
```

Guards: requires `taxonomic(L)`. Mirrors `isPartOf` structure with `subClassOf` instead of `partOf`.

### 3.2 Set Operators (asymmetric encoding)

The set operators (`isAnyOf`, `isAllOf`, `isNoneOf`) present an encoding asymmetry. One direction is clean and lives in Layer 2; the other direction is problematic in FOL and must be grounded per-problem in Layer 3.

**isAnyOf — Union of downward closures**

```
⟦l isAnyOf {v₁, v₂, ...}⟧ = ⋃ᵢ { x | subClassOf(x, vᵢ) }
```

- **If-direction (Layer 2):** Per-value rule fires independently for each `has_value(C, V)`, giving the union automatically. No new encoding pattern needed — identical to `isA` but triggers on `isAnyOf` operator.
- **Only-if direction (problematic):** Requires an existential: `in_denotation(X, C) → ∃V(has_value(C, V) ∧ subClassOf(X, V))`. Clausification introduces a Skolem function `f(X, C)` that causes search space explosion — Vampire exceeded 10s/164MB on ODRL025-1 before this rule was removed.
- **Resolution:** Only-if removed from Layer 2 (v0.3.1). Conflict proofs for `isAnyOf` constraints would use per-problem encoding when needed. In practice, our `isAnyOf` tests pair against `eq` on the other side, so the `eq` only-if rule constrains sufficiently.

**isAllOf — Intersection of downward closures**

```
⟦l isAllOf {v₁, v₂, ...}⟧ = ⋂ᵢ { x | subClassOf(x, vᵢ) }
```

The dual of `isAnyOf`:

- **Only-if direction (Layer 2):** Per-value necessary condition — clean, no existential: `in_denotation(X, C) ∧ has_value(C, V) → subClassOf(X, V)`. Fires independently for each value.
- **If-direction (problematic):** Requires a grounded conjunction: `subClassOf(X, v₁) ∧ subClassOf(X, v₂) → in_denotation(X, C)`. The universally quantified form `∀V(has_value(C,V) → subClassOf(X,V))` has a universal in the antecedent — difficult for provers.
- **Resolution:** If-direction encoded per-problem with concrete values. Example for ODRL026-1:

```tptp
fof(denotation_isAllOf_c1_if, axiom,
    ![X]: ((subClassOf(X, researchAndDevelopment) & subClassOf(X, commercialPurpose)
            & taxonomic(purpose))
        => in_denotation(X, c1))).
```

**isNoneOf — Exclusion (negation of subsumption)**

```
⟦l isNoneOf {v₁, v₂, ...}⟧ = { x | ∀i: ¬subClassOf(x, vᵢ) }
```

- **Only-if direction (Layer 2):** Per-value negative necessary condition: `in_denotation(X, C) ∧ has_value(C, V) → ¬subClassOf(X, V)`. Clean — negation in the consequent is prover-friendly.
- **If-direction (problematic):** `¬subClassOf(X, v₁) → in_denotation(X, c1)` has negation in the antecedent. Clausifies to `subClassOf(X, v₁) ∨ in_denotation(X, c1)` — a disjunctive fact that can expand search.
- **Resolution:** If-direction encoded per-problem. Works well in practice because the disjunction is ground-instantiated.

### 3.3 Encoding Summary

| Operator | If (Layer 2) | Only-if (Layer 2) | Hard direction | Issue |
|----------|:---:|:---:|---|---|
| eq | ✓ | ✓ | neither | — |
| isA | ✓ | ✓ | neither | — |
| isPartOf | ✓ | ✓ | neither | — |
| isAnyOf | ✓ | ✗ per-problem | only-if | ∃ Skolem explosion |
| isAllOf | ✗ per-problem | ✓ | if | ∀ in antecedent |
| isNoneOf | ✗ per-problem | ✓ | if | ¬ in antecedent |

---

## 4. Proof Methodology

### 4.1 Verdict Encoding

The paper defines three verdicts: **Compatible**, **Conflict**, and **Unknown**.

- **Compatible:** Proven by existential conjecture `?[X]: (in_denotation(X, c1) & in_denotation(X, c2))`. Vampire finds a witness. SZS: Theorem.
- **Conflict:** Proven by negated existential conjecture `~?[X]: (in_denotation(X, c1) & in_denotation(X, c2))`. Vampire negates this (Skolem witness `sK0`), assumes it exists in both denotations, derives contradiction. SZS: Theorem.
- **Unknown:** KB is incomplete — can prove neither compatibility nor conflict. SZS: CounterSatisfiable.

There is **no explicit `verdict_conflict` axiom**. An early version included `~∃X(...) → verdict(C1,C2,conflict)` but the negated existential in the antecedent is very hard for provers in open-domain FOL. Instead, conflict is tested as a conjecture.

The `verdict_compatible` axiom exists in Layer 2 but is not used in problem conjectures — problems test denotation overlap directly, which is cleaner and mirrors the mathematical definition more closely.

### 4.2 SZS → ODRL Verdict Mapping

| SZS Status | ODRL Verdict | Meaning |
|:---:|:---:|---|
| Theorem (compatibility conjecture) | Compatible | Denotations overlap — witness found |
| Theorem (conflict conjecture) | Conflict | Denotations provably disjoint |
| CounterSatisfiable | Unknown | KB incomplete — cannot decide |
| Timeout / GaveUp | Unknown | Prover limit |

### 4.3 The Bidirectional Denotation Discovery

The most important debugging insight: **sufficient conditions alone are not enough for conflict proofs in open-domain FOL**.

Initial Layer 2 (v0.1) had only if-direction rules:

```
partOf(X, V) → in_denotation(X, C)   % sufficient condition
```

When ODRL013-1 (germany vs france, expected Conflict) was run, Vampire returned **CounterSatisfiable**. The model showed `in_denotation(X, C) := true` for all inputs — trivially satisfying all implications. No contradiction possible.

The fix: add only-if rules (necessary conditions):

```
in_denotation(X, C) → partOf(X, V)   % necessary condition
```

Now Vampire's Skolem witness `sK0` is forced to satisfy `partOf(sK0, france)` (via isPartOf only-if) and `sK0 = germany` (via eq only-if), yielding `partOf(germany, france)` which contradicts the Layer 0 negative axiom. Refutation in 0.003s.

This bidirectional pattern is analogous to **if-and-only-if** characterisation of denotation sets — essential for soundness of conflict detection in open-domain reasoning.

### 4.4 Open-World Semantics and Unknown

The framework deliberately uses **open-world assumption** (no domain closure). Missing negative facts yield Unknown, not false Conflict.

Example: ODRL015-1 tests `spatial isPartOf france` vs `spatial eq bavaria`. The KB has `~partOf(germany, france)` but does **not** have `~partOf(bavaria, france)`. In open-domain FOL, absence of a fact ≠ its negation. Vampire correctly returns CounterSatisfiable — the KB genuinely cannot decide.

Adding domain closure axioms like `![X]: (X = europe | X = france | X = germany | X = bavaria)` would force every variable in the entire theory (including policy names, operators, constraint IDs) to be one of four spatial constants — catastrophic. Open-world is the correct modeling choice.

### 4.5 The isAnyOf Skolem Explosion

ODRL025-1 initially included the isAnyOf only-if rule with existential:

```
in_denotation(X, C) ∧ isAnyOf ∧ taxonomic → ∃V(has_value(C, V) ∧ subClassOf(X, V))
```

Clausification produces a Skolem function `f(X, C)` that Vampire repeatedly instantiates, generating `has_value(C, f(X, C))` for every X. Combined with the reflexive `subClassOf(X, X)` and transitive closure, the search space explodes: 10s timeout, 164MB memory.

After removing the only-if rule (v0.3.1), the same problem solves in 0.004s / 8MB. The if-direction alone is sufficient for compatibility proofs, and the eq only-if rule on the paired constraint constrains the witness sufficiently.

### 4.6 FOL Fragment

All problems fall within the **EPR (Effectively Propositional / Bernays–Schönfinkel–Ramsey)** fragment: function-free, finite constants, universally quantified implications. This fragment is decidable, and Vampire's CASC mode detects it automatically. Typical proof times: 0.002–0.022s, 8MB peak memory.

---

## 5. Benchmark Results

### 5.1 Spatial Domain (GeoNames) — 6 problems

| Problem | Conjecture | SZS | Verdict | What it tests |
|:---:|---|:---:|:---:|---|
| ODRL010-1 | `partOf(bavaria, europe)` | Theorem | — | Layer 0 transitivity (sanity check) |
| ODRL011-1 | `~partOf(germany, france)` | Theorem | — | Layer 0 negative fact (sanity check) |
| ODRL012-1 | `∃X(denot(X,c1) ∧ denot(X,c2))` | Theorem | Compatible | Paper Table 1: france ⊑ europe |
| ODRL013-1 | `~∃X(denot(X,c1) ∧ denot(X,c2))` | Theorem | Conflict | germany ⊄ france (bidirectional rules) |
| ODRL014-1 | `∃X(denot(X,c1) ∧ denot(X,c2))` | Theorem | Compatible | Transitive chain: bavaria → germany → europe |
| ODRL015-1 | `~∃X(denot(X,c1) ∧ denot(X,c2))` | CounterSat | Unknown | Missing `~partOf(bavaria, france)` — KB gap |

### 5.2 Purpose Domain (DPV) — 10 problems

| Problem | Operator | Policy | Request | SZS | Verdict | What it tests |
|:---:|:---:|---|---|:---:|:---:|---|
| ODRL020-1 | isA | purpose isA nonCommPurpose | eq nonCommResearch | Theorem | Compatible | Basic taxonomic subsumption |
| ODRL021-1 | isA | purpose isA nonCommPurpose | eq scientificResearch | CounterSat | Unknown | No DPV path (key paper finding) |
| ODRL022-1 | isA | purpose isA commPurpose | eq commResearch | Theorem | Compatible | DAG multi-parent subsumption |
| ODRL023-1 | isA | purpose isA nonCommPurpose | eq advertising | Theorem | Conflict | Cross-branch disjointness |
| ODRL024-1 | isAnyOf | purpose isAnyOf {nonCommPurpose, marketing} | eq advertising | Theorem | Compatible | Union: advertising ⊑ marketing |
| ODRL025-1 | isAnyOf | purpose isAnyOf {nonCommPurpose, marketing} | eq commResearch | CounterSat | Unknown | Union still incomplete |
| ODRL026-1 | isAllOf | purpose isAllOf {R&D, commPurpose} | eq commResearch | Theorem | Compatible | Intersection via DAG multi-parent |
| ODRL027-1 | isAllOf | purpose isAllOf {R&D, nonCommPurpose} | eq scientificResearch | CounterSat | Unknown | Intersection: one leg missing |
| ODRL028-1 | isNoneOf | purpose isNoneOf {commPurpose} | eq nonCommResearch | Theorem | Compatible | Negation + disjointness |
| ODRL029-1 | isNoneOf | purpose isNoneOf {commPurpose} | eq commResearch | Theorem | Conflict | Negation catches subclass |

### 5.3 Verdict Distribution

| Verdict | Count | Mechanism |
|---|:---:|---|
| Compatible (Theorem) | 8 | Existential witness found |
| Conflict (Theorem) | 4 | Negated existential — contradiction via bidirectional rules |
| Unknown (CounterSat) | 4 | KB incomplete — open-world |

---

## 6. File Map

```
tptp-odrl/
├── README.md                                  ← this file
├── Problems/ODRL/
│   ├── Axioms/
│   │   ├── Layer0-DomainKB/
│   │   │   ├── GEO000-0.ax                   4 concepts, partOf, 7 axioms
│   │   │   ├── DPV000-0.ax                   10 concepts, subClassOf, DAG
│   │   │   └── DPV-README.md                  DPV taxonomy docs + test plan
│   │   ├── Layer1-ODRLCore/
│   │   │   └── ODRL000-0.ax                   constraint structure, operators
│   │   └── Layer2-Grounding/
│   │       └── GROUND000-1.ax                 denotation semantics v0.5
│   └── KBGrounding/
│       ├── Spatial/
│       │   ├── ODRL010-1.p … ODRL015-1.p     6 spatial problems
│       └── Purpose/
│           ├── ODRL020-1.p … ODRL029-1.p     10 purpose problems
└── Solutions/
    └── ODRL0xx-1.proof                        saved Vampire output
```

---

## 7. Running the Benchmarks

```bash
cd Problems/ODRL
vampire KBGrounding/Spatial/ODRL012-1.p    # single problem
```

Include paths are relative to `Problems/ODRL/` — Vampire resolves them from the working directory.

Batch run with SZS extraction:

```bash
cd Problems/ODRL
for f in KBGrounding/Spatial/*.p KBGrounding/Purpose/*.p; do
    result=$(vampire --time_limit 10 "$f" 2>&1 | grep "SZS status")
    echo "$(basename $f): $result"
done
```

---

## 8. Design Decisions and Rationale

### Why no domain closure?

Domain closure (`![X]: (X = a | X = b | ...)`) forces every variable in the entire theory to one of the listed constants — including policy names, constraint IDs, and operators. This makes the axiom system inconsistent or trivial. Open-world is the correct choice for KB-parameterised reasoning.

### Why no explicit verdict_conflict axiom?

The axiom `~∃X(...) → verdict(C1,C2,conflict)` puts a negated existential in an antecedent. Provers struggle with this in open-domain FOL. Instead, we test conflict as a conjecture: `~∃X(denot(X,c1) ∧ denot(X,c2))`. Vampire negates this, introduces Skolem constant `sK0`, assumes it's in both denotations, and derives contradiction via the only-if rules.

### Why hierarchical (not flat) operators?

The ODRL W3C specification defines `isAnyOf` as flat set membership and `isA` as direct subsumption. Our semantics extends these to **transitive closure** (hierarchical): `isPartOf` uses transitive `partOf`, `isA` uses transitive `subClassOf`, `isAnyOf` computes union of downward closures. This is documented as a semantic **extension**, not an interpretation of the standard.

The flat variants would use `GROUND000-0.ax` (not yet implemented) with direct-relation-only denotation rules.

### Why per-problem if-directions for set operators?

The set operators' hard directions involve either existentials (isAnyOf only-if), universals in antecedents (isAllOf if), or negation in antecedents (isNoneOf if). These either cause Skolem explosion or are not Horn-friendly. The per-problem encoding grounds these to specific values, keeping the FOL fragment within EPR.

---

## 9. ODRL Semantic Extension Note

This benchmark suite reveals that the paper's Definition 5 silently extends ODRL semantics:

| Operator | ODRL W3C Spec | Paper Semantics |
|---|---|---|
| `isAnyOf` | Flat set membership | Union of downward closures (hierarchical) |
| `isA` | Direct subsumption | Transitive closure of subsumption |
| `isPartOf` | Direct containment | Transitive closure of containment |
| `isAllOf` | Membership in all listed values | Intersection of downward closures |
| `isNoneOf` | Not member of any listed value | Exclusion from all downward closures |

This distinction must be explicitly documented in the paper. The TPTP suite could support both variants: `GROUND000-0.ax` (flat/standard) and `GROUND000-1.ax` (hierarchical/extended).

---

## 10. Version History

| Version | Layer 2 Changes | Problems Added |
|---|---|---|
| 0.1.0 | eq, isPartOf, isA (if-direction only) | ODRL010–012 |
| 0.2.0 | Added only-if rules (bidirectional) | ODRL013–015 |
| 0.3.0 | Added isAnyOf (if + only-if with existential) | ODRL020–025 |
| 0.3.1 | Removed isAnyOf only-if (Skolem explosion fix) | — |
| 0.4.0 | Added isAllOf only-if | ODRL026–027 |
| 0.5.0 | Added isNoneOf only-if | ODRL028–029 |

---

## 11. Status and Next Steps

- [x] Layer 0 — GeoNames spatial KB (frozen)
- [x] Layer 0 — DPV purpose KB (frozen)
- [x] Layer 1 — ODRL core (frozen)
- [x] Layer 2 — Grounding bridge: eq, isA, isPartOf, isAnyOf, isAllOf, isNoneOf
- [x] Spatial domain — 6 problems (Compatible, Conflict, Unknown)
- [x] Purpose domain — 10 problems (all operators validated)
- [ ] `neq` operator encoding
- [ ] `GROUND000-0.ax` — flat (standard ODRL) variant
- [ ] SMT-LIB parallel encoding (Z3/CVC5 comparison)
- [ ] Cross-dataspace alignment problems
- [ ] Multi-prover comparison table (Vampire, E, SPASS, iProver)

---

## 12. Prover Details

All results obtained with:

```
Vampire 5.0.0 (Release build, commit 55c27f5 on 2025-09-09)
Linked with Z3 4.14.0.0
CASC mode with automatic EPR detection
```
