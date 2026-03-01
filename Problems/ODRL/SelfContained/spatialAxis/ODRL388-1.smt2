; --------------------------------------------------------------------------
; File     : ODRL388-1.smt2
; Domain   : ODRL Spatial Axis Profile
; Problem  : Temporal axis breaks cross-domain subsumption
; Expected : sat
; Verdict  : Refuted
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
;           odrl:rightOperand "600"^^xsd:decimal ;
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
;           odrl:operator odrl:lteq ;
;           odrl:rightOperand "1200"^^xsd:decimal ;
;           odrl:unit <http://dbpedia.org/resource/Pixel> ]
;         odrl:constraint [
;           odrl:leftOperand odrl:dateTime ;
;           odrl:operator odrl:lteq ;
;           odrl:rightOperand "181"^^xsd:integer ]
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

; --- Axis 2: dateTime (∈ box_A) ---
(assert (>= y 0))
(assert (<= y 365))

; --- ¬(∈ box_B): De Morgan disjunction ---
(assert (or (not (<= x 1200)) (not (<= y 181))))

; Result: sat → Refuted
(check-sat)
(exit)
