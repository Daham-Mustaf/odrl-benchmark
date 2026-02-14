# TPTP Encoding Guide: Paper → Vampire Axioms

**Paper:** *Grounding ODRL Constraints: Knowledge-Based Conflict Detection Across Dataspaces*  
**Authors:** Mustafa, D. & Sutcliffe, G.  
**Purpose:** Step-by-step mapping from every paper definition to its TPTP layer.

---

## Architecture Overview

```
Layer 0 — Domain KB          (one file per KB: GEO000-0.ax, DPV000-0.ax, ...)
  │  concepts, leq, disjoint, UNA
  │
Layer 1 — ODRL Core          (ODRL000-0.ax — ONE file, shared by ALL problems)
  │  KB properties, denotation rules, structural predicates
  │
Layer 2 — Grounding           (GROUND000-1.ax — gamma mappings per problem set)
  │  gamma(value) = concept
  │
Problem  — Conjecture         (ODRL010-1.p, ODRL011-1.p, ...)
     specific constraint pair + negated conjecture
```

**Rule:** If an axiom is true for ALL knowledge bases and ALL problems, it goes in Layer 1.  
If it depends on a specific KB, it goes in Layer 0.  
If it maps ODRL values to KB concepts, it goes in Layer 2.  
The conjecture is always in the problem file.

---

## Layer 1: ODRL000-0.ax (Complete Specification)

Everything below goes in ONE file. Ordered by paper definition.

### Part A: Structural Predicates (Definition 1 — Constraint)

These declare what constraints, policies, and rules look like.  
**Status: Already present. Keep as-is.**

```tptp
% --- Policy typing ---
fof(permission_is_policy,  axiom, ![P]: (permission(P)  => policy(P))).
fof(prohibition_is_policy, axiom, ![P]: (prohibition(P) => policy(P))).
fof(obligation_is_policy,  axiom, ![P]: (obligation(P)  => policy(P))).

% --- Structural relations ---
fof(has_asset_policy,       axiom, ![P,A]:  (has_asset(P, A)      => policy(P))).
fof(has_constraint_policy,  axiom, ![P,C]:  (has_constraint(P, C) => policy(P))).
fof(has_operand_constraint, axiom, ![C,L]:  (has_operand(C, L)    => constraint(C))).
fof(has_operator_constraint,axiom, ![C,Op]: (has_operator(C, Op)  => constraint(C))).
fof(has_value_constraint,   axiom, ![C,V]:  (has_value(C, V)      => constraint(C))).

% --- Same-operand pairing (scope for conflict detection) ---
fof(same_operand_def, axiom,
    ![C1,C2,L]: ((has_operand(C1, L) & has_operand(C2, L))
        => same_operand(C1, C2))).
```

### Part B: KB Universal Properties (Definition 2 — Knowledge Base)

These hold for EVERY knowledge base regardless of domain.  
**Status: MISSING. Must add.**

```tptp
% ===================================================================
% Definition 2: KB structure — universal properties of ≤
% ===================================================================

% Reflexivity: ∀x ∈ C, x ≤ x
fof(leq_refl, axiom,
    ![X]: (concept(X) => leq(X, X))).

% Transitivity: x ≤ y ∧ y ≤ z → x ≤ z
fof(leq_trans, axiom,
    ![X,Y,Z]: ((leq(X, Y) & leq(Y, Z)) => leq(X, Z))).

% ===================================================================
% Definition 2: KB structure — universal properties of ⊥⊥
% ===================================================================

% Symmetry: x ⊥⊥ y → y ⊥⊥ x
fof(disj_sym, axiom,
    ![X,Y]: (disjoint(X, Y) => disjoint(Y, X))).

% Irreflexivity: ¬(x ⊥⊥ x)
fof(disj_irrefl, axiom,
    ![X]: ~disjoint(X, X)).

% Downward closure: x ⊥⊥ y ∧ x' ≤ x ∧ y' ≤ y → x' ⊥⊥ y'
fof(disj_downward, axiom,
    ![X,Y,Xp,Yp]: ((disjoint(X, Y) & leq(Xp, X) & leq(Yp, Y))
        => disjoint(Xp, Yp))).
```

### Part C: Disjointness–Order Consistency (Lemma 1)

Derived from Part B, but asserted explicitly for Vampire performance.  
**Status: MISSING. Must add.**

```tptp
% ===================================================================
% Lemma 1: x ≤ y → ¬(x ⊥⊥ y)
% (Follows from disj_downward + disj_irrefl, but helps Vampire)
% ===================================================================
fof(disj_order_consistency, axiom,
    ![X,Y]: (leq(X, Y) => ~disjoint(X, Y))).
```

### Part D: Denotation Rules — Bidirectional (Definition 3)

The core of the framework. Each operator gets TWO axioms:
- **IF-direction** (populates denotation → proves Compatible via witness)
- **ONLY-IF direction** (extracts from denotation → proves Conflict via closure)

**Status: MISSING. Must add.**

```tptp
% ===================================================================
% Definition 3: Constraint Denotation — bidirectional rules
%
% Predicate: in_denotation(X, G, Op)
%   "concept X is in the denotation of constraint (_, Op, v)
%    where gamma(v) = G"
% ===================================================================

% --- eq: ⟦ℓ eq v⟧ = {g} ---
fof(den_eq_if, axiom,
    ![X,G]: ((X = G) => in_denotation(X, G, eq))).
fof(den_eq_onlyif, axiom,
    ![X,G]: (in_denotation(X, G, eq) => (X = G))).

% --- neq: ⟦ℓ neq v⟧ = C \ {g} ---
fof(den_neq_if, axiom,
    ![X,G]: ((concept(X) & X != G) => in_denotation(X, G, neq))).
fof(den_neq_onlyif, axiom,
    ![X,G]: (in_denotation(X, G, neq) => X != G)).

% --- isA: ⟦ℓ isA v⟧ = {x ∈ C | x ≤ g} ---
fof(den_isA_if, axiom,
    ![X,G]: (leq(X, G) => in_denotation(X, G, isA))).
fof(den_isA_onlyif, axiom,
    ![X,G]: (in_denotation(X, G, isA) => leq(X, G))).

% --- isPartOf: ⟦ℓ isPartOf v⟧ = {x ∈ C | x ≤ g} ---
%     Same as isA — distinction carried by KB's ≤ (see paper footnote)
fof(den_isPartOf_if, axiom,
    ![X,G]: (leq(X, G) => in_denotation(X, G, isPartOf))).
fof(den_isPartOf_onlyif, axiom,
    ![X,G]: (in_denotation(X, G, isPartOf) => leq(X, G))).

% --- hasPart: ⟦ℓ hasPart v⟧ = {x ∈ C | g ≤ x} ---
fof(den_hasPart_if, axiom,
    ![X,G]: (leq(G, X) => in_denotation(X, G, hasPart))).
fof(den_hasPart_onlyif, axiom,
    ![X,G]: (in_denotation(X, G, hasPart) => leq(G, X))).
```

### Part E: Set-Valued Operators (Definition 3 continued)

These use a list-membership predicate `in_value_list(G, ListId)`.  
**Status: MISSING. Must add.**

```tptp
% ===================================================================
% Definition 3 (continued): Set-valued operators
%
% For isAnyOf/isAllOf/isNoneOf, right operands are sets {v1,...,vn}.
% Encoding: in_value_list(G, ListId) asserts that concept G is one
% of the grounded values in the list identified by ListId.
% These are asserted per-problem in the problem file or Layer 2.
% ===================================================================

% --- isAnyOf: ⟦ℓ isAnyOf {v1,...,vn}⟧ = ∪ {x | x ≤ gi} ---
fof(den_isAnyOf_if, axiom,
    ![X,Gi,L]: ((in_value_list(Gi, L) & leq(X, Gi))
        => in_denotation_set(X, L, isAnyOf))).
fof(den_isAnyOf_onlyif, axiom,
    ![X,L]: (in_denotation_set(X, L, isAnyOf)
        => ?[Gi]: (in_value_list(Gi, L) & leq(X, Gi)))).

% --- isAllOf: ⟦ℓ isAllOf {v1,...,vn}⟧ = {x | ∀i: x ≤ gi} ---
%     IF: x ≤ every gi in the list → x in denotation
%     ONLY-IF: x in denotation → x ≤ every gi in the list
fof(den_isAllOf_if, axiom,
    ![X,L]: ((![Gi]: (in_value_list(Gi, L) => leq(X, Gi)))
        => in_denotation_set(X, L, isAllOf))).
fof(den_isAllOf_onlyif, axiom,
    ![X,L,Gi]: ((in_denotation_set(X, L, isAllOf) & in_value_list(Gi, L))
        => leq(X, Gi))).

% --- isNoneOf: ⟦ℓ isNoneOf {v1,...,vn}⟧ = C \ ∪ {x | x ≤ gi} ---
fof(den_isNoneOf_if, axiom,
    ![X,L]: ((concept(X) & ![Gi]: (in_value_list(Gi, L) => ~leq(X, Gi)))
        => in_denotation_set(X, L, isNoneOf))).
fof(den_isNoneOf_onlyif, axiom,
    ![X,L,Gi]: ((in_denotation_set(X, L, isNoneOf) & in_value_list(Gi, L))
        => ~leq(X, Gi))).
```

### Part F: What to DELETE from current ODRL000-0.ax

```tptp
% DELETE — dead code, never referenced by any axiom:
%   fof(op_eq, ...)         comparison_operator/1
%   fof(op_neq, ...)        comparison_operator/1
%   fof(op_isA, ...)        set_operator/1
%   fof(op_isPartOf, ...)   set_operator/1
%   fof(op_hasPart, ...)    set_operator/1
%   fof(op_isNoneOf, ...)   set_operator/1
%   fof(op_isAnyOf, ...)    set_operator/1
%   fof(op_isAllOf, ...)    set_operator/1
%   fof(lo_spatial, ...)    mereological/1
%   fof(lo_purpose, ...)    taxonomic/1
%   fof(lo_language, ...)   taxonomic/1
%   fof(lo_channel, ...)    nominal/1
```

---

## Layer 0: Domain KBs (one file per KB)

Each file asserts KB-specific facts. The universal properties (reflexivity,
transitivity, disjointness closure) are in Layer 1 — do NOT repeat here.

### What goes in a Layer 0 file

| Paper element | Predicate | Example |
|---|---|---|
| Concept membership | `concept/1` | `concept(france)` |
| Hierarchy (≤) | `leq/2` | `leq(france, europe)` |
| Disjointness (⊥⊥) | `disjoint/2` | `disjoint(commercial, nonCommercial)` |
| UNA (distinct concepts) | `!=` via fof | `france != germany` |

### Template: GEO000-0.ax (GeoNames spatial)

```tptp
%--------------------------------------------------------------------------
% File: GEO000-0.ax — GeoNames spatial KB (mereological)
% Paper: Definition 2, Table 1 (spatial, ≤ = ⪯)
%--------------------------------------------------------------------------

% --- Concepts ---
fof(c_europe,  axiom, concept(europe)).
fof(c_france,  axiom, concept(france)).
fof(c_germany, axiom, concept(germany)).
fof(c_bavaria, axiom, concept(bavaria)).

% --- Hierarchy (part-whole: ⪯) ---
%     Only non-reflexive, non-transitive edges needed.
%     Layer 1 provides reflexivity + transitivity.
fof(geo_fr_eu,  axiom, leq(france, europe)).
fof(geo_de_eu,  axiom, leq(germany, europe)).
fof(geo_bav_de, axiom, leq(bavaria, germany)).
%     Vampire derives: leq(bavaria, europe) via leq_trans

% --- Disjointness ---
%     Sibling regions under same parent are disjoint.
fof(geo_disj_fr_de, axiom, disjoint(france, germany)).
%     Vampire derives: disjoint(bavaria, france) via disj_downward
%     Vampire derives: disjoint(france, bavaria) via disj_sym

% --- UNA (Unique Name Assumption) ---
fof(una_geo_1, axiom, europe != france).
fof(una_geo_2, axiom, europe != germany).
fof(una_geo_3, axiom, europe != bavaria).
fof(una_geo_4, axiom, france != germany).
fof(una_geo_5, axiom, france != bavaria).
fof(una_geo_6, axiom, germany != bavaria).
```

### Template: DPV000-0.ax (W3C DPV purpose — taxonomic)

```tptp
%--------------------------------------------------------------------------
% File: DPV000-0.ax — W3C Data Privacy Vocabulary (taxonomic)
% Paper: Definition 2, Table 1 (purpose, ≤ = ⊑)
%--------------------------------------------------------------------------

% --- Concepts ---
fof(c_purpose,       axiom, concept(purpose)).
fof(c_commercial,    axiom, concept(commercial)).
fof(c_nonCommercial, axiom, concept(nonCommercial)).
fof(c_research,      axiom, concept(research)).
fof(c_commRes,       axiom, concept(commercialResearch)).
fof(c_nonCommRes,    axiom, concept(nonCommercialResearch)).
fof(c_marketing,     axiom, concept(marketing)).
fof(c_academic,      axiom, concept(academicResearch)).
fof(c_sciRes,        axiom, concept(scientificResearch)).
fof(c_rnd,           axiom, concept(researchAndDevelopment)).

% --- Hierarchy (class subsumption: ⊑) ---
fof(dpv_comm_purp,     axiom, leq(commercial, purpose)).
fof(dpv_nonc_purp,     axiom, leq(nonCommercial, purpose)).
fof(dpv_res_purp,      axiom, leq(research, purpose)).
fof(dpv_commres_comm,  axiom, leq(commercialResearch, commercial)).
fof(dpv_commres_res,   axiom, leq(commercialResearch, research)).
fof(dpv_noncres_nonc,  axiom, leq(nonCommercialResearch, nonCommercial)).
fof(dpv_noncres_res,   axiom, leq(nonCommercialResearch, research)).
fof(dpv_mkt_comm,      axiom, leq(marketing, commercial)).
fof(dpv_acad_noncres,  axiom, leq(academicResearch, nonCommercialResearch)).
fof(dpv_sci_res,       axiom, leq(scientificResearch, research)).
fof(dpv_rnd_res,       axiom, leq(researchAndDevelopment, research)).

% --- Disjointness ---
fof(dpv_disj_comm_nonc, axiom, disjoint(commercial, nonCommercial)).
%     Vampire derives: disjoint(marketing, nonCommercialResearch)
%     Vampire derives: disjoint(commercialResearch, academicResearch)
%     etc. via disj_downward

% --- UNA ---
fof(una_dpv_01, axiom, purpose != commercial).
fof(una_dpv_02, axiom, purpose != nonCommercial).
% ... (all pairs of distinct concepts)
```

### Template: NOM000-0.ax (Nominal — delivery channels)

```tptp
%--------------------------------------------------------------------------
% File: NOM000-0.ax — Nominal KB (identity only)
% Paper: Definition 2 (≤ = =, ⊥⊥ total on distinct)
% Note: Under identity, leq_refl from Layer 1 gives leq(X,X).
%       No additional leq facts needed.
%       Disjointness = all UNA pairs.
%--------------------------------------------------------------------------

% --- Concepts ---
fof(c_mobile,  axiom, concept(mobile)).
fof(c_web,     axiom, concept(web)).
fof(c_api,     axiom, concept(api)).
fof(c_print,   axiom, concept(print)).

% --- Disjointness (total on distinct: x ⊥⊥ y ↔ x ≠ y) ---
fof(nom_disj_1, axiom, disjoint(mobile, web)).
fof(nom_disj_2, axiom, disjoint(mobile, api)).
fof(nom_disj_3, axiom, disjoint(mobile, print)).
fof(nom_disj_4, axiom, disjoint(web, api)).
fof(nom_disj_5, axiom, disjoint(web, print)).
fof(nom_disj_6, axiom, disjoint(api, print)).

% --- UNA ---
fof(una_nom_1, axiom, mobile != web).
fof(una_nom_2, axiom, mobile != api).
fof(una_nom_3, axiom, mobile != print).
fof(una_nom_4, axiom, web != api).
fof(una_nom_5, axiom, web != print).
fof(una_nom_6, axiom, api != print).
```

---

## Layer 2: Grounding (GROUND000-1.ax)

Maps ODRL right-operand values to KB concepts (Definition 2, γ function).

```tptp
%--------------------------------------------------------------------------
% File: GROUND000-1.ax — γ mappings
% Paper: Definition 2, γ: V ⇀ C
%--------------------------------------------------------------------------

% Grounding predicate: gamma(OdrlValue, KBConcept)
% "The ODRL right-operand value V maps to KB concept G"

% Example groundings for spatial:
fof(g_france, axiom, gamma(val_france, france)).
fof(g_europe, axiom, gamma(val_europe, europe)).

% Example groundings for purpose:
fof(g_comm,     axiom, gamma(val_commercial, commercial)).
fof(g_noncomm,  axiom, gamma(val_nonCommercial, nonCommercial)).
fof(g_sciRes,   axiom, gamma(val_scientificResearch, scientificResearch)).
```

**Note:** When `gamma(v) = ⊥` (unmapped), simply omit the gamma fact.
The open-world assumption means absence = unknown, producing ⊤ denotation.

---

## Problem Files: Conjecture Patterns (Definition 5, Table 2)

### Pattern 1: Testing Compatibility (∃ witness)

```tptp
% File: ODRL010-1.p — France isPartOf Europe vs Germany eq Germany
% Expected: Compatible (witness: germany ∈ both denotations? No...)
% Actually testing: is there X in both denotations?

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% Conjecture: ∃x in both denotations
fof(conjecture_compatible, conjecture,
    ?[X]: (in_denotation(X, europe, isPartOf)
         & in_denotation(X, germany, eq))).

% If Vampire returns Theorem → Compatible
% If Vampire returns CounterSatisfiable → Unknown (open world)
```

### Pattern 2: Testing Conflict (¬∃ witness)

```tptp
% File: ODRL011-1.p — France eq France vs Germany eq Germany
% Expected: Conflict

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% Conjecture: ¬∃x in both denotations
fof(conjecture_conflict, conjecture,
    ~?[X]: (in_denotation(X, france, eq)
          & in_denotation(X, germany, eq))).

% If Vampire returns Theorem → Conflict
% If Vampire returns CounterSatisfiable → Unknown
```

### Pattern 3: Testing Unknown (both conjectures fail)

For Unknown verdicts, run BOTH patterns. Both should return
CounterSatisfiable, confirming genuine indeterminacy.

### Pattern 4: Set-valued operators

```tptp
% isAnyOf example: purpose isAnyOf {commercial, research}
% Assert value list membership, then use in_denotation_set

fof(vl_comm, axiom, in_value_list(commercial, list1)).
fof(vl_res,  axiom, in_value_list(research, list1)).

fof(conjecture, conjecture,
    ?[X]: (in_denotation_set(X, list1, isAnyOf)
         & in_denotation(X, nonCommercial, eq))).
```

---

## Cross-KB Alignment (Definition 7, Layer: Alignment files)

### ALIGN001-0.ax template

```tptp
%--------------------------------------------------------------------------
% File: ALIGN001-0.ax — GeoNames ↔ ISO 3166 alignment
% Paper: Definition 7, α: C_A ⇀ C_B
%--------------------------------------------------------------------------

% Alignment predicate: align(ConceptInA, ConceptInB)
% Must be injective and order-preserving (biconditional).

fof(align_fr, axiom, align(france, iso_FR)).
fof(align_de, axiom, align(germany, iso_DE)).
fof(align_eu, axiom, align(europe, iso_EU)).
% Note: bavaria has NO counterpart in ISO 3166 → omit → graceful degradation

% Alignment axiom: order preservation (biconditional)
fof(align_order, axiom,
    ![X,Y,Xa,Ya]: ((align(X, Xa) & align(Y, Ya))
        => (leq(X, Y) <=> leq_b(Xa, Ya)))).

% Alignment axiom: disjointness preservation (forward only)
fof(align_disj, axiom,
    ![X,Y,Xa,Ya]: ((align(X, Xa) & align(Y, Ya) & disjoint(X, Y))
        => disjoint_b(Xa, Ya))).

% Alignment axiom: injectivity
fof(align_inj, axiom,
    ![X,Y,Z]: ((align(X, Z) & align(Y, Z)) => (X = Y))).
```

---

## Complete Axiom Count for ODRL000-0.ax

| Section | Paper Reference | # Axioms | Status |
|---|---|---|---|
| A. Structural | Def. 1 | 8 | ✅ Keep |
| B. KB properties | Def. 2 (≤) | 2 | ❌ Add |
| B. KB properties | Def. 2 (⊥⊥) | 3 | ❌ Add |
| C. Consistency | Lemma 1 | 1 | ❌ Add |
| D. Denotation (single) | Def. 3 (eq, neq, isA, isPartOf, hasPart) | 10 | ❌ Add |
| E. Denotation (set) | Def. 3 (isAnyOf, isAllOf, isNoneOf) | 6 | ❌ Add |
| **Total** | | **30** | 8 present, 22 missing |
| *To delete* | | *12* | Dead code |

---

## Verification Checklist

After updating ODRL000-0.ax:

```bash
# 1. Run one Compatible problem
vampire --mode casc Problems/ODRL/KBGrounding/Spatial/ODRL010-1.p
# Expect: Theorem (SZS status)

# 2. Run one Conflict problem
vampire --mode casc Problems/ODRL/KBGrounding/Spatial/ODRL011-1.p
# Expect: Theorem

# 3. Run one Unknown problem (alignment with unmapped concept)
vampire --mode casc Problems/ODRL/KBGrounding/Alignment/ODRL057-1.p
# Expect: CounterSatisfiable

# 4. Full suite
python evaluate_provers.py
# Expect: 154/154 agreement
```

---

## Predicate Inventory

| Predicate | Arity | Defined in | Paper Reference |
|---|---|---|---|
| `concept/1` | 1 | Layer 0 | Def. 2 (C) |
| `leq/2` | 2 | Layer 0 | Def. 2 (≤) |
| `disjoint/2` | 2 | Layer 0 | Def. 2 (⊥⊥) |
| `gamma/2` | 2 | Layer 2 | Def. 2 (γ) |
| `in_denotation/3` | 3 | Layer 1 | Def. 3 |
| `in_denotation_set/3` | 3 | Layer 1 | Def. 3 (set ops) |
| `in_value_list/2` | 2 | Problem/Layer 2 | Def. 3 (set ops) |
| `align/2` | 2 | Alignment | Def. 7 (α) |
| `policy/1` | 1 | Layer 1 | Sec. 3.1 |
| `permission/1` | 1 | Layer 1 | Sec. 3.1 |
| `prohibition/1` | 1 | Layer 1 | Sec. 3.1 |
| `constraint/1` | 1 | Layer 1 | Def. 1 |
| `has_operand/2` | 2 | Layer 1 | Def. 1 |
| `has_operator/2` | 2 | Layer 1 | Def. 1 |
| `has_value/2` | 2 | Layer 1 | Def. 1 |
| `same_operand/2` | 2 | Layer 1 | Def. 5 scope |

---

## What Is NOT Encoded (Future Work)

| Paper element | Why not encoded | Target |
|---|---|---|
| Def. 4 (Conservative ∩) | Implicit: ⊤ = open world, Vampire handles | N/A |
| Def. 5 (Verdict function) | Meta-level: read from SZS output | N/A |
| Def. 6 (Composition) | Meta-level: combine per-operand verdicts in Python | N/A |
| Thm. 1–3, Props, Lemmas | Verified in Isabelle, tested by benchmarks | N/A |
| Def. 8–9 (Aligned constraint) | Per-problem alignment in problem files | N/A |
| Runtime semantics | Def. 10–12 tested by Runtime benchmarks (070–075) | N/A |
