%--------------------------------------------------------------------------
% File     : ODRL410-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : ★★★★☆ Hard: 4-axis De Morgan subsumption, 8 constants
% Expected : Theorem
% Verdict  : Subsumes
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
%         odrl:rightOperand "600"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "400"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeDepth ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "16"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand odrl:resolution ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "150"^^xsd:decimal ] ;
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
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "1080"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeDepth ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "48"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand odrl:resolution ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "600"^^xsd:decimal ] ;
%     ] .
%
% Formal   : (0, 600] ⊆ (0, 1920]
% Notes    : 4-way De Morgan: (or not-w not-h not-d not-r). All branches unsat.
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
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(val_v1080, axiom, val(v1080)).
fof(val_v1920, axiom, val(v1920)).
fof(ord_v0_v16, axiom, less(v0, v16)).
fof(ord_v0_v48, axiom, less(v0, v48)).
fof(ord_v0_v150, axiom, less(v0, v150)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v1080, axiom, less(v0, v1080)).
fof(ord_v0_v1920, axiom, less(v0, v1920)).
fof(ord_v16_v48, axiom, less(v16, v48)).
fof(ord_v16_v150, axiom, less(v16, v150)).
fof(ord_v16_v400, axiom, less(v16, v400)).
fof(ord_v16_v600, axiom, less(v16, v600)).
fof(ord_v16_v1080, axiom, less(v16, v1080)).
fof(ord_v16_v1920, axiom, less(v16, v1920)).
fof(ord_v48_v150, axiom, less(v48, v150)).
fof(ord_v48_v400, axiom, less(v48, v400)).
fof(ord_v48_v600, axiom, less(v48, v600)).
fof(ord_v48_v1080, axiom, less(v48, v1080)).
fof(ord_v48_v1920, axiom, less(v48, v1920)).
fof(ord_v150_v400, axiom, less(v150, v400)).
fof(ord_v150_v600, axiom, less(v150, v600)).
fof(ord_v150_v1080, axiom, less(v150, v1080)).
fof(ord_v150_v1920, axiom, less(v150, v1920)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v400_v1080, axiom, less(v400, v1080)).
fof(ord_v400_v1920, axiom, less(v400, v1920)).
fof(ord_v600_v1080, axiom, less(v600, v1080)).
fof(ord_v600_v1920, axiom, less(v600, v1920)).
fof(ord_v1080_v1920, axiom, less(v1080, v1920)).
fof(distinct, axiom, $distinct(v0, v16, v48, v150, v400, v600, v1080, v1920)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl410, conjecture,
    ![X,Y,Z,W]: ((in_lopen(X, v0, v600) & in_lopen(Y, v0, v400) & in_lopen(Z, v0, v16) & in_lopen(W, v0, v150)) => (in_lopen(X, v0, v1920) & in_lopen(Y, v0, v1080) & in_lopen(Z, v0, v48) & in_lopen(W, v0, v600)))).
%--------------------------------------------------------------------------
