%--------------------------------------------------------------------------
% File     : ODRL067-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Partial overlap: neq(germany) vs isPartOf(westernEurope)
% Expected : Theorem
% Verdict  : Partial-Overlap
% Paper    : Refinement Conflict (neq vs isPartOf)
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
%   ⟦neq(de)⟧ = C \ {de}  (57 concepts)
%   ⟦isPartOf(wE)⟧ = ↓wE  (10 concepts)
%   Intersection = ↓wE \ {de} = {wE, austria, belgium, france, ...} ≠ ∅
%   neq(de) \ isPartOf(wE) = {poland, eE, nE, sE, europe, ...} → c1 ⊄ c2
%   isPartOf(wE) \ neq(de) = {germany}                          → c2 ⊄ c1
%   → PARTIAL OVERLAP
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl067, conjecture,
    ( ?[X]: ( in_denotation(X, germany, neq)
           & in_denotation(X, westernEurope, isPartOf) )
    & ?[Y]: ( in_denotation(Y, germany, neq)
           & ~in_denotation(Y, westernEurope, isPartOf) )
    & ?[Z]: ( in_denotation(Z, westernEurope, isPartOf)
           & ~in_denotation(Z, germany, neq) ) )).
%--------------------------------------------------------------------------
