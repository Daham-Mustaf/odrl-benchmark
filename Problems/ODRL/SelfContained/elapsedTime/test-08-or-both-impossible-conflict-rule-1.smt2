; ============================================================================
; SMT-LIB2 Benchmark: ODRL Policy Conflict Detection
; ============================================================================
; Source:     test_08_or_both_impossible_conflict.ttl
; Policy:     http://example.org/policy_elapsed_time_08
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
 (or (> 0.0 elapsedTime_default_default) (= 0.0 elapsedTime_default_default)))
(assert
 (> elapsedTime_default_default 0.0))
(check-sat)
