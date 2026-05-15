; --------------------------------------------------------------------------
; File     : ODRL643-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : or_verdict_total: result is always one of three verdicts
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL643-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: Composition  Difficulty: Easy
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
(declare-fun vv1 () Verdict)
(declare-fun vv2 () Verdict)

; or_verdict_total (COMP000-0.ax)
(assert (forall ((v1 Verdict) (v2 Verdict))
    (=> (and (is_verdict v1) (is_verdict v2))
        (or (= (or_verdict v1 v2) compatible)
            (= (or_verdict v1 v2) conflict)
            (= (or_verdict v1 v2) unknown)))))
; Negated conjecture (Skolemized)
(assert (is_verdict vv1))
(assert (is_verdict vv2))
(assert (not (or (= (or_verdict vv1 vv2) compatible)
                 (= (or_verdict vv1 vv2) conflict)
                 (= (or_verdict vv1 vv2) unknown))))
(check-sat)
(exit)
