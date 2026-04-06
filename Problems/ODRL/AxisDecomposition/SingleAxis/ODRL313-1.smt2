; --------------------------------------------------------------------------
; File     : ODRL313-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : BSB running example: width ≤ 600 vs width ≥ 1200
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL313-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: SingleAxis  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(assert (> x 0.0))
(assert (<= x 600.0))
(assert (>= x 1200.0))
(check-sat)
(exit)
