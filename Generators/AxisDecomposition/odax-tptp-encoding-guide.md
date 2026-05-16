# Best TPTP / SMT-LIB Encoding for the ODAX Evaluation

A reference for the §10 (Evaluation) translation. One encoding strategy,
applied uniformly across all 13 problem groups, with the BSR(BD) decidability
provenance visible in the syntax.

---

## 1. Strategic choices

### 1.1 Three parallel encodings per problem

| Encoding | Logic                          | Provers           | Purpose                                   |
|----------|--------------------------------|-------------------|-------------------------------------------|
| TFF      | TFF + `$real` arithmetic       | Vampire, E, Z3    | Primary workhorse                         |
| FOF      | Pure FOF + axiomatised order   | All FOF provers   | TPTP library submission; strict BSR(BD)   |
| SMT-LIB  | `LRA` (or `QF_LRA` if ground)  | Z3, cvc5          | SMT solver native input                   |

All three are derivable from one source representation; ship a generator.

### 1.2 Why TFF for the primary

The two E timeouts on ODRL347 and ODRL414 trace back to the dense-order
axiom `! [X,Y]: lt(X,Y) => ? [Z]: lt(X,Z) & lt(Z,Y)`. In pure FOF this
axiom is necessary; saturation provers chain Skolem witnesses on it. In
TFF with `$real`, density is part of the theory and does not appear as
an axiom at all. The TFF encoding therefore eliminates the root cause
of those timeouts.

### 1.3 Why also keep pure FOF

For TPTP problem-library submission, Geoff's convention is FOF or CNF
without theory annotations — the EPR / BSR(BD) classification only applies
to the unannotated form. Carrying both versions keeps the submission
clean and keeps the empirical comparison honest.

### 1.4 Bounds, always

Every universally quantified axis variable `X` appears in every clause
together with explicit lower and upper bounds drawn from its domain
`D_k` (Table 6 of the paper). This is the BSR(BD) condition; once
respected, the entire encoding is in a decidable fragment by Voigt's
Theorem 20.

---

## 2. Signature conventions

```
%---- Per-constraint denotation predicates (one per atomic constraint)
in_w_c1(X)         : axis-X membership in the denotation of c1 (width)
in_h_c1(X)         : axis-X membership in c1 (height)
in_box_C1(X,Y,Z)   : box-denotation of constraint set C1

%---- Verdict constants (finite enum sort)
verdict_conflict, verdict_compatible, verdict_unknown

%---- Order on verdicts
vle/2              : conflict <= unknown <= compatible
```

Keep predicate names problem-local; do not share predicates across
problems. Each `.p` file is self-contained.

---

## 3. Per-group templates

The 13 problem groups of Table 4, each with the recommended TFF
template. SMT-LIB counterpart shown only where it diverges meaningfully.

### 3.1 ODRL300–314 — Single-axis intersection (Definition 2)

**Pattern.** Two denotations on the same axis; conjecture is empty
intersection (Conflict) or non-empty intersection (Compatible).

```tptp
%---- ODRL300_1.p : width (lteq 1920) vs width (eq 2400) ; SZS: Theorem
tff(c1_width, axiom,
    ! [X: $real] :
      ( in_w_c1(X)
    <=> ( $greater(X, 0.0) & $lesseq(X, 1920.0) ) ) ).

tff(c2_width, axiom,
    ! [X: $real] :
      ( in_w_c2(X)
    <=> ( $greater(X, 0.0) & X = 2400.0 ) ) ).

tff(conflict, conjecture,
    ! [X: $real] : ~ ( in_w_c1(X) & in_w_c2(X) ) ).
```

**SMT-LIB.**

```smt2
(set-logic LRA)
(declare-fun in_w_c1 (Real) Bool)
(declare-fun in_w_c2 (Real) Bool)
(assert (forall ((x Real)) (= (in_w_c1 x) (and (> x 0) (<= x 1920)))))
(assert (forall ((x Real)) (= (in_w_c2 x) (and (> x 0) (= x 2400)))))
(assert (not (forall ((x Real)) (not (and (in_w_c1 x) (in_w_c2 x))))))
(check-sat)   ; expect: unsat
```

**Compatible variant.** Replace the conjecture with the existential
`? [X: $real]: (in_w_c1(X) & in_w_c2(X))` and expect `Theorem`
when a witness exists, or invert to `Satisfiable` if you keep the
conjecture as `~?`.

### 3.2 ODRL320–334, 340–353 — Multi-axis box (Definition 3)

**Pattern.** Box denotation as conjunction across axes; conjecture
is box-level disjointness or non-disjointness.

```tptp
%---- ODRL340_1.p : 3-axis box ; SZS: Theorem (box disjoint via width)
tff(c1_w, axiom, ! [X: $real]: ( in_w_c1(X) <=> ($greater(X,0.0) & $lesseq(X,1920.0)) ) ).
tff(c1_h, axiom, ! [Y: $real]: ( in_h_c1(Y) <=> ($greater(Y,0.0) & $lesseq(Y,1080.0)) ) ).
tff(c1_d, axiom, ! [Z: $real]: ( in_d_c1(Z) <=> ($greater(Z,0.0) & $lesseq(Z,50.0))   ) ).

tff(c2_w, axiom, ! [X: $real]: ( in_w_c2(X) <=> ($greater(X,0.0) & X = 2400.0) ) ).
tff(c2_h, axiom, ! [Y: $real]: ( in_h_c2(Y) <=> ($greater(Y,0.0) & Y = 800.0)  ) ).
%  (depth unconstrained on c2 — see §3.11 for the Unknown handling)

tff(box_c1, axiom,
    ! [X: $real, Y: $real, Z: $real]:
      ( in_box_C1(X,Y,Z) <=> ( in_w_c1(X) & in_h_c1(Y) & in_d_c1(Z) ) ) ).

tff(box_c2, axiom,
    ! [X: $real, Y: $real, Z: $real]:
      ( in_box_C2(X,Y,Z) <=> ( in_w_c2(X) & in_h_c2(Y) ) ) ).   % depth: D_d

tff(box_conflict, conjecture,
    ! [X: $real, Y: $real, Z: $real]:
      ~ ( in_box_C1(X,Y,Z) & in_box_C2(X,Y,Z) ) ).
```

### 3.3 ODRL360–371 — Per-axis projection (Theorem 3)

**Pattern.** Membership in the box iff per-axis membership in all
component intervals.

```tptp
tff(projection, conjecture,
    ! [X: $real, Y: $real, Z: $real]:
      ( in_box_C1(X,Y,Z) <=> ( in_w_c1(X) & in_h_c1(Y) & in_d_c1(Z) ) ) ).
```

This is essentially a biconditional check on the box definition;
it always discharges trivially under the axioms of §3.2 — the
point of the problem is verifying that the axioms themselves are
consistent and yield this projection.

### 3.4 ODRL400–416 — Subsumption / containment (Definition 6)

**Pattern.** Universal implication between denotations.

```tptp
%---- ODRL400_1.p : c1 (lteq 1500) ⊆ c2 (lteq 1920) ; SZS: Theorem
tff(c1, axiom, ! [X: $real]: ( in_w_c1(X) <=> ($greater(X,0.0) & $lesseq(X,1500.0)) ) ).
tff(c2, axiom, ! [X: $real]: ( in_w_c2(X) <=> ($greater(X,0.0) & $lesseq(X,1920.0)) ) ).

tff(containment, conjecture,
    ! [X: $real]: ( in_w_c1(X) => in_w_c2(X) ) ).
```

### 3.5 ODRL420–435 — Boundary cases (Definition 5, endpoint precedence)

**Pattern.** Strict vs non-strict, open vs closed; touching intervals
that share an endpoint where one is open.

```tptp
%---- ODRL420_3.p : (lt 1200) vs (gteq 1200) ; SZS: Theorem (disjoint, u ≺ l)
tff(c1, axiom, ! [X: $real]: ( in_w_c1(X) <=> ($greater(X,0.0) & $less(X,1200.0))   ) ).
tff(c2, axiom, ! [X: $real]: ( in_w_c2(X) <=> $greatereq(X,1200.0) ) ).

tff(touch_disjoint, conjecture,
    ! [X: $real]: ~ ( in_w_c1(X) & in_w_c2(X) ) ).
```

The four sub-cases of `≺` (closed/closed, open/closed, closed/open,
open/open) each get their own problem in this group.

### 3.6 ODRL440–451 — `or` composition (Definition 8)

**Pattern.** Compatible iff at least one branch pair overlaps.

```tptp
%---- ODRL440_1.p : two-branch or, second branch compatible ; SZS: Theorem
tff(branch1_offer, axiom, ! [X: $real]: ( in_b1(X) <=> $lesseq(X,1920.0) & $greater(X,0.0) ) ).
tff(branch1_req,   axiom, ! [X: $real]: ( in_b1r(X) <=> X = 2400.0 ) ).         % conflict
tff(branch2_offer, axiom, ! [X: $real]: ( in_b2(X) <=> $lesseq(X,1920.0) & $greater(X,0.0) ) ).
tff(branch2_req,   axiom, ! [X: $real]: ( in_b2r(X) <=> X = 1200.0 ) ).         % compatible

tff(or_compatible, conjecture,
    ( ? [X: $real]: ( in_b1(X) & in_b1r(X) ) )
  | ( ? [X: $real]: ( in_b2(X) & in_b2r(X) ) ) ).
```

The Strong Kleene `min` aggregation across branch pairs is handled
*outside* the FOL conjecture, by a small Python harness over the SZS
statuses returned per branch pair. Trying to encode the verdict
algebra inside the conjecture inflates the problem and obscures the
fragment classification.

### 3.7 ODRL460–470 — `xone` composition (Definition 9)

**Pattern.** Exactly one branch pair overlaps; the rest disjoint.

```tptp
%---- ODRL460_1.p : 2-branch xone, b1 compatible & b2 conflict ; SZS: Theorem
tff(xone_compatible, conjecture,
    (   ( ? [X: $real]: in_b1(X) & in_b1r(X) )
      & ~ ( ? [X: $real]: in_b2(X) & in_b2r(X) ) )
  | (   ~ ( ? [X: $real]: in_b1(X) & in_b1r(X) )
      & ( ? [X: $real]: in_b2(X) & in_b2r(X) ) ) ).
```

For *n* branch pairs the conjecture is a disjunction of *n* mutually
exclusive cases. Keep *n* small per problem (≤ 3); above that, harness
the aggregation in Python.

### 3.8 ODRL500–513 — Totality, normalisation, projection (Lem. 1, Lem. 2, Thm. 3)

**Pattern.** Universal closure of the structural lemmas; one conjecture
per lemma instance with concrete denotations.

```tptp
%---- ODRL500_1.p : normalisation = intersection of three constraints
tff(c1, axiom, ! [X: $real]: ( in_a(X) <=> $lesseq(X,1920.0) & $greater(X,0.0) ) ).
tff(c2, axiom, ! [X: $real]: ( in_b(X) <=> $greatereq(X,100.0) ) ).
tff(c3, axiom, ! [X: $real]: ( in_c(X) <=> $lesseq(X,1500.0) ) ).
tff(norm, axiom, ! [X: $real]: ( in_norm(X) <=> in_a(X) & in_b(X) & in_c(X) ) ).
tff(witness, conjecture,
    ! [X: $real]: ( in_norm(X) <=> ($greatereq(X,100.0) & $lesseq(X,1500.0)) ) ).
```

### 3.9 ODRL600–609 — Conflict criterion (Theorem 2)

**Pattern.** The biconditional `disjoint(c1,c2) <=> u1 ≺ l2 ∨ u2 ≺ l1`,
instantiated for each combination of operator pairs.

Encoding the criterion *symbolically* over arbitrary intervals is
painful in TFF (you would need to expose endpoints and openness flags).
The cleaner approach: one ground problem per operator pair, asserting
the biconditional with the concrete `(l, u, open?)` substituted in.
This keeps every problem inside BSR(BD).

### 3.10 ODRL630–637 — Completion sharpness (Theorem 5)

**Pattern.** Existence of two completions, one Compatible and one
Conflict, witnessing that Unknown is open.

```tptp
%---- ODRL630_1.p : compatible completion exists ; SZS: Satisfiable
tff(c1_w, axiom, ! [X: $real]: ( in_w_c1(X) <=> X = 1500.0 ) ).
tff(c2_w, axiom, ! [X: $real]: ( in_w_c2(X) <=> X = 1500.0 ) ).
tff(c1_d_complete, axiom, ! [Z: $real]: ( in_d_c1(Z) <=> ($greater(Z,0.0) & $lesseq(Z,50.0)) ) ).
tff(c2_d_complete, axiom, ! [Z: $real]: ( in_d_c2(Z) <=> Z = 25.0 ) ).

tff(witness, conjecture,
    ? [X: $real, Z: $real]: ( in_w_c1(X) & in_w_c2(X) & in_d_c1(Z) & in_d_c2(Z) ) ).
```

Run with Vampire FMB and cvc5 finite-model finding; both should return
`Satisfiable` with a model exhibiting the witness.

### 3.11 ODRL640–649 — Composition soundness (Theorem 6)

**Pattern.** Conflict at any axis lifts to box conflict; analogous for
`or` and `xone`.

```tptp
%---- ODRL640_1.p : conjunction soundness ; SZS: Theorem
tff(c1_w, axiom, ! [X: $real]: ( in_w_c1(X) <=> $lesseq(X,1920.0) & $greater(X,0.0) ) ).
tff(c2_w, axiom, ! [X: $real]: ( in_w_c2(X) <=> X = 2400.0 ) ).
tff(c1_h, axiom, ! [Y: $real]: ( in_h_c1(Y) <=> $lesseq(Y,1080.0) & $greater(Y,0.0) ) ).
tff(c2_h, axiom, ! [Y: $real]: ( in_h_c2(Y) <=> Y = 800.0 ) ).

tff(box_disjoint_from_axis_disjoint, conjecture,
    ! [X: $real, Y: $real]:
      ~ ( (in_w_c1(X) & in_w_c2(X)) & (in_h_c1(Y) & in_h_c2(Y)) ) ).
```

Note: the conjecture is true because the width axis already gives
disjointness; the box-level claim follows. The prover should close
quickly on the width conjunct alone.

### 3.12 ODRL650–657 — Multi-axis box containment

**Pattern.** Chained or nested containments. ODRL657, called out in
the paper, is the recursive-chain variant where the conjecture is that
the chain reduces to `Unknown` rather than `Compatible`. Encode it as
a finite chain (depth ≤ 6) of `=>` implications; do not introduce a
recursive definition (saturation provers handle the finite unrolling,
SMT solvers prefer it ground).

### 3.13 ODRL700–739 — Counter-satisfiable (negative tier)

**Pattern.** Conjecture asserts a *wrong* verdict; expected SZS status
is `CounterSatisfiable` (or `Satisfiable` for the negated form).
The refutation witnesses that the actual semantics rejects the claim.

```tptp
%---- ODRL700_1.p : claim that disjoint intervals overlap ; SZS: CounterSatisfiable
tff(c1, axiom, ! [X: $real]: ( in_w_c1(X) <=> $lesseq(X,1920.0) & $greater(X,0.0) ) ).
tff(c2, axiom, ! [X: $real]: ( in_w_c2(X) <=> X = 2400.0 ) ).

tff(wrong_claim, conjecture,
    ? [X: $real] : ( in_w_c1(X) & in_w_c2(X) ) ).        % no such X exists
```

Vampire's finite-model builder (`--mode portfolio --fmb_start_size 1`)
and cvc5's `--finite-model-find` are the natural tools here.

### 3.14 ODRL750–769 — Satisfiability tier (Theorem 8, Runtime Soundness)

**Pattern.** Existence of a request satisfying a constraint set.

```tptp
%---- ODRL750_1.p : compatible request exists ; SZS: Satisfiable
tff(c1, axiom, ! [X: $real]: ( in_w_c1(X) <=> $lesseq(X,1920.0) & $greater(X,0.0) ) ).
tff(c1_witness, conjecture,
    ? [X: $real] : in_w_c1(X) ).
```

---

## 4. SZS status mapping

| Verdict (paper)                | Encoding shape           | Expected SZS                   |
|--------------------------------|---------------------------|--------------------------------|
| Conflict (disjoint)            | `! [X]: ~(A(X) & B(X))`   | `Theorem` (FOF/TFF) / `unsat` (SMT) |
| Compatible (overlap exists)    | `? [X]: A(X) & B(X)`      | `Theorem` or `Satisfiable`     |
| Unknown                        | Two-completion problem    | Both completions verified separately |
| Counter-satisfiable            | Wrong claim as conjecture | `CounterSatisfiable` or `Satisfiable` |
| Containment `A ⊆ B`            | `! [X]: A(X) => B(X)`     | `Theorem` / `unsat`            |

The `Unknown` case is a single conceptual problem split into two
TPTP files (the two completions of Definition 7); the verdict at the
paper level aggregates from the SZS statuses of both.

---

## 5. Fragment provenance

Under the TFF encoding with `$real`, every problem is in TFA
(TFF + arithmetic), which is the SMT-LIB-aligned theory fragment.

Under the pure FOF encoding with axiomatised order, every problem is
in BSR(BD) provided:

- no function symbols appear (only constants and predicates) — ✓ by construction;
- every universally quantified real variable carries explicit lower
  and upper bounds in the same clause — ✓ by the "bounds, always"
  convention of §1.4;
- only constraints of shape `x ⊳ c`, `x ⊳ y`, `x − y ⊳ c` appear in
  the universal scope — ✓ since the operators of Definition 1 only
  produce these forms.

Decidability of every problem follows from Voigt's Theorem 20 (FroCoS
2017) under the FOF encoding; under TFF/SMT-LIB it follows from the
decidability of LRA + UF with the quantifier structure restricted to
∀* over bounded reals.

---

## 6. Practical notes

- **One conjecture per problem.** Do not bundle. SZS status is per-file.
- **No theory imports.** Each TPTP file is self-contained.
- **Stable predicate naming.** `in_<axis>_<constraint_id>` is enough.
- **Generate, don't hand-write.** A single Python script should produce
  all three encodings (TFF, FOF, SMT-LIB) from a common policy
  representation. The 247 files become 247 × 3 = 741 artefacts.
- **TPTP header.** Use the standard `% Domain : ODRL Policy Reasoning`,
  `% Status : Theorem` etc.; this is required for TPTP-library submission.
- **Per-prover invocations.** Pin versions and switches in a `runner.sh`:
  - Vampire: `vampire --mode portfolio --time_limit 60`
  - Vampire FMB: `vampire --mode fmb --time_limit 60`
  - E: `eprover --auto-schedule --cpu-limit=60`
  - Z3: `z3 -smt2 -T:60`
  - cvc5: `cvc5 --tlimit-per=60000 --finite-model-find`

This guide is meant to be precise enough that a single afternoon of
work converts the existing 247 problems to the unified template above
without losing any of the empirical results already reported.