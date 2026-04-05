; ODRL505 — lem:normalisation — same-axis lteq intersection reduces to tighter bound
(set-logic QF_LRA)
(declare-const x Real)
(assert (> x 0.0))
(assert (<= x 400.0))
(assert (<= x 600.0))
(check-sat)
