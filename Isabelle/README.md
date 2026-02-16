# ODRL Semantic Grounding — Isabelle/HOL Verification

Machine-verified meta-theorems for the ODRL constraint conflict detection framework.

## Build

```bash
~/Downloads/Isabelle2025-2.app/bin/isabelle build -d ~/Desktop/tptp-odrl/Isabelle ODRL_Grounding

~/Downloads/Isabelle2025-2.app/bin/isabelle jedit \
  -d ~/Desktop/tptp-odrl/Isabelle \
  ~/Desktop/tptp-odrl/Isabelle/ODRL_Grounding.thy
  
```

## Verified Results (17 theorems, 0 sorry)

### knowledge_base locale
| # | Isabelle name | Paper reference |
|---|---|---|
| 1 | `disj_order_consistency` | Lemma (Disjointness–Order Consistency) |
| 2 | `soundness` | Theorem 1 (Soundness) |
| 3 | `soundness_witness` | Theorem 1 (witness form) |
| 4 | `runtime_soundness` | Theorem 3 (Runtime Soundness) |
| 5 | `conflict_propagation` | Lemma (Conflict Propagation) |
| 6 | `top_never_conflict` | Foundation lemma |
| 7 | `conflict_requires_classical` | Foundation lemma |
| 8 | `composition_soundness_and` | Theorem 2 — and |
| 9 | `composition_soundness_or` | Theorem 2 — or |
| 10 | `composition_soundness_xone` | Theorem 2 — xone |
| 11 | `xone_compatible_requires_exclusivity` | xone provable non-overlap |

### kb_extension locale
| # | Isabelle name | Paper reference |
|---|---|---|
| 12 | `ground_preserved` | Grounded denotation stable under KB extension |
| 13 | `kb_monotonicity_verdict` | Proposition 3: verdict preserved |
| 14 | `kb_monotonicity_resolves_unknown` | Proposition 3: Unknown resolves |

### alignment locale
| # | Isabelle name | Paper reference |
|---|---|---|
| 15 | `denotation_preservation_isA` | Lemma 2 (Denotation Preservation) |
| 16 | `verdict_preservation_conflict` | Proposition 2 (Verdict Preservation) |
| 17 | `subsumption_preservation` | Corollary 1 (Subsumption Preservation) |



