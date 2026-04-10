; --------------------------------------------------------------------------
; File     : ODRL719-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : CSA Box2D: claim 2D compatible when height conflicts (wrong)
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL719-1.smt2
; Status   : unsat
; Comments : CSA: wrong verdict. Category: CSA.
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(assert (> x 0.0))(assert (<= x 800.0))(assert (>= x 400.0))
(assert (> y 0.0))(assert (<= y 300.0))(assert (>= y 600.0))
(check-sat)
(exit)
