%--------------------------------------------------------------------------
% File     : ODRL329-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : Narrow width strip × wide height → Compatible
% Expected : Theorem
% Verdict  : Compatible
% Category : Box2D
% Difficulty: Easy
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
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "500"^^xsd:decimal ;
%         odrl:unit <http://dbpedia.org/resource/Pixel> ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "100"^^xsd:decimal ;
%         odrl:unit <http://dbpedia.org/resource/Pixel> ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeWidth ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "510"^^xsd:decimal ;
%         odrl:unit <http://dbpedia.org/resource/Pixel> ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "900"^^xsd:decimal ;
%         odrl:unit <http://dbpedia.org/resource/Pixel> ] ] .
%
% Formal   : width gteq 500  →  [500, ∞)
%            width lteq 510  →  (0, 510]
%            [500, ∞) ∩ (0, 510] ≠ ∅  →  Compatible
%
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_axis_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v100, axiom, val(v100)).
fof(val_v500, axiom, val(v500)).
fof(val_v510, axiom, val(v510)).
fof(val_v900, axiom, val(v900)).
fof(ord_v0_v100, axiom, less(v0, v100)).
fof(ord_v0_v500, axiom, less(v0, v500)).
fof(ord_v0_v510, axiom, less(v0, v510)).
fof(ord_v0_v900, axiom, less(v0, v900)).
fof(ord_v100_v500, axiom, less(v100, v500)).
fof(ord_v100_v510, axiom, less(v100, v510)).
fof(ord_v100_v900, axiom, less(v100, v900)).
fof(ord_v500_v510, axiom, less(v500, v510)).
fof(ord_v500_v900, axiom, less(v500, v900)).
fof(ord_v510_v900, axiom, less(v510, v900)).
fof(distinct, axiom, $distinct(v0, v100, v500, v510, v900)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl329, conjecture,
    ?[X,Y]: (leq(v500, X) & in_lopen(X, v0, v510) &
          leq(v100, Y) & in_lopen(Y, v0, v900))).
%--------------------------------------------------------------------------
