; --------------------------------------------------------------------------
; File     : ODRL320-1.smt2
; Domain   : ODRL Spatial Axis Profile
; Problem  : BSB: width conflict × height compatible → box Conflict
; Expected : unsat
; Verdict  : Conflict
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
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "600"^^xsd:decimal ;
;         odrl:unit <http://dbpedia.org/resource/Pixel> ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeHeight ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "600"^^xsd:decimal ;
;         odrl:unit <http://dbpedia.org/resource/Pixel> ] ] .
;
;   ex:policyB a odrl:Set ;
;     odrl:permission [
;       odrl:action odrl:use ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeWidth ;
;         odrl:operator odrl:gteq ;
;         odrl:rightOperand "1200"^^xsd:decimal ;
;         odrl:unit <http://dbpedia.org/resource/Pixel> ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeHeight ;
;         odrl:operator odrl:gteq ;
;         odrl:rightOperand "400"^^xsd:decimal ;
;         odrl:unit <http://dbpedia.org/resource/Pixel> ] ] .
;
; Gen      : gen_axis_suite.py
; --------------------------------------------------------------------------
(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)

; --- Axis 1: width ---
(assert (> x 0))
; width: lteq 600  ∧  gteq 1200
(assert (<= x 600))
(assert (>= x 1200))

; --- Axis 2: height ---
(assert (> y 0))
; height: lteq 600  ∧  gteq 400
(assert (<= y 600))
(assert (>= y 400))

; Result: unsat → Conflict
(check-sat)
(exit)
