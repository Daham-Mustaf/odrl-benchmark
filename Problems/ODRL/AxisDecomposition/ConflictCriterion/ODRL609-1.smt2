; --------------------------------------------------------------------------
; File     : ODRL609-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : operator tags: lt has open upper, gt has open lower
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL609-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: ConflictCriterion  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
; Indirect: lt 600 and gt 600 are contradictory (x < 600 and x > 600).
(assert (< x 600.0))
(assert (> x 600.0))
(check-sat)
(exit)
