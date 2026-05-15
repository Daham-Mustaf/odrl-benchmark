; --------------------------------------------------------------------------
; File     : ODRL446-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : 3-branch or: depth branch overlaps → Compatible
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL446-1.smt2
; Status   : sat
; Comments : Verdict: Compatible  Category: LogicalOr  Difficulty: Medium
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(declare-const z Real)
(assert (> x 0.0)) (assert (> y 0.0)) (assert (> z 0.0))
(assert (or (<= x 200.0) (<= y 100.0) (<= z 200.0)))
(assert (>= x 400.0))
(assert (>= y 200.0))
(assert (>= z 100.0))
(check-sat)
(exit)
