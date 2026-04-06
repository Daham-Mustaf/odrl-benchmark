; --------------------------------------------------------------------------
; File     : ODRL464-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : xone-A vs xone-B: cross-branch pair overlaps → Compatible
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL464-1.smt2
; Status   : sat
; Comments : Verdict: Compatible  Category: LogicalXone  Difficulty: Medium
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(assert (> x 0.0)) (assert (> y 0.0))
(assert (or (and (<= x 400.0) (not (<= y 300.0)))
            (and (not (<= x 400.0)) (<= y 300.0))))
(assert (or (and (<= x 600.0) (not (<= y 500.0)))
            (and (not (<= x 600.0)) (<= y 500.0))))
(check-sat)
(exit)
