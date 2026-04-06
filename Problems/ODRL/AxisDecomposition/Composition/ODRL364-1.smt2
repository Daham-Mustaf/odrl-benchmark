; --------------------------------------------------------------------------
; File     : ODRL364-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : Mixed operators across 4 axes → box Compatible
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL364-1.smt2
; Status   : sat
; Comments : Verdict: Compatible  Category: Composition  Difficulty: Medium
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(declare-const z Real)
(declare-const w Real)
(assert (> x 0.0)) (assert (= x 600.0)) (assert (<= x 800.0))
(assert (> y 0.0)) (assert (> y 100.0)) (assert (< y 500.0))
(assert (> z 0.0)) (assert (>= z 8.0))   (assert (<= z 32.0))
(assert (> w 0.0)) (assert (<= w 300.0)) (assert (>= w 150.0))
(check-sat)
(exit)
