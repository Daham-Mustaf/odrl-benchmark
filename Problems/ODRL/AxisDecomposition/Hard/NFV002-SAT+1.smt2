; --------------------------------------------------------------------------
; File     : NFV002-SAT+1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Problem  : SAT companion for NFV002 — axis_compatible consistency
; Version  : 1.0
; Refs     : [Mus+26] Mustafa, D., et al. arXiv:2602.19878.
; Source   : Mustafa, D. (2026)
; Authors  : Mustafa, D. & Sutcliffe, G.
; Names    : NFV002-SAT+1.smt2
; Status   : sat
; Comments : axis_compatible([n0,n10],[n5,n10]) — witness X with n0<=X<=n10 AND n5<=X<=n10
;          : i.e. max(n0,n5) <= X <= min(n10,n10). Ordering n0<n5<n10 gives X in [n5,n10].
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(set-info :status sat)
(declare-const n0  Real)
(declare-const n5  Real)
(declare-const n10 Real)
(declare-const x   Real)
(assert (< n0 n5))
(assert (< n5 n10))
; axis_compatible([n0,n10],[n5,n10]): witness X in the intersection [n5,n10]
(assert (and (<= n0 x) (<= x n10)))
(assert (and (<= n5 x) (<= x n10)))
(check-sat)
(exit)
