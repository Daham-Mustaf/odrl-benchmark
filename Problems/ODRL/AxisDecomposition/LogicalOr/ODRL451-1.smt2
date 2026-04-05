; --------------------------------------------------------------------------
; File     : ODRL451-1.smt2
; Domain   : ODRL Spatial Axis Profile / Axis Decomposition
; Problem  : 3-branch or with mixed ops: all branches conflict → Conflict
; Expected : unsat
; Verdict  : Conflict
; Category : LogicalOr
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
(assert (> x 0.0)) (assert (> y 0.0)) (assert (> z 0.0))
(assert (or (= x 600.0) (< y 200.0) (> z 100.0)))
(assert (> x 800.0))
(assert (>= y 400.0))
(assert (<= z 50.0))
(check-sat)
(exit)
