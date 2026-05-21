; --------------------------------------------------------------------------
; File     : ODRL773-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : Runtime joint permit: a request satisfies both lteq 1080 and eq 800
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL773-1.smt2
; Status   : sat
; Comments : Verdict: Permit  Category: Runtime  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(assert (> x 0.0)) (assert (<= x 1080.0))
(assert (= x 800.0))
(check-sat)
(exit)
