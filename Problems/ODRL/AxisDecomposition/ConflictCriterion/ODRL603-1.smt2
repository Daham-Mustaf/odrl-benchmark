; --------------------------------------------------------------------------
; File     : ODRL603-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : prec_co: leq(U,L) implies prec(U,L,c,o)
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL603-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: ConflictCriterion  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const u Real)
(declare-const l Real)
(assert (<= u l))
(assert (not (<= u l)))
(check-sat)
(exit)
