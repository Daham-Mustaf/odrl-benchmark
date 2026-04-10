; --------------------------------------------------------------------------
; File     : ODRL650-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : 1-axis containment: lteq 600 subsumes lteq 800 → Compatible
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL650-1.smt2
; Status   : unsat
; Comments : Verdict: Compatible  Category: BoxContainment  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const h1 Real)
(declare-const h2 Real)
(assert (= h1 600.0))
(assert (= h2 800.0))
(assert (not (<= h1 h2)))
(check-sat)
(exit)
