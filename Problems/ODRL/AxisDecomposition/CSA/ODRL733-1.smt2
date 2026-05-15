; --------------------------------------------------------------------------
; File     : ODRL733-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : CSA BoxContainment: claim box_subs(unknown,compatible)=compatible (wrong)
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL733-1.smt2
; Status   : unsat
; Comments : Verdict: CounterSatisfiable  Category: CSA  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic UF)
; Three-valued Verdict sort (mirrors AXIS000-0.ax Section D)
(declare-sort Verdict 0)
(declare-fun conflict   () Verdict)
(declare-fun compatible () Verdict)
(declare-fun unknown    () Verdict)
(declare-fun is_verdict (Verdict) Bool)
(assert (distinct conflict compatible unknown))
(assert (is_verdict conflict))
(assert (is_verdict compatible))
(assert (is_verdict unknown))
(assert (forall ((v Verdict))
    (=> (is_verdict v)
        (or (= v conflict) (= v compatible) (= v unknown)))))
(declare-fun box_subs (Verdict Verdict) Verdict)

; box_subs_unknown (SUBS000-0.ax)
(assert (forall ((v1 Verdict) (v2 Verdict))
    (=> (and (is_verdict v1) (is_verdict v2)
             (not (and (= v1 compatible) (= v2 compatible)))
             (not (= v1 conflict)) (not (= v2 conflict)))
        (= (box_subs v1 v2) unknown))))
; Wrong claim asserted directly (CSA)
(assert (= (box_subs unknown compatible) compatible))
(check-sat)
(exit)
