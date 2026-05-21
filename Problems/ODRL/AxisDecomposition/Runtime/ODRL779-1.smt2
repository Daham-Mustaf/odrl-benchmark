; --------------------------------------------------------------------------
; File     : ODRL779-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : Runtime permit at boundary: request width 1920 satisfies lteq 1920
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL779-1.smt2
; Status   : sat
; Comments : Verdict: Permit  Category: Runtime  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(assert (= x 1920.0))
(assert (> x 0.0)) (assert (<= x 1920.0))
(check-sat)
(exit)
