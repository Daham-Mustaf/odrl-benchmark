; --------------------------------------------------------------------------
; File     : ODRL408-1.smt2
; Domain   : ODRL Spatial Axis Profile
; Problem  : ★★★★☆ Hard: 4 axes, 9 constants, gap=1 on width
; Expected : unsat
; Verdict  : Conflict
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
;         odrl:rightOperand "599"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeHeight ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "1080"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeDepth ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "32"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand odrl:resolution ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "300"^^xsd:decimal ] ;
;     ] .
;
;   ex:policyB a odrl:Set ;
;     odrl:permission [
;       odrl:action odrl:use ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeWidth ;
;         odrl:operator odrl:gteq ;
;         odrl:rightOperand "601"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeHeight ;
;         odrl:operator odrl:gteq ;
;         odrl:rightOperand "480"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeDepth ;
;         odrl:operator odrl:gteq ;
;         odrl:rightOperand "8"^^xsd:decimal ] ;
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
(assert (> x 0))
; width: lteq 599  ∧  gteq 601
(assert (<= x 599))
(assert (>= x 601))

; --- Axis 2: height ---
(assert (> y 0))
; height: lteq 1080  ∧  gteq 480
(assert (<= y 1080))
(assert (>= y 480))

; --- Axis 3: depth ---
(assert (> z 0))
; depth: lteq 32  ∧  gteq 8
(assert (<= z 32))
(assert (>= z 8))

; --- Axis 4: resolution ---
(assert (> w 0))
; resolution: lteq 300  ∧  gteq 72
(assert (<= w 300))
(assert (>= w 72))

; Result: unsat → Conflict
(check-sat)
(exit)
