%--------------------------------------------------------------------------
% File     : ODRL408-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : ★★★★☆ Hard: 4 axes, 9 constants, gap=1 on width
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
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "599"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "1080"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeDepth ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "32"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand odrl:resolution ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "300"^^xsd:decimal ] ;
%     ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeWidth ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "601"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "480"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeDepth ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "8"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand odrl:resolution ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "72"^^xsd:decimal ] ;
%     ] .
%
% Formal   : width lteq 599  →  (0, 599]
%            width gteq 601  →  [601, ∞)
%            (0, 599] ∩ [601, ∞) ∅  →  Conflict
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
fof(val_v72, axiom, val(v72)).
fof(val_v300, axiom, val(v300)).
fof(val_v480, axiom, val(v480)).
fof(val_v599, axiom, val(v599)).
fof(val_v601, axiom, val(v601)).
fof(val_v1080, axiom, val(v1080)).
fof(ord_v0_v8, axiom, less(v0, v8)).
fof(ord_v0_v32, axiom, less(v0, v32)).
fof(ord_v0_v72, axiom, less(v0, v72)).
fof(ord_v0_v300, axiom, less(v0, v300)).
fof(ord_v0_v480, axiom, less(v0, v480)).
fof(ord_v0_v599, axiom, less(v0, v599)).
fof(ord_v0_v601, axiom, less(v0, v601)).
fof(ord_v0_v1080, axiom, less(v0, v1080)).
fof(ord_v8_v32, axiom, less(v8, v32)).
fof(ord_v8_v72, axiom, less(v8, v72)).
fof(ord_v8_v300, axiom, less(v8, v300)).
fof(ord_v8_v480, axiom, less(v8, v480)).
fof(ord_v8_v599, axiom, less(v8, v599)).
fof(ord_v8_v601, axiom, less(v8, v601)).
fof(ord_v8_v1080, axiom, less(v8, v1080)).
fof(ord_v32_v72, axiom, less(v32, v72)).
fof(ord_v32_v300, axiom, less(v32, v300)).
fof(ord_v32_v480, axiom, less(v32, v480)).
fof(ord_v32_v599, axiom, less(v32, v599)).
fof(ord_v32_v601, axiom, less(v32, v601)).
fof(ord_v32_v1080, axiom, less(v32, v1080)).
fof(ord_v72_v300, axiom, less(v72, v300)).
fof(ord_v72_v480, axiom, less(v72, v480)).
fof(ord_v72_v599, axiom, less(v72, v599)).
fof(ord_v72_v601, axiom, less(v72, v601)).
fof(ord_v72_v1080, axiom, less(v72, v1080)).
fof(ord_v300_v480, axiom, less(v300, v480)).
fof(ord_v300_v599, axiom, less(v300, v599)).
fof(ord_v300_v601, axiom, less(v300, v601)).
fof(ord_v300_v1080, axiom, less(v300, v1080)).
fof(ord_v480_v599, axiom, less(v480, v599)).
fof(ord_v480_v601, axiom, less(v480, v601)).
fof(ord_v480_v1080, axiom, less(v480, v1080)).
fof(ord_v599_v601, axiom, less(v599, v601)).
fof(ord_v599_v1080, axiom, less(v599, v1080)).
fof(ord_v601_v1080, axiom, less(v601, v1080)).
fof(distinct, axiom, $distinct(v0, v8, v32, v72, v300, v480, v599, v601, v1080)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl408, conjecture,
    ~?[X,Y,Z,W]: (in_lopen(X, v0, v599) & leq(v601, X) &
          in_lopen(Y, v0, v1080) & leq(v480, Y) &
          in_lopen(Z, v0, v32) & leq(v8, Z) &
          in_lopen(W, v0, v300) & leq(v72, W))).
%--------------------------------------------------------------------------
