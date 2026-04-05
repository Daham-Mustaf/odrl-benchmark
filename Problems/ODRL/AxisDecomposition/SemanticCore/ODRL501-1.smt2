; ODRL501 — lem:totality — gteq denotation is non-empty
(set-logic QF_LRA)
(declare-const x Real)
(assert (>= x 200.0))
(check-sat)
