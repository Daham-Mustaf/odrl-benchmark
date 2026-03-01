%--------------------------------------------------------------------------
% File     : ODRL405-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : ★★★☆☆ Medium: 3 axes, 7 constants, mixed ops (eq/gteq/lteq)
% Expected : Theorem
% Verdict  : Compatible
% Category : PolicyQuality
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
%         odrl:operator odrl:eq ;
%         odrl:rightOperand "600"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "200"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeDepth ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "32"^^xsd:decimal ] ;
%     ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeWidth ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "800"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "400"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeDepth ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "16"^^xsd:decimal ] ;
%     ] .
%
% Formal   : width eq 600  →  [600, 600]
%            width lteq 800  →  (0, 800]
%            [600, 600] ∩ (0, 800] ≠ ∅  →  Compatible
%
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_axis_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v16, axiom, val(v16)).
fof(val_v32, axiom, val(v32)).
fof(val_v200, axiom, val(v200)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v16, axiom, less(v0, v16)).
fof(ord_v0_v32, axiom, less(v0, v32)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v16_v32, axiom, less(v16, v32)).
fof(ord_v16_v200, axiom, less(v16, v200)).
fof(ord_v16_v400, axiom, less(v16, v400)).
fof(ord_v16_v600, axiom, less(v16, v600)).
fof(ord_v16_v800, axiom, less(v16, v800)).
fof(ord_v32_v200, axiom, less(v32, v200)).
fof(ord_v32_v400, axiom, less(v32, v400)).
fof(ord_v32_v600, axiom, less(v32, v600)).
fof(ord_v32_v800, axiom, less(v32, v800)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v16, v32, v200, v400, v600, v800)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl405, conjecture,
    ?[X,Y,Z]: (in_closed(X, v600, v600) & in_lopen(X, v0, v800) &
          leq(v200, Y) & in_lopen(Y, v0, v400) &
          in_lopen(Z, v0, v32) & leq(v16, Z))).
%--------------------------------------------------------------------------
