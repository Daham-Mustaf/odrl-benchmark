; ============================================================================
; SMT-LIB2 Benchmark: ODRL Policy Conflict Detection
; ============================================================================
; Source:     percentage_conflict.ttl
; Policy:     http://example.org/policy
; Rule:       rule_1
; Category:   percentage (self-contained, Stage 1)
; Expected:   unsat
; Domain:     ODRL policy reasoning (temporal/numeric constraints)
; Logic:      QF_LIA (Quantifier-Free Linear Integer Arithmetic)
; Status:     unsat
; Generator:  odrl-z3-reasoner v1.0
; Date:       2026-02-17
; ============================================================================

; benchmark generated from python API
(set-info :status unknown)
(declare-fun percentage_default_default () Real)
(assert
 (and (>= 30.0 percentage_default_default) (<= 50.0 percentage_default_default)))
(assert
 (>= percentage_default_default 0.0))
(assert
 (<= percentage_default_default 100.0))
(check-sat)
