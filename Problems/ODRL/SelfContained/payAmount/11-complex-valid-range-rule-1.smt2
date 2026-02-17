; ============================================================================
; SMT-LIB2 Benchmark: ODRL Policy Conflict Detection
; ============================================================================
; Source:     11_complex_valid_range.ttl
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
 (let (($x34 (and (<= 100.0 payAmount_EUR_default) (>= 150.0 payAmount_EUR_default))))
 (let (($x40 (and (<= 50.0 payAmount_EUR_default) (>= 200.0 payAmount_EUR_default))))
 (and $x40 $x34))))
(assert
 (>= payAmount_EUR_default 0.0))
(check-sat)
