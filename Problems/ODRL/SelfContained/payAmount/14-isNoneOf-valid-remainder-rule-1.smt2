; ============================================================================
; SMT-LIB2 Benchmark: ODRL Policy Conflict Detection
; ============================================================================
; Source:     14_isNoneOf_valid_remainder.ttl
; Policy:     http://example.org/policy01
; Rule:       rule_1
; Category:   payAmount (self-contained, Stage 1)
; Expected:   sat
; Domain:     ODRL policy reasoning (temporal/numeric constraints)
; Logic:      QF_LIA (Quantifier-Free Linear Integer Arithmetic)
; Status:     sat
; Generator:  odrl-z3-reasoner v1.0
; Date:       2026-02-17
; ============================================================================

; benchmark generated from python API
(set-info :status unknown)
(declare-fun payAmount_EUR_default () Real)
(assert
 (let (($x31 (and (and (distinct 25.0 payAmount_EUR_default) true) (and (distinct 75.0 payAmount_EUR_default) true))))
 (and $x31 (<= 50.0 payAmount_EUR_default) (>= 100.0 payAmount_EUR_default))))
(assert
 (>= payAmount_EUR_default 0.0))
(check-sat)
