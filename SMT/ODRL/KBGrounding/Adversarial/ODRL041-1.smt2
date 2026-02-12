; ODRL041-1.smt2 — ATTACK: Cross-operator overlap (isA vs isAnyOf)
; Expected: unsat (SZS: Theorem)

(set-logic UF)
(declare-sort Entity 0)

; === Layer 0: DPV Purpose Taxonomy (DAG) ===
(declare-fun subClassOf (Entity Entity) Bool)
(declare-const purpose_top Entity)
(declare-const commercialPurpose Entity)
(declare-const nonCommercialPurpose Entity)
(declare-const researchAndDevelopment Entity)
(declare-const marketing Entity)
(declare-const academicResearch Entity)
(declare-const scientificResearch Entity)
(declare-const commercialResearch Entity)
(declare-const nonCommercialResearch Entity)
(declare-const advertising Entity)
(declare-const directMarketing Entity)

(assert (forall ((x Entity)) (subClassOf x x)))
(assert (forall ((x Entity) (y Entity) (z Entity))
    (=> (and (subClassOf x y) (subClassOf y z)) (subClassOf x z))))

; Top-level
(assert (subClassOf commercialPurpose purpose_top))
(assert (subClassOf nonCommercialPurpose purpose_top))
(assert (subClassOf researchAndDevelopment purpose_top))
(assert (subClassOf marketing purpose_top))

; R&D children
(assert (subClassOf academicResearch researchAndDevelopment))
(assert (subClassOf scientificResearch researchAndDevelopment))
(assert (subClassOf commercialResearch researchAndDevelopment))
(assert (subClassOf nonCommercialResearch researchAndDevelopment))

; Multi-parent (DAG)
(assert (subClassOf commercialResearch commercialPurpose))
(assert (subClassOf nonCommercialResearch nonCommercialPurpose))

; Marketing children
(assert (subClassOf advertising marketing))
(assert (subClassOf directMarketing marketing))

; Disjointness
(assert (not (subClassOf commercialPurpose nonCommercialPurpose)))
(assert (not (subClassOf nonCommercialPurpose commercialPurpose)))
(assert (not (subClassOf marketing nonCommercialPurpose)))
(assert (not (subClassOf advertising nonCommercialPurpose)))
(assert (not (subClassOf nonCommercialResearch commercialPurpose)))

; === Layer 1: ODRL Core ===
(declare-fun has_operand (Entity Entity) Bool)
(declare-fun has_operator (Entity Entity) Bool)
(declare-fun has_value (Entity Entity) Bool)
(declare-fun in_denotation (Entity Entity) Bool)

(declare-const op_eq Entity)
(declare-const op_isPartOf Entity)
(declare-const op_isA Entity)
(declare-const op_isAnyOf Entity)
(declare-const op_isAllOf Entity)
(declare-const op_isNoneOf Entity)

(declare-fun mereological (Entity) Bool)
(declare-fun taxonomic (Entity) Bool)
(declare-const spatial Entity)
(declare-const purpose Entity)
(declare-const language Entity)
(assert (mereological spatial))
(assert (taxonomic purpose))
(assert (taxonomic language))

; --- eq: bidirectional ---
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (has_operand c l) (has_operator c op_eq) (has_value c v) (= x v))
        (in_denotation x c))))
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (in_denotation x c) (has_operand c l) (has_operator c op_eq) (has_value c v))
        (= x v))))

; --- isA: bidirectional ---
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (has_operand c l) (has_operator c op_isA) (has_value c v)
             (taxonomic l) (subClassOf x v))
        (in_denotation x c))))
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (in_denotation x c) (has_operand c l)
             (has_operator c op_isA) (has_value c v) (taxonomic l))
        (subClassOf x v))))

; --- isAnyOf: if-direction only (taxonomic) ---
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (has_operand c l) (has_operator c op_isAnyOf) (has_value c v)
             (taxonomic l) (subClassOf x v))
        (in_denotation x c))))


; === Problem: ODRL041-1 ===
(declare-const c1 Entity)
(declare-const c2 Entity)
(assert (has_operand c1 purpose))
(assert (has_operator c1 op_isA))
(assert (has_value c1 researchAndDevelopment))
(assert (has_operand c2 purpose))
(assert (has_operator c2 op_isAnyOf))
(assert (has_value c2 commercialPurpose))
(assert (has_value c2 marketing))

(assert (not (exists ((x Entity))
    (and (in_denotation x c1) (in_denotation x c2)))))

(check-sat)