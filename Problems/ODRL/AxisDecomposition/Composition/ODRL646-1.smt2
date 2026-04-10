; --------------------------------------------------------------------------
; File     : ODRL646-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : xone_unknown: both pairs compatible implies xone=unknown
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL646-1.smt2
; Status   : unsat
; Comments : Verdict: Compatible  Category: Composition  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(assert (not (= x x)))
(check-sat)
(exit)
