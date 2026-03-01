%--------------------------------------------------------------------------
% File     : ODRL411-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : ★★★★☆ Hard: all 5 ops, gap=1, density, 3 axes
% Expected : Theorem
% Verdict  : Conflict
% Category : PolicyQuality
% Difficulty: Hard
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
%         odrl:rightOperand "300"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeDepth ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "16"^^xsd:decimal ] ;
%     ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeWidth ;
%         odrl:operator odrl:eq ;
%         odrl:rightOperand "601"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:lt ;
%         odrl:rightOperand "500"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeDepth ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "32"^^xsd:decimal ] ;
%     ] .
%
% Formal   : width eq 600  →  [600, 600]
%            width eq 601  →  [601, 601]
%            [600, 600] ∩ [601, 601] ∅  →  Conflict
% Notes    : All 5 O_delta operators: eq*2, gt, lt, gteq, lteq. Gap=1 kills box.
%
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_axis_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/AXIS000-0.ax').
include('Axioms/Layer0-DomainKB/ORD001-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v16, axiom, val(v16)).
fof(val_v32, axiom, val(v32)).
fof(val_v300, axiom, val(v300)).
fof(val_v500, axiom, val(v500)).
fof(val_v600, axiom, val(v600)).
fof(val_v601, axiom, val(v601)).
fof(ord_v0_v16, axiom, less(v0, v16)).
fof(ord_v0_v32, axiom, less(v0, v32)).
fof(ord_v0_v300, axiom, less(v0, v300)).
fof(ord_v0_v500, axiom, less(v0, v500)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v601, axiom, less(v0, v601)).
fof(ord_v16_v32, axiom, less(v16, v32)).
fof(ord_v16_v300, axiom, less(v16, v300)).
fof(ord_v16_v500, axiom, less(v16, v500)).
fof(ord_v16_v600, axiom, less(v16, v600)).
fof(ord_v16_v601, axiom, less(v16, v601)).
fof(ord_v32_v300, axiom, less(v32, v300)).
fof(ord_v32_v500, axiom, less(v32, v500)).
fof(ord_v32_v600, axiom, less(v32, v600)).
fof(ord_v32_v601, axiom, less(v32, v601)).
fof(ord_v300_v500, axiom, less(v300, v500)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v300_v601, axiom, less(v300, v601)).
fof(ord_v500_v600, axiom, less(v500, v600)).
fof(ord_v500_v601, axiom, less(v500, v601)).
fof(ord_v600_v601, axiom, less(v600, v601)).
fof(distinct, axiom, $distinct(v0, v16, v32, v300, v500, v600, v601)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl411, conjecture,
    ~?[X,Y,Z]: (in_closed(X, v600, v600) & in_closed(X, v601, v601) &
          less(v300, Y) & in_open(Y, v0, v500) &
          leq(v16, Z) & in_lopen(Z, v0, v32))).
%--------------------------------------------------------------------------
