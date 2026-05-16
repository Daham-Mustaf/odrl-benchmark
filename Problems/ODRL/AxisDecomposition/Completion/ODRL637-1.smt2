; --------------------------------------------------------------------------
; File     : ODRL637-1.smt2
; Domain   : ODRL Policy / Axis Decomposition
; Axioms   : completion_conflict requires strict U<V: U=V gives no conflict
; Version  : 1.0
; Authors  : Mustafa, D. & Sutcliffe, G.
; Refs     : [Mus+26b] Mustafa, D., et al. Axis Decomposition for ODRL: Resolving Dimensional Ambiguity in Policy Constraints through Interval Semantics. ISWC 2026 (submitted).
; Source   : Mustafa, D. (2026)
; Names    : ODRL637-1.smt2
; Status   : unsat
; Comments : Verdict: Compatible  Category: Completion  Difficulty: Easy
; --------------------------------------------------------------------------

(set-logic QF_LRA)
(declare-const u Real)
; Arithmetic embodiment of the strict-less requirement: u cannot be both
; equal to 600 and strictly less than 600.  Mirrors the irreflexivity that
; refutes the middle conjunct of completion_conflict_def at U=V.
; SMT counterpart of the FOL claim ~completion_conflict(v600, v600, v0, v1200).
; By completion_conflict_def, that FOL claim reduces to ~less(v600, v600).
; QF_LRA's built-in irreflexivity of < on the reals gives the same fact:
; u = 600 AND u < 600 is unsat.  The two decision procedures take
; different paths to the same conclusion.
(assert (= u 600.0))
(assert (< u 600.0))
(check-sat)
(exit)
