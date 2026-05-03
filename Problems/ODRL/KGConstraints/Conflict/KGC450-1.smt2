; --------------------------------------------------------------------------
; File     : KGC450-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : neq / Conflict: neq bcp:de x eq bcp:de
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Denotational Semantics for ODRL: Knowledge-Based Constraint Conflict Detection. 2026. arXiv:2602.19883. https://arxiv.org/abs/2602.19883
; Source   : Mustafa, D. (2026)
; Names    : KGC450-1.smt2
; Status   : unsat
; Verdict  : Conflict
; Comments : Verdict: Conflict  Category: Conflict  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic UF)
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)
; Negation of Conflict: witness x in both denotations.
; [[c_offer]]   = C \ {bcp_de}, so x must satisfy x != bcp_de
; [[c_request]] = {bcp_de}, so x must satisfy x = bcp_de
; These constraints are unsatisfiable; unsat is correct.
(declare-fun x () Concept)
(assert (distinct x bcp_de))
(assert (= x bcp_de))
(check-sat)
(exit)
