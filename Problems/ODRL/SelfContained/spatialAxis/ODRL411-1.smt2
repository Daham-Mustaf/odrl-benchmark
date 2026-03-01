; --------------------------------------------------------------------------
; File     : ODRL411-1.smt2
; Domain   : ODRL Spatial Axis Profile
; Problem  : ★★★★☆ Hard: all 5 ops, gap=1, density, 3 axes
; Expected : unsat
; Verdict  : Conflict
; Category : PolicyQuality
;
; ODRL Policy (Turtle):
;   @prefix odrl: <http://www.w3.org/ns/odrl/2/> .
;   @prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
;   @prefix ex:   <https://example.org/> .
;
;   ex:policyA a odrl:Set ;
;     odrl:permission [
;       odrl:action odrl:use ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeWidth ;
;         odrl:operator odrl:eq ;
;         odrl:rightOperand "600"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeHeight ;
;         odrl:operator odrl:gt ;
;         odrl:rightOperand "300"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeDepth ;
;         odrl:operator odrl:gteq ;
;         odrl:rightOperand "16"^^xsd:decimal ] ;
;     ] .
;
;   ex:policyB a odrl:Set ;
;     odrl:permission [
;       odrl:action odrl:use ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeWidth ;
;         odrl:operator odrl:eq ;
;         odrl:rightOperand "601"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeHeight ;
;         odrl:operator odrl:lt ;
;         odrl:rightOperand "500"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeDepth ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "32"^^xsd:decimal ] ;
;     ] .
;
; Gen      : gen_axis_suite.py
; --------------------------------------------------------------------------
(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(declare-const z Real)

; --- Axis 1: width ---
(assert (> x 0))
; width: eq 600  ∧  eq 601
(assert (= x 600))
(assert (= x 601))

; --- Axis 2: height ---
(assert (> y 0))
; height: gt 300  ∧  lt 500
(assert (> y 300))
(assert (< y 500))

; --- Axis 3: depth ---
(assert (> z 0))
; depth: gteq 16  ∧  lteq 32
(assert (>= z 16))
(assert (<= z 32))

; Result: unsat → Conflict
(check-sat)
(exit)
