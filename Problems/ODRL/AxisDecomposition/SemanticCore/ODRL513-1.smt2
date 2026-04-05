; ODRL513 — def:profile well-formedness (iii) — gt at effective upper bound yields empty denotation
(set-logic QF_LRA)
(declare-const x Real)
(assert (> x 600.0))
(assert (<= x 600.0))
(check-sat)
