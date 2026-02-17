; ============================================================================
; SMT-LIB2 Benchmark: ODRL Policy Conflict Detection
; ============================================================================
; Source:     14_isAllOf_identical_compatible.ttl
; Policy:     http://example.org/policy01
; Rule:       rule_1
; Category:   resolution (self-contained, Stage 1)
; Expected:   sat
; Domain:     ODRL policy reasoning (temporal/numeric constraints)
; Logic:      QF_LIA (Quantifier-Free Linear Integer Arithmetic)
; Status:     sat
; Generator:  odrl-z3-reasoner v1.0
; Date:       2026-02-17
; ============================================================================

; benchmark generated from python API
(set-info :status unknown)
(declare-fun resolution_DPI_default () Real)
(assert
 (and (= 300.0 resolution_DPI_default) (<= 150.0 resolution_DPI_default)))
(assert
 (> resolution_DPI_default 0.0))
(check-sat)
