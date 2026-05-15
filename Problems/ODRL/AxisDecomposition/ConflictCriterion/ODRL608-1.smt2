; --------------------------------------------------------------------------
; File     : ODRL608-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : disjoint symmetry: disjoint(A,B) iff disjoint(B,A)
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL608-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: ConflictCriterion  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const l1 Real) (declare-const u1 Real)
(declare-const l2 Real) (declare-const u2 Real)
; disjoint(A,B) in cc case: u1 < l2
(assert (< u1 l2))
; well-formed intervals: l1 <= u1, l2 <= u2
(assert (<= l1 u1))
(assert (<= l2 u2))
; negate disjoint(B,A): ~(u2 < l1) and ~(u2 <= l1)
(assert (not (< u2 l1)))
(assert (not (<= u2 l1)))
(check-sat)
(exit)
