; --------------------------------------------------------------------------
; File     : ODRL767-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : SAT Box3D: three axis_conflict facts on distinct axes are consistent
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL767-1.smt2
; Status   : sat
; Comments : Verdict: Satisfiable  Category: SAT  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(declare-const z Real)
(assert (>= x 1.0))(assert (<= x 2.0))
(assert (>= y 2.0))(assert (<= y 3.0))
(assert (>= z 3.0))(assert (<= z 4.0))
(check-sat)
(exit)
