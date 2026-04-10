; --------------------------------------------------------------------------
; File     : ODRL653-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : 4-axis box containment: width axis escapes → Conflict
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL653-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: BoxContainment  Difficulty: Medium
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(assert (not (= x x)))
(check-sat)
(exit)
