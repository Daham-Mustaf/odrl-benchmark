
# Validation Protocol — Per-Problem

For each problem `KGC{N}.p` / `KGC{N}.smt2`, run the four blocks below.
All commands assume `cd ~/Desktop/tptp-odrl/Problems/ODRL/KGConstraints`.
[Vampire 4.7-SMT System Description](https://smt-comp.github.io/2022/system-descriptions/Vampire.pdf)

---

## Block 1: Portfolio agreement (5 reasoners)

```bash
NAME=KGC300-1   # change per problem

vampire --mode casc --time_limit 30 --include . Conflict/$NAME.p 2>&1 | grep "SZS status"
eprover --auto --tptp3-format --cpu-limit=30 -s Conflict/$NAME.p 2>&1 | grep "SZS status"
z3 -T:30 Conflict/$NAME.smt2
cvc5 --tlimit=30000 Conflict/$NAME.smt2
```

**Expected:**
| Verdict     | Vampire             | E                   | Z3    | CVC5  |
|-------------|---------------------|---------------------|-------|-------|
| Conflict    | Theorem             | Theorem             | unsat | unsat |
| Compatible  | Theorem             | Theorem             | sat   | sat   |
| Unknown     | CounterSatisfiable  | CounterSatisfiable  | sat   | sat   |

All four must agree. Disagreement = encoding bug.

---

## Block 2: Strategy diversity (Vampire, 4 algorithms)

For Theorem cases (Conflict, Compatible) only:

```bash
for sat in discount lrs otter inst_gen; do
    echo -n "  $sat: "
    vampire --saturation_algorithm $sat --time_limit 30 \
        --include . Conflict/$NAME.p 2>&1 | grep "SZS status" | awk '{print $4}'
done
```

**Expected:** all four return `Theorem`. Confirms result is not strategy-dependent.

---

## Block 3: Model finding (Unknown cases only)

```bash
# Vampire fmb
vampire --saturation_algorithm fmb --fmb_start_size 5 --time_limit 60 \
    --include . Conflict/$NAME.p 2>&1 | head -20

# Mace4
tptp_to_ladr < Conflict/$NAME.p > /tmp/$NAME.in
mace4 -t 30 -f /tmp/$NAME.in 2>&1 | grep -E "MODEL|domain size|model"

# Z3 model
z3 -smt2 <(cat Conflict/$NAME.smt2; echo "(get-model)")
```

**Expected:** all three find a model. Confirms Unknown is genuine OWA, not encoding error.

---

## Block 4: OWA two-extension witness (Unknown cases only)

Confirms the verdict is sensitive to resource extension.

```bash
# Identify the two grounded concepts in this problem
# (read from problem file; example below uses dpv_scientific_research / dpv_non_commercial_purpose)
G1=dpv_scientific_research
G2=dpv_non_commercial_purpose

# Variant A: add subclass → should prove verdict_compatible
(sed 's/verdict_unknown/verdict_compatible/' Conflict/$NAME.p
 echo "fof(force_compat, axiom, kge_leq($G1, $G2))."
) > /tmp/$NAME-A.p

# Variant B: add disjointness → should prove verdict_conflict
(sed 's/verdict_unknown/verdict_conflict/' Conflict/$NAME.p
 echo "fof(force_conflict, axiom, kge_disjoint($G1, $G2))."
) > /tmp/$NAME-B.p

echo -n "  Variant A (force compat):   "
vampire --mode casc --time_limit 30 --include . /tmp/$NAME-A.p 2>&1 \
    | grep "SZS status" | awk '{print $4}'
echo -n "  Variant B (force conflict): "
vampire --mode casc --time_limit 30 --include . /tmp/$NAME-B.p 2>&1 \
    | grep "SZS status" | awk '{print $4}'
```

**Expected:**
- Variant A → `Theorem` (extension makes them compatible)
- Variant B → `Theorem` (extension makes them conflict)

Both extensions consistent → Unknown is the right pre-extension verdict.
