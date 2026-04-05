; --------------------------------------------------------------------------
; File     : ODRL449-1.smt2
; Domain   : ODRL Spatial Axis Profile / Axis Decomposition
; Problem  : 3-branch or vs 3-branch or: depth branch pair overlaps → Compatible
; Expected : sat
; Verdict  : Compatible
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
(declare-const z Real)
(assert (> x 0.0)) (assert (> y 0.0)) (assert (> z 0.0))
(assert (or (<= x 200.0) (<= y 100.0) (<= z 800.0)))
(assert (or (>= x 400.0) (>= y 200.0) (>= z 300.0)))
(check-sat)
(exit)
