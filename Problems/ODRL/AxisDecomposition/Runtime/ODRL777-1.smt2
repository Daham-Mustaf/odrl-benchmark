; --------------------------------------------------------------------------
; File     : ODRL777-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : Runtime xone-permit: request width 1200 satisfies exactly one branch
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL777-1.smt2
; Status   : sat
; Comments : Verdict: Permit  Category: Runtime  Difficulty: Medium
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(assert (= x 1200.0))
(assert (xor (= x 1200.0) (= x 2400.0)))
(check-sat)
(exit)
