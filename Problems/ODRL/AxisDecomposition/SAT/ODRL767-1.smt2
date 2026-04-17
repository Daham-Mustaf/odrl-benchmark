; --------------------------------------------------------------------------
; File     : ODRL767-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : SAT Box3D: three axis_conflict facts on distinct axes are consistent
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL767-1.smt2
; Status   : sat
; Comments : SAT: axiom consistency. Category: SAT.
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(declare-const z Real)
(assert (>= x 1.0))(assert (<= x 2.0))
(assert (>= y 2.0))(assert (<= y 3.0))
(assert (>= z 3.0))(assert (<= z 4.0))
(check-sat)
(exit)
