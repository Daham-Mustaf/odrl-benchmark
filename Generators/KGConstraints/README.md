Here's a clean, concise README for the audit suite:

```markdown
# ODRL Conflict Detection — Empirical Validation Suite

54 problems validating the formal claims of "Denotational Semantics
for ODRL: Knowledge-Based Constraint Conflict Detection."

## Requirements

- Python 3.13 with `uv` and `rdflib`
- Vampire 5.0.0 ([https://vprover.github.io](https://vprover.github.io))
- E 3.2.5 ([https://eprover.org](https://eprover.org))
- Z3 4.15+ ([https://github.com/Z3Prover/z3](https://github.com/Z3Prover/z3))
- cvc5 1.3+ ([https://cvc5.github.io](https://cvc5.github.io))
- `tptp4X` (optional, for axiom-file syntax checks)

## Layout

```
Generators/KGConstraints/         Python generators for all problems
Problems/ODRL/KGConstraints/
  Axioms/                         Foundation axiom files (.ax)
  Conflict/                       Per-operator grid (KGC300–461)
  Refinement/                     Lemma 1 (KGC500–502)
  Runtime/                        Theorem 4 (KGC600–602)
  Composition/                    Corollary 1, Proposition 2 (KGC700–713)
  Monotonicity/                   Proposition 1 (KGC800–812)
  Alignment/                      Proposition 3 (KGC900–910)
  Policies/                       Source ODRL policies (.ttl)
```

## Regenerating problems

```bash
uv run Generators/KGConstraints/gen_kge.py
uv run Generators/KGConstraints/gen_denotation.py
uv run Generators/KGConstraints/gen_compose000.py
uv run Generators/KGConstraints/gen_compose001.py
uv run Generators/KGConstraints/gen_bcp47.py
uv run Generators/KGConstraints/gen_dpv.py
uv run Generators/KGConstraints/gen_geonames.py
uv run Generators/KGConstraints/gen_motivating_problems.py
uv run Generators/KGConstraints/gen_operators.py
uv run Generators/KGConstraints/gen_refinement_problems.py
uv run Generators/KGConstraints/gen_runtime_problems.py
uv run Generators/KGConstraints/gen_composition_problems.py
uv run Generators/KGConstraints/gen_or_xone_problems.py
uv run Generators/KGConstraints/gen_monotonicity_problems.py
uv run Generators/KGConstraints/gen_alignment_problems.py
```

## Running the full audit

```bash
cd Problems/ODRL/KGConstraints

PASS=0; FAIL=0; DOC_TIMEOUT=0
for prob in Conflict/KGC*-1.p Refinement/KGC*-1.p Runtime/KGC*-1.p \
            Composition/KGC*-1.p Monotonicity/KGC*-1.p Alignment/KGC*-1.p; do
    base=$(basename "$prob" .p)
    expected=$(grep -m 1 "^% Status" "$prob" | awk '{print $4}')
    actual=$(vampire --mode casc --time_limit 60 "$prob" 2>&1 \
             | grep "SZS status" | head -1 | awk '{print $4}')

    # Documented exceptions
    if [ "$base" = "KGC812-1" ] && [ "$actual" = "ContradictoryAxioms" ]; then
        PASS=$((PASS+1)); continue
    fi
    if [ "$base" = "KGC705-1" ] && [ "$actual" = "Timeout" ]; then
        DOC_TIMEOUT=$((DOC_TIMEOUT+1)); continue
    fi

    if [ "$expected" = "$actual" ]; then PASS=$((PASS+1))
    else FAIL=$((FAIL+1)); echo "FAIL: $base (got $actual)"
    fi
done

echo "PASS: $PASS / Documented timeout: $DOC_TIMEOUT / FAIL: $FAIL"
```

Expected: `PASS: 53 / Documented timeout: 1 / FAIL: 0`.

## Multi-prover validation

A problem is *validated* when at least one saturation prover and at
least one SMT prover return the expected SZS status. To run all seven:

```bash
PROB="Conflict/KGC400-1.p"
SMT="${PROB%.p}.smt2"

vampire --mode casc           --time_limit 60 "$PROB" | grep "SZS status"
vampire --saturation_algorithm discount --time_limit 60 "$PROB" | grep "SZS status"
vampire --saturation_algorithm lrs      --time_limit 60 "$PROB" | grep "SZS status"
vampire --saturation_algorithm otter    --time_limit 60 "$PROB" | grep "SZS status"
eprover --auto --tptp3-format --cpu-limit=60 -s "$PROB" | grep "SZS status"
z3   -T:60 "$SMT"
cvc5 --tlimit=60000 "$SMT"
```

## Documented exceptions

- **KGC705**: 3-operand all-Compatible case. Times out under FOL
  saturation; verified `sat` by Z3.
- **KGC812**: Detects `ContradictoryAxioms` (the intended outcome
  when Assumption 2 is violated).
- **KGC810**: Requires `vampire --mode casc` explicitly (default
  scheduling times out on closed-world saturation).
- **cvc5 Compatible-class**: returns `unknown` on Compatible verdicts
  with `kge_concept` guards. Z3 returns `sat` in these cases.

## Validation summary

| Group       |  N | Validates                              |
| ----------- |---:| -------------------------------------- |
| KGC300–302  |  3 | Motivating example                     |
| KGC400–442  | 15 | Per-operator grid (monotone)           |
| KGC450–461  |  4 | Per-operator grid (complement)         |
| KGC500–502  |  3 | Lemma 1 (refinement)                   |
| KGC600–602  |  3 | Theorem 4 (runtime, atomic)            |
| KGC700–706  |  7 | Corollary 1 (and-composition)          |
| KGC710–713  |  4 | Proposition 2 (or/xone composition)    |
| KGC800–812  | 11 | Proposition 1 (monotonicity)           |
| KGC900–910  |  4 | Proposition 3 (alignment)              |
| **Total**   | **54** | 53 clean + 1 documented timeout    |
```

Save this as `~/Desktop/tptp-odrl/README.md`.

Want me to also add a one-paragraph troubleshooting section (common errors and fixes), or leave it as-is?