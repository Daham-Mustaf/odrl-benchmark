%--------------------------------------------------------------------------
% File     : ODRL025-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Conflict: isAnyOf({germany,france}) ∩ isNoneOf({westernEurope}) = ∅
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 3 (isAnyOf/isNoneOf), Definition 5
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   ex:policy1 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isAnyOf ;
%         odrl:rightOperand ( geo:germany geo:france ) ] ] .
%
%   ex:policy2 a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isNoneOf ;
%         odrl:rightOperand ( geo:westernEurope ) ] ] .
%
% Denotation analysis:
%   Both de≤wE and fr≤wE → both excluded → ∅
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(list_025a_1, axiom, in_value_list(germany, anyList025)).
fof(list_025a_2, axiom, in_value_list(france, anyList025)).
fof(list_anyList025_closed, axiom,
    ![G]: (in_value_list(G, anyList025) => (G = germany | G = france))).
fof(list_025b_1, axiom, in_value_list(westernEurope, noneList025)).
fof(list_noneList025_closed, axiom,
    ![G]: (in_value_list(G, noneList025) => (G = westernEurope))).

fof(odrl025, conjecture,
    ![X]: ~( in_denotation_set(X, anyList025, isAnyOf)
           & in_denotation_set(X, noneList025, isNoneOf) )).
%--------------------------------------------------------------------------
