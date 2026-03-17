; --------------------------------------------------------------------------
; File     : GRND000-0.smt2
; Domain   : Deontic Ontology / ODRL Grounding 
; Problem  : Signature preamble — sorts, functions, rfr/decl axioms
; Version  : 1.1
; English  : SMT-LIB preamble. SMT-LIB has NO include directive.
;            Embedded verbatim at the top of every .smt2 problem file
;            by the problem generators. Do NOT add (check-sat) here.
;
; Source   : Mohammed et al., What Does ODRL Mean? 
; Generated: 2026-03-17 by gen_signature.py
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
; CHANGELOG v1.1:
;   - founds: 2-ary -> 3-ary (Event Relator Rule)
;   - Added odrl-rel predicate
;   - Added strong predicate
;   - Added issue function
; --------------------------------------------------------------------------
(set-logic UF)
(set-info :source |Mohammed et al., What Does ODRL Mean? |)
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
(declare-fun obl     (Rule) Bool)     ; CANONICAL — paper Ax5.4
(declare-fun has-rem (Rule) Bool)     ; CANONICAL — paper Ax5.7
(declare-fun strong  (Rule) Bool)     ; Profile extension; not in ODRL 2.2
                                      ; Asserted as unit clause in GRND002-strong

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
(declare-fun cnt     (Position Action      Target)   Bool)  ; action content
(declare-fun cnt-f   (Position Forbearance Target)   Bool)  ; forbearance content

; odrl-rel: relator founded by an ODRL rule activation.
; Subset of Relator. Required for ax:correlativity and ax:odrl-rel-typing.
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
;
; RFR1 (rfr(a) != a) holds automatically — Action and Forbearance are
;   distinct sorts in SMT-LIB; rfr(a) : Forbearance cannot equal a : Action.
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
