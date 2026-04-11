; --------------------------------------------------------------------------
; File     : ODRL334-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : box_verdict(conflict, compatible) = conflict: Kleene Rule 1 direct
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL334-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: Box2D  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
; pure Kleene algebra — no Real variable declarations needed
; Kleene ordering: conflict=0.0 < unknown=1.0 < compatible=2.0
; box_verdict(V1,V2) = min(V1,V2) under this ordering
; Negation: min(conflict=0.0, compatible=2.0) != conflict=0.0
(assert (not (= (ite (<= 0.0 2.0) 0.0 2.0) 0.0)))
(check-sat)
(exit)
