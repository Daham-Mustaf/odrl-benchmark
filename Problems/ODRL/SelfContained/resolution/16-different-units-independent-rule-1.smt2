; ============================================================================
; SMT-LIB2 Benchmark: ODRL Policy Conflict Detection
; ============================================================================
; Source:     16_different_units_independent.ttl
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
(declare-fun resolution_PPI_default () Real)
(declare-fun resolution_DPI_default () Real)
(assert
 (and (>= 300.0 resolution_DPI_default) (<= 600.0 resolution_PPI_default)))
(assert
 (> resolution_DPI_default 0.0))
(assert
 (> resolution_PPI_default 0.0))
(check-sat)
