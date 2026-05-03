; --------------------------------------------------------------------------
; File     : KGC441-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : isAnyOf / Compatible: isAnyOf {bcp:de, bcp:fr} x eq bcp:de
; Version  : 1.0
; Authors  : 
; Refs     : [Mus+26b] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Denotational Semantics for ODRL: Knowledge-Based Constraint Conflict Detection. 2026. arXiv:2602.19883. https://arxiv.org/abs/2602.19883
; Source   : Mustafa, D. (2026)
; Names    : KGC441-1.smt2
; Status   : sat
; Verdict  : Compatible
; Comments : Verdict: Compatible  Category: Conflict  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic UF)
(declare-sort Concept 0)
(declare-fun bcp_de () Concept)
(declare-fun bcp_fr () Concept)
(assert (distinct bcp_de bcp_fr))
(declare-fun x () Concept)
(assert (or (= x bcp_de) (= x bcp_fr)))
(assert (= x bcp_de))
(check-sat)
(exit)
