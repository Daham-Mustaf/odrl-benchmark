# ODRL Analysis Modes — SMT-LIB Benchmarks (ODRL400–409)

Three policy analysis capabilities from one denotation-intersection engine.

## Modes

```
┌─────────────────────────────────────────────────────────────┐
│                    verdict_of / subsumption_verdict          │
│                    (same machinery, same soundness)          │
├───────────────────┬───────────────────┬─────────────────────┤
│ Mode 1            │ Mode 2            │ Mode 3              │
│ Self-Contradiction│ Redundancy        │ Refinement          │
│                   │                   │                     │
│ ⟦c1⟧ ∩ ⟦c2⟧ = ∅  │ ⟦c1⟧ ⊆ ⟦c2⟧?     │ ⟦down⟧ ⊆ ⟦up⟧?     │
│ within one policy │ one implies other │ DSSC supply chain   │
│                   │                   │                     │
│ unsat → Conflict  │ unsat → Confirmed │ unsat → Valid       │
│ sat   → OK        │ sat   → Refuted   │ sat   → Violation   │
└───────────────────┴───────────────────┴─────────────────────┘
```

## Knowledge Bases

```
DPV Purpose Taxonomy          GeoNames Spatial Hierarchy
========================      ========================
        Purpose                       Europe
       /       \                     /      \
 ServiceProv  AcademicRes       France    Germany
      |            |           /    \        |
  Marketing   ScientificRes  Paris  Lyon   Berlin

  R&D
   ├── ScientificResearch
   └── CommercialResearch
```

## Benchmarks

### Mode 1: Self-Contradiction (ODRL400–401)

*"Can this policy ever be satisfied?"*

```
ODRL400: (purpose isA ServiceProv) AND (purpose isA AcademicRes)

  ⟦c1⟧ = {ServiceProv, Marketing}
  ⟦c2⟧ = {AcademicRes, ScientificRes}
         ∩ = ∅ → unsat → Conflict
         Policy is DEAD — no request can satisfy it.
```

```
ODRL401: Same + (spatial isPartOf Europe) AND (spatial isPartOf France)

  Purpose: Conflict    ←── kills the AND
  Spatial: Compatible  ←── doesn't matter
  verdict_and [Conflict, Compatible] = Conflict → unsat
```

### Mode 2: Redundancy (ODRL402–404)

*"Is this constraint already implied by another?"*

```
ODRL402: (spatial isPartOf France) ⊆ (spatial isPartOf Europe)?

  {France, Paris, Lyon} ⊆ {Europe, France, ..., Berlin}
  unsat → Confirmed → Europe constraint is redundant under AND

ODRL403: Reverse — (spatial isPartOf Europe) ⊆ (spatial isPartOf France)?

  {Europe, ..., Germany, Berlin} ⊄ {France, Paris, Lyon}
  sat → Refuted → witness: Germany

ODRL404: (purpose isA ScientificRes) ⊆ (purpose isA R&D)?

  {ScientificRes} ⊆ {R&D, ScientificRes, CommercialRes}
  unsat → Confirmed → R&D constraint redundant under AND
```

### Mode 3: Refinement (ODRL405–408)

*"Does downstream validly restrict upstream?"*

```
Supply chain:  BSB Munich ──→ French Archive ──→ Consumer
               (upstream)     (downstream)
               DSSC rule: downstream ⊆ upstream
```

```
ODRL405: R&D → ScientificResearch (purpose)
  {ScientificRes} ⊆ {R&D, ScientificRes, CommercialRes} → unsat → Valid ✓

ODRL406: R&D → ServiceProvision (purpose)
  {ServiceProv, Marketing} ⊄ {R&D, ScientificRes, CommercialRes} → sat → Violation ✗

ODRL407: Europe → France (spatial)
  {France, Paris, Lyon} ⊆ {Europe, ..., Berlin} → unsat → Valid ✓

ODRL408: France → Europe (spatial)
  {Europe, ..., Germany, Berlin} ⊄ {France, Paris, Lyon} → sat → Violation ✗
```

### Combined: Conflict Propagation (ODRL409)

*"If upstream conflicts with a prohibition, does downstream inherit it?"*

```
  Upstream (R&D)          Prohibition (ServiceProv)
  ┌──────────────┐        ┌──────────────┐
  │ R&D          │        │ ServiceProv  │
  │ Scientific   │  ∩ ∅   │ Marketing    │
  │ Commercial   │        │              │
  └──────┬───────┘        └──────────────┘
         │ refines                ↑
  ┌──────┴───────┐                │
  │ Scientific   │  ∩ ∅ ──────────┘  still Conflict
  └──────────────┘
  
  unsat → Conflict propagates through valid refinement
```

## Results

```
File              Expected  Result   Mode
─────────────────────────────────────────────
ODRL400-1.smt2    unsat     unsat    Self-contradiction (purpose)
ODRL401-1.smt2    unsat     unsat    Self-contradiction (multi-op)
ODRL402-1.smt2    unsat     unsat    Redundancy (France ⊆ Europe)
ODRL403-1.smt2    sat       sat      Non-redundancy (Europe ⊄ France)
ODRL404-1.smt2    unsat     unsat    Redundancy (Scientific ⊆ R&D)
ODRL405-1.smt2    unsat     unsat    Refinement valid (purpose)
ODRL406-1.smt2    sat       sat      Refinement invalid (widens)
ODRL407-1.smt2    unsat     unsat    Refinement valid (spatial)
ODRL408-1.smt2    sat       sat      Refinement invalid (widens)
ODRL409-1.smt2    unsat     unsat    Conflict propagation
─────────────────────────────────────────────
                            10/10 ✓
```

## Encoding Note

ODRL400, 401, 409 require **domain closure axioms** — the SMT-LIB
equivalent of Isabelle's `C finite`. Without them, Z3 invents ghost
concepts satisfying both branches simultaneously.

```smt2
(assert (forall ((x Concept))
  (or (= x A) (= x B) (= x C) ...)))
```

Files 402–408 work without closure because subsumption checks
rely on transitivity alone — no ghost can break `France ≤ Europe`.

## Run

```bash
for f in ODRL4*.smt2; do printf "%-20s " "$f"; z3 "$f"; done
```

## Isabelle Correspondence

Each benchmark has a matching lemma in `ODRL_Analysis_Modes.thy`.
Same denotations, same verdicts, same soundness guarantees.
