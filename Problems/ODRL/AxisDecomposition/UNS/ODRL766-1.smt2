; --------------------------------------------------------------------------
; File     : ODRL766-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : intra-policy: eq 600 AND eq 800 on same axis empty
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL766-1.smt2
; Status   : unsat
; Comments : Verdict: Unsatisfiable  Category: UNS  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(assert (= x 600.0))
(assert (= x 800.0))
(check-sat)
(exit)
