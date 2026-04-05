; --------------------------------------------------------------------------
; File     : ODRL431-1.smt2
; Domain   : ODRL Spatial Axis Profile / Axis Decomposition
; Problem  : 2D cc×oc — Y boundary excluded on left kills box → Conflict
; Expected : unsat
; Verdict  : Conflict
; Category : Boundary
; Difficulty: Medium
;
; Refs     : [Mus+26] Mustafa et al. Axis Decomposition for ODRL.
;            arXiv:2602.19878.
;            [MuS26] Mustafa & Sutcliffe. ODRL Benchmark Suite. PAAR 2026.
; --------------------------------------------------------------------------
(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(assert (> x 0.0)) (assert (<= x 600.0)) (assert (>= x 600.0))
(assert (> y 0.0)) (assert (< y 400.0)) (assert (>= y 400.0))
(check-sat)
(exit)
