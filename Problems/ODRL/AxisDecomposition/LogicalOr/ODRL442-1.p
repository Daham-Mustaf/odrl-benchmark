%--------------------------------------------------------------------------
% File     : ODRL442-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : AND(A)×OR(B): B's height arm saves width mismatch
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
%         odrl:leftOperand oax:absoluteSizeWidth ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "800"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "600"^^xsd:decimal ] ;
%     ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         a odrl:LogicalConstraint ;
%         odrl:or (
%           [ odrl:leftOperand oax:absoluteSizeWidth ;
%             odrl:operator odrl:gteq ;
%             odrl:rightOperand "1000"^^xsd:decimal ]
%           [ odrl:leftOperand oax:absoluteSizeHeight ;
%             odrl:operator odrl:gteq ;
%             odrl:rightOperand "200"^^xsd:decimal ]
%         )
%       ]
%     ] .
%
% Formal   : width lteq 800  →  (0, 800]
%            width gteq 1000  →  [1000, ∞)
%            (0, 800] ∩ [1000, ∞) ≠ ∅  →  Compatible
% Notes    : Witness: (400, 300). A: w≤800 ✓, h≤600 ✓. B(OR): w≥1000? No, but h≥200 ✓.
% Connect. : Policy A = AND (implicit)
%            Policy B = odrl:or
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
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(val_v1000, axiom, val(v1000)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v0_v1000, axiom, less(v0, v1000)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v200_v1000, axiom, less(v200, v1000)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(ord_v600_v1000, axiom, less(v600, v1000)).
fof(ord_v800_v1000, axiom, less(v800, v1000)).
fof(distinct, axiom, $distinct(v0, v200, v600, v800, v1000)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl442, conjecture,
    ?[X,Y]: ((in_lopen(X, v0, v800) & in_lopen(Y, v0, v600)) &
          (leq(v1000, X) | leq(v200, Y)))).
%--------------------------------------------------------------------------
