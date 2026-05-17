; --------------------------------------------------------------------------
; File     : ODRL507-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : thm:projection -- box <=> per-axis membership (concrete instance)
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL507-1.smt2
; Status   : unsat
; Comments : Verdict: Compatible  Category: SemanticCore  Difficulty: Medium
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(assert (= x 200.0)) (assert (= y 200.0))
; box membership: x in [0,600], y in [0,400]
; per-axis:       x in [0,600] AND y in [0,400] (identical bounds)
; negation of iff: box_mem != per_axis_mem -- empty at (200, 200)
(assert (not
  (= (and (>= x 0.0) (<= x 600.0) (>= y 0.0) (<= y 400.0))
     (and (and (>= x 0.0) (<= x 600.0))
          (and (>= y 0.0) (<= y 400.0))))))
(check-sat)
(exit)
