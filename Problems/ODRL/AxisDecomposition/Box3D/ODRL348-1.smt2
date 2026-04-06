; --------------------------------------------------------------------------
; File     : ODRL348-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : Depth open/closed boundary conflict kills 3D box
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL348-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: Box3D  Difficulty: Hard
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(declare-const z Real)
(assert (> x 0.0)) (assert (<= x 800.0)) (assert (>= x 200.0))
(assert (> y 0.0)) (assert (<= y 600.0)) (assert (>= y 100.0))
(assert (> z 0.0)) (assert (< z 16.0))   (assert (>= z 16.0))
(check-sat)
(exit)
