; --------------------------------------------------------------------------
; File     : NFV001-SAT+1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Problem  : SAT companion for NFV001 — axis_conflict consistency
; Version  : 1.0
; Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
; Source   : Mustafa, D. (2026)
; Authors  : Mustafa, D. & Sutcliffe, G.
; Names    : NFV001-SAT+1.smt2
; Status   : sat
; Comments : axis_conflict encoded as interval disjointness: max(a1,a2) < min(b1,b2)
;          : or max(b1,b2) < min(a1,a2). Here: [n0,n5] and [n10,n15] disjoint via n5<n10.
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(set-info :status sat)
(declare-const n0  Real)
(declare-const n5  Real)
(declare-const n10 Real)
(declare-const n15 Real)
(assert (< n0  n5))
(assert (< n5  n10))
(assert (< n10 n15))
; axis_conflict([n0,n5],[n10,n15]): the intervals are disjoint — witnessed by n5<n10
(assert (< n5 n10))
(check-sat)
(exit)
