; ODRL506 — lem:normalisation — conflicting same-axis constraints yield empty denotation
(set-logic QF_LRA)
(declare-const x Real)
(assert (> x 0.0))
(assert (<= x 200.0))
(assert (>= x 400.0))
(check-sat)
