; --------------------------------------------------------------------------
; File     : ODRL094-1.smt2
; Domain   : ODRL Policy Conflict Detection
; Problem  : Multi-operand AND: runtime witness for 2-operand Compatible verdict
; Expected : unsat
; Verdict  : Compatible
; Paper    : Theorem 2 + 3 — Multi-Operand Runtime Soundness
;
; ODRL Policy (Turtle):
;   (see problem description)
;
; Formal:
;   omega094s ↦ germany:  germany ≤ europe → satisfies(s, europe, isPartOf)
;   germany = germany → satisfies(s, germany, eq)
;   omega094p ↦ academicResearch:
;   academicResearch ≤ R&D → satisfies(p, R&D, isA)
;   academicResearch ≤ academicResearch → satisfies(p, aR, isA)
;
; Notes    : Operand independence (Assumption 2): separate Ctx constants per operand. Spatial and purpose constraints are evaluated independently. Static verdict is AND-Compatible on both dimensions.
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

; ─── DPV Concepts (minimal fragment for composition) ─────────────
(declare-const purpose C)
(declare-const commercialPurpose C)
(declare-const researchAndDevelopment C)
(declare-const serviceProvision C)
(declare-const commercialResearch C)
(declare-const academicResearch C)
(declare-const marketing C)

; UNA
(assert (distinct purpose commercialPurpose researchAndDevelopment serviceProvision commercialResearch academicResearch marketing))

; leq edges
(assert (leq commercialPurpose purpose))
(assert (leq researchAndDevelopment purpose))
(assert (leq serviceProvision purpose))
(assert (leq commercialResearch commercialPurpose))
(assert (leq commercialResearch researchAndDevelopment))
(assert (leq academicResearch researchAndDevelopment))
(assert (leq marketing commercialPurpose))

; Reflexivity
(assert (leq purpose purpose))
(assert (leq commercialPurpose commercialPurpose))
(assert (leq researchAndDevelopment researchAndDevelopment))
(assert (leq serviceProvision serviceProvision))
(assert (leq commercialResearch commercialResearch))
(assert (leq academicResearch academicResearch))
(assert (leq marketing marketing))

; Sibling disjointness (DAG-safe subset)
(assert (disj commercialPurpose serviceProvision))
(assert (disj researchAndDevelopment serviceProvision))
(assert (disj academicResearch marketing))
(assert (disj academicResearch serviceProvision))
(assert (disj marketing serviceProvision))

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

(assert (leq purpose purpose))
(assert (leq commercialPurpose commercialPurpose))
(assert (leq nonCommercialPurpose nonCommercialPurpose))
(assert (leq researchAndDevelopment researchAndDevelopment))
(assert (leq serviceProvision serviceProvision))
(assert (leq personalisation personalisation))
(assert (leq advertising advertising))
(assert (leq communicationManagement communicationManagement))
(assert (leq customerManagement customerManagement))
(assert (leq optimisationForController optimisationForController))
(assert (leq commercialResearch commercialResearch))
(assert (leq nonCommercialResearch nonCommercialResearch))
(assert (leq personalisedAdvertising personalisedAdvertising))
(assert (leq servicePersonalisation servicePersonalisation))
(assert (leq customerCare customerCare))
(assert (leq customerRelationshipManagement customerRelationshipManagement))
(assert (leq communicationForCustomerCare communicationForCustomerCare))
(assert (leq improveInternalCRMProcesses improveInternalCRMProcesses))

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
(assert (concept purpose))
(assert (concept commercialPurpose))
(assert (concept nonCommercialPurpose))
(assert (concept researchAndDevelopment))
(assert (concept serviceProvision))
(assert (concept personalisation))
(assert (concept advertising))
(assert (concept communicationManagement))
(assert (concept customerManagement))
(assert (concept optimisationForController))
(assert (concept commercialResearch))
(assert (concept nonCommercialResearch))
(assert (concept personalisedAdvertising))
(assert (concept servicePersonalisation))
(assert (concept customerCare))
(assert (concept customerRelationshipManagement))
(assert (concept communicationForCustomerCare))
(assert (concept improveInternalCRMProcesses))
(assert (forall ((Y C))
    (=> (concept Y) (or (= Y europe) (= Y westernEurope) (= Y easternEurope) (= Y northernEurope) (= Y southernEurope) (= Y germany) (= Y france) (= Y austria) (= Y belgium) (= Y liechtenstein) (= Y luxembourg) (= Y monaco) (= Y netherlands) (= Y switzerland) (= Y poland) (= Y czechia) (= Y slovakia) (= Y hungary) (= Y sweden) (= Y norway) (= Y finland) (= Y denmark) (= Y italy) (= Y spain) (= Y bavaria) (= Y ileDeFrance) (= Y purpose) (= Y commercialPurpose) (= Y nonCommercialPurpose) (= Y researchAndDevelopment) (= Y serviceProvision) (= Y personalisation) (= Y advertising) (= Y communicationManagement) (= Y customerManagement) (= Y optimisationForController) (= Y commercialResearch) (= Y nonCommercialResearch) (= Y personalisedAdvertising) (= Y servicePersonalisation) (= Y customerCare) (= Y customerRelationshipManagement) (= Y communicationForCustomerCare) (= Y improveInternalCRMProcesses)))))

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
; Per-operand contexts with explicit assignments
(declare-const omega094s Ctx)
(declare-const omega094p Ctx)

; ─── Conjecture (negated for refutation) ────────────────────────────
; Multi-operand: assigns + negate AND conjunction → unsat
(assert (assigns omega094s germany))
(assert (assigns omega094p academicResearch))
(assert (not (and
    (satisfies omega094s europe isPartOf)
    (satisfies omega094s germany eq)
    (satisfies omega094p researchAndDevelopment isA)
    (satisfies omega094p academicResearch isA))))
(check-sat)
(exit)
; --------------------------------------------------------------------------
