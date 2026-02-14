# ODRL Benchmark Suite: TPTP-Grade Upgrade Plan

## Current State vs. TPTP Requirements

### What you have
- 154 problems in TPTP (.p) and SMT-LIB (.smt2)
- 2 provers: Vampire, Z3
- Binary pass/fail: "both agree on all 154"
- No timing data, no difficulty ratings, no proof analysis

### What TPTP acceptance requires
Every problem in TPTP has standardized metadata. Look at any TPTP file header:

```
%--------------------------------------------------------------------------
% File     : ODRL010-1 : TPTP v9.0.0. Released v9.1.0.
% Domain   : Policy (ODRL)
% Problem  : Spatial compatibility: France isPartOf Europe
% Version  : [Mus26] axioms.
% English  : Test whether a request from France is compatible with a
%            policy requiring Europe, using GeoNames mereological KB.
% Refs     : [Mus26] Mustafa, D. (2026), Grounding ODRL Constraints...
% Source   : [Mus26]
% Names    : ODRL010-1 [Mus26]
%
% Status   : Theorem
% Rating   : 0.00 v9.1.0
% Syntax   : Number of clauses    : 18
%            Number of literals    : 24
%            Maximal clause size   :  3
%            Number of predicates  :  4
%            Number of functors    : 12
%            Number of variables   :  6
%            Maximal term depth    :  1
%            (EPR fragment)
% SPC      : CNF_THM_EPR
%
% Comments : Part of the ODRL KB-grounding benchmark suite.
%--------------------------------------------------------------------------
```

### The 7 gaps you must close

| # | Gap | Impact | Effort |
|---|-----|--------|--------|
| 1 | Only 2 provers | No difficulty rating possible | Medium |
| 2 | No TPTP headers | Instant rejection by Geoff | Low |
| 3 | No timing/performance data | No cactus plots, no analysis | Medium |
| 4 | No syntax statistics | Missing from headers | Low |
| 5 | No difficulty ratings | Core TPTP requirement | Depends on #1 |
| 6 | No proof structure analysis | Misses interesting findings | High |
| 7 | No SPC classification | Required for TPTP categorization | Low |

---

## Gap 1: Multi-Prover Evaluation (Critical)

### Target provers (minimum 6)

| Prover | Type | Why it matters | Install |
|--------|------|----------------|---------|
| **Vampire** | Superposition | Gold standard ATP | Binary from GitHub |
| **Z3** | DPLL(T)/SMT | Ground decision procedures | `pip install z3-solver` or binary |
| **E** | Superposition | Second major ATP, different heuristics | Build from source |
| **CVC5** | SMT | Alternative SMT, different internals | Binary from GitHub |
| **iProver** | Instantiation | EPR-specialized — this is key for you | Build from source |
| **SPASS** | Superposition | Classic prover, long history | Build from source |

**Why iProver is critical**: iProver is specifically designed for the EPR fragment. Your problems are EPR. If iProver handles them differently than Vampire/E, that's a finding. If it's faster, that validates your EPR classification. If it struggles on some, that reveals structural complexity.

### What multi-prover data gives you

1. **Difficulty ratings**: TPTP rates problems 0.00–1.00 based on fraction of provers that fail
2. **Prover disagreements**: If prover X says Theorem but prover Y times out, that's interesting
3. **Performance profiles**: Which prover architecture suits policy reasoning best?
4. **Proof length comparison**: Superposition vs. instantiation proof sizes

### Difficulty rating formula (TPTP standard)
```
Rating = 1 - (provers_that_solved / total_provers)
```
- Rating 0.00: All provers solve it instantly (trivial)
- Rating 0.33: 2/3 of provers solve it
- Rating 1.00: No prover solves it (open)

Your problems are likely all 0.00 for the single-KB ones (small EPR, every prover will crush them). The interesting question is whether composition/alignment/xone problems get nonzero ratings.

---

## Gap 2: TPTP Header Compliance

Every .p file needs the full header block. This is non-negotiable for TPTP submission.

### Required fields
- `File`: Problem name and TPTP version
- `Domain`: "Policy (ODRL)" — this would be a NEW domain in TPTP
- `Problem`: One-line English description
- `Version`: Citation key for axioms
- `English`: Longer description of what's being tested
- `Refs`: BibTeX-style citation
- `Source`: Where it came from
- `Names`: Cross-references
- `Status`: SZS status (Theorem, CounterSatisfiable, etc.)
- `Rating`: Difficulty (computed from multi-prover runs)
- `Syntax`: Clause/literal/predicate/functor/variable counts
- `SPC`: Specifica Problem Class (e.g., `CNF_THM_EPR`, `FOF_CSA_EPR`)

### SPC classification for your problems

Your problems should classify as:
- **Theorem problems** (Conflict/Compatible proved): `FOF_THM_EPR` or `CNF_THM_EPR`
- **CounterSatisfiable problems** (Unknown verdict): `FOF_CSA_EPR` or `CNF_CSA_EPR`

The EPR suffix is important — it tells the community this is decidable.

---

## Gap 3: Performance Analysis Framework

### Required outputs
1. **Per-problem timing table**: All provers × all problems
2. **Cactus plot**: Problems solved (y) vs. time limit (x) per prover
3. **Category breakdown**: Average time per category per prover
4. **Proof size comparison**: Inference count per prover per problem

### Key hypotheses to test
- H1: iProver (instantiation-based) outperforms superposition provers on EPR policy problems
- H2: xone problems are harder than and/or problems across all provers
- H3: Cross-KB alignment problems with partial mappings are harder than total alignment
- H4: Structural KBs (diamond, chain) reveal different prover behavior than domain KBs

---

## Gap 4: EPR Fragment Characterization

### What to measure per problem
```
- Number of clauses (after clausification)
- Number of literals (total)
- Maximal clause size
- Number of predicates
- Number of constants (functors of arity 0)
- Number of variables
- Maximal term depth (should be 1 for pure EPR)
- Whether it's strictly EPR or uses extensions
```

### Named EPR subclasses to check
Your problems may fall into even more restricted fragments:
- **BSR (Bernays-Schönfinkel-Ramsey)**: ∃*∀* prefix, no function symbols — this is EPR
- **EPR with equality**: If you use `=`, this is still decidable but harder
- **Monadic EPR**: All predicates unary — extremely tractable
- **2-variable fragment**: Only 2 variables — decidable even with function symbols

If your problems are in a named tractable subclass, that's a publishable characterization.

---

## Gap 5: What Would Make Geoff Accept This

Based on how TPTP domains get added, you need:

1. **Justification that this is a genuinely new domain**: ODRL/policy reasoning doesn't exist in TPTP. The closest are the "Software Verification" (SWV) and "Knowledge Management" (KNM) domains. Argue that policy conflict detection is distinct.

2. **Sufficient problem diversity**: 154 problems is good. But they need to span a range of difficulties. If all 154 are trivially solved by every prover in 0.01s, Geoff may ask "why bother?" You need some problems that are genuinely challenging.

3. **Problems that stress provers**: This is where you need to think about scaling. Can you generate harder variants?
   - Larger KBs (50, 100, 500 concepts instead of 4-10)
   - Deeper hierarchies (20 levels instead of 5)
   - More constraint dimensions in composition
   - Larger isAnyOf/isAllOf value sets

4. **Clean axiomatization**: Your Layer0/Layer1/Layer2 structure is actually good. Geoff likes modular axiom files.

5. **TPTP naming convention compliance**: Your `ODRL010-1.p` naming is already close. The format is `DOMAIN###-version.p`.

---

## Concrete Action Plan

### Phase 1: Infrastructure (1 week)
- [ ] Add TPTP headers to all 154 .p files (script this)
- [ ] Compute syntax statistics for all problems (script this)  
- [ ] Set up multi-prover runner with timing

### Phase 2: Multi-Prover Evaluation (1-2 weeks)
- [ ] Install/build E, CVC5, iProver, SPASS
- [ ] Run all 154 × 6 provers with 60s timeout
- [ ] Compute difficulty ratings
- [ ] Generate performance tables and cactus plots
- [ ] Identify any disagreements or interesting behaviors

### Phase 3: Scaling (1-2 weeks)
- [ ] Generate harder variants with larger KBs
- [ ] Target 200-300 total problems with difficulty spread
- [ ] Re-run multi-prover evaluation on extended suite

### Phase 4: Analysis & Writing (1-2 weeks)
- [ ] EPR subclass characterization
- [ ] Proof structure analysis (where available)
- [ ] Write up findings for paper
- [ ] Email Geoff with proposal for TPTP inclusion

### Phase 5: TPTP Submission
- [ ] Package problems with headers, axiom files, solutions
- [ ] Provide Geoff with evaluation data
- [ ] Respond to any requests for modifications
