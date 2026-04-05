; --------------------------------------------------------------------------
; File     : ODRL450-1.smt2
; Domain   : ODRL Spatial Axis Profile / Axis Decomposition
; Problem  : Mixed operators or+and: open interval overlap → Compatible (density)
; Expected : sat
; Verdict  : Compatible
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
(assert (> x 0.0)) (assert (> y 0.0))
(assert (or (< x 600.0) (> y 200.0)))
(assert (> x 400.0))
(assert (< y 800.0))
(check-sat)
(exit)
