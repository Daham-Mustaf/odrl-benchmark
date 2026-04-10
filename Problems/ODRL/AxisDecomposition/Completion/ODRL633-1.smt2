; --------------------------------------------------------------------------
; File     : ODRL633-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : sharpness_conflict: U<V in domain implies conflict completion exists
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL633-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: Completion  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const u Real)
(declare-const v Real)
(assert (>= u 0.0)) (assert (<= u 1200.0))
(assert (>= v 0.0)) (assert (<= v 1200.0))
(assert (< u v))
(assert (not (< u v)))
(check-sat)
(exit)
