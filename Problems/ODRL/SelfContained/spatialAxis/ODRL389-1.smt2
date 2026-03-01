; --------------------------------------------------------------------------
; File     : ODRL389-1.smt2
; Domain   : ODRL Spatial Axis Profile
; Problem  : Open temporal intervals + spatial overlap → Compatible
; Expected : sat
; Verdict  : Compatible
; Category : CrossDomain
;
; ODRL Policy (Turtle):
;   @prefix odrl: <http://www.w3.org/ns/odrl/2/> .
;   @prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
;   @prefix ex:   <https://example.org/> .
;
;   ex:policyA a odrl:Set ;
;     odrl:permission [
;       odrl:action odrl:use ;
;         odrl:constraint [
;           odrl:leftOperand oax:absoluteSizeWidth ;
;           odrl:operator odrl:lteq ;
;           odrl:rightOperand "800"^^xsd:decimal ;
;           odrl:unit <http://dbpedia.org/resource/Pixel> ]
;         odrl:constraint [
;           odrl:leftOperand odrl:dateTime ;
;           odrl:operator odrl:gt ;
;           odrl:rightOperand "100"^^xsd:integer ]
;     ] .
;
;   ex:policyB a odrl:Set ;
;     odrl:permission [
;       odrl:action odrl:use ;
;         odrl:constraint [
;           odrl:leftOperand oax:absoluteSizeWidth ;
;           odrl:operator odrl:gteq ;
;           odrl:rightOperand "200"^^xsd:decimal ;
;           odrl:unit <http://dbpedia.org/resource/Pixel> ]
;         odrl:constraint [
;           odrl:leftOperand odrl:dateTime ;
;           odrl:operator odrl:lt ;
;           odrl:rightOperand "300"^^xsd:integer ]
;     ] .
;
; Gen      : gen_axis_suite.py
; --------------------------------------------------------------------------
(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)

; --- Axis 1: width ---
(assert (> x 0))
; width: lteq 800  ∧  gteq 200
(assert (<= x 800))
(assert (>= x 200))

; --- Axis 2: dateTime ---
(assert (>= y 0))
; dateTime: gt 100  ∧  lt 300
(assert (> y 100))
(assert (< y 300))

; Result: sat → Compatible
(check-sat)
(exit)
