; --------------------------------------------------------------------------
; File     : ODRL442-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : PolicyA and-constraints: any PolicyB or-branch overlaps → Compatible
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL442-1.smt2
; Status   : sat
; Comments : Verdict: Compatible  Category: LogicalOr  Difficulty: Medium
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(assert (> x 0.0)) (assert (<= x 800.0))
(assert (> y 0.0)) (assert (<= y 600.0))
(assert (or (>= x 1000.0) (>= y 200.0)))
(check-sat)
(exit)
