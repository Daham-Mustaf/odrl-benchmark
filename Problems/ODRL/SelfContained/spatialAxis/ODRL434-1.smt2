; --------------------------------------------------------------------------
; File     : ODRL434-1.smt2
; Domain   : ODRL Spatial Axis Profile
; Problem  : ≤v ⊄ <v → endpoint 600 ∈ A, ∉ B → Refuted
; Expected : sat
; Verdict  : Refuted
; Category : Boundary
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
;         odrl:rightOperand "600"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeHeight ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "400"^^xsd:decimal ] ;
;     ] .
;
;   ex:policyB a odrl:Set ;
;     odrl:permission [
;       odrl:action odrl:use ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeWidth ;
;         odrl:operator odrl:lt ;
;         odrl:rightOperand "600"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeHeight ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "800"^^xsd:decimal ] ;
;     ] .
;
; Gen      : gen_axis_suite.py
; --------------------------------------------------------------------------
(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)

; --- Axis 1: width (∈ box_A) ---
(assert (> x 0))
(assert (<= x 600))

; --- Axis 2: height (∈ box_A) ---
(assert (> y 0))
(assert (<= y 400))

; --- ¬(∈ box_B): De Morgan disjunction ---
(assert (or (not (< x 600)) (not (<= y 800))))

; Result: sat → Refuted
(check-sat)
(exit)
