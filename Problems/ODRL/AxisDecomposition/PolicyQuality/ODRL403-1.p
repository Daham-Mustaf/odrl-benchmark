%--------------------------------------------------------------------------
% File     : ODRL403-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : ★★☆☆☆ Easy: 1 axis, simple subsumption
% Expected : Theorem
% Verdict  : Subsumes
% Category : PolicyQuality
% Difficulty: Easy
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
%         odrl:rightOperand "400"^^xsd:decimal ] ;
%     ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeWidth ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "800"^^xsd:decimal ] ;
%     ] .
%
% Formal   : (0, 400] ⊆ (0, 800]
%
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_axis_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v400, axiom, val(v400)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(distinct, axiom, $distinct(v0, v400, v800)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl403, conjecture,
    ![X]: ((in_lopen(X, v0, v400)) => (in_lopen(X, v0, v800)))).
%--------------------------------------------------------------------------
