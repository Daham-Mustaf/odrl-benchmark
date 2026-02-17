; ============================================================================
; SMT-LIB2 Benchmark: ODRL Policy Conflict Detection
; ============================================================================
; Source:     dt_or_trivial.ttl
; Policy:     http://example.org/policy_dt_or_trivial
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
 (or (<= 0 dateTime_default_default) (>= 4102444800 dateTime_default_default)))
(check-sat)
