; --------------------------------------------------------------------------
; File     : ODRL648-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : or_sound_2branch: all axis pairs conflict implies no shared point
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL648-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: Composition  Difficulty: Medium
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(assert (or (<= x 400.0) (<= x 300.0)))
(assert (or (>= x 600.0) (>= x 500.0)))
(check-sat)
(exit)
