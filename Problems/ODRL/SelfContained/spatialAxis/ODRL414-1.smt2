; --------------------------------------------------------------------------
; File     : ODRL414-1.smt2
; Domain   : ODRL Spatial Axis Profile
; Problem  : ★★★★★ Very Hard: all 5 ops, 4-axis De Morgan refutation
; Expected : sat
; Verdict  : Refuted
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
;         odrl:operator odrl:eq ;
;         odrl:rightOperand "600"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeHeight ;
;         odrl:operator odrl:gt ;
;         odrl:rightOperand "300"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeDepth ;
;         odrl:operator odrl:gteq ;
;         odrl:rightOperand "16"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand odrl:resolution ;
;         odrl:operator odrl:lt ;
;         odrl:rightOperand "300"^^xsd:decimal ] ;
;     ] .
;
;   ex:policyB a odrl:Set ;
;     odrl:permission [
;       odrl:action odrl:use ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeWidth ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "1920"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeHeight ;
;         odrl:operator odrl:lt ;
;         odrl:rightOperand "1080"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeDepth ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "48"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand odrl:resolution ;
;         odrl:operator odrl:gteq ;
;         odrl:rightOperand "72"^^xsd:decimal ] ;
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
(assert (= x 600))

; --- Axis 2: height (∈ box_A) ---
(assert (> y 2))
(assert (> y 300))

; --- Axis 3: depth (∈ box_A) ---
(assert (> z 3))
(assert (>= z 16))

; --- Axis 4: resolution (∈ box_A) ---
(assert (> w 4))
(assert (< w 300))

; --- ¬(∈ box_B): De Morgan disjunction ---
(assert (or (not (<= x 1920)) (not (< y 1080)) (not (<= z 48)) (not (>= w 72))))

; Result: sat → Refuted
(check-sat)
(exit)
