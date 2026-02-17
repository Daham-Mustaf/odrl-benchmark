; ============================================================================
; SMT-LIB2 Benchmark: ODRL Policy Conflict Detection
; ============================================================================
; Source:     03_isAnyOf_range_conflict.ttl
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
 (let (($x31 (or (= 10.0 payAmount_EUR_default) (= 20.0 payAmount_EUR_default) (= 30.0 payAmount_EUR_default))))
 (and $x31 (< 100.0 payAmount_EUR_default))))
(assert
 (>= payAmount_EUR_default 0.0))
(check-sat)
