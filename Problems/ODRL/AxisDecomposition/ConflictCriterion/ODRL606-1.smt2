; --------------------------------------------------------------------------
; File     : ODRL606-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : NOT disjoint cc: [v0,v5] vs [v5,v10] touching
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL606-1.smt2
; Status   : sat
; Comments : Verdict: Compatible  Category: ConflictCriterion  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(assert (>= x 0.0)) (assert (<= x 600.0))
(assert (>= x 600.0))
(check-sat)
(exit)
