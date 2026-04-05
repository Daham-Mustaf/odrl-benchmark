; --------------------------------------------------------------------------
; File     : ODRL367-1.smt2
; Domain   : ODRL Spatial Axis Profile / Axis Decomposition
; Problem  : HD video width conflict → box Conflict
; Expected : unsat
; Verdict  : Conflict
; Category : Composition
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
(declare-const w Real)
(assert (> x 0.0)) (assert (<= x 640.0))  (assert (>= x 1920.0))
(assert (> y 0.0)) (assert (<= y 1080.0)) (assert (>= y 480.0))
(assert (> z 0.0)) (assert (<= z 48.0))   (assert (>= z 16.0))
(assert (> w 0.0)) (assert (<= w 600.0))  (assert (>= w 150.0))
(check-sat)
(exit)
