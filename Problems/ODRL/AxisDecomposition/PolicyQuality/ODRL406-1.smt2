; --------------------------------------------------------------------------
; File     : ODRL406-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : 2D near-miss gap=1 both axes (5 constants)
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL406-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: PolicyQuality  Difficulty: Medium
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(assert (> x 0.0)) (assert (<= x 599.0)) (assert (>= x 601.0))
(assert (> y 0.0)) (assert (<= y 399.0)) (assert (>= y 401.0))
(check-sat)
(exit)
