; --------------------------------------------------------------------------
; File     : ODRL433-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : Subsumption: lt⊆lteq on width, lteq⊆lteq on height → Compatible
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL433-1.smt2
; Status   : unsat
; Comments : Verdict: Compatible  Category: Boundary  Difficulty: Medium
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(assert (> x 0.0)) (assert (< x 600.0))
(assert (> y 0.0)) (assert (<= y 400.0))
(assert (not (and (<= x 600.0) (<= y 800.0))))
(check-sat)
(exit)
