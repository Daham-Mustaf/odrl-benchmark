; --------------------------------------------------------------------------
; File     : ODRL616-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : wf_gt violation: V=SupD implies not wf(gt)
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL616-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: WellFormedness  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const v Real)
(assert (= v 1200.0))
(assert (> v 1200.0))
(check-sat)
(exit)
