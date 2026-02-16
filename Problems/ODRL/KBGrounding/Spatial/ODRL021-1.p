%--------------------------------------------------------------------------
% File     : ODRL021-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Compatible: isNoneOf({easternEurope, southernEurope}) ∩ isPartOf(westernEurope) ≠ ∅
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3 (isNoneOf), Definition 5
%
% ODRL Policy (Turtle):
%   ex:policy1 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isNoneOf ;
%         odrl:rightOperand ( geo:easternEurope geo:southernEurope ) ] ] .
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
%   Witness: germany — ≤wE, ¬≤eE (disj), ¬≤sE (disj)
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(list_021_1, axiom, in_value_list(easternEurope, excluded021)).
fof(list_021_2, axiom, in_value_list(southernEurope, excluded021)).
fof(list_excluded021_closed, axiom,
    ![G]: (in_value_list(G, excluded021) => (G = easternEurope | G = southernEurope))).

fof(odrl021, conjecture,
    ?[X]: ( in_denotation_set(X, excluded021, isNoneOf)
          & in_denotation(X, westernEurope, isPartOf) )).
%--------------------------------------------------------------------------
