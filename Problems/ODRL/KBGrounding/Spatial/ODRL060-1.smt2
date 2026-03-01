; --------------------------------------------------------------------------
; File     : ODRL060-1.smt2
; Domain   : ODRL Policy Conflict Detection
; Problem  : Tautology: isPartOf(europe) = C (root covers all concepts)
; Expected : unsat
; Verdict  : Tautological
; Paper    : Tautology Detection
;
; ODRL Policy (Turtle):
;   c: [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:europe ] .
;
; Formal:
;   ⟦isPartOf(europe)⟧ = {X ∈ C | leq(X, europe)} = C
;   europe is the root of GEO KB (26 concepts, no world above)
;   Ground encoding: prove leq(c, europe) for each of the 26 named concepts
;   Chain: country → sub-region → europe by transitivity
;
; Notes    : Ground conjunction over all 26 GEO concepts. No concept/1 predicate: open-world quantification is unsound for tautology.
; Difficulty: Easy
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

; ─── Conjecture (negated for refutation) ────────────────────────────
; Tautology: negate ground conjunction → unsat (all 26 concepts ≤ europe)
(assert (not
    (and
    (leq europe europe)
    (leq westernEurope europe)
    (leq easternEurope europe)
    (leq northernEurope europe)
    (leq southernEurope europe)
    (leq germany europe)
    (leq france europe)
    (leq austria europe)
    (leq belgium europe)
    (leq liechtenstein europe)
    (leq luxembourg europe)
    (leq monaco europe)
    (leq netherlands europe)
    (leq switzerland europe)
    (leq poland europe)
    (leq czechia europe)
    (leq slovakia europe)
    (leq hungary europe)
    (leq sweden europe)
    (leq norway europe)
    (leq finland europe)
    (leq denmark europe)
    (leq italy europe)
    (leq spain europe)
    (leq bavaria europe)
    (leq ileDeFrance europe))))
(check-sat)
(exit)
; --------------------------------------------------------------------------
