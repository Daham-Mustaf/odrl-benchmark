%--------------------------------------------------------------------------
% File     : ODRL019-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Conflict: isPartOf(northernEurope) ∩ isPartOf(southernEurope) = ∅
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 2 (disj_downward), Definition 5
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   ex:policy1 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isPartOf ;
%         odrl:rightOperand geo:northernEurope ] ] .
%
%   ex:policy2 a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isPartOf ;
%         odrl:rightOperand geo:southernEurope ] ] .
%
% Denotation analysis:
%   disjoint(nE, sE) [siblings] → ∅ → Conflict
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl019, conjecture,
    ![X]: ~( in_denotation(X, northernEurope, isPartOf)
           & in_denotation(X, southernEurope, isPartOf) )).
%--------------------------------------------------------------------------
