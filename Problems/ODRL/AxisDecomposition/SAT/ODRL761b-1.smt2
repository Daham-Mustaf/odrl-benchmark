; --------------------------------------------------------------------------
; File     : ODRL761b-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : SAT PolicyQuality: real-world HD policy is satisfiable
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL761b-1.smt2
; Status   : sat
; Comments : SAT: axiom consistency. Category: SAT.
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(assert (>= x 640.0))(assert (<= x 1920.0))
(assert (>= y 480.0))(assert (<= y 1080.0))
(check-sat)
(exit)
