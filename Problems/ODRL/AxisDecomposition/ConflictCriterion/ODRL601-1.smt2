; --------------------------------------------------------------------------
; File     : ODRL601-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : prec_cc negative: equal endpoints not prec(cc)
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL601-1.smt2
; Status   : unsat
; Comments : Verdict: Compatible  Category: ConflictCriterion  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const u Real)
(assert (< u u))
(check-sat)
(exit)
