%--------------------------------------------------------------------------
% File     : ODRL451-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : 3-axis mixed-ops OR(A)×AND(B): all OR-arms fail
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
%             odrl:operator odrl:eq ;
%             odrl:rightOperand "600"^^xsd:decimal ]
%           [ odrl:leftOperand oax:absoluteSizeHeight ;
%             odrl:operator odrl:lt ;
%             odrl:rightOperand "200"^^xsd:decimal ]
%           [ odrl:leftOperand oax:absoluteSizeDepth ;
%             odrl:operator odrl:gt ;
%             odrl:rightOperand "100"^^xsd:decimal ]
%         )
%       ]
%     ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeWidth ;
%         odrl:operator odrl:gt ;
%         odrl:rightOperand "800"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "400"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeDepth ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "50"^^xsd:decimal ] ;
%     ] .
%
% Formal   : width eq 600  →  [600, 600]
%            width gt 800  →  (800, ∞)
%            [600, 600] ∩ (800, ∞) ∅  →  Conflict
% Notes    : A(OR): w=600 | h<200 | d>100. B(AND): w>800 & h≥400 & d≤50. w=600 ∩ w>800: ∅. h<200 ∩ h≥400: ∅. d>100 ∩ d≤50: ∅.
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
fof(val_v600, axiom, val(v600)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v50, axiom, less(v0, v50)).
fof(ord_v0_v100, axiom, less(v0, v100)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v400, axiom, less(v0, v400)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v50_v100, axiom, less(v50, v100)).
fof(ord_v50_v200, axiom, less(v50, v200)).
fof(ord_v50_v400, axiom, less(v50, v400)).
fof(ord_v50_v600, axiom, less(v50, v600)).
fof(ord_v50_v800, axiom, less(v50, v800)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v400, axiom, less(v100, v400)).
fof(ord_v100_v600, axiom, less(v100, v600)).
fof(ord_v100_v800, axiom, less(v100, v800)).
fof(ord_v200_v400, axiom, less(v200, v400)).
fof(ord_v200_v600, axiom, less(v200, v600)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v400_v600, axiom, less(v400, v600)).
fof(ord_v400_v800, axiom, less(v400, v800)).
fof(ord_v600_v800, axiom, less(v600, v800)).
fof(distinct, axiom, $distinct(v0, v50, v100, v200, v400, v600, v800)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl451, conjecture,
    ~?[X,Y,Z]: ((in_closed(X, v600, v600) | in_open(Y, v0, v200) | less(v100, Z)) &
          (less(v800, X) & leq(v400, Y) & in_lopen(Z, v0, v50)))).
%--------------------------------------------------------------------------
