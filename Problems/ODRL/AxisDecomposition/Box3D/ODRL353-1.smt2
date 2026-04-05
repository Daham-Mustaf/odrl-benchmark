; --------------------------------------------------------------------------
; File     : ODRL353-1.smt2
; Domain   : ODRL Spatial Axis Profile / Axis Decomposition
; Problem  : prop:monotone in 3D: narrowing width propagates Conflict
; Expected : unsat
; Verdict  : Conflict
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
; Negation: x in [200,600] AND x in [900,1200] (monotone conclusion fails)
(assert (>= x 200.0)) (assert (<= x 600.0))
(assert (>= x 900.0)) (assert (<= x 1200.0))
(assert (> y 0.0))    (assert (<= y 400.0))  (assert (>= y 100.0))
(assert (> z 0.0))    (assert (<= z 32.0))   (assert (>= z 8.0))
(check-sat)
(exit)
