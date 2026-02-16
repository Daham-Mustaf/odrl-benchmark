%--------------------------------------------------------------------------
% File     : ODRL020-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Compatible: isAnyOf({westernEurope, northernEurope}) ∩ eq(germany) ≠ ∅
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3 (isAnyOf), Definition 5
%
% ODRL Policy (Turtle):
%   ex:policy1 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isAnyOf ;
%         odrl:rightOperand ( geo:westernEurope geo:northernEurope ) ] ] .
%
%   ex:policy2 a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:eq ;
%         odrl:rightOperand geo:germany ] ] .
%
% Denotation analysis:
%   ⟦isAnyOf({wE,nE})⟧=↓wE∪↓nE, Witness: germany∈↓wE
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(list_020_1, axiom, in_value_list(westernEurope, regions020)).
fof(list_020_2, axiom, in_value_list(northernEurope, regions020)).
fof(list_regions020_closed, axiom,
    ![G]: (in_value_list(G, regions020) => (G = westernEurope | G = northernEurope))).

fof(odrl020, conjecture,
    ?[X]: ( in_denotation_set(X, regions020, isAnyOf)
          & in_denotation(X, germany, eq) )).
%--------------------------------------------------------------------------
