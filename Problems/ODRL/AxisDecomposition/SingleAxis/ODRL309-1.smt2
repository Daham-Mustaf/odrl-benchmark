; --------------------------------------------------------------------------
; File     : ODRL309-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : (0,600] ⊆ (0,1200]: tighter bound subsumes wider
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL309-1.smt2
; Status   : unsat
; Comments : Verdict: Compatible  Category: SingleAxis  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(assert (> x 0.0))
(assert (<= x 600.0))
(assert (not (<= x 1200.0)))
(check-sat)
(exit)
