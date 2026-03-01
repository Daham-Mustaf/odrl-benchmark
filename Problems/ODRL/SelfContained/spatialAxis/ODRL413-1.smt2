; --------------------------------------------------------------------------
; File     : ODRL413-1.smt2
; Domain   : ODRL Spatial Axis Profile
; Problem  : ★★★★★ Very Hard: 12 constants, razor-thin 4D overlap=0.5
; Expected : sat
; Verdict  : Compatible
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
;   ex:policyB a odrl:Set ;
;     odrl:permission [
;       odrl:action odrl:use ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeWidth ;
;         odrl:operator odrl:gteq ;
;         odrl:rightOperand "600"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeHeight ;
;         odrl:operator odrl:gteq ;
;         odrl:rightOperand "480"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeDepth ;
;         odrl:operator odrl:gteq ;
;         odrl:rightOperand "16"^^xsd:decimal ] ;
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

; --- Axis 1: width ---
(assert (> x 1))
; width: lteq 600.5  ∧  gteq 600
(assert (<= x 600.5))
(assert (>= x 600))

; --- Axis 2: height ---
(assert (> y 2))
; height: lteq 480.5  ∧  gteq 480
(assert (<= y 480.5))
(assert (>= y 480))

; --- Axis 3: depth ---
(assert (> z 3))
; depth: lteq 16.5  ∧  gteq 16
(assert (<= z 16.5))
(assert (>= z 16))

; --- Axis 4: resolution ---
(assert (> w 4))
; resolution: lteq 72.5  ∧  gteq 72
(assert (<= w 72.5))
(assert (>= w 72))

; Result: sat → Compatible
(check-sat)
(exit)
