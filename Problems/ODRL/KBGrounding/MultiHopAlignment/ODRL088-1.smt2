; --------------------------------------------------------------------------
; File     : ODRL088-1.smt2
; Domain   : ODRL Policy Conflict Detection
; Problem  : Downward asymmetry: flat ISO alone cannot detect dE ⊥ pL
; Expected : sat
; Verdict  : Unknown
; Paper    : Proposition 2(2) — Downward Asymmetry: Flat KB Alone
;
; ODRL Policy (Turtle):
;   (see problem description)
;
; Formal:
;   ISO 3166 has $distinct(dE, pL) for UNA — dE ≠ pL
;   BUT $distinct ≠ disjoint/2 (no leq/2 structure forbidding overlap)
;   disjoint(dE, pL) is NOT derivable from ISO alone
;   Compare ODRL081: adds GEO+alignment → Conflict in 0.1s
;
; Notes    : Demonstrates: structural disjointness from richer KB is necessary.
; Difficulty: Hard
; Authors  : Mustafa, D. & Sutcliffe, G.
; Date     : 2026-02-28
; Gen      : gen_hierarchy_suite.py
; --------------------------------------------------------------------------

(set-logic UF)

; ─── ODRL Core axioms (ODRL000-0.ax) ─────────────────────────────────────
; Sort and predicate declarations
(declare-sort C 0)
(declare-fun leq  (C C) Bool)
(declare-fun disj (C C) Bool)

; leq: reflexive (asserted per-concept), transitive
(assert (forall ((x C)(y C)(z C))
    (=> (and (leq x y)(leq y z)) (leq x z))))

; disj: symmetric
(assert (forall ((x C)(y C))
    (=> (disj x y)(disj y x))))

; disj: irreflexive
(assert (forall ((x C))
    (not (disj x x))))

; disj: downward-closed
(assert (forall ((x C)(y C)(xp C)(yp C))
    (=> (and (disj x y)(leq xp x)(leq yp y))
        (disj xp yp))))

; disj/leq consistency: leq(x,y) → ¬disj(x,y)
(assert (forall ((x C)(y C))
    (=> (leq x y)(not (disj x y)))))

; leq: reflexivity (asserted per declared concept below)
; ─── ISO 3166 concepts (EU27 subset, flat code list) ─────────────
(declare-const dE C)
(declare-const fR C)
(declare-const pL C)
(declare-const iT C)
(declare-const eS C)
(declare-const aT C)
(declare-const bE C)
(declare-const nL C)
(declare-const sE C)

; UNA (code-level distinctness — NOT structural disjointness)
(assert (distinct dE fR pL iT eS aT bE nL sE))

; leq edges (flat: each code ≤ europe)
(assert (leq dE europe))
(assert (leq fR europe))
(assert (leq pL europe))
(assert (leq iT europe))
(assert (leq eS europe))
(assert (leq aT europe))
(assert (leq bE europe))
(assert (leq nL europe))
(assert (leq sE europe))

; Reflexivity
(assert (leq europe europe))
(assert (leq dE dE))
(assert (leq fR fR))
(assert (leq pL pL))
(assert (leq iT iT))
(assert (leq eS eS))
(assert (leq aT aT))
(assert (leq bE bE))
(assert (leq nL nL))
(assert (leq sE sE))

; NOTE: NO disjoint/2 axioms — flat code list has no structure

; ─── Conjecture (negated for refutation) ────────────────────────────
; Unknown: ∃X.leq(X,dE)∧leq(X,pL)
; ISO has no disj axioms → Z3 builds a sat model
(assert (exists ((X C))
    (and (leq X dE)(leq X pL))))
(check-sat)
(exit)
; --------------------------------------------------------------------------
