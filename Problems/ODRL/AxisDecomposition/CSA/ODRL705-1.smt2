; --------------------------------------------------------------------------
; File     : ODRL705-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : CSA ConflictCriterion: claim NOT disjoint cc (wrong)
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL705-1.smt2
; Status   : unsat
; Comments : Verdict: CounterSatisfiable  Category: CSA  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(assert (>= x 0.0)) (assert (<= x 5.0))
(assert (>= x 6.0))
(check-sat)
(exit)
