; --------------------------------------------------------------------------
; File     : KGC712-1.smt2
; Domain   : ODRL Policy / KB Grounding Concept-valued
; Axioms   : Proposition 2 (or): Unknown propagation [DPV]
; Version  : 1.0
; Authors  : 
; Refs     : [Mus+26b] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R., Quix, C., Decker, S. Denotational Semantics for ODRL: Knowledge-Based Constraint Conflict Detection. 2026. arXiv:2602.19883. https://arxiv.org/abs/2602.19883
; Source   : Mustafa, D. (2026)
; Names    : KGC712-1.smt2
; Status   : sat
; Verdict  : OrUnknown
; Comments : Verdict: OrUnknown  Category: Composition  Difficulty: Medium
; --------------------------------------------------------------------------

(set-logic UF)
(declare-sort Concept 0)
(declare-fun dpv_non_commercial_purpose () Concept)
(declare-fun dpv_scientific_research    () Concept)
(declare-fun kge_leq      (Concept Concept) Bool)
(declare-fun kge_disjoint (Concept Concept) Bool)
(assert (forall ((c Concept)) (kge_leq c c)))
(assert (forall ((a Concept) (b Concept) (c Concept))
    (=> (and (kge_leq a b) (kge_leq b c)) (kge_leq a c))))
(assert (forall ((a Concept) (b Concept))
    (=> (kge_disjoint a b) (kge_disjoint b a))))
; DPV: no edge or disjointness between SR and NonCommercial.
(assert (distinct dpv_non_commercial_purpose dpv_scientific_research))
;
; Atomic-level Unknown verdict lives in FOL via verdict_unknown_def
; in DENOT000.  SMT side confirms resource consistency only.
(check-sat)
(exit)
