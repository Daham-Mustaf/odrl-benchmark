; --------------------------------------------------------------------------
; File     : ODRL665-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : disjoint via second disjunct: I1=[v6,v10], I2=[v0,v5]
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL665-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: ConflictCriterion  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(assert (> x 0.0))
(assert (>= x 600.0))    ; sem(gteq 600), interval 1
(assert (<= x 500.0))    ; sem(lteq 500), interval 2
(check-sat)
(exit)
