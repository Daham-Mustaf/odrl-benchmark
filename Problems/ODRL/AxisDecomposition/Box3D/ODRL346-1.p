%--------------------------------------------------------------------------
% File     : ODRL346-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : All three axes touch → single-point Compatible
% Expected : Theorem
% Verdict  : Compatible
% Category : Box3D
% Difficulty: Medium
%
% ODRL Policy (Turtle):
%   @prefix odrl: <http://www.w3.org/ns/odrl/2/> .
%   @prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
%   @prefix ex:   <https://example.org/> .
%
%   ex:policyA a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeWidth ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "600"^^xsd:decimal ;
%         odrl:unit <http://dbpedia.org/resource/Pixel> ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "400"^^xsd:decimal ;
%         odrl:unit <http://dbpedia.org/resource/Pixel> ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeDepth ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "16"^^xsd:decimal ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeWidth ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "600"^^xsd:decimal ;
%         odrl:unit <http://dbpedia.org/resource/Pixel> ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "400"^^xsd:decimal ;
%         odrl:unit <http://dbpedia.org/resource/Pixel> ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeDepth ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "16"^^xsd:decimal ] ] .
%
% Formal   : width lteq 600  →  (0, 600]
%            width gteq 600  →  [600, ∞)
%            (0, 600] ∩ [600, ∞) ≠ ∅  →  Compatible
% Notes    : Witness: (600, 400, 16). Intersection is a single point in R³.
%
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_axis_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v16, axiom, val(v16)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v16, axiom, less(v0, v16)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v16_v400, axiom, less(v16, v400)).
fof(ord_v16_v600, axiom, less(v16, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct, axiom, $distinct(v0, v16, v400, v600)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl346, conjecture,
    ?[X,Y,Z]: (in_lopen(X, v0, v600) & leq(v600, X) &
          in_lopen(Y, v0, v400) & leq(v400, Y) &
          in_lopen(Z, v0, v16) & leq(v16, Z))).
%--------------------------------------------------------------------------
