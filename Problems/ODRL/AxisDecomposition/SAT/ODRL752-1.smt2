; --------------------------------------------------------------------------
; File     : ODRL752-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : PREC000 endpoint precedence is satisfiable
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL752-1.smt2
; Status   : sat
; Comments : SAT: axiom consistency. Category: SAT.
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const u Real)
(declare-const l Real)
(assert (= u 5.0)) (assert (= l 6.0))
(assert (< u l))
(check-sat)
(exit)
