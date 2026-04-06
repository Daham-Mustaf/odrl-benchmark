; --------------------------------------------------------------------------
; File     : ODRL366-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : HD video 4-axis: all compatible
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL366-1.smt2
; Status   : sat
; Comments : Verdict: Compatible  Category: Composition  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(declare-const z Real)
(declare-const w Real)
(assert (> x 0.0)) (assert (<= x 1920.0)) (assert (>= x 640.0))
(assert (> y 0.0)) (assert (<= y 1080.0)) (assert (>= y 480.0))
(assert (> z 0.0)) (assert (<= z 48.0))   (assert (>= z 16.0))
(assert (> w 0.0)) (assert (<= w 600.0))  (assert (>= w 150.0))
(check-sat)
(exit)
