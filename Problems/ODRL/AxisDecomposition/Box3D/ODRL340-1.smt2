; --------------------------------------------------------------------------
; File     : ODRL340-1.smt2
; Domain   : ODRL Spatial Axis Profile / Axis Decomposition
; Problem  : All three axes conflict → box Conflict
; Expected : unsat
; Verdict  : Conflict
; Category : Box3D
; Difficulty: Easy
;
; Refs     : [Mus+26] Mustafa et al. Axis Decomposition for ODRL.
;            arXiv:2602.19878.
;            [MuS26] Mustafa & Sutcliffe. ODRL Benchmark Suite. PAAR 2026.
; --------------------------------------------------------------------------
(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(declare-const z Real)
(assert (> x 0.0)) (assert (<= x 600.0)) (assert (>= x 800.0))
(assert (> y 0.0)) (assert (<= y 300.0)) (assert (>= y 500.0))
(assert (> z 0.0)) (assert (<= z 8.0))   (assert (>= z 24.0))
(check-sat)
(exit)
