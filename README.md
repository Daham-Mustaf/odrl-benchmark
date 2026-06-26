# ODRL Conflict-Detection Benchmark
[![E 3.3.2](https://img.shields.io/badge/E-3.3.2-1f6feb)](https://github.com/eprover/eprover)
[![Vampire 5.0.1](https://img.shields.io/badge/Vampire-5.0.1-1f6feb)](https://github.com/vprover/vampire)
[![Z3 4.8.12](https://img.shields.io/badge/Z3-4.8.12-1f6feb)](https://github.com/Z3Prover/z3)
[![cvc5 1.3.4](https://img.shields.io/badge/cvc5-1.3.4-1f6feb)](https://github.com/cvc5/cvc5)

A benchmark for detecting conflicts between ODRL policies. Each problem encodes
whether two policies' constraints can be jointly satisfied, in two formats from a
single description: a TPTP `.p` file (for the first-order provers Vampire and E)
and an SMT-LIB `.smt2` file (for the SMT solvers Z3 and cvc5), together with the
ODRL policy pair as Turtle (`.ttl`). The two encodings are independent and are
cross-validated against each other and across the four reasoners.

> **Note:** This README is a work in progress. Full documentation (problem
> counts, family structure, categories, and usage) will be added as the
> benchmark is finalized.

## Requirements

- `vampire`, `eprover`, `z3`, and `cvc5` on your `PATH`
- Python 3

## License

The code is licensed under the Apache License 2.0 (see `LICENSE` and `NOTICE`).
The benchmark problems under `Problems/` are licensed under CC BY 4.0 (see
`Problems/LICENSE`). If you use this benchmark, please cite the accompanying
papers; citation details and `CITATION.cff` will be finalized with the full
documentation.