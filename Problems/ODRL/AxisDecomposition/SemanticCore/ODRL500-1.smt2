; ODRL500 — lem:totality — lteq denotation is non-empty
(set-logic QF_LRA)
(declare-const x Real)
(assert (> x 0.0))
(assert (<= x 600.0))
(check-sat)
