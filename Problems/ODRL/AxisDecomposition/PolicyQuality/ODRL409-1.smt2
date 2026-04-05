; --------------------------------------------------------------------------
; File     : ODRL409-1.smt2
; Domain   : ODRL Spatial Axis Profile / Axis Decomposition
; Problem  : 4D all open intervals — density (9 constants)
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
(assert (> x 0.0)) (assert (> x 200.0)) (assert (< x 800.0))
(assert (> y 0.0)) (assert (> y 100.0)) (assert (< y 500.0))
(assert (> z 0.0)) (assert (> z 8.0))   (assert (< z 32.0))
(assert (> w 0.0)) (assert (> w 72.0))  (assert (< w 300.0))
(check-sat)
(exit)
