; --------------------------------------------------------------------------
; File     : ODRL769-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : SAT PolicyQuality: 4-axis drone policy is satisfiable
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL769-1.smt2
; Status   : sat
; Comments : Verdict: Satisfiable  Category: SAT  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(declare-const z Real)
(declare-const w Real)
(assert (>= x 200.0))(assert (<= x 800.0))
(assert (>= y 100.0))(assert (<= y 600.0))
(assert (>= z 8.0))  (assert (<= z 32.0))
(assert (>= w 72.0)) (assert (<= w 300.0))
(check-sat)
(exit)
