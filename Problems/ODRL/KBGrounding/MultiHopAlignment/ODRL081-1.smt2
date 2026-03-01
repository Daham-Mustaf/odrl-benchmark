; --------------------------------------------------------------------------
; File     : ODRL081-1.smt2
; Domain   : ODRL Policy Conflict Detection
; Problem  : Aligned conflict: disjoint(dE, pL) via alignment transfer
; Expected : unsat
; Verdict  : Conflict
; Paper    : Def. 8(ii), Proposition 2(1) — Disjointness Transfer
;
; ODRL Policy (Turtle):
;   (see problem description)
;
; Formal:
;   disj_downward(wE⊥eE, de≤wE, pl≤eE) → disj(germany, poland)
;   align_disj_forward(germany→dE, poland→pL, disj(de,pl))
;   → disj(dE, pL) in ISO 3166
;   → ⟦isPartOf(dE)⟧ ∩ ⟦isPartOf(pL)⟧ = ∅ → Conflict
;
; Notes    : Compare ODRL088 (ISO alone) and ODRL089 (data without theory).
; Difficulty: Very Hard
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
(assert (leq europe europe))
(assert (leq westernEurope westernEurope))
(assert (leq easternEurope easternEurope))
(assert (leq northernEurope northernEurope))
(assert (leq southernEurope southernEurope))
(assert (leq germany germany))
(assert (leq france france))
(assert (leq austria austria))
(assert (leq belgium belgium))
(assert (leq liechtenstein liechtenstein))
(assert (leq luxembourg luxembourg))
(assert (leq monaco monaco))
(assert (leq netherlands netherlands))
(assert (leq switzerland switzerland))
(assert (leq poland poland))
(assert (leq czechia czechia))
(assert (leq slovakia slovakia))
(assert (leq hungary hungary))
(assert (leq sweden sweden))
(assert (leq norway norway))
(assert (leq finland finland))
(assert (leq denmark denmark))
(assert (leq italy italy))
(assert (leq spain spain))
(assert (leq bavaria bavaria))
(assert (leq ileDeFrance ileDeFrance))

; ─── GEO Concepts ────────────────────────────────────────────────
(declare-const europe C)
(declare-const westernEurope C)
(declare-const easternEurope C)
(declare-const northernEurope C)
(declare-const southernEurope C)
(declare-const germany C)
(declare-const france C)
(declare-const austria C)
(declare-const belgium C)
(declare-const liechtenstein C)
(declare-const luxembourg C)
(declare-const monaco C)
(declare-const netherlands C)
(declare-const switzerland C)
(declare-const poland C)
(declare-const czechia C)
(declare-const slovakia C)
(declare-const hungary C)
(declare-const sweden C)
(declare-const norway C)
(declare-const finland C)
(declare-const denmark C)
(declare-const italy C)
(declare-const spain C)
(declare-const bavaria C)
(declare-const ileDeFrance C)

; UNA (Unique Name Assumption)
(assert (distinct europe westernEurope easternEurope northernEurope southernEurope germany france austria belgium liechtenstein luxembourg monaco netherlands switzerland poland czechia slovakia hungary sweden norway finland denmark italy spain bavaria ileDeFrance))

; ─── leq edges ───────────────────────────────────────────────────
(assert (leq westernEurope europe))
(assert (leq easternEurope europe))
(assert (leq northernEurope europe))
(assert (leq southernEurope europe))
(assert (leq germany westernEurope))
(assert (leq france westernEurope))
(assert (leq austria westernEurope))
(assert (leq belgium westernEurope))
(assert (leq liechtenstein westernEurope))
(assert (leq luxembourg westernEurope))
(assert (leq monaco westernEurope))
(assert (leq netherlands westernEurope))
(assert (leq switzerland westernEurope))
(assert (leq poland easternEurope))
(assert (leq czechia easternEurope))
(assert (leq slovakia easternEurope))
(assert (leq hungary easternEurope))
(assert (leq sweden northernEurope))
(assert (leq norway northernEurope))
(assert (leq finland northernEurope))
(assert (leq denmark northernEurope))
(assert (leq italy southernEurope))
(assert (leq spain southernEurope))
(assert (leq bavaria germany))
(assert (leq ileDeFrance france))

; ─── Sibling disjointness ────────────────────────────────────────
(assert (disj westernEurope easternEurope))
(assert (disj westernEurope northernEurope))
(assert (disj westernEurope southernEurope))
(assert (disj easternEurope northernEurope))
(assert (disj easternEurope southernEurope))
(assert (disj northernEurope southernEurope))
(assert (disj germany france))
(assert (disj italy spain))
(assert (disj sweden norway))
(assert (disj poland czechia))

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

; ─── Alignment ground facts (GEO → ISO, ALIGN-GEO-ISO.ax) ───────
(declare-fun align (C C) Bool)
(assert (align germany dE))
(assert (align france fR))
(assert (align poland pL))
(assert (align italy iT))
(assert (align spain eS))
(assert (align austria aT))
(assert (align belgium bE))
(assert (align netherlands nL))
(assert (align sweden sE))
(assert (align europe europe))

; ─── Alignment theory axioms (ALIGN000-0.ax Part A) ─────────────────────
; align_order_forward: align(X,Xp) ∧ align(Y,Yp) ∧ leq(X,Y) → leq(Xp,Yp)
(assert (forall ((X C)(Y C)(Xp C)(Yp C))
    (=> (and (align X Xp)(align Y Yp)(leq X Y))
        (leq Xp Yp))))
; align_order_backward: align(X,Xp) ∧ align(Y,Yp) ∧ leq(Xp,Yp) → leq(X,Y)
(assert (forall ((X C)(Y C)(Xp C)(Yp C))
    (=> (and (align X Xp)(align Y Yp)(leq Xp Yp))
        (leq X Y))))
; align_disj_forward: align(X,Xp) ∧ align(Y,Yp) ∧ disj(X,Y) → disj(Xp,Yp)
(assert (forall ((X C)(Y C)(Xp C)(Yp C))
    (=> (and (align X Xp)(align Y Yp)(disj X Y))
        (disj Xp Yp))))
; align_injective: align(X,Z) ∧ align(Y,Z) → X=Y
(assert (forall ((X C)(Y C)(Z C))
    (=> (and (align X Z)(align Y Z)) (= X Y))))
; align_functional: align(X,Y) ∧ align(X,Z) → Y=Z
(assert (forall ((X C)(Y C)(Z C))
    (=> (and (align X Y)(align X Z)) (= Y Z))))

; ─── Conjecture (negated for refutation) ────────────────────────────
; Aligned conflict: ∃X.leq(X,dE)∧leq(X,pL) → unsat
; Proof chain: disj(germany,poland) + align_disj_forward → disj(dE,pL)
(assert (exists ((X C))
    (and (leq X dE)(leq X pL))))
(check-sat)
(exit)
; --------------------------------------------------------------------------
