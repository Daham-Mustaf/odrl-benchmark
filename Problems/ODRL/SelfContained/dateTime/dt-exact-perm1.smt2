; ============================================================================
; SMT-LIB2 Benchmark: ODRL Policy Conflict Detection
; ============================================================================
; Source:     dt_exact.ttl
; Policy:     http://example.org/policy
; Rule:       perm1
; Category:   dateTime (self-contained, Stage 1)
; Expected:   sat
; Domain:     ODRL policy reasoning (temporal/numeric constraints)
; Logic:      QF_LIA (Quantifier-Free Linear Integer Arithmetic)
; Status:     sat
; Generator:  odrl-z3-reasoner v1.0
; Date:       2026-02-17
; ============================================================================

; benchmark generated from python API
(set-info :status unknown)
(declare-fun dateTime_default_default () Int)
(assert
 (= 1718452800 dateTime_default_default))
(check-sat)
