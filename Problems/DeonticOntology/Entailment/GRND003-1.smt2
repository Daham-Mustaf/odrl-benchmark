; --------------------------------------------------------------------------
; File     : GRND003-1.smt2
; Domain   : Deontic Ontology / ODRL Grounding
; Problem  : Prohibition creates Duty and Right over rfr(a)
; Status   : unsat
; Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
; Policy   : Policies/GRND003-policy.ttl
; Generated: 2026-03-25 by gen_foundation_problems.py v1.5
;
; proh(f1) activated by e1 entails Duty(alice,rfr(distribute),d1)
; and Right(acme,rfr(distribute),d1).
;
; ODRL Policy (Turtle) — see Policies/ for full file:
; @prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
; @prefix drk:    <http://w3id.org/drk/ontology/> .
; @prefix dcat:   <http://www.w3.org/ns/dcat#> .
; @prefix schema: <https://schema.org/> .
; <drk:policy-no-distribute> a odrl:Agreement ;
;     odrl:prohibition [ a odrl:Prohibition ;
;         odrl:assignee <drk:StreamingPortalGmbH> ;
;         odrl:assigner <drk:StaatlicheMuseenBerlin> ;
;         odrl:action   odrl:distribute ;
;         odrl:target   <drk:MuseumCollectionAPI> ] .
; <drk:MuseumCollectionAPI>    a dcat:DataService ;
;     schema:name "Staatliche Museen Berlin Collection API" .
; <drk:StaatlicheMuseenBerlin> a schema:Organization .
; <drk:StreamingPortalGmbH>    a schema:Organization .
; --------------------------------------------------------------------------

; === Layer 0 + Layer 1 preamble (embedded — SMT-LIB has no include) ===
; === Source: Axioms/Layer0-Signature/GRND000-0.smt2 ===
; GRND000-0.smt2
(set-logic UF)
(set-info :source |Mohammed et al., What Does ODRL Mean? FOIS 2026|)

; === Appendix A.0 additional sorts/predicates ===
; Appendix A.0 additional sorts and predicates
; Note: odrl-rel and strong are declared in the preamble — not repeated here.
(declare-sort NormPos 0)
(declare-fun norm-state-change (Agent Action Target NormPos) Bool)
(declare-fun inst-event        (Event) Bool)
(declare-fun triggers          (Event Agent Action Target NormPos) Bool)
(declare-fun competent-for     (Agent Event) Bool)
(declare-fun about-event       (Position Event) Bool)
(declare-fun does              (Agent Action Target) Bool)
(declare-fun rem-act           (Rule Action) Bool)
(declare-fun founds-rem        (Event Relator Rule) Bool)
(declare-fun founds-imm        (Event Relator Rule) Bool)
(declare-const duty-rem        NormPos)


; === Layer 1: ALL paper axioms embedded (28 formulae: 27 axioms + 1 corollary) ===
; === Z3 does not timeout on the full set; FOF inlines per-problem subsets ===
; === only (fof_axioms key) to avoid Vampire timeouts. Asymmetry intentional. ===
; === Authoritative source: Axioms/Layer1-Deontic/GRND-AX-1.smt2 ===
; === (SMT-LIB has no include directive — axioms embedded directly) ===

; ax_perm_relator_basic
(assert (forall ((p Rule) (x Agent) (y Agent) (a Action) (t Target) (e Event))
  (=> (and (perm p) (aee p x) (aer p y) (act p a) (tgt p t) (activates e p))
      (exists ((rho Relator) (l Position) (n Position))
        (and (founds e rho p)
             (permission l) (bearer l x) (cnt l a t) (part-of l rho)
             (no-right n)   (bearer n y) (cnt n a t) (part-of n rho))))))

; ax_perm_relator_strong
(assert (forall ((p Rule) (x Agent) (y Agent) (a Action) (t Target) (e Event))
  (=> (and (perm p) (strong p) (aee p x) (aer p y) (act p a) (tgt p t)
           (activates e p))
      (exists ((rho-i Relator) (im Position) (db Position))
        (and (founds-imm e rho-i p)
             (immunity im)   (bearer im x) (cnt im a t) (part-of im rho-i)
             (disability db) (bearer db y) (cnt db a t) (part-of db rho-i))))))

; ax_proh_relator_basic
(assert (forall ((f Rule) (x Agent) (y Agent) (a Action) (t Target) (e Event))
  (=> (and (proh f) (aee f x) (aer f y) (act f a) (tgt f t) (activates e f))
      (exists ((rho Relator) (d Position) (c Position))
        (and (founds e rho f)
             (duty d)  (bearer d x) (cnt d (rfr a) t) (part-of d rho)
             (right c) (bearer c y) (cnt c (rfr a) t) (part-of c rho))))))

; ax_proh_relator_remedy
(assert (forall ((f Rule) (x Agent) (y Agent) (a Action) (t Target) (e Event))
  (=> (and (proh f) (has-rem f) (aee f x) (aer f y) (act f a) (tgt f t)
           (activates e f))
      (exists ((rho-r Relator) (pw Position) (s Position))
        (and (founds-rem e rho-r f)
             (power pw)     (bearer pw y) (cnt pw (decl a) t) (part-of pw rho-r)
             (subjection s) (bearer s x)  (cnt s  (decl a) t) (part-of s rho-r))))))

; ax_unique_founding
(assert (forall ((r Rule) (e Event) (rho1 Relator) (rho2 Relator))
  (=> (and (founds e rho1 r) (founds e rho2 r)) (= rho1 rho2))))

; ax_unique_relator_per_event
(assert (forall ((r Rule) (e1 Event) (e2 Event) (rho Relator))
  (=> (and (founds e1 rho r) (founds e2 rho r)) (= e1 e2))))

; ax_unique_founding_rem
(assert (forall ((r Rule) (e Event) (rho1 Relator) (rho2 Relator))
  (=> (and (founds-rem e rho1 r) (founds-rem e rho2 r))
      (= rho1 rho2))))

; ax_unique_founding_imm
(assert (forall ((r Rule) (e Event) (rho1 Relator) (rho2 Relator))
  (=> (and (founds-imm e rho1 r) (founds-imm e rho2 r))
      (= rho1 rho2))))

; ax_obl_relator
(assert (forall ((d Rule) (x Agent) (y Agent) (a Action) (t Target) (e Event))
  (=> (and (obl d) (aee d x) (aer d y) (act d a) (tgt d t) (activates e d))
      (exists ((rho Relator) (du Position) (c Position))
        (and (founds e rho d)
             (duty du) (bearer du x) (cnt du a t) (part-of du rho)
             (right c) (bearer c y)  (cnt c  a t) (part-of c rho))))))

; ax_correlativity_permission
(assert (forall ((rho Relator) (a Action) (t Target))
  (=> (odrl-rel rho)
      (= (exists ((l Position))
           (and (permission l) (part-of l rho) (cnt l a t)))
         (exists ((n Position))
           (and (no-right n) (part-of n rho) (cnt n a t)
                (forall ((m Position))
                  (=> (and (no-right m) (part-of m rho) (cnt m a t))
                      (= m n)))))))))

; ax_correlativity_duty
(assert (forall ((rho Relator) (a Action) (t Target))
  (=> (odrl-rel rho)
      (= (exists ((d Position))
           (and (duty d) (part-of d rho) (cnt d a t)))
         (exists ((c Position))
           (and (right c) (part-of c rho) (cnt c a t)
                (forall ((k Position))
                  (=> (and (right k) (part-of k rho) (cnt k a t))
                      (= k c)))))))))

; ax_correlativity_power
(assert (forall ((rho Relator) (a Action) (t Target))
  (=> (odrl-rel rho)
      (= (exists ((pw Position))
           (and (power pw) (part-of pw rho) (cnt pw a t)))
         (exists ((s Position))
           (and (subjection s) (part-of s rho) (cnt s a t)
                (forall ((s2 Position))
                  (=> (and (subjection s2) (part-of s2 rho) (cnt s2 a t))
                      (= s2 s)))))))))

; ax_correlativity_immunity
(assert (forall ((rho Relator) (a Action) (t Target))
  (=> (odrl-rel rho)
      (= (exists ((im Position))
           (and (immunity im) (part-of im rho) (cnt im a t)))
         (exists ((db Position))
           (and (disability db) (part-of db rho) (cnt db a t)
                (forall ((db2 Position))
                  (=> (and (disability db2) (part-of db2 rho) (cnt db2 a t))
                      (= db2 db)))))))))

; ax_conflict_detection
(assert (forall ((rho Relator) (l Position) (d Position)
                 (x Agent) (a Action) (t Target))
  (=> (and (part-of l rho) (part-of d rho)
           (permission l) (duty d)
           (bearer l x) (bearer d x)
           (cnt l a t) (cnt d (rfr a) t))
      false)))

; ax_cross_relator_consistency
(assert (forall ((l Position) (d Position) (x Agent) (a Action) (t Target))
  (=> (and (permission l) (bearer l x) (cnt l a t)
           (duty d)       (bearer d x) (cnt d (rfr a) t))
      false)))

; ax_disability_block
(assert (forall ((f Rule) (x Agent) (y Agent) (a Action) (t Target))
  (=> (and (proh f) (aee f x) (aer f y) (act f a) (tgt f t))
      (not (exists ((db Position))
             (and (disability db) (bearer db y) (cnt db a t)))))))

; ax_odrl_rel_typing
(assert (forall ((e Event) (rho Relator) (r Rule))
  (=> (and (founds e rho r) (or (perm r) (proh r) (obl r)))
      (odrl-rel rho))))

; ax_odrl_rel_typing_rem
(assert (forall ((e Event) (rho Relator) (r Rule))
  (=> (and (founds-rem e rho r) (proh r))
      (odrl-rel rho))))

; ax_odrl_rel_typing_imm
(assert (forall ((e Event) (rho Relator) (r Rule))
  (=> (and (founds-imm e rho r) (perm r))
      (odrl-rel rho))))

; ax_A1
(assert (forall ((x Agent) (a Action) (t Target) (q NormPos))
  (=> (norm-state-change x a t q)
      (exists ((e Event))
        (and (inst-event e) (triggers e x a t q))))))

; ax_A2
(assert (forall ((e Event))
  (=> (inst-event e)
      (exists ((y Agent)) (competent-for y e)))))

; ax_A3
(assert (forall ((y Agent) (e Event))
  (=> (competent-for y e)
      (exists ((pw Position) (s Position) (x Agent))
        (and (power pw)     (bearer pw y) (about-event pw e)
             (subjection s) (bearer s x)  (about-event s e))))))

; ax_B1
(assert (forall ((f Rule) (x Agent) (a Action) (t Target))
  (=> (and (proh f) (has-rem f) (act f a) (tgt f t) (aee f x) (does x a t))
      (exists ((b Action))
        (and (rem-act f b) (norm-state-change x b t duty-rem))))))

; ax_B2
(assert (forall ((pw Position) (a Action) (t Target)
                 (rho Relator) (e Event) (r Rule))
  (=> (and (power pw) (cnt pw (decl a) t) (part-of pw rho) (founds-rem e rho r))
      (about-event pw e))))

; ax_B3
(assert (forall ((s Position) (a Action) (t Target)
                 (rho Relator) (e Event) (r Rule))
  (=> (and (subjection s) (cnt s (decl a) t) (part-of s rho) (founds-rem e rho r))
      (about-event s e))))

; === Ground instance (gamma) ===
(declare-const alice      Agent) (declare-const acme       Agent)
(declare-const distribute NormContent) (declare-const d1   Target)
(declare-const f1         Rule)   (declare-const e1        Event)
(assert (proh f1))
(assert (aee f1 alice)) (assert (aer f1 acme))
(assert (act f1 distribute)) (assert (tgt f1 d1))
(assert (activates e1 f1))

; === Negated conjecture ===
(assert (not
  (exists ((rho Relator) (d Position) (c Position))
    (and (founds e1 rho f1)
         (duty d)  (bearer d alice) (cnt d (rfr distribute) d1) (part-of d rho)
         (right c) (bearer c acme)  (cnt c (rfr distribute) d1) (part-of c rho)))))

(check-sat)