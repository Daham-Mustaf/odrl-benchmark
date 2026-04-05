; --------------------------------------------------------------------------
; File     : ODRL415-1.smt2
; Domain   : ODRL Spatial Axis Profile / Axis Decomposition
; Problem  : 4D fractional subsumption Compatible — maximum difficulty (12 constants, 66 orderings)
; Expected : unsat
; Verdict  : Compatible
; Category : PolicyQuality
; Difficulty: VeryHard
;
; Refs     : [Mus+26] Mustafa et al. Axis Decomposition for ODRL.
;            arXiv:2602.19878.
;            [MuS26] Mustafa & Sutcliffe. ODRL Benchmark Suite. PAAR 2026.
; --------------------------------------------------------------------------
(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(declare-const z Real)
(declare-const w Real)
(assert (> x 1.0)) (assert (<= x 599.5))
(assert (> y 2.0)) (assert (<= y 479.5))
(assert (> z 3.0)) (assert (<= z 15.5))
(assert (> w 4.0)) (assert (<= w 71.5))
(assert (not (and (> x 1.0) (<= x 600.5) (> y 2.0) (<= y 480.5) (> z 3.0) (<= z 16.5) (> w 4.0) (<= w 72.5))))
(check-sat)
(exit)
