(set-logic QF_LRA)
(declare-const n0 Real)
(declare-const n3 Real)
(declare-const n5 Real)
(declare-const n10 Real)
(declare-const n20 Real)
; ordering chain n0 < n3 < n5 < n10 < n20
(assert (< n0 n3))
(assert (< n3 n5))
(assert (< n5 n10))
(assert (< n10 n20))
; should be satisfiable
(check-sat)
(exit)
