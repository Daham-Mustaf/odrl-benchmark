; --------------------------------------------------------------------------
; File     : ODRL651-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : 1-axis containment: lteq 800 not subsumed-by lteq 600 -> Conflict
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL651-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: BoxContainment  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const h1 Real)
(declare-const h2 Real)
(assert (= h1 800.0))
(assert (= h2 600.0))
(assert (<= h1 h2))
(check-sat)
(exit)
