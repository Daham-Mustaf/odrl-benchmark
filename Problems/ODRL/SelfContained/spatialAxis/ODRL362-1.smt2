; --------------------------------------------------------------------------
; File     : ODRL362-1.smt2
; Domain   : ODRL Spatial Axis Profile
; Problem  : Conflict on axis 4 of 4 → box Conflict
; Expected : unsat
; Verdict  : Conflict
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
;         odrl:rightOperand "800"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeHeight ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "600"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeDepth ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "32"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand odrl:resolution ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "72"^^xsd:decimal ] ] .
;
;   ex:policyB a odrl:Set ;
;     odrl:permission [
;       odrl:action odrl:use ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeWidth ;
;         odrl:operator odrl:gteq ;
;         odrl:rightOperand "200"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeHeight ;
;         odrl:operator odrl:gteq ;
;         odrl:rightOperand "100"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeDepth ;
;         odrl:operator odrl:gteq ;
;         odrl:rightOperand "8"^^xsd:decimal ] ;
;       odrl:constraint [
;         odrl:leftOperand odrl:resolution ;
;         odrl:operator odrl:gteq ;
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
; width: lteq 800  ∧  gteq 200
(assert (<= x 800))
(assert (>= x 200))

; --- Axis 2: height ---
(assert (> y 0))
; height: lteq 600  ∧  gteq 100
(assert (<= y 600))
(assert (>= y 100))

; --- Axis 3: depth ---
(assert (> z 0))
; depth: lteq 32  ∧  gteq 8
(assert (<= z 32))
(assert (>= z 8))

; --- Axis 4: resolution ---
(assert (> w 0))
; resolution: lteq 72  ∧  gteq 300
(assert (<= w 72))
(assert (>= w 300))

; Result: unsat → Conflict
(check-sat)
(exit)
