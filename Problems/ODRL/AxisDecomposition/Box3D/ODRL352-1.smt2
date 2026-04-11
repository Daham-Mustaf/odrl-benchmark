; --------------------------------------------------------------------------
; File     : ODRL352-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : Associativity: both nestings of box_verdict give Conflict
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL352-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: Box3D  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
; pure Kleene algebra — no Real variable declarations needed
; Kleene: conflict=0, compatible=2, box_verdict = min
; Negation: min(0,min(2,2))!=0 OR min(min(0,2),2)!=0
; min(0,2)=0, min(2,2)=2, min(0,2)=0 -> both =0, negation is unsat
(assert (not (and (= (ite (<= 0.0 (ite (<= 2.0 2.0) 2.0 2.0)) 0.0 (ite (<= 2.0 2.0) 2.0 2.0)) 0.0)
                  (= (ite (<= (ite (<= 0.0 2.0) 0.0 2.0) 2.0) (ite (<= 0.0 2.0) 0.0 2.0) 2.0) 0.0))))
(check-sat)
(exit)
