; --------------------------------------------------------------------------
; File     : ODRL663-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : prec_oo at strict less: less(a,b) implies prec(a,b,o,o)
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL663-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: ConflictCriterion  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const x Real)
(assert (> x 0.0))
(assert (< x 500.0))     ; sem(lt 500)
(assert (> x 600.0))     ; sem(gt 600)
(check-sat)
(exit)
