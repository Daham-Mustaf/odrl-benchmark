; --------------------------------------------------------------------------
; File     : ODRL351-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : BSB 3D: width conflict × height+depth compatible → box Conflict
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL351-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: Box3D  Difficulty: Medium
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(declare-const z Real)
(assert (> x 0.0)) (assert (<= x 600.0))  (assert (>= x 1200.0))
(assert (> y 0.0)) (assert (<= y 600.0))  (assert (>= y 400.0))
(assert (> z 0.0)) (assert (<= z 32.0))   (assert (>= z 8.0))
(check-sat)
(exit)
