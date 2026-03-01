; --------------------------------------------------------------------------
; File     : ODRL370-1.smt2
; Domain   : ODRL Spatial Axis Profile
; Problem  : All 4 axes open overlap → Compatible (density needed)
; Expected : sat
; Verdict  : Compatible
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
;         odrl:operator odrl:gt ;
;         odrl:rightOperand "200"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeHeight ;
;         odrl:operator odrl:gt ;
;         odrl:rightOperand "100"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeDepth ;
;         odrl:operator odrl:gt ;
;         odrl:rightOperand "8"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand odrl:resolution ;
;         odrl:operator odrl:gt ;
;         odrl:rightOperand "72"^^xsd:decimal ] ] .
;
;   ex:policyB a odrl:Set ;
;     odrl:permission [
;       odrl:action odrl:use ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeWidth ;
;         odrl:operator odrl:lt ;
;         odrl:rightOperand "800"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeHeight ;
;         odrl:operator odrl:lt ;
;         odrl:rightOperand "500"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeDepth ;
;         odrl:operator odrl:lt ;
;         odrl:rightOperand "32"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand odrl:resolution ;
;         odrl:operator odrl:lt ;
;         odrl:rightOperand "300"^^xsd:decimal ] ] .
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
; width: gt 200  ∧  lt 800
(assert (> x 200))
(assert (< x 800))

; --- Axis 2: height ---
(assert (> y 0))
; height: gt 100  ∧  lt 500
(assert (> y 100))
(assert (< y 500))

; --- Axis 3: depth ---
(assert (> z 0))
; depth: gt 8  ∧  lt 32
(assert (> z 8))
(assert (< z 32))

; --- Axis 4: resolution ---
(assert (> w 0))
; resolution: gt 72  ∧  lt 300
(assert (> w 72))
(assert (< w 300))

; Result: sat → Compatible
(check-sat)
(exit)
