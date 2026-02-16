%--------------------------------------------------------------------------
% File     : ODRL016-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Compatible: neq(germany) ∩ isPartOf(westernEurope) ≠ ∅
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3 (neq/isPartOf), Definition 5
%
% ODRL Policy (Turtle):
%   ex:policy1 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:neq ;
%         odrl:rightOperand geo:germany ] ] .
%
%   ex:policy2 a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isPartOf ;
%         odrl:rightOperand geo:westernEurope ] ] .
%
% Denotation analysis:
%   ⟦neq(de)⟧=C\{de}, Witness: france
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl016, conjecture,
    ?[X]: ( in_denotation(X, germany, neq)
          & in_denotation(X, westernEurope, isPartOf) )).
%--------------------------------------------------------------------------
