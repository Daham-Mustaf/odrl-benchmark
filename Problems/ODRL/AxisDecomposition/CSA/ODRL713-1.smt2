; --------------------------------------------------------------------------
; File     : ODRL713-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : CSA Projection: claim v400 in point interval [v600,v600] (wrong)
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL713-1.smt2
; Status   : unsat
; Comments : Verdict: CounterSatisfiable  Category: CSA  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(assert (= x 400.0))
(assert (= x 600.0))
(check-sat)
(exit)
