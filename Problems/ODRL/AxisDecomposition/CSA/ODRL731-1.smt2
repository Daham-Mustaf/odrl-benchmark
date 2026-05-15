; --------------------------------------------------------------------------
; File     : ODRL731-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : CSA Completion: claim sharpness_compat holds without less(U,V) (wrong)
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL731-1.smt2
; Status   : unsat
; Comments : Verdict: CounterSatisfiable  Category: CSA  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const v Real)
(assert (= v 800.0))
(assert (>= v 0.0))(assert (<= v 600.0))
(check-sat)
(exit)
