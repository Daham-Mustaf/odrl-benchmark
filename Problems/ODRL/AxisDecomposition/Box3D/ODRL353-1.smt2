; --------------------------------------------------------------------------
; File     : ODRL353-1.smt2
; Domain   : ODRL Spatial Axis Profile / Axis Decomposition
; Problem  : prop:monotone in 3D: narrowing width propagates Conflict
; Expected : unsat
; Verdict  : Conflict
; Category : Box3D
; Difficulty: Medium
;
; Refs     : [Mus+26] Mustafa et al. Axis Decomposition for ODRL.
;            arXiv:2602.19878.
;            [MuS26] Mustafa & Sutcliffe. ODRL Benchmark Suite. PAAR 2026.
; --------------------------------------------------------------------------
(set-logic QF_LRA)
(declare-const x Real)
(assert (>= x 200.0))
(assert (<= x 600.0))
(assert (>= x 900.0))
(assert (<= x 1200.0))
(check-sat)
(exit)
