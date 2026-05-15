; --------------------------------------------------------------------------
; File     : ODRL752-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : PREC000 endpoint precedence is satisfiable
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL752-1.smt2
; Status   : sat
; Comments : Verdict: Satisfiable  Category: SAT  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const u Real)
(declare-const l Real)
(assert (= u 5.0)) (assert (= l 6.0))
(assert (< u l))
(check-sat)
(exit)
