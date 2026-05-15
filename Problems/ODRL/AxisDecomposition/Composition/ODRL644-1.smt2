; --------------------------------------------------------------------------
; File     : ODRL644-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : xone_compat: one match compatible rest conflict => xone=compatible
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL644-1.smt2
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
(declare-fun xone_verdict (Verdict Verdict) Verdict)

; xone_compat (COMP000-0.ax)
(assert (forall ((vm Verdict) (vr Verdict))
    (=> (and (is_verdict vm) (is_verdict vr)
             (= vm compatible) (= vr conflict))
        (= (xone_verdict vm vr) compatible))))
; Negated conjecture
(assert (not (= (xone_verdict compatible conflict) compatible)))
(check-sat)
(exit)
