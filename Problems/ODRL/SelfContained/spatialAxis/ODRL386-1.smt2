; --------------------------------------------------------------------------
; File     : ODRL386-1.smt2
; Domain   : ODRL Spatial Axis Profile
; Problem  : Payment conflict kills 3 compatible domains
; Expected : unsat
; Verdict  : Conflict
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
;         odrl:constraint [
;           odrl:leftOperand odrl:count ;
;           odrl:operator odrl:lteq ;
;           odrl:rightOperand "100"^^xsd:integer ]
;         odrl:constraint [
;           odrl:leftOperand odrl:payAmount ;
;           odrl:operator odrl:lteq ;
;           odrl:rightOperand "1000"^^xsd:decimal ;
;           odrl:unit <http://dbpedia.org/resource/Euro> ]
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
;         odrl:constraint [
;           odrl:leftOperand odrl:count ;
;           odrl:operator odrl:gteq ;
;           odrl:rightOperand "10"^^xsd:integer ]
;         odrl:constraint [
;           odrl:leftOperand odrl:payAmount ;
;           odrl:operator odrl:gteq ;
;           odrl:rightOperand "5000"^^xsd:decimal ;
;           odrl:unit <http://dbpedia.org/resource/Euro> ]
;     ] .
;
; Gen      : gen_axis_suite.py
; --------------------------------------------------------------------------
(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(declare-const z Real)
(declare-const w Real)

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

; --- Axis 3: count ---
(assert (>= z 0))
; count: lteq 100  ∧  gteq 10
(assert (<= z 100))
(assert (>= z 10))

; --- Axis 4: payAmount ---
(assert (>= w 0))
; payAmount: lteq 1000  ∧  gteq 5000
(assert (<= w 1000))
(assert (>= w 5000))

; Result: unsat → Conflict
(check-sat)
(exit)
