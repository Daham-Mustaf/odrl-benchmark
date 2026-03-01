%--------------------------------------------------------------------------
% File     : ODRL351-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : BSB 3D: width conflict × height compat × depth compat → Conflict
% Expected : Theorem
% Verdict  : Conflict
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
%         odrl:rightOperand "600"^^xsd:decimal ;
%         odrl:unit <http://dbpedia.org/resource/Pixel> ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeDepth ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "32"^^xsd:decimal ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeWidth ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "1200"^^xsd:decimal ;
%         odrl:unit <http://dbpedia.org/resource/Pixel> ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "400"^^xsd:decimal ;
%         odrl:unit <http://dbpedia.org/resource/Pixel> ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeDepth ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "8"^^xsd:decimal ] ] .
%
% Formal   : width lteq 600  →  (0, 600]
%            width gteq 1200  →  [1200, ∞)
%            (0, 600] ∩ [1200, ∞) ∅  →  Conflict
% Notes    : Extended BSB example. One conflict axis dominates.
%
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_axis_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v8, axiom, val(v8)).
fof(val_v32, axiom, val(v32)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v8, axiom, less(v0, v8)).
fof(ord_v0_v32, axiom, less(v0, v32)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v1200, axiom, less(v0, v1200)).
fof(ord_v8_v32, axiom, less(v8, v32)).
fof(ord_v8_v400, axiom, less(v8, v400)).
fof(ord_v8_v600, axiom, less(v8, v600)).
fof(ord_v8_v1200, axiom, less(v8, v1200)).
fof(ord_v32_v400, axiom, less(v32, v400)).
fof(ord_v32_v600, axiom, less(v32, v600)).
fof(ord_v32_v1200, axiom, less(v32, v1200)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v400_v1200, axiom, less(v400, v1200)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct, axiom, $distinct(v0, v8, v32, v400, v600, v1200)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl351, conjecture,
    ~?[X,Y,Z]: (in_lopen(X, v0, v600) & leq(v1200, X) &
          in_lopen(Y, v0, v600) & leq(v400, Y) &
          in_lopen(Z, v0, v32) & leq(v8, Z))).
%--------------------------------------------------------------------------
