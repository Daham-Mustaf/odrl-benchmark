%--------------------------------------------------------------------------
% File     : ODRL330-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : Width near-miss (gap=1) × height compatible → Conflict
% Expected : Theorem
% Verdict  : Conflict
% Category : Box2D
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
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeWidth ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "599"^^xsd:decimal ;
%         odrl:unit <http://dbpedia.org/resource/Pixel> ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "800"^^xsd:decimal ;
%         odrl:unit <http://dbpedia.org/resource/Pixel> ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeWidth ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "601"^^xsd:decimal ;
%         odrl:unit <http://dbpedia.org/resource/Pixel> ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "200"^^xsd:decimal ;
%         odrl:unit <http://dbpedia.org/resource/Pixel> ] ] .
%
% Formal   : width lteq 599  →  (0, 599]
%            width gteq 601  →  [601, ∞)
%            (0, 599] ∩ [601, ∞) ∅  →  Conflict
% Notes    : Tests that even a tiny gap on one axis causes box Conflict.
%
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_axis_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v200, axiom, val(v200)).
fof(val_v599, axiom, val(v599)).
fof(val_v601, axiom, val(v601)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v599, axiom, less(v0, v599)).
fof(ord_v0_v601, axiom, less(v0, v601)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v200_v599, axiom, less(v200, v599)).
fof(ord_v200_v601, axiom, less(v200, v601)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v599_v601, axiom, less(v599, v601)).
fof(ord_v599_v800, axiom, less(v599, v800)).
fof(ord_v601_v800, axiom, less(v601, v800)).
fof(distinct, axiom, $distinct(v0, v200, v599, v601, v800)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl330, conjecture,
    ~?[X,Y]: (in_lopen(X, v0, v599) & leq(v601, X) &
          in_lopen(Y, v0, v800) & leq(v200, Y))).
%--------------------------------------------------------------------------
