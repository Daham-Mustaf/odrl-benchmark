%--------------------------------------------------------------------------
% File     : ODRL304-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : width ≤ 600 vs width ≥ 200: overlapping intervals
% Expected : Theorem
% Verdict  : Compatible
% Category : SingleAxis
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
%         odrl:rightOperand "600"^^xsd:decimal ;
%         odrl:unit <http://dbpedia.org/resource/Pixel> ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeWidth ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "200"^^xsd:decimal ;
%         odrl:unit <http://dbpedia.org/resource/Pixel> ] ] .
%
% Formal   : width lteq 600  →  (0, 600]
%            width gteq 200  →  [200, ∞)
%            (0, 600] ∩ [200, ∞) ≠ ∅  →  Compatible
%
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_axis_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v200, axiom, val(v200)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(distinct, axiom, $distinct(v0, v200, v600)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl304, conjecture,
    ?[X]: (in_lopen(X, v0, v600) & leq(v200, X))).
%--------------------------------------------------------------------------
