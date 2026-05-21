; --------------------------------------------------------------------------
; File     : ODRL772-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : Runtime soundness: no request satisfies both lteq 1920 and eq 2400
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL772-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: Runtime  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(assert (> x 0.0)) (assert (<= x 1920.0))
(assert (= x 2400.0))
(check-sat)
(exit)
