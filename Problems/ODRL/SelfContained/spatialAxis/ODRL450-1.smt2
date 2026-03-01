; --------------------------------------------------------------------------
; File     : ODRL450-1.smt2
; Domain   : ODRL Spatial Axis Profile
; Problem  : OR(A)×AND(B) with open boundaries → Compatible
; Expected : sat
; Verdict  : Compatible
; Category : LogicalOr
; Connect. : A=odrl:or, B=AND (implicit)
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
;         a odrl:LogicalConstraint ;
;         odrl:or (
;           [ odrl:leftOperand oax:absoluteSizeWidth ;
;             odrl:operator odrl:lt ;
;             odrl:rightOperand "600"^^xsd:decimal ]
;           [ odrl:leftOperand oax:absoluteSizeHeight ;
;             odrl:operator odrl:gt ;
;             odrl:rightOperand "200"^^xsd:decimal ]
;         )
;       ]
;     ] .
;
;   ex:policyB a odrl:Set ;
;     odrl:permission [
;       odrl:action odrl:use ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeWidth ;
;         odrl:operator odrl:gt ;
;         odrl:rightOperand "400"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeHeight ;
;         odrl:operator odrl:lt ;
;         odrl:rightOperand "800"^^xsd:decimal ] ;
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

; --- Policy A (odrl:or) ---
(assert (or (< x 600) (> y 200)))
; --- Policy B (AND (implicit)) ---
(assert (and (> x 400) (< y 800)))

; Result: sat → Compatible
(check-sat)
(exit)
