; --------------------------------------------------------------------------
; File     : ODRL770-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : Runtime permit: request height 800 satisfies lteq 1080
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL770-1.smt2
; Status   : sat
; Comments : Verdict: Permit  Category: Runtime  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(assert (= x 800.0))
(assert (> x 0.0)) (assert (<= x 1080.0))
(check-sat)
(exit)
