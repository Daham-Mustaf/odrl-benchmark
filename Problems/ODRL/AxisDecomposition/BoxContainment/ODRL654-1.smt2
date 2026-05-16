; --------------------------------------------------------------------------
; File     : ODRL654-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : C1 absent on width axis -> Unknown
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL654-1.smt2
; Status   : unsat
; Comments : Verdict: Unknown  Category: BoxContainment  Difficulty: Easy
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
; Presence sort (mirrors SUBS000-0.ax presence tags)
(declare-sort Presence 0)
(declare-fun present () Presence)
(declare-fun absent  () Presence)
(declare-fun is_presence (Presence) Bool)
(assert (distinct present absent))
(assert (is_presence present))
(assert (is_presence absent))
(assert (forall ((p Presence)) (=> (is_presence p) (or (= p present) (= p absent)))))
; Bound sort: uninterpreted endpoints of intervals
(declare-sort Bound 0)
(declare-fun subs_verdict (Bound Bound Presence Bound Bound Presence) Verdict)
(declare-fun v0 () Bound)
(declare-fun v600 () Bound)
(declare-fun v800 () Bound)

; subs_c1_absent (SUBS000-0.ax)
(assert (forall ((l1 Bound) (h1 Bound) (l2 Bound) (h2 Bound))
    (= (subs_verdict l1 h1 absent l2 h2 present) unknown)))
; Negated conjecture
(assert (not (= (subs_verdict v0 v600 absent v0 v800 present) unknown)))
(check-sat)
(exit)
