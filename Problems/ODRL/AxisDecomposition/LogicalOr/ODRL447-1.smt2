; --------------------------------------------------------------------------
; File     : ODRL447-1.smt2
; Domain   : ODRL Spatial Axis Profile / Axis Decomposition
; Problem  : or-subsumption: A_and ⊆ B_or → Compatible
; Expected : unsat
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
(assert (> x 0.0)) (assert (<= x 600.0))
(assert (> y 0.0)) (assert (<= y 400.0))
(assert (not (or (<= x 800.0) (<= y 600.0))))
(check-sat)
(exit)
