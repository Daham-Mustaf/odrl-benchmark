; ODRL010-1.smt2 — Layer 0 transitivity: partOf(bavaria, europe)
; Expected: unsat (SZS: Theorem)

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


(assert (not (partOf bavaria europe)))

(check-sat)