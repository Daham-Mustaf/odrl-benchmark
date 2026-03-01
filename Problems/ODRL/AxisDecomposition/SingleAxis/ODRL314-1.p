%--------------------------------------------------------------------------
% File     : ODRL314-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : BSB running example: height ≤ 600 vs height ≥ 400
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
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "600"^^xsd:decimal ;
%         odrl:unit <http://dbpedia.org/resource/Pixel> ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "400"^^xsd:decimal ;
%         odrl:unit <http://dbpedia.org/resource/Pixel> ] ] .
%
% Formal   : height lteq 600  →  (0, 600]
%            height gteq 400  →  [400, ∞)
%            (0, 600] ∩ [400, ∞) ≠ ∅  →  Compatible
%
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_axis_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct, axiom, $distinct(v0, v400, v600)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl314, conjecture,
    ?[X]: (in_lopen(X, v0, v600) & leq(v400, X))).
%--------------------------------------------------------------------------
