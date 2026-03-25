; --------------------------------------------------------------------------
; File     : GRND012-corr-duty-1.smt2
; Domain   : Deontic Ontology / ODRL Grounding
; Problem  : Correlativity: Duty implies unique Right in relator
; Status   : unsat
; Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
; Policy   : Policies/GRND012-corr-duty-policy.ttl
; Generated: 2026-03-22 by gen_foundation_problems.py v1.5
;
; odrl_rel(rho1), Duty(d) partOf rho1 => exists unique c. Right(c) partOf rho1.
;
; ODRL Policy (Turtle) — see Policies/ for full file:
; @prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
; @prefix drk:    <http://w3id.org/drk/ontology/> .
; @prefix dcat:   <http://www.w3.org/ns/dcat#> .
; # Correlativity: every Duty in an ODRL relator has a unique correlative Right.
; # Tested on drk:TheaterShowtimeDataset prohibition relator.
; --------------------------------------------------------------------------

; === Layer 0 + Layer 1 preamble (embedded — SMT-LIB has no include) ===
; === Source: Axioms/Layer0-Signature/GRND000-0.smt2 ===
; --------------------------------------------------------------------------
; File     : GRND000-0.smt2
; Domain   : Deontic Ontology / ODRL Grounding
; Problem  : Signature preamble — sorts, functions, rfr/decl axioms
; Version  : 1.5
; English  : SMT-LIB preamble embedded verbatim into every .smt2 file.
;            Do NOT add (check-sat) here.
;            Import via:
;              from gen_layer1_deontic import generate_smt2 as _gen_smt2
;              SMT2_PREAMBLE = _gen_smt2()
;
; Source   : Mohammed et al., What Does ODRL Mean? FOIS 2026
; Generated: 2026-03-22 by gen_layer1_deontic.py
;
; Key design decisions:
;   NormContent (Issue 1): replaces separate Action + Forbearance sorts.
;     rfr : NormContent -> NormContent. cnt : (Position NormContent Target).
;     cnt-f removed. rfr_distinctness (rfr(a)!=a) carries the
;     act/forbearance distinction instead of separate sort disjointness.
;   permission/right (Issue 2): UFO-L terms replace liberty/claim.
;   founds-rem, founds-imm (Issue 3): declared here alongside founds.
;
; CHANGELOG v1.5:
;   - Issue 1: NormContent sort; cnt unified; cnt-f removed.
;   - Issue 2: liberty->permission, claim->right.
;   - Issue 3: founds-rem and founds-imm in SMT2_RELATOR_PREDICATES.
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
;
; Three founding predicates for three kinds of simple legal relator:
;   founds     — conduct relator (Duty-Right or Permission-NoRight)
;   founds-rem — competence relator rho_R for prohibition+remedy (Ax5.4)
;   founds-imm — competence relator rho_I for strong permission (Ax5.2)
; Unique Founding applies independently within each predicate.
;
; cnt: single predicate (Position NormContent Target).
;   rfr(a) and a are distinct NormContent values (rfr_distinctness).
;   cnt-f is removed entirely.
;
; UFO-L position terms (Issue 2): permission/right replace liberty/claim.
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
; pos = left-inverse of rfr.
; rfr_distinctness replaces the sort-level guarantee that formerly held
; when Action and Forbearance were distinct sorts.
; --------------------------------------------------------------------------
(declare-fun rfr (NormContent) NormContent)
(declare-fun pos (NormContent) NormContent)
; Injectivity
(assert (forall ((a NormContent) (b NormContent))
  (=> (= (rfr a) (rfr b)) (= a b))))
; Left-inverse
(assert (forall ((a NormContent))
  (= (pos (rfr a)) a)))
; Distinctness: rfr(a) != a
(assert (forall ((a NormContent))
  (not (= (rfr a) a))))

; --------------------------------------------------------------------------
; DECL FUNCTION  decl : NormContent -> NormContent
; decl(a) = institutional act of declaring a violation on action a.
; --------------------------------------------------------------------------
(declare-fun decl (NormContent) NormContent)
; Injectivity
(assert (forall ((a NormContent) (b NormContent))
  (=> (= (decl a) (decl b)) (= a b))))
; Distinctness from base content
(assert (forall ((a NormContent))
  (not (= (decl a) a))))

; --------------------------------------------------------------------------
; ISSUE FUNCTION  issue : Rule -> NormContent
; --------------------------------------------------------------------------
(declare-fun issue (Rule) NormContent)
; Injectivity
(assert (forall ((a Rule) (b Rule))
  (=> (= (issue a) (issue b)) (= a b))))

; --------------------------------------------------------------------------
; POSITION SORT DISJOINTNESS (UFO-L terms)
; --------------------------------------------------------------------------
; Within conduct level
(assert (forall ((p Position)) (not (and (permission p) (duty p)))))
(assert (forall ((p Position)) (not (and (permission p) (right p)))))
(assert (forall ((p Position)) (not (and (permission p) (no-right p)))))
(assert (forall ((p Position)) (not (and (duty p)       (right p)))))
(assert (forall ((p Position)) (not (and (duty p)       (no-right p)))))
(assert (forall ((p Position)) (not (and (right p)      (no-right p)))))
; Within competence level
(assert (forall ((p Position)) (not (and (power p)      (subjection p)))))
(assert (forall ((p Position)) (not (and (power p)      (immunity p)))))
(assert (forall ((p Position)) (not (and (power p)      (disability p)))))
(assert (forall ((p Position)) (not (and (subjection p) (immunity p)))))
(assert (forall ((p Position)) (not (and (subjection p) (disability p)))))
(assert (forall ((p Position)) (not (and (immunity p)   (disability p)))))
; Conduct vs competence (16 pairs)
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
; --------------------------------------------------------------------------
; END OF PREAMBLE — problem files append axioms + conjecture after this
; --------------------------------------------------------------------------

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


; === Layer 1: Paper axioms (Ax5.1-5.11, A1-A3, B1-B3) ===
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
(declare-const d           Position)
(declare-const rho1        Relator)
(declare-const some-action NormContent)
(declare-const some-target Target)
(assert (duty d)) (assert (part-of d rho1))
(assert (cnt d some-action some-target))
(assert (odrl-rel rho1))

; === Negated conjecture ===
(assert (not
  (exists ((c Position))
    (and (right c) (part-of c rho1) (cnt c some-action some-target)
         (forall ((k Position))
           (=> (and (right k) (part-of k rho1)
                    (cnt k some-action some-target))
               (= k c)))))))

(check-sat)