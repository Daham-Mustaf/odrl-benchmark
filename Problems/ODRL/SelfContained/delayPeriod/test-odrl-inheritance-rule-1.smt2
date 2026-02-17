; ============================================================================
; SMT-LIB2 Benchmark: ODRL Policy Conflict Detection
; ============================================================================
; Source:     test_odrl_inheritance.ttl
; Policy:     http://example.org/child_policy_conflicting
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
 (let (($x6 (<= 2592000.0 delayPeriod_default_default)))
 (let (($x32 (>= 604800.0 delayPeriod_default_default)))
 (and $x32 $x6))))
(assert
 (>= delayPeriod_default_default 0.0))
(check-sat)
