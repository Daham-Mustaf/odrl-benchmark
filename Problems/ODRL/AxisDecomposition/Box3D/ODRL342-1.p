%--------------------------------------------------------------------------
% File     : ODRL342-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : Height conflict, width+depth compatible → Conflict
% Expected : Theorem
% Verdict  : Conflict
% Category : Box3D
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
%         odrl:rightOperand "800"^^xsd:decimal ;
%         odrl:unit <http://dbpedia.org/resource/Pixel> ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "300"^^xsd:decimal ;
%         odrl:unit <http://dbpedia.org/resource/Pixel> ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeDepth ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "32"^^xsd:decimal ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeWidth ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "200"^^xsd:decimal ;
%         odrl:unit <http://dbpedia.org/resource/Pixel> ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "500"^^xsd:decimal ;
%         odrl:unit <http://dbpedia.org/resource/Pixel> ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeDepth ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "8"^^xsd:decimal ] ] .
%
% Formal   : width lteq 800  →  (0, 800]
%            width gteq 200  →  [200, ∞)
%            (0, 800] ∩ [200, ∞) ∅  →  Conflict
% Notes    : Tests commutativity: conflict position shouldn't matter.
%
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_axis_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v8, axiom, val(v8)).
fof(val_v32, axiom, val(v32)).
fof(val_v200, axiom, val(v200)).
fof(val_v300, axiom, val(v300)).
fof(val_v500, axiom, val(v500)).
fof(val_v800, axiom, val(v800)).
fof(ord_v0_v8, axiom, less(v0, v8)).
fof(ord_v0_v32, axiom, less(v0, v32)).
fof(ord_v0_v200, axiom, less(v0, v200)).
fof(ord_v0_v300, axiom, less(v0, v300)).
fof(ord_v0_v500, axiom, less(v0, v500)).
fof(ord_v0_v800, axiom, less(v0, v800)).
fof(ord_v8_v32, axiom, less(v8, v32)).
fof(ord_v8_v200, axiom, less(v8, v200)).
fof(ord_v8_v300, axiom, less(v8, v300)).
fof(ord_v8_v500, axiom, less(v8, v500)).
fof(ord_v8_v800, axiom, less(v8, v800)).
fof(ord_v32_v200, axiom, less(v32, v200)).
fof(ord_v32_v300, axiom, less(v32, v300)).
fof(ord_v32_v500, axiom, less(v32, v500)).
fof(ord_v32_v800, axiom, less(v32, v800)).
fof(ord_v200_v300, axiom, less(v200, v300)).
fof(ord_v200_v500, axiom, less(v200, v500)).
fof(ord_v200_v800, axiom, less(v200, v800)).
fof(ord_v300_v500, axiom, less(v300, v500)).
fof(ord_v300_v800, axiom, less(v300, v800)).
fof(ord_v500_v800, axiom, less(v500, v800)).
fof(distinct, axiom, $distinct(v0, v8, v32, v200, v300, v500, v800)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl342, conjecture,
    ~?[X,Y,Z]: (in_lopen(X, v0, v800) & leq(v200, X) &
          in_lopen(Y, v0, v300) & leq(v500, Y) &
          in_lopen(Z, v0, v32) & leq(v8, Z))).
%--------------------------------------------------------------------------
