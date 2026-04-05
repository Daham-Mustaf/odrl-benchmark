; --------------------------------------------------------------------------
; File     : ODRL352-1.smt2
; Domain   : ODRL Spatial Axis Profile / Axis Decomposition
; Problem  : Associativity: both nestings of box_verdict give Conflict
; Expected : unsat
; Verdict  : Conflict
; Category : Box3D
; Difficulty: Easy
;
; Refs     : [Mus+26] Mustafa et al. Axis Decomposition for ODRL.
;            arXiv:2602.19878.
;            [MuS26] Mustafa & Sutcliffe. ODRL Benchmark Suite. PAAR 2026.
; --------------------------------------------------------------------------
(set-logic QF_LRA)

; Kleene: conflict=0, compatible=2, box_verdict = min
; Negation: min(0,min(2,2))!=0 OR min(min(0,2),2)!=0
; min(0,2)=0, min(2,2)=2, min(0,2)=0 -> both =0, negation is unsat
(assert (not (and (= (ite (<= 0.0 (ite (<= 2.0 2.0) 2.0 2.0)) 0.0 (ite (<= 2.0 2.0) 2.0 2.0)) 0.0)
                  (= (ite (<= (ite (<= 0.0 2.0) 0.0 2.0) 2.0) (ite (<= 0.0 2.0) 0.0 2.0) 2.0) 0.0))))
(check-sat)
(exit)
