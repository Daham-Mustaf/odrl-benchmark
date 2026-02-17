; ============================================================================
; SMT-LIB2 Benchmark: ODRL Policy Conflict Detection
; ============================================================================
; Source:     18_tiered_pricing_valid.ttl
; Policy:     http://example.org/policy01
; Rule:       rule_1
; Category:   payAmount (self-contained, Stage 1)
; Expected:   sat
; Domain:     ODRL policy reasoning (temporal/numeric constraints)
; Logic:      QF_LIA (Quantifier-Free Linear Integer Arithmetic)
; Status:     sat
; Generator:  odrl-z3-reasoner v1.0
; Date:       2026-02-17
; ============================================================================

; benchmark generated from python API
(set-info :status unknown)
(declare-fun payAmount_EUR_default () Real)
(assert
 (let (($x19 (and (<= 100.0 payAmount_EUR_default) (>= 500.0 payAmount_EUR_default))))
 (let (($x28 (and (<= 10.0 payAmount_EUR_default) (>= 50.0 payAmount_EUR_default))))
 (let (($x33 (and (not (and (= 0.0 payAmount_EUR_default) $x28)) (not (and (= 0.0 payAmount_EUR_default) $x19)) (not (and $x28 $x19)))))
 (and (or (= 0.0 payAmount_EUR_default) $x28 $x19) $x33)))))
(assert
 (>= payAmount_EUR_default 0.0))
(check-sat)
