; --------------------------------------------------------------------------
; File     : ODRL608-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : disjoint symmetry: disjoint(A,B) iff disjoint(B,A)
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL608-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: ConflictCriterion  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(assert (>= x 0.0)) (assert (<= x 500.0))
(assert (>= x 600.0))
(check-sat)
(exit)
