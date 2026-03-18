; --------------------------------------------------------------------------
; File     : GRND012-corr-duty-1.smt2
; Domain   : Deontic Ontology / ODRL Grounding
; Problem  : Correlativity: Duty implies unique Claim in relator
; Status   : unsat
; Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
; Policy   : Policies/GRND012-corr-duty-policy.ttl
; Generated: 2026-03-18 by gen_foundation_problems.py v1.4
;
; odrl_rel(rho1), Duty(d) partOf rho1 => exists unique c. Claim(c) partOf rho1.
;
; ODRL Policy (Turtle) — see Policies/ for full file:
; @prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
; @prefix drk:    <http://w3id.org/drk/ontology/> .
; @prefix dcat:   <http://www.w3.org/ns/dcat#> .
; 
; # Correlativity: every Duty in an ODRL relator has a unique correlative Claim.
; # Tested on drk:TheaterShowtimeDataset prohibition relator.
; --------------------------------------------------------------------------

; === Layer 0 + Layer 1 preamble (embedded — SMT-LIB has no include) ===
; === Source: Axioms/Layer0-Signature/GRND000-0.smt2 ===
; --------------------------------------------------------------------------
; File     : GRND000-0.smt2
; Domain   : Deontic Ontology / ODRL Grounding
; Problem  : Signature preamble — sorts, functions, rfr/decl axioms
; Version  : 1.4
; English  : SMT-LIB preamble. SMT-LIB has NO include directive.
;            Embedded verbatim at the top of every .smt2 problem file
;            by the problem generators. Do NOT add (check-sat) here.
;            Import in generators via:
;              from gen_signature import generate_smt2 as _gen_smt2
;              SMT2_PREAMBLE = _gen_smt2()
;
; Source   : Mohammed et al., What Does ODRL Mean? FOIS 2026
; Generated: 2026-03-18 by gen_signature.py
;
; Correspondence with GRND000-0.ax (FOF):
;   FOF guard predicate agent(X)     <->  (declare-sort Agent 0)
;   FOF perm(R)                      <->  (declare-fun perm (Rule) Bool)
;   FOF founds(E,Rho,R) [3-ary]      <->  (declare-fun founds (Event Relator Rule) Bool)
;   FOF cnt/3 (action + forbearance) <->  cnt (Action) + cnt-f (Forbearance)
;                                         Two predicates because Action and
;                                         Forbearance are distinct SMT-LIB sorts.
;   FOF odrl_rel(X)                  <->  (declare-fun odrl-rel (Relator) Bool)
;   FOF strong(R)                    <->  (declare-fun strong (Rule) Bool)
;   FOF issue/1                      <->  (declare-fun issue (Rule) Action)
;
; CHANGELOG v1.4:
;   - version aligned with gen_foundation_problems.py v1.4
;   - trailing whitespace removed from META fields
;   - import path documented in header
; CHANGELOG v1.1:
;   - founds: 2-ary -> 3-ary (Event Relator Rule)
;   - Added odrl-rel predicate
;   - Added strong predicate
;   - Added issue function
; --------------------------------------------------------------------------
(set-logic UF)
(set-info :source |Mohammed et al., What Does ODRL Mean? FOIS 2026|)
(set-info :status unknown)

; --------------------------------------------------------------------------
; SORTS — uninterpreted (closest to FOF guard predicates)
; --------------------------------------------------------------------------
(declare-sort Agent       0)
(declare-sort Action      0)
(declare-sort Forbearance 0)
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
(declare-fun obl     (Rule) Bool)     ; CANONICAL — paper Ax5.6
(declare-fun has-rem (Rule) Bool)     ; CANONICAL — paper Ax5.4
(declare-fun strong  (Rule) Bool)     ; Profile extension; not in ODRL 2.2
(declare-fun aee (Rule Agent)  Bool)
(declare-fun aer (Rule Agent)  Bool)
(declare-fun act (Rule Action) Bool)
(declare-fun tgt (Rule Target) Bool)
(declare-fun activates (Event Rule) Bool)

; --------------------------------------------------------------------------
; UFO RELATOR AND POSITION PREDICATES
; --------------------------------------------------------------------------
; founds: 3-ary — matches paper axioms Ax5.1-Ax5.8
; Third argument (Rule) individuates relator by rule-event pair (Ax5.5).
(declare-fun founds  (Event Relator Rule)            Bool)
(declare-fun part-of (Position Relator)              Bool)
(declare-fun bearer  (Position Agent)                Bool)
; cnt and cnt-f: two predicates because Action and Forbearance are
; distinct SMT-LIB sorts. In FOF (GRND000-0.ax), a single cnt/3
; handles both via action(A)/forbearance(A) type guards.
(declare-fun cnt     (Position Action      Target)   Bool)
(declare-fun cnt-f   (Position Forbearance Target)   Bool)
; odrl-rel: relator founded by an ODRL rule activation.
(declare-fun odrl-rel (Relator) Bool)
; Hohfeldian position type predicates
(declare-fun liberty    (Position) Bool)
(declare-fun no-right   (Position) Bool)
(declare-fun duty       (Position) Bool)
(declare-fun claim      (Position) Bool)
(declare-fun power      (Position) Bool)
(declare-fun subjection (Position) Bool)
(declare-fun immunity   (Position) Bool)
(declare-fun disability (Position) Bool)

; --------------------------------------------------------------------------
; RFR FUNCTION  rfr : Action -> Forbearance
; pos : Forbearance -> Action  (left-inverse of rfr)
; RFR1 holds automatically — Action and Forbearance are distinct sorts.
; RFR4, RFR5 hold by sort separation.
; --------------------------------------------------------------------------
(declare-fun rfr (Action)      Forbearance)
(declare-fun pos (Forbearance) Action)
; RFR2: Injectivity
(assert (forall ((a Action) (b Action))
  (=> (= (rfr a) (rfr b)) (= a b))))
; RFR3: Left-inverse
(assert (forall ((a Action))
  (= (pos (rfr a)) a)))

; --------------------------------------------------------------------------
; DECL FUNCTION  decl : Action -> Action
; decl(A) = institutional act of declaring a violation on action A.
; Used in Ax5.4 (Power-Subjection for remedy).
; --------------------------------------------------------------------------
(declare-fun decl (Action) Action)
; DECL2: Injectivity
(assert (forall ((a Action) (b Action))
  (=> (= (decl a) (decl b)) (= a b))))
; DECL3: Distinctness from base action
(assert (forall ((a Action))
  (not (= (decl a) a))))

; --------------------------------------------------------------------------
; ISSUE FUNCTION  issue : Rule -> Action
; issue(Pi) = institutional act of issuing policy Pi.
; Used in P3-P4 normative hierarchy grounding.
; --------------------------------------------------------------------------
(declare-fun issue (Rule) Action)
; ISSUE2: Injectivity
(assert (forall ((a Rule) (b Rule))
  (=> (= (issue a) (issue b)) (= a b))))

; --------------------------------------------------------------------------
; POSITION SORT DISJOINTNESS
; Grounded in UFO disjointness of moment types.
; --------------------------------------------------------------------------
; Within conduct level
(assert (forall ((p Position)) (not (and (liberty p)  (duty p)))))
(assert (forall ((p Position)) (not (and (liberty p)  (claim p)))))
(assert (forall ((p Position)) (not (and (liberty p)  (no-right p)))))
(assert (forall ((p Position)) (not (and (duty p)     (claim p)))))
(assert (forall ((p Position)) (not (and (duty p)     (no-right p)))))
(assert (forall ((p Position)) (not (and (claim p)    (no-right p)))))
; Within competence level
(assert (forall ((p Position)) (not (and (power p)      (subjection p)))))
(assert (forall ((p Position)) (not (and (power p)      (immunity p)))))
(assert (forall ((p Position)) (not (and (power p)      (disability p)))))
(assert (forall ((p Position)) (not (and (subjection p) (immunity p)))))
(assert (forall ((p Position)) (not (and (subjection p) (disability p)))))
(assert (forall ((p Position)) (not (and (immunity p)   (disability p)))))
; Conduct vs competence
(assert (forall ((p Position)) (not (and (liberty p)  (power p)))))
(assert (forall ((p Position)) (not (and (liberty p)  (subjection p)))))
(assert (forall ((p Position)) (not (and (liberty p)  (immunity p)))))
(assert (forall ((p Position)) (not (and (liberty p)  (disability p)))))
(assert (forall ((p Position)) (not (and (duty p)     (power p)))))
(assert (forall ((p Position)) (not (and (duty p)     (subjection p)))))
(assert (forall ((p Position)) (not (and (duty p)     (immunity p)))))
(assert (forall ((p Position)) (not (and (duty p)     (disability p)))))
(assert (forall ((p Position)) (not (and (claim p)    (power p)))))
(assert (forall ((p Position)) (not (and (claim p)    (subjection p)))))
(assert (forall ((p Position)) (not (and (claim p)    (immunity p)))))
(assert (forall ((p Position)) (not (and (claim p)    (disability p)))))
(assert (forall ((p Position)) (not (and (no-right p) (power p)))))
(assert (forall ((p Position)) (not (and (no-right p) (subjection p)))))
(assert (forall ((p Position)) (not (and (no-right p) (immunity p)))))
(assert (forall ((p Position)) (not (and (no-right p) (disability p)))))
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
(declare-const duty-rem        NormPos)


; === Layer 1: Paper axioms (Ax5.1-5.10, A1-A3, B1-B3) ===
; === Authoritative source: Axioms/Layer1-Deontic/GRND-AX-1.smt2 ===
; === (SMT-LIB has no include directive — axioms embedded directly) ===

; ax_perm_relator_basic
(assert (forall ((p Rule) (x Agent) (y Agent) (a Action) (t Target) (e Event))
  (=> (and (perm p) (aee p x) (aer p y) (act p a) (tgt p t) (activates e p))
      (exists ((rho Relator) (l Position) (n Position))
        (and (founds e rho p)
             (liberty l) (bearer l x) (cnt l a t) (part-of l rho)
             (no-right n) (bearer n y) (cnt n a t) (part-of n rho))))))

; ax_perm_relator_strong
(assert (forall ((p Rule) (x Agent) (y Agent) (a Action) (t Target)
                 (e Event) (rho Relator))
  (=> (and (perm p) (strong p) (aee p x) (aer p y) (act p a) (tgt p t)
           (activates e p) (founds e rho p))
      (exists ((im Position) (db Position))
        (and (immunity im)   (bearer im x) (cnt im a t)  (part-of im rho)
             (disability db) (bearer db y) (cnt db a t)  (part-of db rho))))))

; ax_proh_relator_basic
(assert (forall ((f Rule) (x Agent) (y Agent) (a Action) (t Target) (e Event))
  (=> (and (proh f) (aee f x) (aer f y) (act f a) (tgt f t) (activates e f))
      (exists ((rho Relator) (d Position) (c Position))
        (and (founds e rho f)
             (duty d)  (bearer d x) (cnt-f d (rfr a) t) (part-of d rho)
             (claim c) (bearer c y) (cnt-f c (rfr a) t) (part-of c rho))))))

; ax_proh_relator_remedy
(assert (forall ((f Rule) (x Agent) (y Agent) (a Action) (t Target)
                 (e Event) (rho Relator))
  (=> (and (proh f) (has-rem f) (aee f x) (aer f y) (act f a) (tgt f t)
           (activates e f) (founds e rho f))
      (exists ((pw Position) (s Position))
        (and (power pw)      (bearer pw y) (cnt pw (decl a) t) (part-of pw rho)
             (subjection s)  (bearer s x)  (cnt s  (decl a) t) (part-of s rho))))))

; ax_unique_founding
(assert (forall ((r Rule) (e Event) (rho1 Relator) (rho2 Relator))
  (=> (and (founds e rho1 r) (founds e rho2 r)) (= rho1 rho2))))

; ax_unique_relator_per_event
(assert (forall ((r Rule) (e1 Event) (e2 Event) (rho Relator))
  (=> (and (founds e1 rho r) (founds e2 rho r)) (= e1 e2))))

; ax_obl_relator
(assert (forall ((d Rule) (x Agent) (y Agent) (a Action) (t Target) (e Event))
  (=> (and (obl d) (aee d x) (aer d y) (act d a) (tgt d t) (activates e d))
      (exists ((rho Relator) (du Position) (c Position))
        (and (founds e rho d)
             (duty du) (bearer du x) (cnt du a t)  (part-of du rho)
             (claim c) (bearer c y)  (cnt c  a t)  (part-of c rho))))))

; ax_correlativity_liberty
(assert (forall ((rho Relator) (a Action) (t Target))
  (=> (odrl-rel rho)
      (= (exists ((l Position))
           (and (liberty l) (part-of l rho) (cnt l a t)))
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
           (and (claim c) (part-of c rho) (cnt c a t)
                (forall ((k Position))
                  (=> (and (claim k) (part-of k rho) (cnt k a t))
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
           (liberty l) (duty d)
           (bearer l x) (bearer d x)
           (cnt l a t) (cnt-f d (rfr a) t))
      false)))

; ax_cross_relator_consistency
(assert (forall ((l Position) (d Position) (x Agent) (a Action) (t Target))
  (=> (and (liberty l) (bearer l x) (cnt l a t)
           (duty d)    (bearer d x) (cnt-f d (rfr a) t))
      false)))

; ax_disability_block
(assert (forall ((f Rule) (x Agent) (y Agent) (a Action) (t Target))
  (=> (and (proh f) (aee f x) (aer f y) (act f a) (tgt f t))
      (not (exists ((db Position))
             (and (disability db) (bearer db y) (cnt db a t)))))))

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
        (and (power pw) (bearer pw y) (about-event pw e)
             (subjection s) (bearer s x) (about-event s e))))))

; ax_B1
(assert (forall ((f Rule) (x Agent) (a Action) (t Target) (b Action))
  (=> (and (proh f) (has-rem f) (act f a) (tgt f t) (aee f x) (does x a t))
      (norm-state-change x b t duty-rem))))

; ax_B2
(assert (forall ((pw Position) (a Action) (t Target)
                 (rho Relator) (e Event) (r Rule))
  (=> (and (power pw) (cnt pw (decl a) t) (part-of pw rho) (founds e rho r))
      (about-event pw e))))

; ax_B3
(assert (forall ((s Position) (a Action) (t Target)
                 (rho Relator) (e Event) (r Rule))
  (=> (and (subjection s) (cnt s (decl a) t) (part-of s rho) (founds e rho r))
      (about-event s e))))

; === Ground instance (gamma) ===
(declare-const d           Position)
(declare-const rho1        Relator)
(declare-const some-action Action)
(declare-const some-target Target)
(assert (duty d)) (assert (part-of d rho1))
(assert (cnt d some-action some-target))
(assert (odrl-rel rho1))

; === Negated conjecture ===
(assert (not
  (exists ((c Position))
    (and (claim c) (part-of c rho1) (cnt c some-action some-target)
         (forall ((k Position))
           (=> (and (claim k) (part-of k rho1)
                    (cnt k some-action some-target))
               (= k c)))))))

(check-sat)