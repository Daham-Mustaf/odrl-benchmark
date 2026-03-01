%--------------------------------------------------------------------------
% File     : ODRL384-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : Count conflict kills spatial+temporal compatibility
% Expected : Theorem
% Verdict  : Conflict
% Category : CrossDomain
% Difficulty: Medium
%
% ODRL Policy (Turtle):
%   @prefix odrl: <http://www.w3.org/ns/odrl/2/> .
%   @prefix oax:  <http://w3id.org/odrl/spatial-axis#> .
%   @prefix ex:   <https://example.org/> .
%
%   ex:policyA a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%         odrl:constraint [
%           odrl:leftOperand oax:absoluteSizeWidth ;
%           odrl:operator odrl:lteq ;
%           odrl:rightOperand "800"^^xsd:decimal ;
%           odrl:unit <http://dbpedia.org/resource/Pixel> ]
%         odrl:constraint [
%           odrl:leftOperand odrl:dateTime ;
%           odrl:operator odrl:lteq ;
%           odrl:rightOperand "365"^^xsd:integer ]
%         odrl:constraint [
%           odrl:leftOperand odrl:count ;
%           odrl:operator odrl:lteq ;
%           odrl:rightOperand "5"^^xsd:integer ]
%     ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%         odrl:constraint [
%           odrl:leftOperand oax:absoluteSizeWidth ;
%           odrl:operator odrl:gteq ;
%           odrl:rightOperand "200"^^xsd:decimal ;
%           odrl:unit <http://dbpedia.org/resource/Pixel> ]
%         odrl:constraint [
%           odrl:leftOperand odrl:dateTime ;
%           odrl:operator odrl:gteq ;
%           odrl:rightOperand "181"^^xsd:integer ]
%         odrl:constraint [
%           odrl:leftOperand odrl:count ;
%           odrl:operator odrl:gteq ;
%           odrl:rightOperand "50"^^xsd:integer ]
%     ] .
%
% Formal   : width lteq 800  →  (0, 800]
%            width gteq 200  →  [200, ∞)
%            (0, 800] ∩ [200, ∞) ∅  →  Conflict
% Notes    : Usage count conflict: ≤5 uses vs ≥50 uses.
%
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_axis_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v5, axiom, val(v5)).
fof(val_v50, axiom, val(v50)).
fof(val_v181, axiom, val(v181)).
fof(val_v200, axiom, val(v200)).
fof(val_v365, axiom, val(v365)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v5, axiom, less(v0, v5)).
fof(ord_v0_v50, axiom, less(v0, v50)).
fof(ord_v0_v181, axiom, less(v0, v181)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v365, axiom, less(v0, v365)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v5_v50, axiom, less(v5, v50)).
fof(ord_v5_v181, axiom, less(v5, v181)).
fof(ord_v5_v200, axiom, less(v5, v200)).
fof(ord_v5_v365, axiom, less(v5, v365)).
fof(ord_v5_v800, axiom, less(v5, v800)).
fof(ord_v50_v181, axiom, less(v50, v181)).
fof(ord_v50_v200, axiom, less(v50, v200)).
fof(ord_v50_v365, axiom, less(v50, v365)).
fof(ord_v50_v800, axiom, less(v50, v800)).
fof(ord_v181_v200, axiom, less(v181, v200)).
fof(ord_v181_v365, axiom, less(v181, v365)).
fof(ord_v181_v800, axiom, less(v181, v800)).
fof(ord_v200_v365, axiom, less(v200, v365)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v365_v800, axiom, less(v365, v800)).
fof(distinct, axiom, $distinct(v0, v5, v50, v181, v200, v365, v800)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl384, conjecture,
    ~?[X,Y,Z]: (in_lopen(X, v0, v800) & leq(v200, X) &
          in_closed(Y, v0, v365) & leq(v181, Y) &
          in_closed(Z, v0, v5) & leq(v50, Z))).
%--------------------------------------------------------------------------
