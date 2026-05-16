; --------------------------------------------------------------------------
; File     : ODRL634-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : monotone_conflict (Prop 6.9): subsumes & conflict implies conflict
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL634-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: Completion  Difficulty: Medium
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
; Inner interval [200, 400] and outer-conflict witness [800, infinity):
; disjoint because 400 < 800.
(assert (>= x 200.0))
(assert (<= x 400.0))
(assert (>= x 800.0))
(check-sat)
(exit)
