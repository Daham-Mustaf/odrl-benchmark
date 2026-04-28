; --------------------------------------------------------------------------
; File     : KGC411-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : isA / Compatible: isA dpv:Purpose x eq dpv:ScientificResearch
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Denotational Semantics for ODRL: Knowledge-Based Constraint Conflict Detection. 2026. arXiv:2602.19883. https://arxiv.org/abs/2602.19883
; Source   : Mustafa, D. (2026)
; Names    : KGC411-1.smt2
; Status   : sat
; Verdict  : Compatible
; Comments : Verdict: Compatible  Category: Conflict  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic UF)
(declare-sort Concept 0)
(declare-fun dpv_purpose () Concept)
(declare-fun dpv_scientific_research () Concept)
(declare-fun kge_leq (Concept Concept) Bool)
; DPV: ScientificResearch <= Purpose (transitive closure stand-in).
(assert (kge_leq dpv_scientific_research dpv_purpose))
(declare-fun x () Concept)
(assert (= x dpv_scientific_research))
(assert (kge_leq x dpv_purpose))
(check-sat)
(exit)
