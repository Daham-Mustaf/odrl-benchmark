%--------------------------------------------------------------------------
% File     : ODRL467-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : AND ⊆ XONE: A-region falls in exactly-one XONE arm
% Expected : Theorem
% Verdict  : Subsumes
% Category : LogicalXone
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
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "800"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "200"^^xsd:decimal ] ;
%     ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         a odrl:LogicalConstraint ;
%         odrl:xone (
%           [ odrl:leftOperand oax:absoluteSizeWidth ;
%             odrl:operator odrl:lteq ;
%             odrl:rightOperand "600"^^xsd:decimal ]
%           [ odrl:leftOperand oax:absoluteSizeHeight ;
%             odrl:operator odrl:lteq ;
%             odrl:rightOperand "400"^^xsd:decimal ]
%         )
%       ]
%     ] .
%
% Formal   : [800, ∞) ⊆ (0, 600]
% Notes    : A: w≥800, h≤200. For XONE: w≤600 FALSE, h≤400 TRUE → exactly one arm. All A-points satisfy B-XONE.
% Connect. : Policy A = AND (implicit)
%            Policy B = odrl:xone
%
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_axis_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/AXIS000-0.ax').

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
fof(odrl467, conjecture,
    ![X,Y]: ((leq(v800, X) & in_lopen(Y, v0, v200)) => ((in_lopen(X, v0, v600) & ~(in_lopen(Y, v0, v400))) |
              (~(in_lopen(X, v0, v600)) & in_lopen(Y, v0, v400))))).
%--------------------------------------------------------------------------
