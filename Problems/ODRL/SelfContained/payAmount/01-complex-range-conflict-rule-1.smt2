; ============================================================================
; SMT-LIB2 Benchmark: ODRL Policy Conflict Detection
; ============================================================================
; Source:     01_complex_range_conflict.ttl
; Policy:     http://example.org/policy01
; Rule:       rule_1
; Category:   payAmount (self-contained, Stage 1)
; Expected:   unsat
; Domain:     ODRL policy reasoning (temporal/numeric constraints)
; Logic:      QF_LIA (Quantifier-Free Linear Integer Arithmetic)
; Status:     unsat
; Generator:  odrl-z3-reasoner v1.0
; Date:       2026-02-17
; ============================================================================

; benchmark generated from python API
(set-info :status unknown)
(declare-fun payAmount_EUR_default () Real)
(assert
 (let (($x35 (and (<= 300.0 payAmount_EUR_default) (>= 400.0 payAmount_EUR_default))))
 (let (($x32 (and (<= 100.0 payAmount_EUR_default) (>= 200.0 payAmount_EUR_default))))
 (and $x32 $x35))))
(assert
 (>= payAmount_EUR_default 0.0))
(check-sat)
