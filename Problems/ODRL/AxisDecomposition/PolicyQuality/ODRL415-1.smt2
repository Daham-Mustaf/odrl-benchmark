; --------------------------------------------------------------------------
; File     : ODRL415-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : 4D fractional subsumption Compatible — maximum difficulty (12 constants, 66 orderings)
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL415-1.smt2
; Status   : unsat
; Comments : Verdict: Compatible  Category: PolicyQuality  Difficulty: VeryHard
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(declare-const z Real)
(declare-const w Real)
(assert (> x 1.0)) (assert (<= x 599.5))
(assert (> y 2.0)) (assert (<= y 479.5))
(assert (> z 3.0)) (assert (<= z 15.5))
(assert (> w 4.0)) (assert (<= w 71.5))
(assert (not (and (> x 1.0) (<= x 600.5) (> y 2.0) (<= y 480.5) (> z 3.0) (<= z 16.5) (> w 4.0) (<= w 72.5))))
(check-sat)
(exit)
