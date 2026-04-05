; --------------------------------------------------------------------------
; File     : ODRL443-1.smt2
; Domain   : ODRL Spatial Axis Profile / Axis Decomposition
; Problem  : PolicyA and: all PolicyB or-branches conflict → Conflict
; Expected : unsat
; Verdict  : Conflict
; Category : LogicalOr
; Difficulty: Medium
;
; Refs     : [Mus+26] Mustafa et al. Axis Decomposition for ODRL.
;            arXiv:2602.19878.
;            [MuS26] Mustafa & Sutcliffe. ODRL Benchmark Suite. PAAR 2026.
; --------------------------------------------------------------------------
(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(assert (> x 0.0)) (assert (<= x 400.0))
(assert (> y 0.0)) (assert (<= y 100.0))
(assert (or (>= x 800.0) (>= y 200.0)))
(check-sat)
(exit)
