; --------------------------------------------------------------------------
; File     : ODRL432-1.smt2
; Domain   : ODRL Spatial Axis Profile / Axis Decomposition
; Problem  : 3D cc×co×cc — Y boundary excluded on right kills 3D box → Conflict
; Expected : unsat
; Verdict  : Conflict
; Category : Boundary
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
(assert (> x 0.0)) (assert (<= x 600.0)) (assert (>= x 600.0))
(assert (> y 0.0)) (assert (<= y 400.0)) (assert (> y 400.0))
(assert (> z 0.0)) (assert (<= z 200.0)) (assert (>= z 200.0))
(check-sat)
(exit)
