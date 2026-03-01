%--------------------------------------------------------------------------
% File     : ODRL401-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : ★☆☆☆☆ Trivial: 1 axis, 3 constants, wide overlap
% Expected : Theorem
% Verdict  : Compatible
% Category : PolicyQuality
% Difficulty: Trivial
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
%         odrl:rightOperand "800"^^xsd:decimal ] ;
%     ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeWidth ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "200"^^xsd:decimal ] ;
%     ] .
%
% Formal   : width lteq 800  →  (0, 800]
%            width gteq 200  →  [200, ∞)
%            (0, 800] ∩ [200, ∞) ≠ ∅  →  Compatible
%
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_axis_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v200, axiom, val(v200)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(distinct, axiom, $distinct(v0, v200, v800)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl401, conjecture,
    ?[X]: (in_lopen(X, v0, v800) & leq(v200, X))).
%--------------------------------------------------------------------------
