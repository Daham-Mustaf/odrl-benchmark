%--------------------------------------------------------------------------
% File     : ODRL364-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : All 5 operator types across 4 axes → Compatible
% Expected : Theorem
% Verdict  : Compatible
% Category : Composition
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
%         odrl:operator odrl:gt ;
%         odrl:rightOperand "100"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeDepth ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "8"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand odrl:resolution ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "300"^^xsd:decimal ] ] .
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
%         odrl:operator odrl:lt ;
%         odrl:rightOperand "500"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeDepth ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "32"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand odrl:resolution ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "150"^^xsd:decimal ] ] .
%
% Formal   : width eq 600  →  [600, 600]
%            width lteq 800  →  (0, 800]
%            [600, 600] ∩ (0, 800] ≠ ∅  →  Compatible
% Notes    : Exercises all 5 ODRL operators: eq, lt, lteq, gt, gteq.
%
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_axis_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/AXIS000-0.ax').
include('Axioms/Layer0-DomainKB/ORD001-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v8, axiom, val(v8)).
fof(val_v32, axiom, val(v32)).
fof(val_v100, axiom, val(v100)).
fof(val_v150, axiom, val(v150)).
fof(val_v300, axiom, val(v300)).
fof(val_v500, axiom, val(v500)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v8, axiom, less(v0, v8)).
fof(ord_v0_v32, axiom, less(v0, v32)).
fof(ord_v0_v100, axiom, less(v0, v100)).
fof(ord_v0_v150, axiom, less(v0, v150)).
fof(ord_v0_v300, axiom, less(v0, v300)).
fof(ord_v0_v500, axiom, less(v0, v500)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v8_v32, axiom, less(v8, v32)).
fof(ord_v8_v100, axiom, less(v8, v100)).
fof(ord_v8_v150, axiom, less(v8, v150)).
fof(ord_v8_v300, axiom, less(v8, v300)).
fof(ord_v8_v500, axiom, less(v8, v500)).
fof(ord_v8_v600, axiom, less(v8, v600)).
fof(ord_v8_v800, axiom, less(v8, v800)).
fof(ord_v32_v100, axiom, less(v32, v100)).
fof(ord_v32_v150, axiom, less(v32, v150)).
fof(ord_v32_v300, axiom, less(v32, v300)).
fof(ord_v32_v500, axiom, less(v32, v500)).
fof(ord_v32_v600, axiom, less(v32, v600)).
fof(ord_v32_v800, axiom, less(v32, v800)).
fof(ord_v100_v150, axiom, less(v100, v150)).
fof(ord_v100_v300, axiom, less(v100, v300)).
fof(ord_v100_v500, axiom, less(v100, v500)).
fof(ord_v100_v600, axiom, less(v100, v600)).
fof(ord_v100_v800, axiom, less(v100, v800)).
fof(ord_v150_v300, axiom, less(v150, v300)).
fof(ord_v150_v500, axiom, less(v150, v500)).
fof(ord_v150_v600, axiom, less(v150, v600)).
fof(ord_v150_v800, axiom, less(v150, v800)).
fof(ord_v300_v500, axiom, less(v300, v500)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v300_v800, axiom, less(v300, v800)).
fof(ord_v500_v600, axiom, less(v500, v600)).
fof(ord_v500_v800, axiom, less(v500, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v8, v32, v100, v150, v300, v500, v600, v800)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl364, conjecture,
    ?[X,Y,Z,W]: (in_closed(X, v600, v600) & in_lopen(X, v0, v800) &
          less(v100, Y) & in_open(Y, v0, v500) &
          leq(v8, Z) & in_lopen(Z, v0, v32) &
          in_lopen(W, v0, v300) & leq(v150, W))).
%--------------------------------------------------------------------------
