%--------------------------------------------------------------------------
% File     : ODRL386-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : Payment conflict kills 3 compatible domains
% Expected : Theorem
% Verdict  : Conflict
% Category : CrossDomain
% Difficulty: Hard
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
%           odrl:rightOperand "100"^^xsd:integer ]
%         odrl:constraint [
%           odrl:leftOperand odrl:payAmount ;
%           odrl:operator odrl:lteq ;
%           odrl:rightOperand "1000"^^xsd:decimal ;
%           odrl:unit <http://dbpedia.org/resource/Euro> ]
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
%           odrl:rightOperand "10"^^xsd:integer ]
%         odrl:constraint [
%           odrl:leftOperand odrl:payAmount ;
%           odrl:operator odrl:gteq ;
%           odrl:rightOperand "5000"^^xsd:decimal ;
%           odrl:unit <http://dbpedia.org/resource/Euro> ]
%     ] .
%
% Formal   : width lteq 800  →  (0, 800]
%            width gteq 200  →  [200, ∞)
%            (0, 800] ∩ [200, ∞) ∅  →  Conflict
% Notes    : Provider caps at €10, consumer requires ≥€50. Incompatible.
%
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_axis_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v10, axiom, val(v10)).
fof(val_v100, axiom, val(v100)).
fof(val_v181, axiom, val(v181)).
fof(val_v200, axiom, val(v200)).
fof(val_v365, axiom, val(v365)).
fof(val_v800, axiom, val(v800)).
fof(val_v1000, axiom, val(v1000)).
fof(val_v5000, axiom, val(v5000)).
fof(ord_v0_v10, axiom, less(v0, v10)).
fof(ord_v0_v100, axiom, less(v0, v100)).
fof(ord_v0_v181, axiom, less(v0, v181)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v365, axiom, less(v0, v365)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v0_v1000, axiom, less(v0, v1000)).
fof(ord_v0_v5000, axiom, less(v0, v5000)).
fof(ord_v10_v100, axiom, less(v10, v100)).
fof(ord_v10_v181, axiom, less(v10, v181)).
fof(ord_v10_v200, axiom, less(v10, v200)).
fof(ord_v10_v365, axiom, less(v10, v365)).
fof(ord_v10_v800, axiom, less(v10, v800)).
fof(ord_v10_v1000, axiom, less(v10, v1000)).
fof(ord_v10_v5000, axiom, less(v10, v5000)).
fof(ord_v100_v181, axiom, less(v100, v181)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v365, axiom, less(v100, v365)).
fof(ord_v100_v800, axiom, less(v100, v800)).
fof(ord_v100_v1000, axiom, less(v100, v1000)).
fof(ord_v100_v5000, axiom, less(v100, v5000)).
fof(ord_v181_v200, axiom, less(v181, v200)).
fof(ord_v181_v365, axiom, less(v181, v365)).
fof(ord_v181_v800, axiom, less(v181, v800)).
fof(ord_v181_v1000, axiom, less(v181, v1000)).
fof(ord_v181_v5000, axiom, less(v181, v5000)).
fof(ord_v200_v365, axiom, less(v200, v365)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v200_v1000, axiom, less(v200, v1000)).
fof(ord_v200_v5000, axiom, less(v200, v5000)).
fof(ord_v365_v800, axiom, less(v365, v800)).
fof(ord_v365_v1000, axiom, less(v365, v1000)).
fof(ord_v365_v5000, axiom, less(v365, v5000)).
fof(ord_v800_v1000, axiom, less(v800, v1000)).
fof(ord_v800_v5000, axiom, less(v800, v5000)).
fof(ord_v1000_v5000, axiom, less(v1000, v5000)).
fof(distinct, axiom, $distinct(v0, v10, v100, v181, v200, v365, v800, v1000, v5000)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl386, conjecture,
    ~?[X,Y,Z,W]: (in_lopen(X, v0, v800) & leq(v200, X) &
          in_closed(Y, v0, v365) & leq(v181, Y) &
          in_closed(Z, v0, v100) & leq(v10, Z) &
          in_closed(W, v0, v1000) & leq(v5000, W))).
%--------------------------------------------------------------------------
