; --------------------------------------------------------------------------
; File     : ODRL423-1.smt2
; Domain   : ODRL Spatial Axis Profile / Axis Decomposition
; Problem  : oo: lt ∩ gt — boundary excluded both sides → Conflict
; Expected : unsat
; Verdict  : Conflict
; Category : Boundary
; Difficulty: Easy
;
; Refs     : [Mus+26] Mustafa et al. Axis Decomposition for ODRL.
;            arXiv:2602.19878.
;            [MuS26] Mustafa & Sutcliffe. ODRL Benchmark Suite. PAAR 2026.
; --------------------------------------------------------------------------
(set-logic QF_LRA)
(declare-const x Real)
(assert (> x 0.0))
(assert (< x 600.0))
(assert (> x 600.0))
(check-sat)
(exit)
