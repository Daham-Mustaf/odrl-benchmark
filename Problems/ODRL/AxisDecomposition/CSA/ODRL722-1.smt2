; --------------------------------------------------------------------------
; File     : ODRL722-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : CSA ConflictCriterion: claim touching-cc intervals are disjoint (wrong — they share the boundary point)
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL722-1.smt2
; Status   : unsat
; Comments : Verdict: CounterSatisfiable  Category: CSA  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(assert (= x 5.0))
(assert (>= x 0.0))(assert (<= x 5.0))
(assert (not (and (>= x 5.0) (<= x 10.0))))
(check-sat)
(exit)
