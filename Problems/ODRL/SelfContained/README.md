# ODRL Self-Contained SMT2 Benchmarks (Stage 1)

**Self-contained numeric/temporal reasoning - no external KB required.**

## Quick Stats
- **Total:** 165 problems across 6 categories
- **Format:** SMT-LIB2 (QF_LRA logic)
- **Solver:** Z3
- **Expected:** 108 sat, 57 unsat

## Categories

| Category     | Problems | Description                           |
|--------------|----------|---------------------------------------|
| delayPeriod  | 24       | Temporal delay constraints (seconds)  |
| elapsedTime  | 22       | Duration constraints (seconds)        |
| percentage   | 14       | Bounded numeric [0-100]               |
| resolution   | 49       | Image resolution (DPI)                |
| dateTime     | 11       | Date/time constraints (timestamps)    |
| payAmount    | 22       | Payment amounts (currency)            |

## Testing
```bash
# Test conflict (should be unsat)
z3 delayPeriod/test-01-impossible-delay-range-conflict-rule-1.smt2

# Test valid (should be sat)  
z3 delayPeriod/test-12-simple-minimum-wait-rule-1.smt2
```

## Example Problem
```smtlib
; delayPeriod conflict: delay <= 30min AND delay >= 1hour
(declare-fun delayPeriod_default_default () Real)
(assert (>= 3600.0 delayPeriod_default_default))
(assert (<= 1800.0 delayPeriod_default_default))
(assert (>= delayPeriod_default_default 0.0))
(check-sat)
; Expected: unsat
```

## Contrast with Stage 2

| **Stage 1** (here)      | **Stage 2** (KBGrounding, SMT-LIB) |
|-------------------------|-------------------------------------|
| Self-contained          | KB-dependent                        |
| Numeric/temporal        | Spatial, Purpose, Language          |
| Z3 (SMT2)               | Vampire (TPTP), CVC5 (SMT2)         |
| 165 problems            | 146 TPTP + 20 SMT2                  |

See `MANIFEST.txt` for complete listing.

## Source
Generated from: https://github.com/Daham-Mustaf/odrl-z3-reasoner
