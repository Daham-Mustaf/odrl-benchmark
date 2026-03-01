; --------------------------------------------------------------------------
; File     : ODRL423-1.smt2
; Domain   : ODRL Spatial Axis Profile
; Problem  : P4: <v ∧ >v → double gap at v=600 → Conflict
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
;         odrl:operator odrl:lt ;
;         odrl:rightOperand "600"^^xsd:decimal ] ;
;     ] .
;
;   ex:policyB a odrl:Set ;
;     odrl:permission [
;       odrl:action odrl:use ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeWidth ;
;         odrl:operator odrl:gt ;
;         odrl:rightOperand "600"^^xsd:decimal ] ;
;     ] .
;
; Gen      : gen_axis_suite.py
; --------------------------------------------------------------------------
(set-logic QF_LRA)
(declare-const x Real)

; --- Axis 1: width ---
(assert (> x 0))
; width: lt 600  ∧  gt 600
(assert (< x 600))
(assert (> x 600))

; Result: unsat → Conflict
(check-sat)
(exit)
