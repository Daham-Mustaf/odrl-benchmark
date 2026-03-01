%--------------------------------------------------------------------------
% File     : ODRL415-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : ★★★★★ Very Hard: 12 constants, 4-axis tight subsumption (margin=1)
% Expected : Theorem
% Verdict  : Subsumes
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
%         odrl:rightOperand "599.5"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "479.5"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeDepth ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "15.5"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand odrl:resolution ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "71.5"^^xsd:decimal ] ;
%     ] .
%
%   ex:policyB a odrl:Set ;
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
% Formal   : (1, 599.5] ⊆ (1, 600.5]
% Notes    : A subset B by margin=1 on each axis. 66 ordering axioms. 4-way De Morgan: all 4 disjuncts must be proven unsatisfiable.
%
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_axis_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v1, axiom, val(v1)).
fof(val_v2, axiom, val(v2)).
fof(val_v3, axiom, val(v3)).
fof(val_v4, axiom, val(v4)).
fof(val_v15_5, axiom, val(v15_5)).
fof(val_v16_5, axiom, val(v16_5)).
fof(val_v71_5, axiom, val(v71_5)).
fof(val_v72_5, axiom, val(v72_5)).
fof(val_v479_5, axiom, val(v479_5)).
fof(val_v480_5, axiom, val(v480_5)).
fof(val_v599_5, axiom, val(v599_5)).
fof(val_v600_5, axiom, val(v600_5)).
fof(ord_v1_v2, axiom, less(v1, v2)).
fof(ord_v1_v3, axiom, less(v1, v3)).
fof(ord_v1_v4, axiom, less(v1, v4)).
fof(ord_v1_v15_5, axiom, less(v1, v15_5)).
fof(ord_v1_v16_5, axiom, less(v1, v16_5)).
fof(ord_v1_v71_5, axiom, less(v1, v71_5)).
fof(ord_v1_v72_5, axiom, less(v1, v72_5)).
fof(ord_v1_v479_5, axiom, less(v1, v479_5)).
fof(ord_v1_v480_5, axiom, less(v1, v480_5)).
fof(ord_v1_v599_5, axiom, less(v1, v599_5)).
fof(ord_v1_v600_5, axiom, less(v1, v600_5)).
fof(ord_v2_v3, axiom, less(v2, v3)).
fof(ord_v2_v4, axiom, less(v2, v4)).
fof(ord_v2_v15_5, axiom, less(v2, v15_5)).
fof(ord_v2_v16_5, axiom, less(v2, v16_5)).
fof(ord_v2_v71_5, axiom, less(v2, v71_5)).
fof(ord_v2_v72_5, axiom, less(v2, v72_5)).
fof(ord_v2_v479_5, axiom, less(v2, v479_5)).
fof(ord_v2_v480_5, axiom, less(v2, v480_5)).
fof(ord_v2_v599_5, axiom, less(v2, v599_5)).
fof(ord_v2_v600_5, axiom, less(v2, v600_5)).
fof(ord_v3_v4, axiom, less(v3, v4)).
fof(ord_v3_v15_5, axiom, less(v3, v15_5)).
fof(ord_v3_v16_5, axiom, less(v3, v16_5)).
fof(ord_v3_v71_5, axiom, less(v3, v71_5)).
fof(ord_v3_v72_5, axiom, less(v3, v72_5)).
fof(ord_v3_v479_5, axiom, less(v3, v479_5)).
fof(ord_v3_v480_5, axiom, less(v3, v480_5)).
fof(ord_v3_v599_5, axiom, less(v3, v599_5)).
fof(ord_v3_v600_5, axiom, less(v3, v600_5)).
fof(ord_v4_v15_5, axiom, less(v4, v15_5)).
fof(ord_v4_v16_5, axiom, less(v4, v16_5)).
fof(ord_v4_v71_5, axiom, less(v4, v71_5)).
fof(ord_v4_v72_5, axiom, less(v4, v72_5)).
fof(ord_v4_v479_5, axiom, less(v4, v479_5)).
fof(ord_v4_v480_5, axiom, less(v4, v480_5)).
fof(ord_v4_v599_5, axiom, less(v4, v599_5)).
fof(ord_v4_v600_5, axiom, less(v4, v600_5)).
fof(ord_v15_5_v16_5, axiom, less(v15_5, v16_5)).
fof(ord_v15_5_v71_5, axiom, less(v15_5, v71_5)).
fof(ord_v15_5_v72_5, axiom, less(v15_5, v72_5)).
fof(ord_v15_5_v479_5, axiom, less(v15_5, v479_5)).
fof(ord_v15_5_v480_5, axiom, less(v15_5, v480_5)).
fof(ord_v15_5_v599_5, axiom, less(v15_5, v599_5)).
fof(ord_v15_5_v600_5, axiom, less(v15_5, v600_5)).
fof(ord_v16_5_v71_5, axiom, less(v16_5, v71_5)).
fof(ord_v16_5_v72_5, axiom, less(v16_5, v72_5)).
fof(ord_v16_5_v479_5, axiom, less(v16_5, v479_5)).
fof(ord_v16_5_v480_5, axiom, less(v16_5, v480_5)).
fof(ord_v16_5_v599_5, axiom, less(v16_5, v599_5)).
fof(ord_v16_5_v600_5, axiom, less(v16_5, v600_5)).
fof(ord_v71_5_v72_5, axiom, less(v71_5, v72_5)).
fof(ord_v71_5_v479_5, axiom, less(v71_5, v479_5)).
fof(ord_v71_5_v480_5, axiom, less(v71_5, v480_5)).
fof(ord_v71_5_v599_5, axiom, less(v71_5, v599_5)).
fof(ord_v71_5_v600_5, axiom, less(v71_5, v600_5)).
fof(ord_v72_5_v479_5, axiom, less(v72_5, v479_5)).
fof(ord_v72_5_v480_5, axiom, less(v72_5, v480_5)).
fof(ord_v72_5_v599_5, axiom, less(v72_5, v599_5)).
fof(ord_v72_5_v600_5, axiom, less(v72_5, v600_5)).
fof(ord_v479_5_v480_5, axiom, less(v479_5, v480_5)).
fof(ord_v479_5_v599_5, axiom, less(v479_5, v599_5)).
fof(ord_v479_5_v600_5, axiom, less(v479_5, v600_5)).
fof(ord_v480_5_v599_5, axiom, less(v480_5, v599_5)).
fof(ord_v480_5_v600_5, axiom, less(v480_5, v600_5)).
fof(ord_v599_5_v600_5, axiom, less(v599_5, v600_5)).
fof(distinct, axiom, $distinct(v1, v2, v3, v4, v15_5, v16_5, v71_5, v72_5, v479_5, v480_5, v599_5, v600_5)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl415, conjecture,
    ![X,Y,Z,W]: ((in_lopen(X, v1, v599_5) & in_lopen(Y, v2, v479_5) & in_lopen(Z, v3, v15_5) & in_lopen(W, v4, v71_5)) => (in_lopen(X, v1, v600_5) & in_lopen(Y, v2, v480_5) & in_lopen(Z, v3, v16_5) & in_lopen(W, v4, v72_5)))).
%--------------------------------------------------------------------------
