; --------------------------------------------------------------------------
; File     : ODRL412-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : 4D fractional bounds Conflict (12 constants)
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL412-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: PolicyQuality  Difficulty: Hard
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(declare-const z Real)
(declare-const w Real)
(assert (> x 1.0))   (assert (< x 599.5))  (assert (>= x 600.0))
(assert (> y 2.0))   (assert (> y 479.5))  (assert (< y 480.0))
(assert (> z 3.0))   (assert (> z 15.5))   (assert (< z 16.0))
(assert (> w 4.0))   (assert (< w 71.5))   (assert (>= w 72.0))
(check-sat)
(exit)
