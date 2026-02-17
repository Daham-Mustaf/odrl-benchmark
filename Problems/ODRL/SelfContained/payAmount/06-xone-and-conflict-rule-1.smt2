; ============================================================================
; SMT-LIB2 Benchmark: ODRL Policy Conflict Detection
; ============================================================================
; Source:     06_xone_and_conflict.ttl
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
 (let (($x36 (<= 200.0 payAmount_EUR_default)))
 (let (($x39 (>= 50.0 payAmount_EUR_default)))
 (and (and (or $x39 $x36) (and (not (and $x39 $x36)))) (= 100.0 payAmount_EUR_default)))))
(assert
 (>= payAmount_EUR_default 0.0))
(check-sat)
