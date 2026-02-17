; ============================================================================
; SMT-LIB2 Benchmark: ODRL Policy Conflict Detection
; ============================================================================
; Source:     test_20_complex_nested_valid.ttl
; Policy:     http://example.org/policy_elapsed_time_20
; Rule:       rule_1
; Category:   elapsedTime (self-contained, Stage 1)
; Expected:   sat
; Domain:     ODRL policy reasoning (temporal/numeric constraints)
; Logic:      QF_LIA (Quantifier-Free Linear Integer Arithmetic)
; Status:     sat
; Generator:  odrl-z3-reasoner v1.0
; Date:       2026-02-17
; ============================================================================

; benchmark generated from python API
(set-info :status unknown)
(declare-fun elapsedTime_default_default () Real)
(assert
 (let (($x12 (and (<= 1800.0 elapsedTime_default_default) (>= 7200.0 elapsedTime_default_default))))
 (and (or $x12 (<= 14400.0 elapsedTime_default_default)) (>= 21600.0 elapsedTime_default_default))))
(assert
 (> elapsedTime_default_default 0.0))
(check-sat)
