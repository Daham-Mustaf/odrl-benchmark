; ============================================================================
; SMT-LIB2 Benchmark: ODRL Policy Conflict Detection
; ============================================================================
; Source:     24_full_iri_unit_conflict.ttl
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
(declare-fun resolution_DPI_default () Real)
(assert
 (let (($x68 (and (and (distinct 72.0 resolution_DPI_default) true) (and (distinct 150.0 resolution_DPI_default) true) (and (distinct 300.0 resolution_DPI_default) true))))
 (let (($x41 (= 150.0 resolution_DPI_default)))
 (let (($x36 (= 72.0 resolution_DPI_default)))
 (and (or $x36 $x41) $x68)))))
(assert
 (> resolution_DPI_default 0.0))
(check-sat)
