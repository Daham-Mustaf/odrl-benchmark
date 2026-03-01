%--------------------------------------------------------------------------
% File     : ODRL420-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : P1: ≤v ∧ ≥v → touch at v=600 → Compatible
% Expected : Theorem
% Verdict  : Compatible
% Category : Boundary
% Difficulty: Easy
%
% ODRL Policy (Turtle):
%   @prefix odrl: <http://www.w3.org/ns/odrl/2/> .
%   @prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
%   @prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
%   @prefix ex:   <https://example.org/> .
%
%   ex:policyA a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeWidth ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "600"^^xsd:decimal ] ;
%     ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeWidth ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "600"^^xsd:decimal ] ;
%     ] .
%
% Formal   : width lteq 600  →  (0, 600]
%            width gteq 600  →  [600, ∞)
%            (0, 600] ∩ [600, ∞) ≠ ∅  →  Compatible
% Notes    : Witness: X=600. The simplest boundary case.
%
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_axis_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(distinct, axiom, $distinct(v0, v600)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl420, conjecture,
    ?[X]: (in_lopen(X, v0, v600) & leq(v600, X))).
%--------------------------------------------------------------------------
