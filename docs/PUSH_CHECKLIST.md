# TPTP-ODRL Benchmark — Push Checklist for Geoff

**Goal:** Stable repo that Geoff can clone and test.
**Deadline:** Before he flies to Germany (next weekend).

---

## 1. KB Files — Status

### Layer 0: Domain KBs

| File | Generator | Status | Action |
|------|-----------|--------|--------|
| `GEO000-0.ax` | `gen_layer0_geo.py --scope europe --sibling-disjointness --no-una` | ⬜ Regenerate | Run with `--no-una`, verify axiom count (~430) |
| `DPV000-0.ax` | `gen_layer0_kb.py --no-una` (NO `--sibling-disjointness`) | ⬜ Regenerate | Hierarchy only, no disjointness. Verified consistent  |
| `LANG000-0.ax` | `gen_layer0_lang.py --sibling-disjointness --base-disjointness --no-una` | ⬜ Regenerate | Run with `--no-una`, verify axiom count (~445) |

**After regeneration, verify ALL three are consistent:**

```bash
# Each should return CounterSatisfiable (= consistent KB)
for kb in GEO000-0 DPV000-0 LANG000-0; do
  cat > /tmp/test_${kb}.p << EOF
include('Axioms/Layer0-DomainKB/${kb}.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
fof(test, conjecture, a = b).
EOF
  echo -n "${kb}: "
  vampire --include Problems/ODRL --time_limit 60 --mode casc /tmp/test_${kb}.p 2>&1 | grep "SZS status"
done
```

### Layer 1: ODRL Core

| File | Status | Action |
|------|--------|--------|
| `ODRL000-0.ax` | Exists | Verify: leq_refl, leq_trans, leq_antisym, disj_sym, disj_downward, disj_irrefl |

### Layer 2: Grounding (if used)

| File | Status | Action |
|------|--------|--------|
| `GROUND000-1.ax` | ⬜ Check | Only used by deep-embedding problems. Do we still need this? |

---

## 2. Geoff's Three Questions — Responses

### Q1: CounterSatisfiable conflation  RESOLVED

**Geoff said:** THM, CSA, CTH exist. ATP systems don't claim CTH — user negates conjecture.

**Our approach:** `gen_spatial_suite.py --encoding prover` flips all CSA conjectures.
- Original: `∃X: den₁∧den₂` → Expected: CounterSatisfiable
- Flipped:  `∀X: ¬(den₁∧den₂)` → Expected: Theorem (proves disjointness)

**Action:** Keep both encodings. Default = prover (all Theorem). Document in headers.

### Q2: UNA vs disjointness  RESOLVED

**Geoff said:** Use `$distinct(a,b,c,...)` built-in. Good ATP systems know it.

**Our finding:** Implicit UNA Lemma — tree + disjointness → UNA for free.

**Action for GEO/LANG:** Drop UNA entirely (`--no-una`). Disjointness handles it.
**Action for DPV:** No disjointness → may need `$distinct` IF any problem needs it.
**Test:** Do any DPV problems need distinctness? If only subsumption → no.

⬜ Check: Do composition problems 040-047 need DPV distinctness?

### Q3: Composition encoding  RESOLVED

**Geoff said:** Let's do tests. Single conjecture if easy enough, split if too hard.

**Our approach:** Single conjecture. Already encoded as:
- AND: `∃Xs(spatial) ∧ ∃Xp(purpose)`
- OR:  `∃Xs(spatial) ∨ ∃Xp(purpose)`
- XONE: `(∃Xs ∧ ¬∃Xp) ∨ (∃Xp ∧ ¬∃Xs)`

---

## 3. Problem Files — Issues to Fix

### GEO-only problems (010-039, 050-055): 31 problems

These use ONLY GEO000-0.ax + ODRL000-0.ax. Should work cleanly.

| # | Problem | Expected | Potential Issue |
|---|---------|----------|-----------------|
| 010 | KB transitivity test | Theorem | None — pure KB |
| 011-019 | Basic conflict/compatible | Mixed | ⬜ Retest all with new GEO (no UNA) |
| 020-025 | Set-valued operators | Mixed | ⬜ Retest |
| 030-037 | Subsumption | Mixed | ⬜ Retest |
| 044 | Self-conflict (single rule) | CSA/Theorem | ⬜ Retest — uses same GEO conjecture as 013 |
| 050-055 | Edge cases | Mixed | ⬜ Retest |

**Action:** Run full suite after KB regeneration:

```bash
uv run python gen_spatial_suite.py -o Problems/ODRL/KBGrounding/Spatial --encoding prover --run
```

### Composition problems (040-047): 7 problems — ⚠️ CRITICAL

These include BOTH GEO + DPV. The DPV dimension tests purpose reasoning.

| # | Spatial | Purpose | Verdict | Issue |
|---|---------|---------|---------|-------|
| 040 | Compatible | Compatible | AND-Compatible | ⬜ Purpose: isA(R&D) ∩ isA(AcademicRes) — needs leq only  |
| 041 | Compatible | **Conflict** | AND-Conflict | 🔴 Purpose: isA(AcadRes) ∩ isA(Marketing) — needs disjointness! |
| 042 | Conflict | Compatible | OR-Compatible | ⬜ Purpose compatible saves it  |
| 043 | Conflict | **Conflict** | OR-Conflict | 🔴 Purpose: isA(AcadRes) ∩ isA(Marketing) — needs disjointness! |
| 045 | Conflict | Compatible | XONE-Compatible | ⬜ Purpose compatible, spatial conflict proven  |
| 046 | Compatible | Compatible | XONE-Unknown | ⬜ Both compatible, needs witness  |
| 047 | Conflict | **Conflict** | XONE-Conflict | 🔴 Purpose: isA(AcadRes) ∩ isA(Marketing) — needs disjointness! |

**Problems 041, 043, 047 need DPV disjointness to prove purpose conflict.**

Without disjointness: Vampire can't prove `isA(AcademicResearch) ∩ isA(Marketing) = ∅`.
It will **timeout** instead of returning the expected verdict.

### Options for 041/043/047:

**Option A (FASTEST): Change purpose pairs to use `eq` instead of `isA`**

Replace:
```
isA(AcademicResearch) ∩ isA(Marketing) → needs disjointness
```
With:
```
eq(AcademicResearch) ∩ eq(Marketing) → needs only distinctness (UNA or $distinct)
```

Add one line to these files:
```
fof(dpv_distinct, axiom, $distinct(academicResearch, marketing)).
```

**Option B: Build DPV000-safe.ax (DAG-safe disjointness)**

Implement `compute_safe_sibling_disjointness` in gen_layer0_kb.py.
~279 safe disjoint pairs, skip 6 protected pairs.
More complete but more work.

**Option C: Drop DPV purpose dimension, use GEO × LANG instead**

Replace purpose operand with language operand. LANG has disjointness.
Cleanest but loses DPV entirely.

### ⬜ DECISION NEEDED: Which option for 041/043/047?

---

## 4. File Structure for Geoff

```
Problems/ODRL/
├── Axioms/
│   ├── Layer0-DomainKB/
│   │   ├── GEO000-0.ax          (UN M49 Europe, tree, sibling-disj, no UNA)
│   │   ├── DPV000-0.ax          (W3C DPV Purpose, DAG, no disjointness, no UNA)
│   │   └── LANG000-0.ax         (BCP47 Languages, forest, sibling+base disj, no UNA)
│   └── Layer1-ODRLCore/
│       └── ODRL000-0.ax         (leq, disj, in_denotation axioms)
├── KBGrounding/
│   └── Spatial/
│       ├── ODRL010-1.p          (38 problem files)
│       ├── ...
│       └── ODRL055-1.p
└── README.md                     (benchmark documentation)
```

---

## 5. $distinct — Implementation

Geoff wants `$distinct` instead of pairwise UNA. Add to generators:

```python
# Instead of:
for c1, c2 in combinations(cs, 2):
    lines.append(f"fof(una_{i}, axiom, {c1} != {c2}).")

# Use:
lines.append(f"fof(una, axiom, $distinct({', '.join(cs)})).")
```

**But we proved UNA is implicit for GEO/LANG.** So:
- GEO: `--no-una` (implicit from tree + disjointness)
- LANG: `--no-una` (implicit from forest + disjointness)
- DPV: May need `$distinct` if any problem requires distinctness

⬜ Test: Does any DPV problem fail without UNA or $distinct?

---

## 6. README.md for Geoff

⬜ Write README covering:
- Benchmark structure (3-layer architecture)
- KB properties (tree vs DAG, disjointness strategy)
- How to run: `vampire --include Problems/ODRL --mode casc <file>`
- SZS status mapping (Theorem=Compatible/Confirmed, CSA=Conflict/Refuted)
- Implicit UNA Lemma (why no UNA needed for tree KBs)
- DAG note (DPV has no disjointness, here's why)

---

## 7. Execution Order

```
Step 1: ⬜ DECIDE on composition fix (Option A/B/C above)
Step 2: ⬜ Regenerate all 3 KBs with --no-una
Step 3: ⬜ Verify all 3 KBs consistent
Step 4: ⬜ Regenerate 38 problems (gen_spatial_suite.py --encoding prover)
Step 5: ⬜ Fix composition problems (per decision in Step 1)
Step 6: ⬜ Run full benchmark, all 38 pass
Step 7: ⬜ Write README.md
Step 8: ⬜ Push to GitHub
Step 9: ⬜ Email Geoff: "stable, ready to clone"
Step 10: ⬜ Attach draft paper
```

---

## 8. Reply to Geoff (Draft)

> Hi Geoff,
>
> Thanks for the detailed feedback. Updates:
>
> 1. CounterSatisfiable: I now pair each CSA problem with a dual (negated) 
>    conjecture. Prover-friendly encoding makes everything Theorem. Both 
>    encodings are in the repo.
>
> 2. $distinct: Noted — will use where needed. I also discovered that for 
>    tree-structured KBs with sibling disjointness, UNA is derivable from 
>    the axioms (antisymmetry + disj_downward + disj_irrefl), so $distinct 
>    is unnecessary for GEO and LANG. DPV is a DAG, so different treatment.
>
> 3. Composition: Encoded as single conjectures (∃Xs∧∃Xp for AND, etc.). 
>    Will test and report.
>
> Repository is now stable. Ready for you to clone and test.
> Draft paper attached — reading for the flight.
>
> Best,
> Daham
