%--------------------------------------------------------------------------
% File     : ODRL426-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : P7: =v ∧ <v → v ∉ (0,v) → Conflict
% Expected : Theorem
% Verdict  : Conflict
% Category : Boundary
% Difficulty: Medium
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
%         odrl:operator odrl:eq ;
%         odrl:rightOperand "600"^^xsd:decimal ] ;
%     ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeWidth ;
%         odrl:operator odrl:lt ;
%         odrl:rightOperand "600"^^xsd:decimal ] ;
%     ] .
%
% Formal   : width eq 600  →  [600, 600]
%            width lt 600  →  (0, 600)
%            [600, 600] ∩ (0, 600) ∅  →  Conflict
% Notes    : {600} ∩ (0,600) = ∅. The strict < excludes the point.
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
fof(odrl426, conjecture,
    ~?[X]: (in_closed(X, v600, v600) & in_open(X, v0, v600))).
%--------------------------------------------------------------------------
