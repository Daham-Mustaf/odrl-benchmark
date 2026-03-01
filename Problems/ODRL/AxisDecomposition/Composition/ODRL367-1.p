%--------------------------------------------------------------------------
% File     : ODRL367-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : SD vs 4K width conflict, other 3 axes compatible
% Expected : Theorem
% Verdict  : Conflict
% Category : Composition
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
%         odrl:rightOperand "640"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "1080"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeDepth ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "48"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand odrl:resolution ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "600"^^xsd:decimal ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeWidth ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "1920"^^xsd:decimal ] ;
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
%         odrl:rightOperand "150"^^xsd:decimal ] ] .
%
% Formal   : width lteq 640  →  (0, 640]
%            width gteq 1920  →  [1920, ∞)
%            (0, 640] ∩ [1920, ∞) ∅  →  Conflict
% Notes    : Same 8 constants as ODRL366, but width now conflicts.
%
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_axis_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v16, axiom, val(v16)).
fof(val_v48, axiom, val(v48)).
fof(val_v150, axiom, val(v150)).
fof(val_v480, axiom, val(v480)).
fof(val_v600, axiom, val(v600)).
fof(val_v640, axiom, val(v640)).
fof(val_v1080, axiom, val(v1080)).
fof(val_v1920, axiom, val(v1920)).
fof(ord_v0_v16, axiom, less(v0, v16)).
fof(ord_v0_v48, axiom, less(v0, v48)).
fof(ord_v0_v150, axiom, less(v0, v150)).
fof(ord_v0_v480, axiom, less(v0, v480)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v640, axiom, less(v0, v640)).
fof(ord_v0_v1080, axiom, less(v0, v1080)).
fof(ord_v0_v1920, axiom, less(v0, v1920)).
fof(ord_v16_v48, axiom, less(v16, v48)).
fof(ord_v16_v150, axiom, less(v16, v150)).
fof(ord_v16_v480, axiom, less(v16, v480)).
fof(ord_v16_v600, axiom, less(v16, v600)).
fof(ord_v16_v640, axiom, less(v16, v640)).
fof(ord_v16_v1080, axiom, less(v16, v1080)).
fof(ord_v16_v1920, axiom, less(v16, v1920)).
fof(ord_v48_v150, axiom, less(v48, v150)).
fof(ord_v48_v480, axiom, less(v48, v480)).
fof(ord_v48_v600, axiom, less(v48, v600)).
fof(ord_v48_v640, axiom, less(v48, v640)).
fof(ord_v48_v1080, axiom, less(v48, v1080)).
fof(ord_v48_v1920, axiom, less(v48, v1920)).
fof(ord_v150_v480, axiom, less(v150, v480)).
fof(ord_v150_v600, axiom, less(v150, v600)).
fof(ord_v150_v640, axiom, less(v150, v640)).
fof(ord_v150_v1080, axiom, less(v150, v1080)).
fof(ord_v150_v1920, axiom, less(v150, v1920)).
fof(ord_v480_v600, axiom, less(v480, v600)).
fof(ord_v480_v640, axiom, less(v480, v640)).
fof(ord_v480_v1080, axiom, less(v480, v1080)).
fof(ord_v480_v1920, axiom, less(v480, v1920)).
fof(ord_v600_v640, axiom, less(v600, v640)).
fof(ord_v600_v1080, axiom, less(v600, v1080)).
fof(ord_v600_v1920, axiom, less(v600, v1920)).
fof(ord_v640_v1080, axiom, less(v640, v1080)).
fof(ord_v640_v1920, axiom, less(v640, v1920)).
fof(ord_v1080_v1920, axiom, less(v1080, v1920)).
fof(distinct, axiom, $distinct(v0, v16, v48, v150, v480, v600, v640, v1080, v1920)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl367, conjecture,
    ~?[X,Y,Z,W]: (in_lopen(X, v0, v640) & leq(v1920, X) &
          in_lopen(Y, v0, v1080) & leq(v480, Y) &
          in_lopen(Z, v0, v48) & leq(v16, Z) &
          in_lopen(W, v0, v600) & leq(v150, W))).
%--------------------------------------------------------------------------
