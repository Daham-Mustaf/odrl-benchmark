; ============================================================================
; SMT-LIB2 Benchmark: ODRL Policy Conflict Detection
; ============================================================================
; Source:     policy_duty.ttl
; Policy:     http://example.org/policy3
; Rule:       rule_1
; Category:   percentage (self-contained, Stage 1)
; Expected:   sat
; Domain:     ODRL policy reasoning (temporal/numeric constraints)
; Logic:      QF_LIA (Quantifier-Free Linear Integer Arithmetic)
; Status:     sat
; Generator:  odrl-z3-reasoner v1.0
; Date:       2026-02-17
; ============================================================================

; benchmark generated from python API
(set-info :status unknown)
(declare-fun count_default_default () Int)
(assert
 (>= 3 count_default_default))
(assert
 (>= count_default_default 0))
(check-sat)
