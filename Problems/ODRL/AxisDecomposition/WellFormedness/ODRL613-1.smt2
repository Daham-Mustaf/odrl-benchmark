; --------------------------------------------------------------------------
; File     : ODRL613-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : wf_lt: V strictly above InfD is well-formed
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL613-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: WellFormedness  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const v Real)
; Pin-witness: v=600 outside-domain-or-equal-InfD => negation of wf_lt.
; Three disjuncts: v<0, v>1200, v=0.  All false at v=600 => unsat.
(assert (= v 600.0))
(assert (or (< v 0.0) (> v 1200.0) (= v 0.0)))
(check-sat)
(exit)
