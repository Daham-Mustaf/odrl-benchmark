%--------------------------------------------------------------------------
% File     : ODRL024-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Compatible: isAnyOf({france,germany}) ∩ isNoneOf({easternEurope}) ≠ ∅
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3 (isAnyOf/isNoneOf), Definition 5
%
% ODRL Policy (Turtle):
%   ex:policy1 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isAnyOf ;
%         odrl:rightOperand ( geo:france geo:germany ) ] ] .
%
%   ex:policy2 a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isNoneOf ;
%         odrl:rightOperand ( geo:easternEurope ) ] ] .
%
% Denotation analysis:
%   Witness: france — ¬≤eE by disjointness (wE⊥eE)
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(list_024a_1, axiom, in_value_list(france, anyList024)).
fof(list_024a_2, axiom, in_value_list(germany, anyList024)).
fof(list_anyList024_closed, axiom,
    ![G]: (in_value_list(G, anyList024) => (G = france | G = germany))).
fof(list_024b_1, axiom, in_value_list(easternEurope, noneList024)).
fof(list_noneList024_closed, axiom,
    ![G]: (in_value_list(G, noneList024) => (G = easternEurope))).

fof(odrl024, conjecture,
    ?[X]: ( in_denotation_set(X, anyList024, isAnyOf)
          & in_denotation_set(X, noneList024, isNoneOf) )).
%--------------------------------------------------------------------------
