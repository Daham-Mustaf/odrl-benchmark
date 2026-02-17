; ============================================================================
; SMT-LIB2 Benchmark: ODRL Policy Conflict Detection
; ============================================================================
; Source:     31_xone_three_branches.ttl
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
(declare-fun resolution_DPI_default () Real)
(assert
 (let (($x72 (<= 600.0 resolution_DPI_default)))
 (let (($x21 (= 300.0 resolution_DPI_default)))
 (let (($x69 (and (not (and (>= 72.0 resolution_DPI_default) $x21)) (not (and (>= 72.0 resolution_DPI_default) $x72)) (not (and $x21 $x72)))))
 (and (or (>= 72.0 resolution_DPI_default) $x21 $x72) $x69)))))
(assert
 (> resolution_DPI_default 0.0))
(check-sat)
