; --------------------------------------------------------------------------
; File     : ODRL600-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : prec_cc: less(U,L) implies prec(U,L,c,c)
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL600-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: ConflictCriterion  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const u Real)
(declare-const l Real)
(assert (< u l))
(assert (not (< u l)))
(check-sat)
(exit)
