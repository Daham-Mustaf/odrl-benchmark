; --------------------------------------------------------------------------
; File     : ODRL630-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : completion_compat: value in domain gives compatible completion
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL630-1.smt2
; Status   : unsat
; Comments : Verdict: Compatible  Category: Completion  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const v Real)
; Membership at the specific witness v=600 (verified semantic by substitution:
; flipping v to 2000 makes this sat).
(assert (= v 600.0))
(assert (not (and (>= v 0.0) (<= v 1200.0))))
(check-sat)
(exit)
