%--------------------------------------------------------------------------
% File     : ODRL464-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : XONE(A)×XONE(B): arm 1 regions overlap → Compatible
% Expected : Theorem
% Verdict  : Compatible
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
%             odrl:rightOperand "400"^^xsd:decimal ]
%           [ odrl:leftOperand oax:absoluteSizeHeight ;
%             odrl:operator odrl:lteq ;
%             odrl:rightOperand "300"^^xsd:decimal ]
%         )
%       ]
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
%             odrl:rightOperand "500"^^xsd:decimal ]
%         )
%       ]
%     ] .
%
% Formal   : width lteq 400  →  (0, 400]
%            width lteq 600  →  (0, 600]
%            (0, 400] ∩ (0, 600] ≠ ∅  →  Compatible
% Notes    : A-arm1 (w≤400, h>300) ∩ B-arm1 (w≤600, h>500): w≤400 & h>500. Witness: (200, 600).
% Connect. : Policy A = odrl:xone
%            Policy B = odrl:xone
%
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_axis_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v300, axiom, val(v300)).
fof(val_v400, axiom, val(v400)).
fof(val_v500, axiom, val(v500)).
fof(val_v600, axiom, val(v600)).
fof(ord_v0_v300, axiom, less(v0, v300)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v500, axiom, less(v0, v500)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v300_v400, axiom, less(v300, v400)).
fof(ord_v300_v500, axiom, less(v300, v500)).
fof(ord_v300_v600, axiom, less(v300, v600)).
fof(ord_v400_v500, axiom, less(v400, v500)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v500_v600, axiom, less(v500, v600)).
fof(distinct, axiom, $distinct(v0, v300, v400, v500, v600)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl464, conjecture,
    ?[X,Y]: (((in_lopen(X, v0, v400) & ~(in_lopen(Y, v0, v300))) |
              (~(in_lopen(X, v0, v400)) & in_lopen(Y, v0, v300))) &
          ((in_lopen(X, v0, v600) & ~(in_lopen(Y, v0, v500))) |
              (~(in_lopen(X, v0, v600)) & in_lopen(Y, v0, v500))))).
%--------------------------------------------------------------------------
