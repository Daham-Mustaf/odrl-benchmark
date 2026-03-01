%--------------------------------------------------------------------------
% File     : ODRL449-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : 3-axis OR×OR: cross-combination → Compatible
% Expected : Theorem
% Verdict  : Compatible
% Category : LogicalOr
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
%         a odrl:LogicalConstraint ;
%         odrl:or (
%           [ odrl:leftOperand oax:absoluteSizeWidth ;
%             odrl:operator odrl:lteq ;
%             odrl:rightOperand "200"^^xsd:decimal ]
%           [ odrl:leftOperand oax:absoluteSizeHeight ;
%             odrl:operator odrl:lteq ;
%             odrl:rightOperand "100"^^xsd:decimal ]
%           [ odrl:leftOperand oax:absoluteSizeDepth ;
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
%         a odrl:LogicalConstraint ;
%         odrl:or (
%           [ odrl:leftOperand oax:absoluteSizeWidth ;
%             odrl:operator odrl:gteq ;
%             odrl:rightOperand "400"^^xsd:decimal ]
%           [ odrl:leftOperand oax:absoluteSizeHeight ;
%             odrl:operator odrl:gteq ;
%             odrl:rightOperand "200"^^xsd:decimal ]
%           [ odrl:leftOperand oax:absoluteSizeDepth ;
%             odrl:operator odrl:gteq ;
%             odrl:rightOperand "300"^^xsd:decimal ]
%         )
%       ]
%     ] .
%
% Formal   : width lteq 200  →  (0, 200]
%            width gteq 400  →  [400, ∞)
%            (0, 200] ∩ [400, ∞) ≠ ∅  →  Compatible
% Notes    : Width and height arms all conflict pairwise, but A's depth arm (≤800) × B's depth arm (≥300): witness (400, 200, 500).
% Connect. : Policy A = odrl:or
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
fof(val_v100, axiom, val(v100)).
fof(val_v200, axiom, val(v200)).
fof(val_v300, axiom, val(v300)).
fof(val_v400, axiom, val(v400)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v100, axiom, less(v0, v100)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v300, axiom, less(v0, v300)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v300, axiom, less(v100, v300)).
fof(ord_v100_v400, axiom, less(v100, v400)).
fof(ord_v100_v800, axiom, less(v100, v800)).
fof(ord_v200_v300, axiom, less(v200, v300)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v300_v400, axiom, less(v300, v400)).
fof(ord_v300_v800, axiom, less(v300, v800)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(distinct, axiom, $distinct(v0, v100, v200, v300, v400, v800)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl449, conjecture,
    ?[X,Y,Z]: ((in_lopen(X, v0, v200) | in_lopen(Y, v0, v100) | in_lopen(Z, v0, v800)) &
          (leq(v400, X) | leq(v200, Y) | leq(v300, Z)))).
%--------------------------------------------------------------------------
