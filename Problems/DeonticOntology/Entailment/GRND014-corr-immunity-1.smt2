; --------------------------------------------------------------------------
; File     : GRND014-corr-immunity-1.smt2
; Domain   : Deontic Ontology / ODRL Grounding
; Problem  : Correlativity: Immunity implies unique Disability in relator
; Version  : 1.6
; Status   : unsat
; Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
; Source   : Mohammed, D. (2026)
; Names    : GRND014-corr-immunity-1.smt2
;
; odrl_rel(rho1), Immunity(im) partOf rho1 => exists unique db. Disability(db) partOf rho1.
;
; ODRL Policy (Turtle) — see Policies/ for full file:
; @prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
; @prefix drk:    <http://w3id.org/drk/ontology/> .
; @prefix dcat:   <http://www.w3.org/ns/dcat#> .
; # Correlativity: every Immunity in an ODRL relator has a unique correlative Disability.
; # Grounded in a strong-permission relator over drk:MuseumCollectionAPI.
; --------------------------------------------------------------------------

; === Layer 0 + Layer 1 preamble (embedded — SMT-LIB has no include) ===
; === Source: Axioms/GRND000-0.smt2 ===
; (set-logic UF)
; (set-info :source |Mohammed et al., What Does ODRL Mean? FOIS 2026|)
; (set-info :status unknown)
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
; NOTE: not used in GRND001-024. Present for PAAR 2026 benchmark only.
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


; === Layer 1: ALL 28 axioms embedded ===
; === Z3 handles full set; FOF inlines subsets only (Vampire timeout avoidance) ===
; === Authoritative source: Axioms/GRND-AX-1.smt2 ===

; ax_perm_relator_weak
(assert (forall ((p Rule) (x Agent) (y Agent) (a NormContent) (t Target) (e Event))
  (=> (and (perm p) (aee p x) (aer p y) (act p a) (tgt p t) (activates e p))
      (exists ((rho Relator) (l Position) (n Position))
        (and (founds e rho p)
             (permission l) (bearer l x) (cnt l a t) (part-of l rho)
             (no-right n)   (bearer n y) (cnt n a t) (part-of n rho))))))

; ax_perm_relator_strong
(assert (forall ((p Rule) (x Agent) (y Agent) (a NormContent) (t Target) (e Event))
  (=> (and (perm p) (strong p) (aee p x) (aer p y) (act p a) (tgt p t)
           (activates e p))
      (exists ((rho-i Relator) (im Position) (db Position))
        (and (founds-imm e rho-i p)
             (immunity im)   (bearer im x) (cnt im a t) (part-of im rho-i)
             (disability db) (bearer db y) (cnt db a t) (part-of db rho-i))))))

; ax_proh_relator_conduct
(assert (forall ((f Rule) (x Agent) (y Agent) (a NormContent) (t Target) (e Event))
  (=> (and (proh f) (aee f x) (aer f y) (act f a) (tgt f t) (activates e f))
      (exists ((rho Relator) (d Position) (c Position))
        (and (founds e rho f)
             (duty d)  (bearer d x) (cnt d (rfr a) t) (part-of d rho)
             (right c) (bearer c y) (cnt c (rfr a) t) (part-of c rho))))))

; ax_proh_relator_remedy
(assert (forall ((f Rule) (x Agent) (y Agent) (a NormContent) (t Target) (e Event))
  (=> (and (proh f) (has-rem f) (aee f x) (aer f y) (act f a) (tgt f t)
           (activates e f))
      (exists ((rho-r Relator) (pw Position) (s Position))
        (and (founds-rem e rho-r f)
             (power pw)     (bearer pw y) (cnt pw (decl a) t) (part-of pw rho-r)
             (subjection s) (bearer s x)  (cnt s  (decl a) t) (part-of s rho-r))))))

; ax_obl_relator
(assert (forall ((d Rule) (x Agent) (y Agent) (a NormContent) (t Target) (e Event))
  (=> (and (obl d) (aee d x) (aer d y) (act d a) (tgt d t) (activates e d))
      (exists ((rho Relator) (du Position) (c Position))
        (and (founds e rho d)
             (duty du) (bearer du x) (cnt du a t) (part-of du rho)
             (right c) (bearer c y)  (cnt c  a t) (part-of c rho))))))

; ax_unique_founding
(assert (forall ((r Rule) (e Event) (rho1 Relator) (rho2 Relator))
  (=> (and (founds e rho1 r) (founds e rho2 r)) (= rho1 rho2))))

; ax_unique_event
(assert (forall ((r Rule) (e1 Event) (e2 Event) (rho Relator))
  (=> (and (founds e1 rho r) (founds e2 rho r)) (= e1 e2))))

; ax_unique_founding_rem
(assert (forall ((r Rule) (e Event) (rho1 Relator) (rho2 Relator))
  (=> (and (founds-rem e rho1 r) (founds-rem e rho2 r))
      (= rho1 rho2))))

; ax_unique_event_rem
(assert (forall ((r Rule) (e1 Event) (e2 Event) (rho Relator))
  (=> (and (founds-rem e1 rho r) (founds-rem e2 rho r)) (= e1 e2))))

; ax_unique_founding_imm
(assert (forall ((r Rule) (e Event) (rho1 Relator) (rho2 Relator))
  (=> (and (founds-imm e rho1 r) (founds-imm e rho2 r))
      (= rho1 rho2))))

; ax_unique_event_imm
(assert (forall ((r Rule) (e1 Event) (e2 Event) (rho Relator))
  (=> (and (founds-imm e1 rho r) (founds-imm e2 rho r)) (= e1 e2))))

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

; ax_correlativity_permission
(assert (forall ((rho Relator) (a NormContent) (t Target))
  (=> (odrl-rel rho)
      (= (exists ((l Position))
           (and (permission l) (part-of l rho) (cnt l a t)
                (forall ((l2 Position))
                  (=> (and (permission l2) (part-of l2 rho) (cnt l2 a t))
                      (= l2 l)))))
         (exists ((n Position))
           (and (no-right n) (part-of n rho) (cnt n a t)
                (forall ((m Position))
                  (=> (and (no-right m) (part-of m rho) (cnt m a t))
                      (= m n)))))))))

; ax_correlativity_duty
(assert (forall ((rho Relator) (a NormContent) (t Target))
  (=> (odrl-rel rho)
      (= (exists ((d Position))
           (and (duty d) (part-of d rho) (cnt d a t)
                (forall ((d2 Position))
                  (=> (and (duty d2) (part-of d2 rho) (cnt d2 a t))
                      (= d2 d)))))
         (exists ((c Position))
           (and (right c) (part-of c rho) (cnt c a t)
                (forall ((k Position))
                  (=> (and (right k) (part-of k rho) (cnt k a t))
                      (= k c)))))))))

; ax_correlativity_power
(assert (forall ((rho Relator) (a NormContent) (t Target))
  (=> (odrl-rel rho)
      (= (exists ((pw Position))
           (and (power pw) (part-of pw rho) (cnt pw a t)
                (forall ((pw2 Position))
                  (=> (and (power pw2) (part-of pw2 rho) (cnt pw2 a t))
                      (= pw2 pw)))))
         (exists ((s Position))
           (and (subjection s) (part-of s rho) (cnt s a t)
                (forall ((s2 Position))
                  (=> (and (subjection s2) (part-of s2 rho) (cnt s2 a t))
                      (= s2 s)))))))))

; ax_correlativity_immunity
(assert (forall ((rho Relator) (a NormContent) (t Target))
  (=> (odrl-rel rho)
      (= (exists ((im Position))
           (and (immunity im) (part-of im rho) (cnt im a t)
                (forall ((im2 Position))
                  (=> (and (immunity im2) (part-of im2 rho) (cnt im2 a t))
                      (= im2 im)))))
         (exists ((db Position))
           (and (disability db) (part-of db rho) (cnt db a t)
                (forall ((db2 Position))
                  (=> (and (disability db2) (part-of db2 rho) (cnt db2 a t))
                      (= db2 db)))))))))

; ax_cross_relator
; Z3 accepts `false` as Bool term in (=> P false); equivalent to (not P)
(assert (forall ((l Position) (d Position) (x Agent) (a NormContent) (t Target))
  (=> (and (permission l) (bearer l x) (cnt l a t)
           (duty d)       (bearer d x) (cnt d (rfr a) t))
      false)))

; ax_conflict
; Z3 accepts `false` as Bool term in (=> P false); equivalent to (not P)
(assert (forall ((rho Relator) (l Position) (d Position)
                 (x Agent) (a NormContent) (t Target))
  (=> (and (part-of l rho) (part-of d rho)
           (permission l) (duty d)
           (bearer l x) (bearer d x)
           (cnt l a t) (cnt d (rfr a) t))
      false)))

; ax_disability_block
(assert (forall ((f Rule) (x Agent) (y Agent) (a NormContent) (t Target))
  (=> (and (proh f) (aee f x) (aer f y) (act f a) (tgt f t))
      (not (exists ((db Position))
             (and (disability db) (bearer db y) (cnt db a t)))))))

; ax_odrl_rel_is_rel
(assert (forall ((rho Relator))
  (=> (odrl-rel rho) (legal-relator rho))))

; ax_A1
(assert (forall ((x Agent) (a NormContent) (t Target) (q NormPos))
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
(assert (forall ((f Rule) (x Agent) (a NormContent) (t Target))
  (=> (and (proh f) (has-rem f) (act f a) (tgt f t) (aee f x) (does x a t))
      (exists ((b NormContent))
        (and (rem-act f b) (norm-state-change x b t duty-rem))))))

; ax_B2
(assert (forall ((pw Position) (a NormContent) (t Target)
                 (rho Relator) (e Event) (r Rule))
  (=> (and (power pw) (cnt pw (decl a) t) (part-of pw rho) (founds-rem e rho r))
      (about-event pw e))))

; ax_B3
(assert (forall ((s Position) (a NormContent) (t Target)
                 (rho Relator) (e Event) (r Rule))
  (=> (and (subjection s) (cnt s (decl a) t) (part-of s rho) (founds-rem e rho r))
      (about-event s e))))

; === Ground instance (gamma) ===
(declare-const im          Position)
(declare-const rho1        Relator)
(declare-const some-action NormContent)
(declare-const some-target Target)
(assert (immunity im)) (assert (part-of im rho1))
(assert (cnt im some-action some-target))
(assert (odrl-rel rho1))
; im is the unique immunity in rho1 — triggers exists-unique antecedent
(assert (forall ((im2 Position))
  (=> (and (immunity im2) (part-of im2 rho1) (cnt im2 some-action some-target))
      (= im2 im))))

; === Negated conjecture ===
(assert (not
  (exists ((db Position))
    (and (disability db) (part-of db rho1) (cnt db some-action some-target)
         (forall ((db2 Position))
           (=> (and (disability db2) (part-of db2 rho1)
                    (cnt db2 some-action some-target))
               (= db2 db)))))))

(check-sat)