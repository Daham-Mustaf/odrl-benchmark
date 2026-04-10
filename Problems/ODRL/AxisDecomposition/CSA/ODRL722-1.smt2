; --------------------------------------------------------------------------
; File     : ODRL722-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : CSA ConflictCriterion: claim touching cc NOT disjoint is wrong (touching IS disjoint cc)
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL722-1.smt2
; Status   : unsat
; Comments : CSA: wrong verdict. Category: CSA.
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(assert (= x 5.0))
(assert (>= x 0.0))(assert (<= x 5.0))
(assert (not (and (>= x 5.0) (<= x 10.0))))
(check-sat)
(exit)
