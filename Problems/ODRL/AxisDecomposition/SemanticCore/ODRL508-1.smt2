; ODRL508 — thm:aabb — closed bounded interval is non-empty
(set-logic QF_LRA)
(declare-const x Real)
(assert (>= x 200.0))
(assert (<= x 400.0))
(check-sat)
