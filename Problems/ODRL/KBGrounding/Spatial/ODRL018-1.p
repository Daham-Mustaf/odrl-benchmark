%--------------------------------------------------------------------------
% File     : ODRL018-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Compatible: isPartOf(westernEurope) ∩ hasPart(bavaria) ≠ ∅
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 2, Definition 3
%
% ODRL Policy (Turtle):
%   ex:policy1 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isPartOf ;
%         odrl:rightOperand geo:westernEurope ] ] .
%
%   ex:policy2 a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:hasPart ;
%         odrl:rightOperand geo:bavaria ] ] .
%
% Denotation analysis:
%   Witness: germany (leq(bavaria,germany) ∧ leq(germany,westernEurope))
%
% Difficulty: Medium-Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl018, conjecture,
    ?[X]: ( in_denotation(X, westernEurope, isPartOf)
          & in_denotation(X, bavaria, hasPart) )).
%--------------------------------------------------------------------------
