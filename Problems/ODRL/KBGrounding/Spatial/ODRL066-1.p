%--------------------------------------------------------------------------
% File     : ODRL066-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Partial overlap: hasPart(germany) vs isPartOf(westernEurope)
% Expected : Theorem
% Verdict  : Partial-Overlap
% Paper    : Refinement Conflict (hasPart vs isPartOf)
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
%         odrl:rightOperand geo:westernEurope ] ] .
%
% Denotation analysis:
%   ⟦hasPart(de)⟧ = {de, wE, europe}  (ancestors of germany)
%   ⟦isPartOf(wE)⟧ = {wE, austria, belgium, france, de, ...}  (10 concepts)
%   Intersection = {germany, westernEurope} ≠ ∅
%   hasPart(de) \ isPartOf(wE) = {europe}             → c1 ⊄ c2
%   isPartOf(wE) \ hasPart(de) = {austria, belgium, france, ...}  → c2 ⊄ c1
%   → PARTIAL OVERLAP (modification conflict)
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl066, conjecture,
    ( ?[X]: ( in_denotation(X, germany, hasPart)
           & in_denotation(X, westernEurope, isPartOf) )
    & ?[Y]: ( in_denotation(Y, germany, hasPart)
           & ~in_denotation(Y, westernEurope, isPartOf) )
    & ?[Z]: ( in_denotation(Z, westernEurope, isPartOf)
           & ~in_denotation(Z, germany, hasPart) ) )).
%--------------------------------------------------------------------------
