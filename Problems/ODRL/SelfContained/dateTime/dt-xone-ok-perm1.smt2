; ============================================================================
; SMT-LIB2 Benchmark: ODRL Policy Conflict Detection
; ============================================================================
; Source:     dt_xone_ok.ttl
; Policy:     http://example.org/policy_dt_xone_ok
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
 (let (($x470 (= 1748736000 dateTime_default_default)))
(let (($x934 (= 1740787200 dateTime_default_default)))
(and (or $x934 $x470) (and (not (and $x934 $x470)))))))
(check-sat)
