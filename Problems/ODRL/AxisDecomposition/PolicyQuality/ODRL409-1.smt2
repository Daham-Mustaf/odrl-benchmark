; --------------------------------------------------------------------------
; File     : ODRL409-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : 4D all open intervals — density (9 constants)
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL409-1.smt2
; Status   : sat
; Comments : Verdict: Compatible  Category: PolicyQuality  Difficulty: Hard
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(declare-const z Real)
(declare-const w Real)
(assert (> x 0.0)) (assert (> x 200.0)) (assert (< x 800.0))
(assert (> y 0.0)) (assert (> y 100.0)) (assert (< y 500.0))
(assert (> z 0.0)) (assert (> z 8.0))   (assert (< z 32.0))
(assert (> w 0.0)) (assert (> w 72.0))  (assert (< w 300.0))
(check-sat)
(exit)
