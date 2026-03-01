%--------------------------------------------------------------------------
% File     : ODRL445-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : 3-axis OR(A)×AND(B): all 3 OR-arms fail → Conflict
% Expected : Theorem
% Verdict  : Conflict
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
%             odrl:rightOperand "50"^^xsd:decimal ]
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
%         odrl:rightOperand "400"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "200"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeDepth ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "100"^^xsd:decimal ] ;
%     ] .
%
% Formal   : width lteq 200  →  (0, 200]
%            width gteq 400  →  [400, ∞)
%            (0, 200] ∩ [400, ∞) ∅  →  Conflict
% Notes    : 3-way OR: (w≤200 | h≤100 | d≤50) vs AND(w≥400, h≥200, d≥100). Each arm individually disjoint from B.
% Connect. : Policy A = odrl:or
%            Policy B = AND (implicit)
%
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_axis_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v50, axiom, val(v50)).
fof(val_v100, axiom, val(v100)).
fof(val_v200, axiom, val(v200)).
fof(val_v400, axiom, val(v400)).
fof(ord_v0_v50, axiom, less(v0, v50)).
fof(ord_v0_v100, axiom, less(v0, v100)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v50_v100, axiom, less(v50, v100)).
fof(ord_v50_v200, axiom, less(v50, v200)).
fof(ord_v50_v400, axiom, less(v50, v400)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v400, axiom, less(v100, v400)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(distinct, axiom, $distinct(v0, v50, v100, v200, v400)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl445, conjecture,
    ~?[X,Y,Z]: ((in_lopen(X, v0, v200) | in_lopen(Y, v0, v100) | in_lopen(Z, v0, v50)) &
          (leq(v400, X) & leq(v200, Y) & leq(v100, Z)))).
%--------------------------------------------------------------------------
