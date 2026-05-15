; ODRL512 — def:profile (ii) — lt at domain lower bound yields empty denotation
(set-logic QF_LRA)
(declare-const x Real)
(assert (> x 0.0))
(assert (< x 0.0))
(check-sat)
