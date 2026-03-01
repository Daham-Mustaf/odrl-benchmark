; --------------------------------------------------------------------------
; File     : ODRL442-1.smt2
; Domain   : ODRL Spatial Axis Profile
; Problem  : AND(A)×OR(B): B's height arm saves width mismatch
; Expected : sat
; Verdict  : Compatible
; Category : LogicalOr
; Connect. : A=AND (implicit), B=odrl:or
;
; ODRL Policy (Turtle):
;   @prefix odrl: <http://www.w3.org/ns/odrl/2/> .
;   @prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
;   @prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
;   @prefix ex:   <https://example.org/> .
;
;   ex:policyA a odrl:Set ;
;     odrl:permission [
;       odrl:action odrl:use ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeWidth ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "800"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeHeight ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "600"^^xsd:decimal ] ;
;     ] .
;
;   ex:policyB a odrl:Set ;
;     odrl:permission [
;       odrl:action odrl:use ;
;       odrl:constraint [
;         a odrl:LogicalConstraint ;
;         odrl:or (
;           [ odrl:leftOperand oax:absoluteSizeWidth ;
;             odrl:operator odrl:gteq ;
;             odrl:rightOperand "1000"^^xsd:decimal ]
;           [ odrl:leftOperand oax:absoluteSizeHeight ;
;             odrl:operator odrl:gteq ;
;             odrl:rightOperand "200"^^xsd:decimal ]
;         )
;       ]
;     ] .
;
; Gen      : gen_axis_suite.py
; --------------------------------------------------------------------------
(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)

; --- Axis 1: width (domain) ---
(assert (> x 0))

; --- Axis 2: height (domain) ---
(assert (> y 0))

; --- Policy A (AND (implicit)) ---
(assert (and (<= x 800) (<= y 600)))
; --- Policy B (odrl:or) ---
(assert (or (>= x 1000) (>= y 200)))

; Result: sat → Compatible
(check-sat)
(exit)
