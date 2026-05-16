; --------------------------------------------------------------------------
; File     : ODRL626-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : thm:aabb shape_point: in_closed(X,V,V) iff X=V
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL626-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: Projection  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(assert (= x 400.0))
(assert (and (>= x 600.0) (<= x 600.0)))
(check-sat)
(exit)
