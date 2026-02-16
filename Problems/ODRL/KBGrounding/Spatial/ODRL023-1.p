%--------------------------------------------------------------------------
% File     : ODRL023-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Conflict: isAllOf({westernEurope, easternEurope}) ∩ eq(germany) = ∅
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 3 (isAllOf), Definition 5
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   ex:policy1 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isAllOf ;
%         odrl:rightOperand ( geo:westernEurope geo:easternEurope ) ] ] .
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
%   disjoint(wE,eE) → ⟦isAllOf⟧=∅ → ∅∩{de}=∅
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(list_023_1, axiom, in_value_list(westernEurope, allRegions023)).
fof(list_023_2, axiom, in_value_list(easternEurope, allRegions023)).
fof(list_allRegions023_closed, axiom,
    ![G]: (in_value_list(G, allRegions023) => (G = westernEurope | G = easternEurope))).

fof(odrl023, conjecture,
    ![X]: ~( in_denotation_set(X, allRegions023, isAllOf)
           & in_denotation(X, germany, eq) )).
%--------------------------------------------------------------------------
