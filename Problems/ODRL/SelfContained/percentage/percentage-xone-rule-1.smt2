; ============================================================================
; SMT-LIB2 Benchmark: ODRL Policy Conflict Detection
; ============================================================================
; Source:     percentage_xone.ttl
; Policy:     http://example.org/policy
; Rule:       rule_1
; Category:   percentage (self-contained, Stage 1)
; Expected:   sat
; Domain:     ODRL policy reasoning (temporal/numeric constraints)
; Logic:      QF_LIA (Quantifier-Free Linear Integer Arithmetic)
; Status:     sat
; Generator:  odrl-z3-reasoner v1.0
; Date:       2026-02-17
; ============================================================================

; benchmark generated from python API
(set-info :status unknown)
(declare-fun percentage_default_default () Real)
(assert
 (let (($x16 (= 50.0 percentage_default_default)))
 (let (($x27 (= 25.0 percentage_default_default)))
 (and (or $x27 $x16) (and (not (and $x27 $x16)))))))
(assert
 (>= percentage_default_default 0.0))
(assert
 (<= percentage_default_default 100.0))
(check-sat)
