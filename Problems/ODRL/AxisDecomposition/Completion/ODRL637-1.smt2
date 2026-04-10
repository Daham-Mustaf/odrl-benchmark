; --------------------------------------------------------------------------
; File     : ODRL637-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : completion_conflict requires strict U<V: U=V gives no conflict
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL637-1.smt2
; Status   : unsat
; Comments : Verdict: Compatible  Category: Completion  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const u Real)
(assert (= u 600.0))
(assert (< u 600.0))
(check-sat)
(exit)
