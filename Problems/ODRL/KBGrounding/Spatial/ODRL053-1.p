%--------------------------------------------------------------------------
% File     : ODRL053-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Cross-branch hasPart: hasPart(germany) ∩ hasPart(poland) ≠ ∅
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3 (hasPart)
%
% ODRL Policy (Turtle):
%   ex:policy1 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:hasPart ;
%         odrl:rightOperand geo:germany ] ] .
%
%   ex:policy2 a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:hasPart ;
%         odrl:rightOperand geo:poland ] ] .
%
% Denotation analysis:
%   NOTE: isPartOf(de)∩isPartOf(pl)=Conflict, but hasPart looks UPWARD!
%   Common ancestors: {europe, world}. Witness: europe
%
% Difficulty: Medium-Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl053, conjecture,
    ?[X]: ( in_denotation(X, germany, hasPart)
          & in_denotation(X, poland, hasPart) )).
%--------------------------------------------------------------------------
