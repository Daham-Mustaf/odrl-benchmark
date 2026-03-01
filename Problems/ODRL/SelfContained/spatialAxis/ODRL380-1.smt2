; --------------------------------------------------------------------------
; File     : ODRL380-1.smt2
; Domain   : ODRL Spatial Axis Profile
; Problem  : Spatial compatible × temporal compatible → Compatible
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
;           odrl:operator odrl:lteq ;
;           odrl:rightOperand "365"^^xsd:integer ]
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
;           odrl:operator odrl:gteq ;
;           odrl:rightOperand "181"^^xsd:integer ]
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
; dateTime: lteq 365  ∧  gteq 181
(assert (<= y 365))
(assert (>= y 181))

; Result: sat → Compatible
(check-sat)
(exit)
