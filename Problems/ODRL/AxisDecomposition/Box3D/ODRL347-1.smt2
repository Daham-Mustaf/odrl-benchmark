; --------------------------------------------------------------------------
; File     : ODRL347-1.smt2
; Domain   : ODRL Spatial Axis Profile / Axis Decomposition
; Problem  : All three axes open overlap → box Compatible
; Expected : sat
; Verdict  : Compatible
; Category : Box3D
; Difficulty: Medium
;
; Refs     : [Mus+26] Mustafa et al. Axis Decomposition for ODRL.
;            arXiv:2602.19878.
;            [MuS26] Mustafa & Sutcliffe. ODRL Benchmark Suite. PAAR 2026.
; --------------------------------------------------------------------------
(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(declare-const z Real)
(assert (> x 0.0)) (assert (> x 200.0)) (assert (< x 800.0))
(assert (> y 0.0)) (assert (> y 100.0)) (assert (< y 500.0))
(assert (> z 0.0)) (assert (> z 8.0))   (assert (< z 32.0))
(check-sat)
(exit)
