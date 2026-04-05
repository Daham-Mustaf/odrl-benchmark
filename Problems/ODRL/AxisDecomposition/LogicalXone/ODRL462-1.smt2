; --------------------------------------------------------------------------
; File     : ODRL462-1.smt2
; Domain   : ODRL Spatial Axis Profile / Axis Decomposition
; Problem  : and-B vs xone-A: ~A_x & A_y branch matches → Compatible
; Expected : sat
; Verdict  : Compatible
; Category : LogicalXone
; Difficulty: Medium
;
; Refs     : [Mus+26] Mustafa et al. Axis Decomposition for ODRL.
;            arXiv:2602.19878.
;            [MuS26] Mustafa & Sutcliffe. ODRL Benchmark Suite. PAAR 2026.
; --------------------------------------------------------------------------
(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(assert (> x 0.0)) (assert (> y 0.0))
(assert (>= x 800.0))
(assert (<= y 200.0))
(assert (or (and (<= x 600.0) (not (<= y 400.0)))
            (and (not (<= x 600.0)) (<= y 400.0))))
(check-sat)
(exit)
