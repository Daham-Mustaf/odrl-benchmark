; --------------------------------------------------------------------------
; File     : ODRL614-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : wf_lt violation: V=InfD implies not wf(lt)
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL614-1.smt2
; Status   : unsat
; Comments : Verdict: Conflict  Category: WellFormedness  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const v Real)
; Irreflexivity at the value 0: lt at InfD requires V != InfD, but v=0
; here.  Mirrors the FOL conjecture's derivation via wf_lt_def's third
; conjunct V != InfD failing at v=InfD=0.
(assert (= v 0.0))
(assert (< v 0.0))
(check-sat)
(exit)
