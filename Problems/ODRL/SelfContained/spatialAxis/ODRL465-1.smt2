; --------------------------------------------------------------------------
; File     : ODRL465-1.smt2
; Domain   : ODRL Spatial Axis Profile
; Problem  : 3-axis XONE(A)×AND(B): B in all-hold zone → Conflict
; Expected : unsat
; Verdict  : Conflict
; Category : LogicalXone
; Connect. : A=odrl:xone, B=AND (implicit)
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
;         odrl:xone (
;           [ odrl:leftOperand oax:absoluteSizeWidth ;
;             odrl:operator odrl:lteq ;
;             odrl:rightOperand "600"^^xsd:decimal ]
;           [ odrl:leftOperand oax:absoluteSizeHeight ;
;             odrl:operator odrl:lteq ;
;             odrl:rightOperand "400"^^xsd:decimal ]
;           [ odrl:leftOperand oax:absoluteSizeDepth ;
;             odrl:operator odrl:lteq ;
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
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "400"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeHeight ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "200"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeDepth ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "100"^^xsd:decimal ] ;
;     ] .
;
; Gen      : gen_axis_suite.py
; --------------------------------------------------------------------------
(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(declare-const z Real)

; --- Axis 1: width (domain) ---
(assert (> x 0))

; --- Axis 2: height (domain) ---
(assert (> y 0))

; --- Axis 3: depth (domain) ---
(assert (> z 0))

; --- Policy A (odrl:xone) ---
(assert (or (and (<= x 600) (not (<= y 400)) (not (<= z 200))) (and (not (<= x 600)) (<= y 400) (not (<= z 200))) (and (not (<= x 600)) (not (<= y 400)) (<= z 200))))
; --- Policy B (AND (implicit)) ---
(assert (and (<= x 400) (<= y 200) (<= z 100)))

; Result: unsat → Conflict
(check-sat)
(exit)
