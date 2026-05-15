; --------------------------------------------------------------------------
; File     : ODRL402-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : 2D Conflict via width (5 constants)
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL402-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: PolicyQuality  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(assert (> x 0.0)) (assert (<= x 400.0)) (assert (>= x 800.0))
(assert (> y 0.0)) (assert (<= y 600.0)) (assert (>= y 200.0))
(check-sat)
(exit)
