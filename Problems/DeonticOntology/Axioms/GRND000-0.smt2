; --------------------------------------------------------------------------
; File     : GRND000-0.smt2
; Domain   : Deontic Ontology / ODRL Grounding 
; Problem  : Signature preamble — sorts, functions, rfr/decl axioms
; Version  : 1.0
; English  : SMT-LIB preamble. SMT-LIB has NO include directive.
;            Embedded verbatim at the top of every .smt2 problem file
;            by the problem generators. Do NOT add (check-sat) here.
;
; Source   : Mohammed et al., What Does ODRL Mean? 
; Generated: 2026-03-10 by gen_signature.py
;
; Correspondence with GRND000-0.ax (FOF):
;   FOF guard predicate agent(X)  <->  (declare-sort Agent 0)
;   FOF perm(R)                   <->  (declare-fun perm (Rule) Bool)
;   FOF fof(rfr_irreflexive,...)  <->  (assert (forall ((a Action)) ...))
;   cnt/3 dual-sort              <->  cnt (Action) + cnt-f (Forbearance)
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
(declare-fun obl     (Rule) Bool)   ; CANONICAL — paper Ax5.4 uses ODRLDuty, must change to obl
(declare-fun has-rem (Rule) Bool)   ; CANONICAL — paper Ax5.7 uses rem, must change to has-rem

(declare-fun aee (Rule Agent)  Bool)
(declare-fun aer (Rule Agent)  Bool)
(declare-fun act (Rule Action) Bool)
(declare-fun tgt (Rule Target) Bool)

(declare-fun activates (Event Rule) Bool)


; --------------------------------------------------------------------------
; UFO RELATOR AND POSITION PREDICATES
; --------------------------------------------------------------------------

(declare-fun founds  (Event    Relator)            Bool)
(declare-fun part-of (Position Relator)            Bool)
(declare-fun bearer  (Position Agent)              Bool)
(declare-fun cnt     (Position Action      Target) Bool)  ; action content — CANONICAL
(declare-fun cnt-f   (Position Forbearance Target) Bool)  ; forbearance content
; cnt   = action content (permissions, obligations). Used in Ax5.1 for Liberty/NoRight too.
;         Paper uses about(l,a,t) in Ax5.1 — must be unified to cnt everywhere.
; cnt-f = forbearance content (prohibitions, Ax5.2).
; Two predicates because Action and Forbearance are distinct SMT-LIB sorts.
; In FOF (GRND000-0.ax), a single cnt/3 handles both via type guards.

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
; --------------------------------------------------------------------------

(declare-fun decl (Action) Action)

; DECL2: Injectivity
(assert (forall ((a Action) (b Action))
  (=> (= (decl a) (decl b)) (= a b))))

; DECL3: Distinctness
(assert (forall ((a Action))(not (= (decl a) a))))


; --------------------------------------------------------------------------
; POSITION SORT DISJOINTNESS
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
