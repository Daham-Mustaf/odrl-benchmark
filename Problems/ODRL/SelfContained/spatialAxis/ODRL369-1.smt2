; --------------------------------------------------------------------------
; File     : ODRL369-1.smt2
; Domain   : ODRL Spatial Axis Profile
; Problem  : Resolution axis breaks 4D subsumption → Refuted
; Expected : sat
; Verdict  : Refuted
; Category : Composition
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
;         odrl:rightOperand "600"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeHeight ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "400"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeDepth ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "16"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand odrl:resolution ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "300"^^xsd:decimal ] ] .
;
;   ex:policyB a odrl:Set ;
;     odrl:permission [
;       odrl:action odrl:use ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeWidth ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "1200"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeHeight ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "800"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeDepth ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "32"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand odrl:resolution ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "150"^^xsd:decimal ] ] .
;
; Gen      : gen_axis_suite.py
; --------------------------------------------------------------------------
(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(declare-const z Real)
(declare-const w Real)

; --- Axis 1: width (∈ box_A) ---
(assert (> x 0))
(assert (<= x 600))

; --- Axis 2: height (∈ box_A) ---
(assert (> y 0))
(assert (<= y 400))

; --- Axis 3: depth (∈ box_A) ---
(assert (> z 0))
(assert (<= z 16))

; --- Axis 4: resolution (∈ box_A) ---
(assert (> w 0))
(assert (<= w 300))

; --- ¬(∈ box_B): De Morgan disjunction ---
(assert (or (not (<= x 1200)) (not (<= y 800)) (not (<= z 32)) (not (<= w 150))))

; Result: sat → Refuted
(check-sat)
(exit)
