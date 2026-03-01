%--------------------------------------------------------------------------
% File     : ODRL431-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : Axis 1 touches but axis 2 open gap → Conflict
% Expected : Theorem
% Verdict  : Conflict
% Category : Boundary
% Difficulty: Hard
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
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:lt ;
%         odrl:rightOperand "400"^^xsd:decimal ] ;
%     ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeWidth ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "600"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "400"^^xsd:decimal ] ;
%     ] .
%
% Formal   : width lteq 600  →  (0, 600]
%            width gteq 600  →  [600, ∞)
%            (0, 600] ∩ [600, ∞) ∅  →  Conflict
% Notes    : Width compatible at boundary, but height open/closed gap kills the box.
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
fof(odrl431, conjecture,
    ~?[X,Y]: (in_lopen(X, v0, v600) & leq(v600, X) &
          in_open(Y, v0, v400) & leq(v400, Y))).
%--------------------------------------------------------------------------
