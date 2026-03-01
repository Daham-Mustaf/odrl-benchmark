%--------------------------------------------------------------------------
% File     : ODRL413-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : ★★★★★ Very Hard: 12 constants, razor-thin 4D overlap=0.5
% Expected : Theorem
% Verdict  : Compatible
% Category : PolicyQuality
% Difficulty: Very Hard
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
%         odrl:rightOperand "600.5"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "480.5"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeDepth ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "16.5"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand odrl:resolution ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "72.5"^^xsd:decimal ] ;
%     ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeWidth ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "600"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "480"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeDepth ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "16"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand odrl:resolution ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "72"^^xsd:decimal ] ;
%     ] .
%
% Formal   : width lteq 600.5  →  (1, 600.5]
%            width gteq 600  →  [600, ∞)
%            (1, 600.5] ∩ [600, ∞) ≠ ∅  →  Compatible
% Notes    : 12 distinct values → 66 ordering axioms. Each axis overlaps by exactly 0.5. Witness: (600.25, 480.25, 16.25, 72.25).
%
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_axis_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/AXIS000-0.ax').
include('Axioms/Layer0-DomainKB/ORD001-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v1, axiom, val(v1)).
fof(val_v2, axiom, val(v2)).
fof(val_v3, axiom, val(v3)).
fof(val_v4, axiom, val(v4)).
fof(val_v16, axiom, val(v16)).
fof(val_v16_5, axiom, val(v16_5)).
fof(val_v72, axiom, val(v72)).
fof(val_v72_5, axiom, val(v72_5)).
fof(val_v480, axiom, val(v480)).
fof(val_v480_5, axiom, val(v480_5)).
fof(val_v600, axiom, val(v600)).
fof(val_v600_5, axiom, val(v600_5)).
fof(ord_v1_v2, axiom, less(v1, v2)).
fof(ord_v1_v3, axiom, less(v1, v3)).
fof(ord_v1_v4, axiom, less(v1, v4)).
fof(ord_v1_v16, axiom, less(v1, v16)).
fof(ord_v1_v16_5, axiom, less(v1, v16_5)).
fof(ord_v1_v72, axiom, less(v1, v72)).
fof(ord_v1_v72_5, axiom, less(v1, v72_5)).
fof(ord_v1_v480, axiom, less(v1, v480)).
fof(ord_v1_v480_5, axiom, less(v1, v480_5)).
fof(ord_v1_v600, axiom, less(v1, v600)).
fof(ord_v1_v600_5, axiom, less(v1, v600_5)).
fof(ord_v2_v3, axiom, less(v2, v3)).
fof(ord_v2_v4, axiom, less(v2, v4)).
fof(ord_v2_v16, axiom, less(v2, v16)).
fof(ord_v2_v16_5, axiom, less(v2, v16_5)).
fof(ord_v2_v72, axiom, less(v2, v72)).
fof(ord_v2_v72_5, axiom, less(v2, v72_5)).
fof(ord_v2_v480, axiom, less(v2, v480)).
fof(ord_v2_v480_5, axiom, less(v2, v480_5)).
fof(ord_v2_v600, axiom, less(v2, v600)).
fof(ord_v2_v600_5, axiom, less(v2, v600_5)).
fof(ord_v3_v4, axiom, less(v3, v4)).
fof(ord_v3_v16, axiom, less(v3, v16)).
fof(ord_v3_v16_5, axiom, less(v3, v16_5)).
fof(ord_v3_v72, axiom, less(v3, v72)).
fof(ord_v3_v72_5, axiom, less(v3, v72_5)).
fof(ord_v3_v480, axiom, less(v3, v480)).
fof(ord_v3_v480_5, axiom, less(v3, v480_5)).
fof(ord_v3_v600, axiom, less(v3, v600)).
fof(ord_v3_v600_5, axiom, less(v3, v600_5)).
fof(ord_v4_v16, axiom, less(v4, v16)).
fof(ord_v4_v16_5, axiom, less(v4, v16_5)).
fof(ord_v4_v72, axiom, less(v4, v72)).
fof(ord_v4_v72_5, axiom, less(v4, v72_5)).
fof(ord_v4_v480, axiom, less(v4, v480)).
fof(ord_v4_v480_5, axiom, less(v4, v480_5)).
fof(ord_v4_v600, axiom, less(v4, v600)).
fof(ord_v4_v600_5, axiom, less(v4, v600_5)).
fof(ord_v16_v16_5, axiom, less(v16, v16_5)).
fof(ord_v16_v72, axiom, less(v16, v72)).
fof(ord_v16_v72_5, axiom, less(v16, v72_5)).
fof(ord_v16_v480, axiom, less(v16, v480)).
fof(ord_v16_v480_5, axiom, less(v16, v480_5)).
fof(ord_v16_v600, axiom, less(v16, v600)).
fof(ord_v16_v600_5, axiom, less(v16, v600_5)).
fof(ord_v16_5_v72, axiom, less(v16_5, v72)).
fof(ord_v16_5_v72_5, axiom, less(v16_5, v72_5)).
fof(ord_v16_5_v480, axiom, less(v16_5, v480)).
fof(ord_v16_5_v480_5, axiom, less(v16_5, v480_5)).
fof(ord_v16_5_v600, axiom, less(v16_5, v600)).
fof(ord_v16_5_v600_5, axiom, less(v16_5, v600_5)).
fof(ord_v72_v72_5, axiom, less(v72, v72_5)).
fof(ord_v72_v480, axiom, less(v72, v480)).
fof(ord_v72_v480_5, axiom, less(v72, v480_5)).
fof(ord_v72_v600, axiom, less(v72, v600)).
fof(ord_v72_v600_5, axiom, less(v72, v600_5)).
fof(ord_v72_5_v480, axiom, less(v72_5, v480)).
fof(ord_v72_5_v480_5, axiom, less(v72_5, v480_5)).
fof(ord_v72_5_v600, axiom, less(v72_5, v600)).
fof(ord_v72_5_v600_5, axiom, less(v72_5, v600_5)).
fof(ord_v480_v480_5, axiom, less(v480, v480_5)).
fof(ord_v480_v600, axiom, less(v480, v600)).
fof(ord_v480_v600_5, axiom, less(v480, v600_5)).
fof(ord_v480_5_v600, axiom, less(v480_5, v600)).
fof(ord_v480_5_v600_5, axiom, less(v480_5, v600_5)).
fof(ord_v600_v600_5, axiom, less(v600, v600_5)).
fof(distinct, axiom, $distinct(v1, v2, v3, v4, v16, v16_5, v72, v72_5, v480, v480_5, v600, v600_5)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl413, conjecture,
    ?[X,Y,Z,W]: (in_lopen(X, v1, v600_5) & leq(v600, X) &
          in_lopen(Y, v2, v480_5) & leq(v480, Y) &
          in_lopen(Z, v3, v16_5) & leq(v16, Z) &
          in_lopen(W, v4, v72_5) & leq(v72, W))).
%--------------------------------------------------------------------------
