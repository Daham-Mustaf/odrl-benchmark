; --------------------------------------------------------------------------
; File     : ODRL413-1.smt2
; Domain   : ODRL Spatial Axis Profile / Axis Decomposition
; Problem  : 4D fractional bounds Compatible (12 constants)
; Expected : sat
; Verdict  : Compatible
; Category : PolicyQuality
; Difficulty: Hard
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
(assert (> x 1.0)) (assert (<= x 600.5)) (assert (>= x 600.0))
(assert (> y 2.0)) (assert (<= y 480.5)) (assert (>= y 480.0))
(assert (> z 3.0)) (assert (<= z 16.5))  (assert (>= z 16.0))
(assert (> w 4.0)) (assert (<= w 72.5))  (assert (>= w 72.0))
(check-sat)
(exit)
