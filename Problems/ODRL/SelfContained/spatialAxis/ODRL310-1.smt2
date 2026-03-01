; --------------------------------------------------------------------------
; File     : ODRL310-1.smt2
; Domain   : ODRL Spatial Axis Profile
; Problem  : (0,1200] ⊄ (0,600]: wider does not subsume tighter
; Expected : sat
; Verdict  : Refuted
; Category : SingleAxis
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
;         odrl:rightOperand "1200"^^xsd:decimal ;
;         odrl:unit <http://dbpedia.org/resource/Pixel> ] ] .
;
;   ex:policyB a odrl:Set ;
;     odrl:permission [
;       odrl:action odrl:use ;
;       odrl:constraint [
;         odrl:leftOperand oax:absoluteSizeWidth ;
;         odrl:operator odrl:lteq ;
;         odrl:rightOperand "600"^^xsd:decimal ;
;         odrl:unit <http://dbpedia.org/resource/Pixel> ] ] .
;
; Gen      : gen_axis_suite.py
; --------------------------------------------------------------------------
(set-logic QF_LRA)
(declare-const x Real)

; --- Axis 1: width (∈ box_A) ---
(assert (> x 0))
(assert (<= x 1200))

; --- ¬(∈ box_B): De Morgan disjunction ---
(assert (not (<= x 600)))

; Result: sat → Refuted
(check-sat)
(exit)
