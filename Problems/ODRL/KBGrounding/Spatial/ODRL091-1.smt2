; --------------------------------------------------------------------------
; File     : ODRL091-1.smt2
; Domain   : ODRL Policy Conflict Detection
; Problem  : Runtime witness: Compatible verdict → satisfying context exists
; Expected : unsat
; Verdict  : Compatible
; Paper    : Definition 10 — Runtime Witness for Compatible Verdict
;
; ODRL Policy (Turtle):
;   (see problem description)
;
; Formal:
;   assigns(ω, germany)
;   → leq(germany, europe) [GEO KB] → in_den(germany, europe, isPartOf)
;   → satisfies(ω, europe, isPartOf)  [denotation_to_satisfaction]
;   → germany = germany → in_den(germany, germany, eq)
;   → satisfies(ω, germany, eq)  [denotation_to_satisfaction]
;
; Difficulty: Medium
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

; ─── concept/1 predicate (closed-world over declared concepts) ─────
(declare-fun concept (C) Bool)
(assert (concept europe))
(assert (concept westernEurope))
(assert (concept easternEurope))
(assert (concept northernEurope))
(assert (concept southernEurope))
(assert (concept germany))
(assert (concept france))
(assert (concept austria))
(assert (concept belgium))
(assert (concept liechtenstein))
(assert (concept luxembourg))
(assert (concept monaco))
(assert (concept netherlands))
(assert (concept switzerland))
(assert (concept poland))
(assert (concept czechia))
(assert (concept slovakia))
(assert (concept hungary))
(assert (concept sweden))
(assert (concept norway))
(assert (concept finland))
(assert (concept denmark))
(assert (concept italy))
(assert (concept spain))
(assert (concept bavaria))
(assert (concept ileDeFrance))
(assert (forall ((Y C))
    (=> (concept Y) (or (= Y europe) (= Y westernEurope) (= Y easternEurope) (= Y northernEurope) (= Y southernEurope) (= Y germany) (= Y france) (= Y austria) (= Y belgium) (= Y liechtenstein) (= Y luxembourg) (= Y monaco) (= Y netherlands) (= Y switzerland) (= Y poland) (= Y czechia) (= Y slovakia) (= Y hungary) (= Y sweden) (= Y norway) (= Y finland) (= Y denmark) (= Y italy) (= Y spain) (= Y bavaria) (= Y ileDeFrance)))))

; ─── Op sort + operator constants ────────────────────────────────────────
; In FOF, operator names are untyped; SMT2 (sorted UF) requires a sort.
(declare-sort Op 0)
(declare-const isPartOf Op)
(declare-const hasPart  Op)
(declare-const eq       Op)
(declare-const neq      Op)
(declare-const isA      Op)
(declare-const isAnyOf  Op)
(declare-const isAllOf  Op)
(declare-const isNoneOf Op)
(assert (distinct isPartOf hasPart eq neq isA isAnyOf isAllOf isNoneOf))

; ─── in_denotation declaration + bridge axioms (ODRL000-0.ax) ────────────
; in_denotation(X, G, Op): X is in the denotation of constraint (_, Op, G).
; Bridge axioms mirror den_*_if and den_*_onlyif from ODRL000-0.ax.
(declare-fun in_denotation (C C Op) Bool)

; isPartOf: ⟦isPartOf(G)⟧ = ↓G
(assert (forall ((X C)(G C))
    (= (in_denotation X G isPartOf) (leq X G))))
; hasPart: ⟦hasPart(G)⟧ = ↑G
(assert (forall ((X C)(G C))
    (= (in_denotation X G hasPart) (leq G X))))
; eq: ⟦eq(G)⟧ = {G}
(assert (forall ((X C)(G C))
    (= (in_denotation X G eq) (= X G))))
; neq: ⟦neq(G)⟧ = C \ {G}
(assert (forall ((X C)(G C))
    (= (in_denotation X G neq) (not (= X G)))))
; isA: leq-based (same semantics as isPartOf in DPV)
(assert (forall ((X C)(G C))
    (= (in_denotation X G isA) (leq X G))))

; ─── Runtime Semantics (RUNTIME000-0.ax) ─────────────────────────────────
; Separate sort Ctx for execution context constants (distinct from C and Op)
(declare-sort Ctx 0)
(declare-fun assigns    (Ctx C)    Bool)
(declare-fun satisfies  (Ctx C Op) Bool)
(declare-fun ungrounded (C)        Bool)

; Part A: Context Structure (Definition 9)
; context_functional
(assert (forall ((Omega Ctx)(X C)(Y C))
    (=> (and (assigns Omega X)(assigns Omega Y)) (= X Y))))
; assigns_typed
(assert (forall ((Omega Ctx)(X C))
    (=> (assigns Omega X)(concept X))))

; Part B: Grounded Satisfaction Bridge (Definition 10, case 2)
; denotation_to_satisfaction (forward)
(assert (forall ((Omega Ctx)(X C)(G C)(O Op))
    (=> (and (assigns Omega X)(in_denotation X G O))
        (satisfies Omega G O))))
; satisfaction_to_denotation (backward, guarded by concept(G))
(assert (forall ((Omega Ctx)(X C)(G C)(O Op))
    (=> (and (assigns Omega X)(satisfies Omega G O)(concept G))
        (in_denotation X G O))))

; Part C: Ungrounded Satisfaction (Definition 10, ⊤ case)
; permissive_satisfaction
(assert (forall ((Omega Ctx)(X C)(G C)(O Op))
    (=> (and (assigns Omega X)(ungrounded G))
        (satisfies Omega G O))))
; ungrounded_not_concept
(assert (forall ((G C))
    (=> (ungrounded G)(not (concept G)))))

; Part D: Satisfaction requires assignment (dom(ω) requirement)
; Enables Theorem 3: Skolem context → assigns(ω_sk,X) → backward bridge fires
(assert (forall ((Omega Ctx)(G C)(O Op))
    (=> (satisfies Omega G O)
        (exists ((X C))(assigns Omega X)))))

; ─── Conjecture (negated for refutation) ────────────────────────────
(declare-const omega091 Ctx)

; ─── Conjecture (negated for refutation) ────────────────────────────
; Compatible witness: assigns(omega091, germany) → satisfies both
(assert (assigns omega091 germany))
(assert (not (and
    (satisfies omega091 europe isPartOf)
    (satisfies omega091 germany eq))))
(check-sat)
(exit)
; --------------------------------------------------------------------------
