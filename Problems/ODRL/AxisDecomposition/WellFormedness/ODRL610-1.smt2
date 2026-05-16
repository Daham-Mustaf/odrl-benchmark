; --------------------------------------------------------------------------
; File     : ODRL610-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : wf_eq: value inside domain is well-formed
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL610-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: WellFormedness  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const v Real)
; Pin the witness v=600 and assert the negated wf_eq condition.
; Unsat iff 600 is in [0, 1200].  Verified semantic by perturbation:
; changing v=600 -> v=2000, or upper 1200 -> 500, flips to sat.
(assert (= v 600.0))
(assert (or (< v 0.0) (> v 1200.0)))
(check-sat)
(exit)
