%--------------------------------------------------------------------------
% File     : ODRL390-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : Open/closed temporal boundary conflict kills spatial
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
%           odrl:operator odrl:lt ;
%           odrl:rightOperand "181"^^xsd:integer ]
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
%     ] .
%
% Formal   : width lteq 800  →  (0, 800]
%            width gteq 200  →  [200, ∞)
%            (0, 800] ∩ [200, ∞) ∅  →  Conflict
% Notes    : Temporal open/closed boundary: <June30 vs ≥June30.
%
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_axis_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/AXIS000-0.ax').
include('Axioms/Layer0-DomainKB/ORD001-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v181, axiom, val(v181)).
fof(val_v200, axiom, val(v200)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v181, axiom, less(v0, v181)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v181_v200, axiom, less(v181, v200)).
fof(ord_v181_v800, axiom, less(v181, v800)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(distinct, axiom, $distinct(v0, v181, v200, v800)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl390, conjecture,
    ~?[X,Y]: (in_lopen(X, v0, v800) & leq(v200, X) &
          in_ropen(Y, v0, v181) & leq(v181, Y))).
%--------------------------------------------------------------------------
