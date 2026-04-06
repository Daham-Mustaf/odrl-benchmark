; --------------------------------------------------------------------------
; File     : ODRL350-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : Depth breaks 3D subsumption → Conflict
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL350-1.smt2
; Status   : sat
; Comments : Verdict: Conflict  Category: Box3D  Difficulty: Medium
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(declare-const z Real)
(assert (> x 0.0)) (assert (<= x 600.0))
(assert (> y 0.0)) (assert (<= y 400.0))
(assert (> z 0.0)) (assert (<= z 32.0))
(assert (not (and (<= x 1200.0) (<= y 800.0) (<= z 16.0))))
(check-sat)
(exit)
