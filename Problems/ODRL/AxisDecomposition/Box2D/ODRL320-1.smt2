; --------------------------------------------------------------------------
; File     : ODRL320-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : BSB: width conflict × height compatible → box Conflict
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL320-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: Box2D  Difficulty: Medium
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(assert (> x 0.0))
(assert (<= x 600.0))
(assert (>= x 1200.0))
(assert (> y 0.0))
(assert (<= y 600.0))
(assert (>= y 400.0))
(check-sat)
(exit)
