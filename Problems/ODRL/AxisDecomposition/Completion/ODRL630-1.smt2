; --------------------------------------------------------------------------
; File     : ODRL630-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : completion_compat: value in domain gives compatible completion
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL630-1.smt2
; Status   : unsat
; Comments : Verdict: Compatible  Category: Completion  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const v Real)
(assert (>= v 0.0)) (assert (<= v 1200.0))
(assert (not (and (>= v 0.0) (<= v 1200.0))))
(check-sat)
(exit)
