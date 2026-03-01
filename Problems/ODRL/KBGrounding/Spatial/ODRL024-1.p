%--------------------------------------------------------------------------
% File     : ODRL024-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Compatible: isAnyOf({france,germany}) ∩ isNoneOf({eE}) ≠ ∅
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3 (isAnyOf/isNoneOf), Definition 5
%
% ODRL Policy (Turtle):
%   ex:policyA a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isAnyOf ;
%         odrl:rightOperand ( geo:france geo:germany ) ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isNoneOf ;
%         odrl:rightOperand ( geo:easternEurope ) ] ] .
%
% Formal:
%   ⟦isAnyOf({fr,de})⟧  = ↓france ∪ ↓germany
%   ⟦isNoneOf({eE})⟧ = C \ ↓eE
%   Witness: france
%     leq(france, westernEurope) → france ∈ isAnyOf
%     disj(wE,eE) + disj_downward → ¬leq(france,eE) → france ∈ isNoneOf
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Problem-specific axioms ─────────────────────────────────────
fof(list_anyList024_1, axiom, in_value_list(france, anyList024)).
fof(list_anyList024_2, axiom, in_value_list(germany, anyList024)).
fof(list_anyList024_closed, axiom,
    ![G]: (in_value_list(G, anyList024) => (G = france | G = germany))).
fof(list_noneList024_1, axiom, in_value_list(easternEurope, noneList024)).
fof(list_noneList024_closed, axiom,
    ![G]: (in_value_list(G, noneList024) => (G = easternEurope))).
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl024, conjecture,
    ?[X]: ( in_denotation_set(X, anyList024, isAnyOf)
          & in_denotation_set(X, noneList024, isNoneOf) )).
%--------------------------------------------------------------------------
