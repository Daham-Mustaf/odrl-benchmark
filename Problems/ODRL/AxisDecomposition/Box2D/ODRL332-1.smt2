; --------------------------------------------------------------------------
; File     : ODRL332-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : 2D box A ⊄ B on width axis → Conflict
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL332-1.smt2
; Status   : sat
; Comments : Verdict: Conflict  Category: Box2D  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(assert (> x 0.0))
(assert (<= x 1200.0))
(assert (> y 0.0))
(assert (<= y 800.0))
(assert (not (and (<= x 600.0) (<= y 1200.0))))
(check-sat)
(exit)
