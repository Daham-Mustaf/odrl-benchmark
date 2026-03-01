%--------------------------------------------------------------------------
% File     : ODRL388-1 : TPTP v0.2.0
% Domain   : ODRL Spatial Axis Profile
% Problem  : Temporal axis breaks cross-domain subsumption
% Expected : Theorem
% Verdict  : Refuted
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
%           odrl:rightOperand "600"^^xsd:decimal ;
%           odrl:unit <http://dbpedia.org/resource/Pixel> ]
%         odrl:constraint [
%           odrl:leftOperand odrl:dateTime ;
%           odrl:operator odrl:lteq ;
%           odrl:rightOperand "365"^^xsd:integer ]
%     ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%         odrl:constraint [
%           odrl:leftOperand oax:absoluteSizeWidth ;
%           odrl:operator odrl:lteq ;
%           odrl:rightOperand "1200"^^xsd:decimal ;
%           odrl:unit <http://dbpedia.org/resource/Pixel> ]
%         odrl:constraint [
%           odrl:leftOperand odrl:dateTime ;
%           odrl:operator odrl:lteq ;
%           odrl:rightOperand "181"^^xsd:integer ]
%     ] .
%
% Formal   : (0, 600] ⊄ (0, 1200]
% Notes    : Counterexample: (1, 300). Width OK but date 300 > 181.
%
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_axis_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/AXIS000-0.ax').

% ─── Named constants and ordering ─────────────────────────────────────
fof(val_v0, axiom, val(v0)).
fof(val_v181, axiom, val(v181)).
fof(val_v365, axiom, val(v365)).
fof(val_v600, axiom, val(v600)).
fof(val_v1200, axiom, val(v1200)).
fof(ord_v0_v181, axiom, less(v0, v181)).
fof(ord_v0_v365, axiom, less(v0, v365)).
fof(ord_v0_v600, axiom, less(v0, v600)).
fof(ord_v0_v1200, axiom, less(v0, v1200)).
fof(ord_v181_v365, axiom, less(v181, v365)).
fof(ord_v181_v600, axiom, less(v181, v600)).
fof(ord_v181_v1200, axiom, less(v181, v1200)).
fof(ord_v365_v600, axiom, less(v365, v600)).
fof(ord_v365_v1200, axiom, less(v365, v1200)).
fof(ord_v600_v1200, axiom, less(v600, v1200)).
fof(distinct, axiom, $distinct(v0, v181, v365, v600, v1200)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl388, conjecture,
    ?[X,Y]: ((in_lopen(X, v0, v600) & in_closed(Y, v0, v365)) & ~(in_lopen(X, v0, v1200) & in_closed(Y, v0, v181)))).
%--------------------------------------------------------------------------
