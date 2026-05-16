; --------------------------------------------------------------------------
; File     : ODRL631-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : completion_conflict: U<V in domain gives conflict completion
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL631-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: Completion  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
; Policy-level disjointness: [0, 400] and [800, infinity) share no point.
(assert (>= x 0.0))
(assert (<= x 400.0))
(assert (>= x 800.0))
(check-sat)
(exit)
