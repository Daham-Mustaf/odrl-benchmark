; --------------------------------------------------------------------------
; File     : ODRL312-1.smt2
; Domain   : ODRL Spatial Axis Profile
; Problem  : {400} ⊆ (0,600]: point inside interval
; Expected : unsat
; Verdict  : Subsumes
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
;         odrl:operator odrl:eq ;
;         odrl:rightOperand "400"^^xsd:decimal ;
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
(assert (= x 400))

; --- ¬(∈ box_B): De Morgan disjunction ---
(assert (not (<= x 600)))

; Result: unsat → Subsumes
(check-sat)
(exit)
