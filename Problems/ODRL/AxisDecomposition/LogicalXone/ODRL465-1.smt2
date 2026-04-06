; --------------------------------------------------------------------------
; File     : ODRL465-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : 3-branch xone-A vs and-B: B implies 2+ branches → Conflict
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL465-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: LogicalXone  Difficulty: Medium
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(declare-const z Real)
(assert (> x 0.0)) (assert (> y 0.0)) (assert (> z 0.0))
(assert (or (and (<= x 600.0) (not (<= y 400.0)) (not (<= z 200.0)))
            (and (not (<= x 600.0)) (<= y 400.0) (not (<= z 200.0)))
            (and (not (<= x 600.0)) (not (<= y 400.0)) (<= z 200.0))))
(assert (<= x 400.0))
(assert (<= y 200.0))
(assert (<= z 100.0))
(check-sat)
(exit)
