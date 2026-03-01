%--------------------------------------------------------------------------
% File     : ODRL465-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : 3-axis XONE(A)×AND(B): B in all-hold zone → Conflict
% Expected : Theorem
% Verdict  : Conflict
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
%         a odrl:LogicalConstraint ;
%         odrl:xone (
%           [ odrl:leftOperand oax:absoluteSizeWidth ;
%             odrl:operator odrl:lteq ;
%             odrl:rightOperand "600"^^xsd:decimal ]
%           [ odrl:leftOperand oax:absoluteSizeHeight ;
%             odrl:operator odrl:lteq ;
%             odrl:rightOperand "400"^^xsd:decimal ]
%           [ odrl:leftOperand oax:absoluteSizeDepth ;
%             odrl:operator odrl:lteq ;
%             odrl:rightOperand "200"^^xsd:decimal ]
%         )
%       ]
%     ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeWidth ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "400"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "200"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeDepth ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "100"^^xsd:decimal ] ;
%     ] .
%
% Formal   : width lteq 600  →  (0, 600]
%            width lteq 400  →  (0, 400]
%            (0, 600] ∩ (0, 400] ∅  →  Conflict
% Notes    : B (w≤400, h≤200, d≤100) ⊂ all three XONE arms (w≤600 ✓, h≤400 ✓, d≤200 ✓) → three hold → XONE=false.
% Connect. : Policy A = odrl:xone
%            Policy B = AND (implicit)
%
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_axis_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v100, axiom, val(v100)).
fof(val_v200, axiom, val(v200)).
fof(val_v400, axiom, val(v400)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v100, axiom, less(v0, v100)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v400, axiom, less(v100, v400)).
fof(ord_v100_v600, axiom, less(v100, v600)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(distinct, axiom, $distinct(v0, v100, v200, v400, v600)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl465, conjecture,
    ~?[X,Y,Z]: (((in_lopen(X, v0, v600) & ~(in_lopen(Y, v0, v400)) & ~(in_lopen(Z, v0, v200))) |
              (~(in_lopen(X, v0, v600)) & in_lopen(Y, v0, v400) & ~(in_lopen(Z, v0, v200))) |
              (~(in_lopen(X, v0, v600)) & ~(in_lopen(Y, v0, v400)) & in_lopen(Z, v0, v200))) &
          (in_lopen(X, v0, v400) & in_lopen(Y, v0, v200) & in_lopen(Z, v0, v100)))).
%--------------------------------------------------------------------------
