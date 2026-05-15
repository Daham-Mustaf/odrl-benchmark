; --------------------------------------------------------------------------
; File     : ODRL628-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : thm:aabb shape_open: in_open(X,v400,v600)
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL628-1.smt2
; Status   : sat
; Comments : Verdict: Compatible  Category: Projection  Difficulty: Medium
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(assert (> x 400.0)) (assert (< x 600.0))
(check-sat)
(exit)
