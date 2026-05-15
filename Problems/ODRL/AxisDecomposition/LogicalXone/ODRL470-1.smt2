; --------------------------------------------------------------------------
; File     : ODRL470-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : xone-A vs xone-B: all 4 branch-pair intersections empty → Conflict
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL470-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: LogicalXone  Difficulty: Hard
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
