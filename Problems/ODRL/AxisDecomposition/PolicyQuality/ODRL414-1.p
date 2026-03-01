%--------------------------------------------------------------------------
% File     : ODRL414-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : ★★★★★ Very Hard: all 5 ops, 4-axis De Morgan refutation
% Expected : Theorem
% Verdict  : Refuted
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
%       odrl:constraint [
%         odrl:leftOperand odrl:resolution ;
%         odrl:operator odrl:lt ;
%         odrl:rightOperand "300"^^xsd:decimal ] ;
%     ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeWidth ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "1920"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:lt ;
%         odrl:rightOperand "1080"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeDepth ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "48"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand odrl:resolution ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "72"^^xsd:decimal ] ;
%     ] .
%
% Formal   : [600, 600] ⊄ (1, 1920]
% Notes    : All 5 ops (eq, gt, gteq, lt, lteq). De Morgan: (or not-w not-h not-d not-r). Counterexample: (600, 301, 16, 50) — res 50 < 72.
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
fof(val_v48, axiom, val(v48)).
fof(val_v72, axiom, val(v72)).
fof(val_v300, axiom, val(v300)).
fof(val_v600, axiom, val(v600)).
fof(val_v1080, axiom, val(v1080)).
fof(val_v1920, axiom, val(v1920)).
fof(ord_v1_v2, axiom, less(v1, v2)).
fof(ord_v1_v3, axiom, less(v1, v3)).
fof(ord_v1_v4, axiom, less(v1, v4)).
fof(ord_v1_v16, axiom, less(v1, v16)).
fof(ord_v1_v48, axiom, less(v1, v48)).
fof(ord_v1_v72, axiom, less(v1, v72)).
fof(ord_v1_v300, axiom, less(v1, v300)).
fof(ord_v1_v600, axiom, less(v1, v600)).
fof(ord_v1_v1080, axiom, less(v1, v1080)).
fof(ord_v1_v1920, axiom, less(v1, v1920)).
fof(ord_v2_v3, axiom, less(v2, v3)).
fof(ord_v2_v4, axiom, less(v2, v4)).
fof(ord_v2_v16, axiom, less(v2, v16)).
fof(ord_v2_v48, axiom, less(v2, v48)).
fof(ord_v2_v72, axiom, less(v2, v72)).
fof(ord_v2_v300, axiom, less(v2, v300)).
fof(ord_v2_v600, axiom, less(v2, v600)).
fof(ord_v2_v1080, axiom, less(v2, v1080)).
fof(ord_v2_v1920, axiom, less(v2, v1920)).
fof(ord_v3_v4, axiom, less(v3, v4)).
fof(ord_v3_v16, axiom, less(v3, v16)).
fof(ord_v3_v48, axiom, less(v3, v48)).
fof(ord_v3_v72, axiom, less(v3, v72)).
fof(ord_v3_v300, axiom, less(v3, v300)).
fof(ord_v3_v600, axiom, less(v3, v600)).
fof(ord_v3_v1080, axiom, less(v3, v1080)).
fof(ord_v3_v1920, axiom, less(v3, v1920)).
fof(ord_v4_v16, axiom, less(v4, v16)).
fof(ord_v4_v48, axiom, less(v4, v48)).
fof(ord_v4_v72, axiom, less(v4, v72)).
fof(ord_v4_v300, axiom, less(v4, v300)).
fof(ord_v4_v600, axiom, less(v4, v600)).
fof(ord_v4_v1080, axiom, less(v4, v1080)).
fof(ord_v4_v1920, axiom, less(v4, v1920)).
fof(ord_v16_v48, axiom, less(v16, v48)).
fof(ord_v16_v72, axiom, less(v16, v72)).
fof(ord_v16_v300, axiom, less(v16, v300)).
fof(ord_v16_v600, axiom, less(v16, v600)).
fof(ord_v16_v1080, axiom, less(v16, v1080)).
fof(ord_v16_v1920, axiom, less(v16, v1920)).
fof(ord_v48_v72, axiom, less(v48, v72)).
fof(ord_v48_v300, axiom, less(v48, v300)).
fof(ord_v48_v600, axiom, less(v48, v600)).
fof(ord_v48_v1080, axiom, less(v48, v1080)).
fof(ord_v48_v1920, axiom, less(v48, v1920)).
fof(ord_v72_v300, axiom, less(v72, v300)).
fof(ord_v72_v600, axiom, less(v72, v600)).
fof(ord_v72_v1080, axiom, less(v72, v1080)).
fof(ord_v72_v1920, axiom, less(v72, v1920)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v300_v1080, axiom, less(v300, v1080)).
fof(ord_v300_v1920, axiom, less(v300, v1920)).
fof(ord_v600_v1080, axiom, less(v600, v1080)).
fof(ord_v600_v1920, axiom, less(v600, v1920)).
fof(ord_v1080_v1920, axiom, less(v1080, v1920)).
fof(distinct, axiom, $distinct(v1, v2, v3, v4, v16, v48, v72, v300, v600, v1080, v1920)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl414, conjecture,
    ?[X,Y,Z,W]: ((in_closed(X, v600, v600) & less(v300, Y) & leq(v16, Z) & in_open(W, v4, v300)) & ~(in_lopen(X, v1, v1920) & in_open(Y, v2, v1080) & in_lopen(Z, v3, v48) & leq(v72, W)))).
%--------------------------------------------------------------------------
