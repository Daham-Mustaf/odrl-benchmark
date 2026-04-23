# THF Layer — ODRL Grounding Benchmark

## Overview

Three problems re-encoded in THF0 using the **Shallow Semantic Embedding (SSE)**
technique of Benzmüller & Sutcliffe (JFR 2010). These supplement the main FOF/SMT-LIB
benchmark (GRND001–036) and are referenced in Section 6 (Validation) of the paper.

## Structure

```
THF/
├── Axioms/
│   └── GRND000-0-thf.ax    type declarations (reference; problems inline their subset)
├── Entailment/
│   ├── GRND002-thf-1.p     permission soundness (Ax5.1)
│   └── GRND012-thf-1.p     corr-duty / Right to Omission (Ax5.3)
└── Discriminating/
    └── GRND024-thf-1.p     obl-proh coexist (Ax5.3 + Ax5.5)
```

## SSE Design

| FOF encoding | THF0 SSE encoding |
|---|---|
| `permission(L) & bearer(L,X) & cnt(L,A,T)` | `permission_p @ L @ W & bearer @ L @ X @ W & cnt @ L @ A @ T @ W` |
| `rfr(A)` unary function, guarded by `forbearance(rfr(A))` | `rfr : action_t > action_t` — type enforces sort |
| `decl(A)` guarded by `action(decl(A))` | `decl_fn : action_t > action_t` — type enforces sort |
| Ax5.9 requires explicit guard predicates | `~ (permission_p @ L @ W & duty_p @ D @ W)` — direct clause |

The `world_t` type is the Kripke world type. All position classifiers
(`permission_p`, `duty_p`, `right_p`, etc.) and relational predicates
(`bearer`, `founds`, `cnt`, `part_of`) are world-lifted with an extra
`world_t` argument. Structural predicates (`perm`, `proh`, `aee`, `aer`,
`act`, `tgt`) are not world-lifted — they describe the rule graph, not
what holds at a world.

Deontic operators `d_obl` and `d_perm_op` are defined as HOL functions
over the accessibility relation `d_access : world_t > world_t > $o`.
These are in scope but the main conjectures use direct world-lifted form.

## Running

```bash
# Leo-III (recommended)
leo3 THF/Entailment/GRND002-thf-1.p --timeout 60
leo3 THF/Entailment/GRND012-thf-1.p --timeout 60
leo3 THF/Discriminating/GRND024-thf-1.p --timeout 60

# Satallax
satallax -t 60 THF/Entailment/GRND002-thf-1.p
satallax -t 60 THF/Entailment/GRND012-thf-1.p
satallax -t 60 THF/Discriminating/GRND024-thf-1.p
```

Expected SZS status: `Theorem` for all three.

## Paper Citation

> Three representative problems (GRND002, GRND012, GRND024) were additionally
> encoded in THF0 using the shallow semantic embedding of [BS10]: positions
> become world-lifted predicates of type `position_t > world_t > $o`, `rfr`
> and `decl_fn` are typed functions `action_t > action_t` (eliminating the
> FOF forbearance guard predicates), and deontic operators are defined as HOL
> functions over the accessibility relation. All three conjectures are
> discharged by Leo-III and Satallax, confirming that the entailments of
> Section 5 hold under Henkin semantics with the SSE deontic interpretation.
