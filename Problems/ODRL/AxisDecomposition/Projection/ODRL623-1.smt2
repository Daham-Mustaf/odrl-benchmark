; --------------------------------------------------------------------------
; File     : ODRL623-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : thm:projection 3D: point outside box3 on axis 2
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL623-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: Projection  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(declare-const z Real)
(assert (= x 300.0)) (assert (= y 800.0)) (assert (= z 200.0))
(assert (and (>= x 0.0) (<= x 600.0)
             (>= y 0.0) (<= y 600.0)
             (>= z 0.0) (<= z 600.0)))
(check-sat)
(exit)
