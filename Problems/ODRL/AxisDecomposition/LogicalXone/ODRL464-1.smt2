; --------------------------------------------------------------------------
; File     : ODRL464-1.smt2
; Domain   : ODRL Spatial Axis Profile / Axis Decomposition
; Problem  : xone-A vs xone-B: cross-branch pair overlaps → Compatible
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
(assert (or (and (<= x 400.0) (not (<= y 300.0)))
            (and (not (<= x 400.0)) (<= y 300.0))))
(assert (or (and (<= x 600.0) (not (<= y 500.0)))
            (and (not (<= x 600.0)) (<= y 500.0))))
(check-sat)
(exit)
