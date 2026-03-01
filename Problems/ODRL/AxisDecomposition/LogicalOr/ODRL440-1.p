%--------------------------------------------------------------------------
% File     : ODRL440-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : OR(A)×AND(B): height arm rescues width conflict
% Expected : Theorem
% Verdict  : Compatible
% Category : LogicalOr
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
%         a odrl:LogicalConstraint ;
%         odrl:or (
%           [ odrl:leftOperand oax:absoluteSizeWidth ;
%             odrl:operator odrl:lteq ;
%             odrl:rightOperand "400"^^xsd:decimal ]
%           [ odrl:leftOperand oax:absoluteSizeHeight ;
%             odrl:operator odrl:lteq ;
%             odrl:rightOperand "800"^^xsd:decimal ]
%         )
%       ]
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
%         odrl:rightOperand "200"^^xsd:decimal ] ;
%     ] .
%
% Formal   : width lteq 400  →  (0, 400]
%            width gteq 600  →  [600, ∞)
%            (0, 400] ∩ [600, ∞) ≠ ∅  →  Compatible
% Notes    : Width arm conflicts but height arm ≤800 overlaps ≥200. Witness: (600, 300). With AND(A), this would be Conflict.
% Connect. : Policy A = odrl:or
%            Policy B = AND (implicit)
%
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_axis_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/AXIS000-0.ax').
include('Axioms/Layer0-DomainKB/ORD001-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v200, axiom, val(v200)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v200, v400, v600, v800)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl440, conjecture,
    ?[X,Y]: ((in_lopen(X, v0, v400) | in_lopen(Y, v0, v800)) &
          (leq(v600, X) & leq(v200, Y)))).
%--------------------------------------------------------------------------
