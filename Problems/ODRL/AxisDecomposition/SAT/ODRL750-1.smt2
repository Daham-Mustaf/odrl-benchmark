; --------------------------------------------------------------------------
; File     : ODRL750-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : ORD000 strict total order is satisfiable
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL750-1.smt2
; Status   : sat
; Comments : SAT: axiom consistency. Category: SAT.
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(assert (< 0.0 600.0))
(assert (< 600.0 1200.0))
(check-sat)
(exit)
