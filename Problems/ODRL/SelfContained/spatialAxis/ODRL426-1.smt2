; --------------------------------------------------------------------------
; File     : ODRL426-1.smt2
; Domain   : ODRL Spatial Axis Profile
; Problem  : P7: =v ∧ <v → v ∉ (0,v) → Conflict
; Expected : unsat
; Verdict  : Conflict
; Category : Boundary
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
;         odrl:leftOperand oax:absoluteSizeWidth ;
;         odrl:operator odrl:eq ;
;         odrl:rightOperand "600"^^xsd:decimal ] ;
;     ] .
;
;   ex:policyB a odrl:Set ;
;     odrl:permission [
;       odrl:action odrl:use ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeWidth ;
;         odrl:operator odrl:lt ;
;         odrl:rightOperand "600"^^xsd:decimal ] ;
;     ] .
;
; Gen      : gen_axis_suite.py
; --------------------------------------------------------------------------
(set-logic QF_LRA)
(declare-const x Real)

; --- Axis 1: width ---
(assert (> x 0))
; width: eq 600  ∧  lt 600
(assert (= x 600))
(assert (< x 600))

; Result: unsat → Conflict
(check-sat)
(exit)
