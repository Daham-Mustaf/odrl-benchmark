; --------------------------------------------------------------------------
; File     : ODRL413-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : 4D fractional bounds Compatible (12 constants)
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL413-1.smt2
; Status   : sat
; Comments : Verdict: Compatible  Category: PolicyQuality  Difficulty: Hard
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(declare-const z Real)
(declare-const w Real)
(assert (> x 1.0)) (assert (<= x 600.5)) (assert (>= x 600.0))
(assert (> y 2.0)) (assert (<= y 480.5)) (assert (>= y 480.0))
(assert (> z 3.0)) (assert (<= z 16.5))  (assert (>= z 16.0))
(assert (> w 4.0)) (assert (<= w 72.5))  (assert (>= w 72.0))
(check-sat)
(exit)
