; ============================================================================
; SMT-LIB2 Benchmark: ODRL Policy Conflict Detection
; ============================================================================
; Source:     dt_conflict.ttl
; Policy:     http://example.org/policy
; Rule:       perm1
; Category:   dateTime (self-contained, Stage 1)
; Expected:   unsat
; Domain:     ODRL policy reasoning (temporal/numeric constraints)
; Logic:      QF_LIA (Quantifier-Free Linear Integer Arithmetic)
; Status:     unsat
; Generator:  odrl-z3-reasoner v1.0
; Date:       2026-02-17
; ============================================================================

; benchmark generated from python API
(set-info :status unknown)
(declare-fun dateTime_default_default () Int)
(assert
 (let (($x22 (< 1735689600 dateTime_default_default)))
(let (($x243 (> 1704067200 dateTime_default_default)))
(and $x243 $x22))))
(check-sat)
