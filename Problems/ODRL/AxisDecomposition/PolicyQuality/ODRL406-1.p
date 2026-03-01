%--------------------------------------------------------------------------
% File     : ODRL406-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : ★★★☆☆ Medium: 2 axes, near-miss gap=2 on both axes
% Expected : Theorem
% Verdict  : Conflict
% Category : PolicyQuality
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
%         odrl:rightOperand "599"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:lteq ;
%         odrl:rightOperand "399"^^xsd:decimal ] ;
%     ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeWidth ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "601"^^xsd:decimal ] ;
%       odrl:constraint [
%         odrl:leftOperand oax:absoluteSizeHeight ;
%         odrl:operator odrl:gteq ;
%         odrl:rightOperand "401"^^xsd:decimal ] ;
%     ] .
%
% Formal   : width lteq 599  →  (0, 599]
%            width gteq 601  →  [601, ∞)
%            (0, 599] ∩ [601, ∞) ∅  →  Conflict
%
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_axis_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v399, axiom, val(v399)).
fof(val_v401, axiom, val(v401)).
fof(val_v599, axiom, val(v599)).
fof(val_v601, axiom, val(v601)).
fof(ord_v0_v399, axiom, less(v0, v399)).
fof(ord_v0_v401, axiom, less(v0, v401)).
fof(ord_v0_v599, axiom, less(v0, v599)).
fof(ord_v0_v601, axiom, less(v0, v601)).
fof(ord_v399_v401, axiom, less(v399, v401)).
fof(ord_v399_v599, axiom, less(v399, v599)).
fof(ord_v399_v601, axiom, less(v399, v601)).
fof(ord_v401_v599, axiom, less(v401, v599)).
fof(ord_v401_v601, axiom, less(v401, v601)).
fof(ord_v599_v601, axiom, less(v599, v601)).
fof(distinct, axiom, $distinct(v0, v399, v401, v599, v601)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl406, conjecture,
    ~?[X,Y]: (in_lopen(X, v0, v599) & leq(v601, X) &
          in_lopen(Y, v0, v399) & leq(v401, Y))).
%--------------------------------------------------------------------------
