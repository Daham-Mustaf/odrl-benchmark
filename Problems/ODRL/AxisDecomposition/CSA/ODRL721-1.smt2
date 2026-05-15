; --------------------------------------------------------------------------
; File     : ODRL721-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : CSA ConflictCriterion: claim prec(v5,v5,c,c) holds (wrong)
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL721-1.smt2
; Status   : unsat
; Comments : Verdict: CounterSatisfiable  Category: CSA  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const u Real)
(assert (= u 5.0))
(assert (< u u))
(check-sat)
(exit)
