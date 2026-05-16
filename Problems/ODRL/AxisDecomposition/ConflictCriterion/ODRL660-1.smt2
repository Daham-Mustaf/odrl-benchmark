; --------------------------------------------------------------------------
; File     : ODRL660-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : prec_cc backward: prec(u,l,c,c) implies less(u,l)
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL660-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: ConflictCriterion  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(assert (> x 0.0))
(assert (<= x 500.0))
(assert (>= x 600.0))
(check-sat)
(exit)
