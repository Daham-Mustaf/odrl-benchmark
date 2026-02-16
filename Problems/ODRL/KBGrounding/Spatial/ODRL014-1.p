%--------------------------------------------------------------------------
% File     : ODRL014-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Compatible: hasPart(germany) ∩ isPartOf(europe) ≠ ∅
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3 (hasPart/isPartOf), Definition 5
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
%         odrl:operator odrl:isPartOf ;
%         odrl:rightOperand geo:europe ] ] .
%
% Denotation analysis:
%   ⟦hasPart(de)⟧={de,wE,europe,world}, ⟦isPartOf(eu)⟧={eu,...,de,...}
%   Witnesses: westernEurope, europe
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl014, conjecture,
    ?[X]: ( in_denotation(X, germany, hasPart)
          & in_denotation(X, europe, isPartOf) )).
%--------------------------------------------------------------------------
