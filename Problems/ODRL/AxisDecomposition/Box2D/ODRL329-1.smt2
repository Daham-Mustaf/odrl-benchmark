; --------------------------------------------------------------------------
; File     : ODRL329-1.smt2
; Domain   : ODRL Spatial Axis Profile / Axis Decomposition
; Problem  : Narrow width strip × wide height → box Compatible
; Expected : sat
; Verdict  : Compatible
; Category : Box2D
; Difficulty: Easy
;
; Refs     : [Mus+26] Mustafa et al. Axis Decomposition for ODRL.
;            arXiv:2602.19878.
;            [MuS26] Mustafa & Sutcliffe. ODRL Benchmark Suite. PAAR 2026.
; --------------------------------------------------------------------------
(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(assert (> x 0.0))
(assert (>= x 500.0))
(assert (<= x 510.0))
(assert (> y 0.0))
(assert (>= y 100.0))
(assert (<= y 900.0))
(check-sat)
(exit)
