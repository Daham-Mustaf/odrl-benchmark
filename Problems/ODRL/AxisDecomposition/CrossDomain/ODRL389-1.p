%--------------------------------------------------------------------------
% File     : ODRL389-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : Open temporal intervals + spatial overlap → Compatible
% Expected : Theorem
% Verdict  : Compatible
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
%           odrl:operator odrl:gt ;
%           odrl:rightOperand "100"^^xsd:integer ]
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
%           odrl:operator odrl:lt ;
%           odrl:rightOperand "300"^^xsd:integer ]
%     ] .
%
% Formal   : width lteq 800  →  (0, 800]
%            width gteq 200  →  [200, ∞)
%            (0, 800] ∩ [200, ∞) ≠ ∅  →  Compatible
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
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v100, axiom, less(v0, v100)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v300, axiom, less(v0, v300)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v100_v200, axiom, less(v100, v200)).
fof(ord_v100_v300, axiom, less(v100, v300)).
fof(ord_v100_v800, axiom, less(v100, v800)).
fof(ord_v200_v300, axiom, less(v200, v300)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v300_v800, axiom, less(v300, v800)).
fof(distinct, axiom, $distinct(v0, v100, v200, v300, v800)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl389, conjecture,
    ?[X,Y]: (in_lopen(X, v0, v800) & leq(v200, X) &
          less(v100, Y) & in_ropen(Y, v0, v300))).
%--------------------------------------------------------------------------
