; --------------------------------------------------------------------------
; File     : ODRL351-1.smt2
; Domain   : ODRL Spatial Axis Profile
; Problem  : BSB 3D: width conflict × height compat × depth compat → Conflict
; Expected : unsat
; Verdict  : Conflict
; Category : Box3D
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
;         odrl:unit <http://dbpedia.org/resource/Pixel> ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeDepth ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "32"^^xsd:decimal ] ] .
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
;         odrl:unit <http://dbpedia.org/resource/Pixel> ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeDepth ;
;         odrl:operator odrl:gteq ;
;         odrl:rightOperand "8"^^xsd:decimal ] ] .
;
; Gen      : gen_axis_suite.py
; --------------------------------------------------------------------------
(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(declare-const z Real)

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

; --- Axis 3: depth ---
(assert (> z 0))
; depth: lteq 32  ∧  gteq 8
(assert (<= z 32))
(assert (>= z 8))

; Result: unsat → Conflict
(check-sat)
(exit)
