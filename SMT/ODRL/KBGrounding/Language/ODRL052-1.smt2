; ODRL052-1.smt2 — Language isAnyOf conflict: fr ∉ {de, en}↓
; Expected: unsat (SZS: Theorem)

(set-logic UF)
(declare-sort Entity 0)

; === Layer 0: BCP 47 Language Tags ===
(declare-fun subClassOf (Entity Entity) Bool)
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

(assert (forall ((x Entity)) (subClassOf x x)))
(assert (forall ((x Entity) (y Entity) (z Entity))
    (=> (and (subClassOf x y) (subClassOf y z)) (subClassOf x z))))

(assert (subClassOf de_AT de))
(assert (subClassOf de_CH de))
(assert (subClassOf en_US en))
(assert (subClassOf en_GB en))
(assert (subClassOf arb ar))
(assert (subClassOf arz ar))

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

; --- isAnyOf: if-direction only (taxonomic) ---
(assert (forall ((c Entity) (l Entity) (v Entity) (x Entity))
    (=> (and (has_operand c l) (has_operator c op_isAnyOf) (has_value c v)
             (taxonomic l) (subClassOf x v))
        (in_denotation x c))))


; === Problem: ODRL052-1 ===
(declare-const c1 Entity)
(declare-const c2 Entity)
(assert (has_operand c1 language))
(assert (has_operator c1 op_isAnyOf))
(assert (has_value c1 de))
(assert (has_value c1 en))
(assert (forall ((x Entity))
    (=> (in_denotation x c1) (or (subClassOf x de) (subClassOf x en)))))
(assert (has_operand c2 language))
(assert (has_operator c2 op_eq))
(assert (has_value c2 fr))

(assert (exists ((x Entity))
    (and (in_denotation x c1) (in_denotation x c2))))

(check-sat)