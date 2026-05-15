; --------------------------------------------------------------------------
; File     : ODRL724-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : CSA ConflictCriterion: claim upper_tag(eq,o) (wrong - eq has closed upper)
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL724-1.smt2
; Status   : unsat
; Comments : Verdict: CounterSatisfiable  Category: CSA  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic UF)
; Op and Tag sorts (PREC000-0.ax)
(declare-sort Op 0)
(declare-sort Tag 0)
(declare-fun eq   () Op)
(declare-fun lteq () Op)
(declare-fun gteq () Op)
(declare-fun lt   () Op)
(declare-fun gt   () Op)
(declare-fun c () Tag)
(declare-fun o () Tag)
(declare-fun upper_tag (Op Tag) Bool)
(assert (distinct c o))

; upper_tag ground facts (PREC000-0.ax)
(assert (upper_tag eq c))
(assert (upper_tag lteq c))
(assert (upper_tag gteq c))
(assert (upper_tag lt o))
(assert (upper_tag gt c))
; Functionality: upper_tag is single-valued on Op
(assert (forall ((op Op) (t1 Tag) (t2 Tag))
    (=> (and (upper_tag op t1) (upper_tag op t2)) (= t1 t2))))
; Wrong claim asserted directly (CSA)
(assert (upper_tag eq o))
(check-sat)
(exit)
