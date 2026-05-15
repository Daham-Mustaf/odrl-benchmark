; --------------------------------------------------------------------------
; File     : ODRL750-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : ORD000 strict total order is satisfiable
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL750-1.smt2
; Status   : sat
; Comments : Verdict: Satisfiable  Category: SAT  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(assert (< 0.0 600.0))
(assert (< 600.0 1200.0))
(check-sat)
(exit)
