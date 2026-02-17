; ============================================================================
; SMT-LIB2 Benchmark: ODRL Policy Conflict Detection
; ============================================================================
; Source:     15_xone_disjoint_valid.ttl
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
 (let (($x34 (<= 100.0 payAmount_EUR_default)))
 (let (($x64 (>= 50.0 payAmount_EUR_default)))
 (and (or $x64 $x34) (and (not (and $x64 $x34)))))))
(assert
 (>= payAmount_EUR_default 0.0))
(check-sat)
