# Cross-KB Alignment Benchmarks (ODRL057–059)

**Validates:** Section 3.3 — Cross-Dataspace Alignment (Proposition 1)

## Motivation

Sections 3.1–3.2 assume a shared KB per operand. In practice,
dataspaces use different standards for the same domain:

| Operand | Dataspace A | Dataspace B | Mismatch |
|---|---|---|---|
| language | BCP 47 (de, en, fr) | ISO 639-3 (deu, eng, fra) | identifiers |
| spatial | GeoNames (cities+regions) | ISO 3166 (countries only) | granularity |

These benchmarks validate that conflict verdicts transfer correctly
across KBs, and that partial alignment degrades safely to Unknown.

## KB Pair

| KB | File | Concepts | Regional variants |
|---|---|:---:|:---:|
| BCP 47 | `LNG000-0.ax` | 10 | ✓ (de_AT, de_CH, en_US, en_GB) |
| ISO 639-3 | `LNG001-0.ax` | 6 | ✗ (not in standard) |

Alignment α (partial):
```
α(de)=deu  α(en)=eng  α(fr)=fra  α(ar)=ara  α(arb)=arb  α(arz)=arz
α(de_AT)=⊥  α(de_CH)=⊥  α(en_US)=⊥  α(en_GB)=⊥
```

## Problems

### Verdict Preservation (Proposition 1.1 — total for relevant concepts)

| Problem | BCP 47 parallel | BCP 47 verdict | ISO 639-3 verdict | Preserved? |
|---|---|:---:|:---:|:---:|
| ODRL057-1 | ODRL051-1 (de↔fr) | Conflict | Conflict | ✓ |
| ODRL058-1 | ODRL053-1 (ar↔arz) | Compatible | Compatible | ✓ |

### Graceful Degradation (Proposition 1.2 — partial alignment)

| Problem | BCP 47 parallel | BCP 47 verdict | ISO 639-3 verdict | Degraded? |
|---|---|:---:|:---:|:---:|
| ODRL059-1 | ODRL050-1 (de↔de_AT) | Compatible | Unknown | ✓ |
| ODRL059-2 | (conflict direction) | — | Unknown | ✓ no false conflict |

ODRL059-1 + ODRL059-2 together prove genuine Unknown:
- 059-1 (compatible conjecture) → CounterSat: can't prove overlap
- 059-2 (conflict conjecture) → CounterSat: can't prove disjointness
- Both CounterSat → verdict is Unknown, not false Conflict

## Key Demonstration

```
BCP 47:     de_AT ⊑ de     →  Compatible (witness: de_AT)
ISO 639-3:  de_AT unknown   →  Unknown (no facts about de_AT)
```

The framework does NOT guess. It reports what it can prove.
Partial alignment weakens verdicts toward Unknown, never fabricates conflicts.

## Paper Mapping

| Claim | Problem | Result |
|---|---|---|
| Conflicts transfer across KBs | ODRL057-1 | Theorem = Conflict preserved |
| Compatibility transfers | ODRL058-1 | Theorem = Compatible preserved |
| Partial alignment → Unknown | ODRL059-1 | CounterSat = degraded safely |
| No false conflicts | ODRL059-2 | CounterSat = not fabricated |
