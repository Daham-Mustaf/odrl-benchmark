; --------------------------------------------------------------------------
; File     : ODRL324-1.smt2
; Domain   : ODRL Spatial Axis Profile
; Problem  : Width eq+lteq, height overlap → box Compatible
; Expected : sat
; Verdict  : Compatible
; Category : Box2D
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
;         odrl:rightOperand "600"^^xsd:decimal ;
;         odrl:unit <http://dbpedia.org/resource/Pixel> ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeHeight ;
;         odrl:operator odrl:gteq ;
;         odrl:rightOperand "200"^^xsd:decimal ;
;         odrl:unit <http://dbpedia.org/resource/Pixel> ] ] .
;
;   ex:policyB a odrl:Set ;
;     odrl:permission [
;       odrl:action odrl:use ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeWidth ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "800"^^xsd:decimal ;
;         odrl:unit <http://dbpedia.org/resource/Pixel> ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeHeight ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "600"^^xsd:decimal ;
;         odrl:unit <http://dbpedia.org/resource/Pixel> ] ] .
;
; Gen      : gen_axis_suite.py
; --------------------------------------------------------------------------
(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)

; --- Axis 1: width ---
(assert (> x 0))
; width: eq 600  ∧  lteq 800
(assert (= x 600))
(assert (<= x 800))

; --- Axis 2: height ---
(assert (> y 0))
; height: gteq 200  ∧  lteq 600
(assert (>= y 200))
(assert (<= y 600))

; Result: sat → Compatible
(check-sat)
(exit)
