; ============================================================================
; SMT-LIB2 Benchmark: ODRL Policy Conflict Detection
; ============================================================================
; Source:     test_16_xone_disjoint_valid.ttl
; Policy:     http://example.org/policy_delay_period_16
; Rule:       rule_1
; Category:   delayPeriod (self-contained, Stage 1)
; Expected:   sat
; Domain:     ODRL policy reasoning (temporal/numeric constraints)
; Logic:      QF_LIA (Quantifier-Free Linear Integer Arithmetic)
; Status:     sat
; Generator:  odrl-z3-reasoner v1.0
; Date:       2026-02-17
; ============================================================================

; benchmark generated from python API
(set-info :status unknown)
(declare-fun delayPeriod_default_default () Real)
(assert
 (let (($x15 (<= 2592000.0 delayPeriod_default_default)))
 (let (($x32 (>= 604800.0 delayPeriod_default_default)))
 (and (or $x32 $x15) (and (not (and $x32 $x15)))))))
(assert
 (>= delayPeriod_default_default 0.0))
(check-sat)
