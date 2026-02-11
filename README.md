# TPTP-ODRL Benchmark Suite

ODRL policy conflict detection — multi-prover benchmarks.  
Mustafa & Sutcliffe · 

## Architecture

```
L0  Domain KB         GEO000-0.ax          partOf, subClassOf facts
L1  ODRL Core         ODRL000-0.ax         constraint structure, operators
L2  Grounding Bridge  GROUND000-1.ax       denotation semantics (bidirectional)
L3  Problems          ODRL0xx-1.p          conjectures derived from L0–L2
```

Freeze order: L0 → L1 → L2 → L3. Never modify a lower layer.

## Results — Spatial Domain (GeoNames)

| Problem | Conjecture | SZS | ODRL Verdict | Tests |
|---------|-----------|-----|-------------|-------|
| ODRL010-1 | `partOf(bavaria, europe)` | **Theorem** | — | L0 transitivity |
| ODRL011-1 | `~partOf(germany, france)` | **Theorem** | — | L0 negative fact |
| ODRL012-1 | `∃X. denot(X,c1) ∧ denot(X,c2)` | **Theorem** | Compatible | france ⪯ europe (Table 1) |
| ODRL013-1 | `~∃X. denot(X,c1) ∧ denot(X,c2)` | **Theorem** | Conflict | germany ⊄ france |
| ODRL014-1 | `∃X. denot(X,c1) ∧ denot(X,c2)` | **Theorem** | Compatible | bavaria → germany → europe |
| ODRL015-1 | `~∃X. denot(X,c1) ∧ denot(X,c2)` | **CounterSat** | Unknown | missing ~partOf(bavaria,france) |

## SZS → ODRL Mapping

| SZS Status | ODRL Verdict | Meaning |
|------------|-------------|---------|
| Theorem | Conflict or Compatible | conjecture proven |
| CounterSatisfiable | Unknown | KB incomplete |
| Timeout / GaveUp | Unknown | prover limit |

## Key Design Decisions

- **Bidirectional denotation** — "if" + "only if" rules. Without "only if", conflict proofs fail in open-domain FOL.
- **No domain closure** — open-world. Missing negative facts → Unknown, not false Conflict.
- **No verdict_conflict axiom** — conflict proven via negated compatibility (prover-friendly).
- **Hierarchical operators** — isPartOf uses transitive partOf. Extends ODRL spec.

## Running

```bash
cd Problems/ODRL
vampire KBGrounding/Spatial/ODRL0xx-1.p
```

## Status

- [x] Spatial domain (GeoNames) — Compatible, Conflict, Unknown
- [ ] Purpose domain (DPV) — taxonomic isA
- [ ] Language domain (ISO 639)
- [ ] Cross-dataspace alignment
- [ ] SMT-LIB parallel encoding