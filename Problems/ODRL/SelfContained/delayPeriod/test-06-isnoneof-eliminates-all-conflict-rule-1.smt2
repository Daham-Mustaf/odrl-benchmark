; ============================================================================
; SMT-LIB2 Benchmark: ODRL Policy Conflict Detection
; ============================================================================
; Source:     test_06_isnoneof_eliminates_all_conflict.ttl
; Policy:     http://example.org/policy_delay_period_06
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
 (let (($x33 (= 5184000.0 delayPeriod_default_default)))
 (let (($x12 (= 2592000.0 delayPeriod_default_default)))
 (let (($x59 (and (and (distinct 2592000.0 delayPeriod_default_default) true) (and (distinct 5184000.0 delayPeriod_default_default) true))))
 (and $x59 (or $x12 $x33))))))
(assert
 (>= delayPeriod_default_default 0.0))
(check-sat)
