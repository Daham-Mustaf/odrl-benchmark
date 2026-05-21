; --------------------------------------------------------------------------
; File     : ODRL775-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : Runtime and-deny: request (2400,900) fails width, so box denied
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL775-1.smt2
; Status   : unsat
; Comments : Verdict: Deny  Category: Runtime  Difficulty: Medium
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(assert (= x 2400.0)) (assert (> x 0.0)) (assert (<= x 1920.0))
(assert (= y 900.0))  (assert (> y 0.0)) (assert (<= y 1080.0))
(check-sat)
(exit)
