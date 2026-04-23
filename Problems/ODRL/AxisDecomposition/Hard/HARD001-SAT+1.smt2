; --------------------------------------------------------------------------
; File     : HARD001-SAT+1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Problem  : SAT companion for HARD001 — hypothesis set consistency
; Version  : 1.0
; Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
; Source   : Mustafa, D. (2026)
; Authors  : Mustafa, D. & Sutcliffe, G.
; Names    : HARD001-SAT+1.smt2
; Status   : sat
; Comments : Ordering chain n0<n3<n5<n10<n20 with ninf<everything<nsup.
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(set-info :status sat)
(declare-const ninf Real)
(declare-const n0   Real)
(declare-const n3   Real)
(declare-const n5   Real)
(declare-const n10  Real)
(declare-const n20  Real)
(declare-const nsup Real)
(assert (< ninf n0))
(assert (< n0   n3))
(assert (< n3   n5))
(assert (< n5   n10))
(assert (< n10  n20))
(assert (< n20  nsup))
(check-sat)
(exit)
