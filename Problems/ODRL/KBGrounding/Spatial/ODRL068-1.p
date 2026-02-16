%--------------------------------------------------------------------------
% File     : ODRL068-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Partial overlap: isNoneOf({easternEurope}) vs hasPart(poland)
% Expected : Theorem
% Verdict  : Partial-Overlap
% Paper    : Refinement Conflict (isNoneOf vs hasPart)
%
% ODRL Policy (Turtle):
%   ex:policy1 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isNoneOf ;
%         odrl:rightOperand ( geo:easternEurope ) ] ] .
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
%   ⟦isNoneOf({eE})⟧ = C \ ↓eE  (47 concepts: all non-eastern + europe)
%
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(list_068_1, axiom, in_value_list(easternEurope, excl068)).
fof(list_excl068_closed, axiom,
    ![G]: (in_value_list(G, excl068) => (G = easternEurope))).

fof(odrl068, conjecture,
    ( ?[X]: ( in_denotation_set(X, excl068, isNoneOf)
           & in_denotation(X, poland, hasPart) )
    & ?[Y]: ( in_denotation_set(Y, excl068, isNoneOf)
           & ~in_denotation(Y, poland, hasPart) )
    & ?[Z]: ( in_denotation(Z, poland, hasPart)
           & ~in_denotation_set(Z, excl068, isNoneOf) ) )).
%--------------------------------------------------------------------------
