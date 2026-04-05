; --------------------------------------------------------------------------
; File     : ODRL334-1.smt2
; Domain   : ODRL Spatial Axis Profile / Axis Decomposition
; Problem  : box_verdict(conflict, compatible) = conflict: Kleene Rule 1 direct
; Expected : unsat
; Verdict  : Conflict
; Category : Box2D
; Difficulty: Easy
;
; Refs     : [Mus+26] Mustafa et al. Axis Decomposition for ODRL.
;            arXiv:2602.19878.
;            [MuS26] Mustafa & Sutcliffe. ODRL Benchmark Suite. PAAR 2026.
; --------------------------------------------------------------------------
(set-logic QF_LRA)

; Kleene ordering: conflict=0.0 < unknown=1.0 < compatible=2.0
; box_verdict(V1,V2) = min(V1,V2) under this ordering
; Negation: min(conflict=0.0, compatible=2.0) != conflict=0.0
(assert (not (= (ite (<= 0.0 2.0) 0.0 2.0) 0.0)))
(check-sat)
(exit)
