; ============================================================================
; SMT-LIB2 Benchmark: ODRL Policy Conflict Detection
; ============================================================================
; Source:     test_14_cue_points_valid.ttl
; Policy:     http://example.org/policy_elapsed_time_14
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
 (let (($x19 (or (= 900.0 elapsedTime_default_default) (= 1800.0 elapsedTime_default_default) (= 2700.0 elapsedTime_default_default))))
 (and $x19 (>= 3600.0 elapsedTime_default_default))))
(assert
 (> elapsedTime_default_default 0.0))
(check-sat)
