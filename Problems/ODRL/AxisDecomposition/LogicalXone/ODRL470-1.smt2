; --------------------------------------------------------------------------
; File     : ODRL470-1.smt2
; Domain   : ODRL Spatial Axis Profile / Axis Decomposition
; Problem  : xone-A vs xone-B: all 4 branch-pair intersections empty → Conflict
; Expected : unsat
; Verdict  : Conflict
; Category : LogicalXone
; Difficulty: Hard
;
; Refs     : [Mus+26] Mustafa et al. Axis Decomposition for ODRL.
;            arXiv:2602.19878.
;            [MuS26] Mustafa & Sutcliffe. ODRL Benchmark Suite. PAAR 2026.
; --------------------------------------------------------------------------
(set-logic QF_LRA)
(declare-const x Real)
(assert (> x 0.0))
; xone_A: x∈(0,100] XOR x∈[500,600]
(assert (or (and (<= x 100.0) (not (and (>= x 500.0) (<= x 600.0))))
            (and (> x 100.0)  (and (>= x 500.0) (<= x 600.0)))))
; xone_B: x∈[200,300] XOR x∈[700,800]
(assert (or (and (>= x 200.0) (<= x 300.0) (not (and (>= x 700.0) (<= x 800.0))))
            (and (not (and (>= x 200.0) (<= x 300.0))) (>= x 700.0) (<= x 800.0))))
(check-sat)
(exit)
