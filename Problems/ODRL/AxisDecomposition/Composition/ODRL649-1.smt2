; --------------------------------------------------------------------------
; File     : ODRL649-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : or vs xone: differ when two branch pairs compatible
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL649-1.smt2
; Status   : unsat
; Comments : Verdict: Compatible  Category: Composition  Difficulty: Easy
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
(declare-fun or_verdict (Verdict Verdict) Verdict)
(declare-fun xone_verdict (Verdict Verdict) Verdict)

; or_compat (COMP000-0.ax)
(assert (forall ((v1 Verdict) (v2 Verdict))
    (=> (and (is_verdict v1) (is_verdict v2)
             (or (= v1 compatible) (= v2 compatible)))
        (= (or_verdict v1 v2) compatible))))
; xone_unknown (COMP000-0.ax) - residual case
(assert (forall ((vm Verdict) (vr Verdict))
    (=> (and (is_verdict vm) (is_verdict vr)
             (not (and (= vm compatible) (= vr conflict)))
             (not (and (= vm conflict)  (= vr conflict))))
        (= (xone_verdict vm vr) unknown))))
; Negated conjunction
(assert (or (not (= (or_verdict compatible compatible) compatible))
            (not (= (xone_verdict compatible compatible) unknown))))
(check-sat)
(exit)
