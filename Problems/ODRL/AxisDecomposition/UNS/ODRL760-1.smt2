; --------------------------------------------------------------------------
; File     : ODRL760-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : intra-policy: eq 600 AND gteq 700 gives empty denotation
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. arXiv:2602.19878. https://arxiv.org/abs/2602.19878
; Source   : Mustafa, D. (2026)
; Names    : ODRL760-1.smt2
; Status   : unsat
; Comments : UNS: intra-policy contradiction. Category: UNS.
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(assert (= x 600.0))
(assert (>= x 700.0))
(check-sat)
(exit)
