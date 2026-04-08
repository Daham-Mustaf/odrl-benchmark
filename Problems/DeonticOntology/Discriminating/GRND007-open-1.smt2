; --------------------------------------------------------------------------
; File     : GRND007-open-1.smt2
; Domain   : Deontic Ontology / ODRL Grounding
; Axioms   : Open-world: uncovered action entails Permission by default
; Version  : 1.6
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [MMC+26] Mohammed, D., Mustafa, D., Collarana, D., Lange, C., Guizzardi, G. What Does ODRL Mean? Grounding Permissions, Prohibitions, and Duties in Deontic Logic and Foundational Ontology. FOIS 2026.
; Source   : Mustafa, D. (2026)
; Names    : GRND007-open-1.smt2
; Status   : unsat
; Comments : Open-world closure added. No proh for modify_act.
;            Permission(portal,modify_act,theater_ds) is derivable.
;            Abstract constants: portal=drk:StreamingPortalGmbH,
;            ensemble=drk:BerlinerEnsemble, modify_act=odrl:modify,
;            theater_ds=drk:TheaterShowtimeDataset
;            Foundational ontology tier. FOIS 2026 benchmark.
;            Policy source: Policies/GRND007-open-policy.ttl
;            @prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
;            @prefix drk:    <http://w3id.org/drk/ontology/> .
;            @prefix dcat:   <http://www.w3.org/ns/dcat#> .
;            # behaviour=open policy over drk:TheaterShowtimeDataset.
;            # No prohibition on odrl:modify declared.
;            ... (5 more lines — see Policies/ file)
; --------------------------------------------------------------------------


; === Layer 0 + Layer 1 preamble (embedded — SMT-LIB has no include) ===
; === Source: Axioms/GRND000-0.smt2 ===
; --------------------------------------------------------------------------
; File     : GRND000-0.smt2
; Domain   : Deontic Ontology / ODRL Grounding
; Axioms   : Signature — sorts, predicates, rfr/decl/issue functions
; Version  : 1.5
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [MMC+26] Mohammed, D., Mustafa, D., Collarana, D., Lange, C., Guizzardi, G. What Does ODRL Mean? Grounding Permissions, Prohibitions, and Duties in Deontic Logic and Foundational Ontology. FOIS 2026.
; Source   : Mustafa, D. (2026)
; Names    : GRND000-0.smt2
; Status   : unknown
; Comments : SMT-LIB has no include directive. This preamble is embedded verbatim by every problem generator. Do NOT add (check-sat) here.
; --------------------------------------------------------------------------

(set-logic UF)
(set-info :source |Mohammed et al., What Does ODRL Mean? FOIS 2026|)
(set-info :status unknown)
; --------------------------------------------------------------------------
; SORTS
; NormContent is a unified sort for Act and Forbearance content.
; rfr maps within NormContent; rfr_distinctness (rfr(a)!=a) replaces
; the former sort-level disjointness that held when Action and
; Forbearance were separate sorts.
; --------------------------------------------------------------------------
(declare-sort Agent       0)
(declare-sort NormContent 0)
(declare-sort Target      0)
(declare-sort Rule        0)
(declare-sort Position    0)
(declare-sort Relator     0)
(declare-sort Event       0)

; --------------------------------------------------------------------------
; ODRL RULE TYPE PREDICATES
; --------------------------------------------------------------------------
(declare-fun perm    (Rule) Bool)
(declare-fun proh    (Rule) Bool)
(declare-fun obl     (Rule) Bool)
(declare-fun has-rem (Rule) Bool)
(declare-fun strong  (Rule) Bool)
(declare-fun aee (Rule Agent)       Bool)
(declare-fun aer (Rule Agent)       Bool)
(declare-fun act (Rule NormContent) Bool)
(declare-fun tgt (Rule Target)      Bool)
(declare-fun activates (Event Rule) Bool)

; --------------------------------------------------------------------------
; UFO RELATOR AND POSITION PREDICATES
; founds     — conduct relator (Duty-Right or Permission-NoRight)
; founds-rem — competence relator rho_R for prohibition+remedy (Ax5.4)
; founds-imm — competence relator rho_I for strong permission (Ax5.2)
; --------------------------------------------------------------------------
(declare-fun founds     (Event Relator Rule) Bool)
(declare-fun founds-rem (Event Relator Rule) Bool)
(declare-fun founds-imm (Event Relator Rule) Bool)
(declare-fun part-of    (Position Relator)   Bool)
(declare-fun bearer     (Position Agent)     Bool)
(declare-fun cnt        (Position NormContent Target) Bool)
(declare-fun odrl-rel   (Relator) Bool)
; UFO-L position type predicates
(declare-fun permission (Position) Bool)
(declare-fun no-right   (Position) Bool)
(declare-fun duty       (Position) Bool)
(declare-fun right      (Position) Bool)
(declare-fun power      (Position) Bool)
(declare-fun subjection (Position) Bool)
(declare-fun immunity   (Position) Bool)
(declare-fun disability (Position) Bool)

; --------------------------------------------------------------------------
; RFR FUNCTION  rfr : NormContent -> NormContent
; --------------------------------------------------------------------------
(declare-fun rfr (NormContent) NormContent)
(declare-fun pos (NormContent) NormContent)
(assert (forall ((a NormContent) (b NormContent))
  (=> (= (rfr a) (rfr b)) (= a b))))
(assert (forall ((a NormContent))
  (= (pos (rfr a)) a)))
(assert (forall ((a NormContent))
  (not (= (rfr a) a))))

; --------------------------------------------------------------------------
; DECL FUNCTION  decl : NormContent -> NormContent
; --------------------------------------------------------------------------
(declare-fun decl (NormContent) NormContent)
(assert (forall ((a NormContent) (b NormContent))
  (=> (= (decl a) (decl b)) (= a b))))
(assert (forall ((a NormContent))
  (not (= (decl a) a))))
(assert (forall ((a NormContent))
  (not (= (decl a) (rfr a)))))

; --------------------------------------------------------------------------
; ISSUE FUNCTION  issue : Rule -> NormContent
; --------------------------------------------------------------------------
(declare-fun issue (Rule) NormContent)
(assert (forall ((a Rule) (b Rule))
  (=> (= (issue a) (issue b)) (= a b))))

; --------------------------------------------------------------------------
; NORMCONTENT TYPE DISTINCTION
; --------------------------------------------------------------------------
(assert (forall ((p Position) (a NormContent) (t Target))
  (not (and (cnt p a t) (cnt p (rfr a) t)))))

; --------------------------------------------------------------------------
; POSITION SORT DISJOINTNESS (UFO-L terms)
; --------------------------------------------------------------------------
(assert (forall ((p Position)) (not (and (permission p) (duty p)))))
(assert (forall ((p Position)) (not (and (permission p) (right p)))))
(assert (forall ((p Position)) (not (and (permission p) (no-right p)))))
(assert (forall ((p Position)) (not (and (duty p)       (right p)))))
(assert (forall ((p Position)) (not (and (duty p)       (no-right p)))))
(assert (forall ((p Position)) (not (and (right p)      (no-right p)))))
(assert (forall ((p Position)) (not (and (power p)      (subjection p)))))
(assert (forall ((p Position)) (not (and (power p)      (immunity p)))))
(assert (forall ((p Position)) (not (and (power p)      (disability p)))))
(assert (forall ((p Position)) (not (and (subjection p) (immunity p)))))
(assert (forall ((p Position)) (not (and (subjection p) (disability p)))))
(assert (forall ((p Position)) (not (and (immunity p)   (disability p)))))
(assert (forall ((p Position)) (not (and (permission p) (power p)))))
(assert (forall ((p Position)) (not (and (permission p) (subjection p)))))
(assert (forall ((p Position)) (not (and (permission p) (immunity p)))))
(assert (forall ((p Position)) (not (and (permission p) (disability p)))))
(assert (forall ((p Position)) (not (and (duty p)       (power p)))))
(assert (forall ((p Position)) (not (and (duty p)       (subjection p)))))
(assert (forall ((p Position)) (not (and (duty p)       (immunity p)))))
(assert (forall ((p Position)) (not (and (duty p)       (disability p)))))
(assert (forall ((p Position)) (not (and (right p)      (power p)))))
(assert (forall ((p Position)) (not (and (right p)      (subjection p)))))
(assert (forall ((p Position)) (not (and (right p)      (immunity p)))))
(assert (forall ((p Position)) (not (and (right p)      (disability p)))))
(assert (forall ((p Position)) (not (and (no-right p)   (power p)))))
(assert (forall ((p Position)) (not (and (no-right p)   (subjection p)))))
(assert (forall ((p Position)) (not (and (no-right p)   (immunity p)))))
(assert (forall ((p Position)) (not (and (no-right p)   (disability p)))))
; END OF PREAMBLE — problem files append axioms + conjecture after this

; === Appendix A.0 additional sorts/predicates ===
; Appendix A.0 additional sorts and predicates
; Embedded before SMT2_AXIOMS — legal-relator and NormPos must be declared
; before ax_odrl_rel_is_rel and A1/B1 respectively.
; Note: odrl-rel, strong, founds-rem, founds-imm are declared in the
; Layer 0 preamble — not repeated here.
(declare-sort NormPos 0)
(declare-fun legal-relator      (Relator) Bool)
(declare-fun norm-state-change  (Agent NormContent Target NormPos) Bool)
(declare-fun inst-event         (Event) Bool)
(declare-fun triggers           (Event Agent NormContent Target NormPos) Bool)
(declare-fun competent-for      (Agent Event) Bool)
(declare-fun about-event        (Position Event) Bool)
(declare-fun does               (Agent NormContent Target) Bool)
(declare-fun rem-act            (Rule NormContent) Bool)
(declare-const duty-rem         NormPos)


; === Layer 1: axioms omitted (skip_smt2_axioms=True) ===
; === Problem is self-contained in smt2_extra_decls. ===

; === Ground instance (gamma) ===
(declare-const portal     Agent) (declare-const ensemble   Agent)
(declare-const modify-act NormContent) (declare-const theater-ds Target)
(assert (not (exists ((f Rule) (e Event))
               (and (proh f) (aee f portal) (act f modify-act) (activates e f)))))
(assert (forall ((x Agent) (a NormContent) (t Target))
  (=> (not (exists ((f Rule) (e Event))
              (and (proh f) (aee f x) (act f a) (activates e f))))
      (exists ((l Position))
        (and (permission l) (bearer l x) (cnt l a t))))))

; === Negated conjecture ===
(assert (not
  (exists ((l Position))
    (and (permission l) (bearer l portal) (cnt l modify-act theater-ds)))))

(check-sat)