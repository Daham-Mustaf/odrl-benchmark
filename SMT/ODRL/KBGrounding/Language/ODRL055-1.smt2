; ODRL055-1.smt2 — Three-KB cross-dataspace: language blocks (fr ⊄ de)
; Expected: sat (SZS: CounterSatisfiable)

(set-logic UF)
(declare-sort Entity 0)

; === Layer 0: GeoNames Spatial KB ===
(declare-fun partOf (Entity Entity) Bool)
(declare-const europe Entity)
(declare-const france Entity)
(declare-const germany Entity)
(declare-const bavaria Entity)

(assert (forall ((x Entity)) (partOf x x)))
(assert (forall ((x Entity) (y Entity) (z Entity))
    (=> (and (partOf x y) (partOf y z)) (partOf x z))))
(assert (partOf france europe))
(assert (partOf germany europe))
(assert (partOf bavaria germany))
(assert (not (partOf germany france)))
(assert (not (partOf france germany)))

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

; === Layer 0: BCP 47 Language Tags (facts only) ===
(declare-const de Entity)
(declare-const de_AT Entity)
(declare-const de_CH Entity)
(declare-const en Entity)
(declare-const en_US Entity)
(declare-const en_GB Entity)
(declare-const fr Entity)
(declare-const ar Entity)
(declare-const arb Entity)
(declare-const arz Entity)

; German variants
(assert (subClassOf de_AT de))
(assert (subClassOf de_CH de))
; English variants
(assert (subClassOf en_US en))
(assert (subClassOf en_GB en))
; Arabic macrolanguage
(assert (subClassOf arb ar))
(assert (subClassOf arz ar))

; Cross-branch disjointness
(assert (not (subClassOf de en)))
(assert (not (subClassOf en de)))
(assert (not (subClassOf de fr)))
(assert (not (subClassOf fr de)))
(assert (not (subClassOf en fr)))
(assert (not (subClassOf fr en)))
(assert (not (subClassOf de ar)))
(assert (not (subClassOf ar de)))
(assert (not (subClassOf en ar)))
(assert (not (subClassOf ar en)))
(assert (not (subClassOf fr ar)))
(assert (not (subClassOf ar fr)))

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

; --- isPartOf: bidirectional ---
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (has_operand c l) (has_operator c op_isPartOf) (has_value c v)
             (mereological l) (partOf x v))
        (in_denotation x c))))
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (in_denotation x c) (has_operand c l)
             (has_operator c op_isPartOf) (has_value c v) (mereological l))
        (partOf x v))))

; --- isA: bidirectional ---
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (has_operand c l) (has_operator c op_isA) (has_value c v)
             (taxonomic l) (subClassOf x v))
        (in_denotation x c))))
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (in_denotation x c) (has_operand c l)
             (has_operator c op_isA) (has_value c v) (taxonomic l))
        (subClassOf x v))))


; === Problem: ODRL055-1 ===
(declare-const c1 Entity)
(declare-const c2 Entity)
(declare-const c3 Entity)
(declare-const c4 Entity)
(declare-const c5 Entity)
(declare-const c6 Entity)
(assert (has_operand c1 spatial))
(assert (has_operator c1 op_isPartOf))
(assert (has_value c1 europe))
(assert (has_operand c3 purpose))
(assert (has_operator c3 op_isA))
(assert (has_value c3 nonCommercialPurpose))
(assert (has_operand c5 language))
(assert (has_operator c5 op_isA))
(assert (has_value c5 de))
(assert (has_operand c2 spatial))
(assert (has_operator c2 op_eq))
(assert (has_value c2 france))
(assert (has_operand c4 purpose))
(assert (has_operator c4 op_eq))
(assert (has_value c4 scientificResearch))
(assert (has_operand c6 language))
(assert (has_operator c6 op_eq))
(assert (has_value c6 fr))

(assert (not (and
    (exists ((x Entity)) (and (in_denotation x c1) (in_denotation x c2)))
    (exists ((y Entity)) (and (in_denotation y c3) (in_denotation y c4)))
    (exists ((z Entity)) (and (in_denotation z c5) (in_denotation z c6))))))

(check-sat)