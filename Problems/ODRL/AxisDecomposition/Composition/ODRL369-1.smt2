; --------------------------------------------------------------------------
; File     : ODRL369-1.smt2
; Domain   : ODRL Spatial Axis Profile / Axis Decomposition
; Problem  : 4D box A ⊄ B: alt axis escape → Conflict
; Expected : sat
; Verdict  : Conflict
; Category : Composition
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
(declare-const w Real)
(assert (> x 0.0)) (assert (<= x 600.0))
(assert (> y 0.0)) (assert (<= y 400.0))
(assert (> z 0.0)) (assert (<= z 16.0))
(assert (> w 0.0)) (assert (<= w 300.0))
(assert (not (and (<= x 1200.0) (<= y 800.0) (<= z 32.0) (<= w 150.0))))
(check-sat)
(exit)
