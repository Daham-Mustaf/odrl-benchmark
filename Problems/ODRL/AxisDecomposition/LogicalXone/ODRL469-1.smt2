; --------------------------------------------------------------------------
; File     : ODRL469-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : xone-A vs or-B: ~A_x & A_y branch with B satisfied → Compatible
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL469-1.smt2
; Status   : sat
; Comments : Verdict: Compatible  Category: LogicalXone  Difficulty: Medium
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(assert (> x 0.0)) (assert (> y 0.0))
(assert (or (and (<= x 600.0) (not (<= y 400.0)))
            (and (not (<= x 600.0)) (<= y 400.0))))
(assert (or (>= x 800.0) (>= y 200.0)))
(check-sat)
(exit)
