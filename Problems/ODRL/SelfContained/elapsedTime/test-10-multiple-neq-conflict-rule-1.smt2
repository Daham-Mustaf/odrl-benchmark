; ============================================================================
; SMT-LIB2 Benchmark: ODRL Policy Conflict Detection
; ============================================================================
; Source:     test_10_multiple_neq_conflict.ttl
; Policy:     http://example.org/policy_elapsed_time_10
; Rule:       rule_1
; Category:   elapsedTime (self-contained, Stage 1)
; Expected:   unsat
; Domain:     ODRL policy reasoning (temporal/numeric constraints)
; Logic:      QF_LIA (Quantifier-Free Linear Integer Arithmetic)
; Status:     unsat
; Generator:  odrl-z3-reasoner v1.0
; Date:       2026-02-17
; ============================================================================

; benchmark generated from python API
(set-info :status unknown)
(declare-fun elapsedTime_default_default () Real)
(assert
 (let (($x15 (= 7200.0 elapsedTime_default_default)))
 (let (($x34 (= 3600.0 elapsedTime_default_default)))
 (and (and (distinct 3600.0 elapsedTime_default_default) true) (and (distinct 7200.0 elapsedTime_default_default) true) (or $x34 $x15)))))
(assert
 (> elapsedTime_default_default 0.0))
(check-sat)
