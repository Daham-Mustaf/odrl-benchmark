; --------------------------------------------------------------------------
; File     : ODRL612-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : wf_gteq: value inside domain is well-formed
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL612-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: WellFormedness  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const v Real)
(assert (>= v 0.0))
(assert (>= 1200.0 v))
(assert (not (>= v 0.0)))
(check-sat)
(exit)
