; --------------------------------------------------------------------------
; File     : ODRL466-1.smt2
; Domain   : ODRL Spatial Axis Profile / Axis Decomposition
; Problem  : 3-branch xone-A vs and-B: A_x branch alone compatible → Compatible
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
(declare-const z Real)
(assert (> x 0.0)) (assert (> y 0.0)) (assert (> z 0.0))
(assert (or (and (<= x 600.0) (not (<= y 400.0)) (not (<= z 200.0)))
            (and (not (<= x 600.0)) (<= y 400.0) (not (<= z 200.0)))
            (and (not (<= x 600.0)) (not (<= y 400.0)) (<= z 200.0))))
(assert (<= x 400.0))
(assert (>= y 500.0))
(assert (>= z 300.0))
(check-sat)
(exit)
