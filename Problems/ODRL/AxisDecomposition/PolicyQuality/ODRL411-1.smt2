; --------------------------------------------------------------------------
; File     : ODRL411-1.smt2
; Domain   : ODRL Spatial Axis Profile / Axis Decomposition
; Problem  : 3D eq conflict via distinctness (7 constants)
; Expected : unsat
; Verdict  : Conflict
; Category : PolicyQuality
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
(assert (> x 0.0)) (assert (= x 600.0)) (assert (= x 601.0))
(assert (> y 0.0)) (assert (> y 300.0)) (assert (< y 500.0))
(assert (> z 0.0)) (assert (<= z 32.0)) (assert (>= z 16.0))
(check-sat)
(exit)
