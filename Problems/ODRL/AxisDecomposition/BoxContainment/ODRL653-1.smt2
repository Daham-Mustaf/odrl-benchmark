; --------------------------------------------------------------------------
; File     : ODRL653-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : 4-axis box containment: width axis escapes → Conflict
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL653-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: BoxContainment  Difficulty: Medium
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
(declare-fun axis_subsumes (Bound Bound Bound Bound) Bool)
(declare-fun subs_verdict (Bound Bound Presence Bound Bound Presence) Verdict)
(declare-fun v0 () Bound)
(declare-fun v600 () Bound)
(declare-fun v800 () Bound)

; subs_present_yes (SUBS000-0.ax)
(assert (forall ((l1 Bound) (h1 Bound) (l2 Bound) (h2 Bound))
    (=> (axis_subsumes l1 h1 l2 h2)
        (= (subs_verdict l1 h1 present l2 h2 present) compatible))))
; subs_present_no (SUBS000-0.ax)
(assert (forall ((l1 Bound) (h1 Bound) (l2 Bound) (h2 Bound))
    (=> (not (axis_subsumes l1 h1 l2 h2))
        (= (subs_verdict l1 h1 present l2 h2 present) conflict))))
; axis_subsumes ground hint (negative)
(assert (not (axis_subsumes v0 v800 v0 v600)))
; Negated conjecture
(assert (not (= (subs_verdict v0 v800 present v0 v600 present) conflict)))
(check-sat)
(exit)
