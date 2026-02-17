; ============================================================================
; SMT-LIB2 Benchmark: ODRL Policy Conflict Detection
; ============================================================================
; Source:     test_05_isanyof_range_conflict.ttl
; Policy:     http://example.org/policy_delay_period_05
; Rule:       rule_1
; Category:   delayPeriod (self-contained, Stage 1)
; Expected:   unsat
; Domain:     ODRL policy reasoning (temporal/numeric constraints)
; Logic:      QF_LIA (Quantifier-Free Linear Integer Arithmetic)
; Status:     unsat
; Generator:  odrl-z3-reasoner v1.0
; Date:       2026-02-17
; ============================================================================

; benchmark generated from python API
(set-info :status unknown)
(declare-fun delayPeriod_default_default () Real)
(assert
 (let (($x6 (or (= 604800.0 delayPeriod_default_default) (= 1209600.0 delayPeriod_default_default) (= 2592000.0 delayPeriod_default_default))))
 (and $x6 (< 5184000.0 delayPeriod_default_default))))
(assert
 (>= delayPeriod_default_default 0.0))
(check-sat)
