# Killer Benchmark: What You Have vs. What You Need

## TL;DR

**Your ODRL210–213 is NOT the killer benchmark from the paper.**

It tests:
- ✓ Strengthened Def 8 (unmapped witnesses) 
- ✓ Cross-KB alignment properties
- ✓ Individual constraint operators

It does NOT test:
- ✗ Full XONE composition (tests branches separately)
- ✗ Multi-operand AND within XONE branches
- ✗ The actual BSB/French Archive scenario
- ✗ Three-stage verdict progression (Unknown → Compatible → Unknown)

---

## What You Should Do

### Option A: Add ODRL214 (Recommended)

Create **3 new problem files** implementing the full killer scenario:

1. **ODRL214-1.p** — Base KB → Unknown
   - Uses DPV000 (no negative axiom)
   - Full XONE encoding
   - Expected: CounterSatisfiable

2. **ODRL214-2.p** — Enriched KB → Compatible
   - Uses DPV004 (with ¬(sciRes ⊑ comm))
   - Same encoding as 214-1
   - Expected: Theorem

3. **ODRL214-3.p** — Aligned KB → Unknown
   - Uses GDPR001 + ISO3166
   - Tests Prop 1.2 (graceful degradation)
   - Expected: CounterSatisfiable

**I've already created these files for you** (see the 3 .p files).

**Benefits:**
- ✓ Actually tests what the paper claims
- ✓ One scenario, three KB configs → clean story
- ✓ Validates full stack (Def 1–8, Lemma 2, Prop 1.1–1.2, Thm 1–2)
- ✓ Can claim "killer benchmark" honestly

**Cost:**
- Need to create 2 new KB files (DPV004, GDPR001)
- Need to create 2 alignment files (DPV→GDPR, GEO→ISO)
- ~3 new problem files

**Paper changes:**
- Add Section 5.5 "Integration Test: The Killer Benchmark"
- Update Table 5: add 3 problems (154 → 157 total)
- Reference ODRL214 throughout as the comprehensive example

---

### Option B: Rename ODRL210–213

If you don't want to add new benchmarks:

**Rename to:** "Alignment Validation Suite" or "Def 8 Test Suite"

**Remove claim:** "exercises every definition" (it doesn't!)

**Add note:** "The full multi-operand XONE scenario is validated through unit tests across ODRL085/086 (XONE), ODRL211 (AND composition), and ODRL212 (alignment). An integrated benchmark combining all aspects is left for future work."

**Benefits:**
- ✓ Honest about scope
- ✓ No new work needed

**Cost:**
- ✗ Less impressive ("test suite" vs "killer benchmark")
- ✗ Doesn't actually validate the paper's opening scenario

---

### Option C: Expand ODRL211

Merge the two ODRL211 files into a single XONE encoding:

**Current:**
- ODRL211-1: Branch A separately
- ODRL211-2: Branch B separately

**New:**
- ODRL211-unified: Full XONE(Branch A, Branch B) vs Request

This is **half-way** to the killer benchmark but still doesn't test:
- ✗ Three-stage KB progression
- ✗ Cross-KB alignment on full scenario

---

## My Recommendation

**Do Option A.** Here's why:

1. **You already have 90% of the needed KBs**
   - GEO003 exists (you reference it)
   - DPV000 exists (base version)
   - Just need: DPV004 (add 1 negative axiom), GDPR001 (subset of DPV000)

2. **The TPTP encoding is straightforward**
   - I've already written all 3 files for you
   - Just copy to your repo and test with Vampire

3. **Makes the paper MUCH stronger**
   - Reviewers love integration tests
   - Shows you didn't just cherry-pick easy cases
   - Validates the actual scenario you trace in the intro

4. **Fixes the semantic gap I found**
   - Your current suite doesn't actually test XONE composition
   - ODRL085/086 test witness-level XONE in isolation
   - ODRL214 tests verdict-level XONE with multi-operand composition

---

## Next Steps (If You Choose Option A)

### Step 1: Create Missing KB Files

**DPV004-0.ax** (enriched purpose KB):
```tptp
% Copy DPV000-0.ax entirely
% Then ADD this single axiom at the end:
fof(dpv_sci_not_comm, axiom, 
    ~subClassOf(scientificResearch, commercialPurpose)).
```

**GDPR001-0.ax** (GDPR-derived purpose KB):
```tptp
% Subset of DPV with only 6 concepts:
% - purpose (root)
% - commercialPurpose
% - nonCommercialPurpose  
% - commercialResearch
% - nonCommercialResearch
% (Omit: R&D, scientificResearch, academicResearch, marketing, advertising)

% Standard reflexive + transitive
% 5 positive axioms (same as DPV000 but restricted)
% 2 negative axioms (commercial vs nonCommercial disjoint)
```

**ISO3166-0.ax** (ISO country codes spatial KB):
```tptp
% Subset of GEO003 with only 6 concepts:
% - world (root)
% - europe, asia (level 1)
% - france, germany, austria (level 2 under europe)
% (Omit: westernEurope, easternEurope, paris)

% Standard reflexive + transitive for partOf
% UNA axioms for countries
```

### Step 2: Create Alignment Files

**ALIGN-DPV-GDPR.ax**:
```tptp
% Documents the alignment map (no TPTP encoding needed, just comments)
% Mapped: purpose, commercial, nonCommercial, commRes, nonCommRes
% Unmapped: R&D, sciRes, academicRes, marketing, advertising, directMktg
```

**ALIGN-GEO-ISO.ax**:
```tptp
% Mapped: world, europe, asia, france, germany, austria
% Unmapped: westernEurope, easternEurope, paris
```

### Step 3: Test with Vampire

```bash
vampire --mode casc ODRL214-1.p
# Expected: % SZS status CounterSatisfiable

vampire --mode casc ODRL214-2.p  
# Expected: % SZS status Theorem

vampire --mode casc ODRL214-3.p
# Expected: % SZS status CounterSatisfiable
```

### Step 4: Update Paper

**Section 5.5 (new):**
```latex
\subsection{Integration Test: The Killer Benchmark}

The BSB/French Archive scenario from Table~\ref{tab:challenges} exercises 
the complete stack. ODRL214 encodes this scenario across three KB 
configurations:

\begin{itemize}
\item \textbf{ODRL214-1} (base DPV): Missing negative axiom for 
  \texttt{scientificResearch} yields \textsc{Unknown} (CounterSat).
\item \textbf{ODRL214-2} (enriched DPV): Adding 
  \texttt{¬(sciRes $\sqsubseteq$ commercial)} resolves XONE → 
  \textsc{Compatible} (Theorem).
\item \textbf{ODRL214-3} (GDPR/ISO3166): Cross-KB alignment degrades 
  verdict to \textsc{Unknown} via unmapped concepts (CounterSat), 
  validating Proposition~\ref{prop:alignment}.
\end{itemize}

This validates the framework end-to-end: Definitions 1–8, Lemma 2, 
Propositions 1.1–1.2, and Theorems 1–2.
```

**Table 5 update:**
```
Integration test: 214 (3 problems)
Total: 154 → 157
```

---

## Bottom Line

Your ODRL210–213 is a **good unit test suite** for alignment properties.

But it's NOT the "killer benchmark" that exercises the full scenario.

**Add ODRL214** (I've already written it for you!) and you'll have:
- ✓ Honest coverage claim
- ✓ Impressive integration test
- ✓ Validation of actual paper scenario
- ✓ Stronger paper

It's ~2 hours of work (create 2 KB files, test 3 problems, update 1 section).

Worth it?
