; --------------------------------------------------------------------------
; File     : ODRL415-1.smt2
; Domain   : ODRL Spatial Axis Profile
; Problem  : ★★★★★ Very Hard: 12 constants, 4-axis tight subsumption (margin=1)
; Expected : unsat
; Verdict  : Subsumes
; Category : PolicyQuality
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
;         odrl:rightOperand "599.5"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeHeight ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "479.5"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeDepth ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "15.5"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand odrl:resolution ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "71.5"^^xsd:decimal ] ;
;     ] .
;
;   ex:policyB a odrl:Set ;
;     odrl:permission [
;       odrl:action odrl:use ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeWidth ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "600.5"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeHeight ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "480.5"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeDepth ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "16.5"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand odrl:resolution ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "72.5"^^xsd:decimal ] ;
;     ] .
;
; Gen      : gen_axis_suite.py
; --------------------------------------------------------------------------
(set-logic QF_LRA)
(declare-const x Real)
(declare-const y Real)
(declare-const z Real)
(declare-const w Real)

; --- Axis 1: width (∈ box_A) ---
(assert (> x 1))
(assert (<= x 599.5))

; --- Axis 2: height (∈ box_A) ---
(assert (> y 2))
(assert (<= y 479.5))

; --- Axis 3: depth (∈ box_A) ---
(assert (> z 3))
(assert (<= z 15.5))

; --- Axis 4: resolution (∈ box_A) ---
(assert (> w 4))
(assert (<= w 71.5))

; --- ¬(∈ box_B): De Morgan disjunction ---
(assert (or (not (<= x 600.5)) (not (<= y 480.5)) (not (<= z 16.5)) (not (<= w 72.5))))

; Result: unsat → Subsumes
(check-sat)
(exit)
