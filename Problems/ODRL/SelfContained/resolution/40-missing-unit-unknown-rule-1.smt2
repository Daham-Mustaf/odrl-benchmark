; ============================================================================
; SMT-LIB2 Benchmark: ODRL Policy Conflict Detection
; ============================================================================
; Source:     40_missing_unit_unknown.ttl
; Policy:     http://example.org/policy01
; Rule:       rule_1
; Category:   resolution (self-contained, Stage 1)
; Expected:   unsat
; Domain:     ODRL policy reasoning (temporal/numeric constraints)
; Logic:      QF_LIA (Quantifier-Free Linear Integer Arithmetic)
; Status:     unsat
; Generator:  odrl-z3-reasoner v1.0
; Date:       2026-02-17
; ============================================================================

; benchmark generated from python API
(set-info :status unknown)
(declare-fun resolution_default_default () Real)
(assert
 (and (>= 300.0 resolution_default_default) (<= 600.0 resolution_default_default)))
(assert
 (> resolution_default_default 0.0))
(check-sat)
