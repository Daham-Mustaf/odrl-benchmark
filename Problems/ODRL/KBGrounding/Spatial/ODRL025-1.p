%--------------------------------------------------------------------------
% File     : ODRL025-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Conflict: isAnyOf({germany,france}) ∩ isNoneOf({wE}) = ∅
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 3 (isAnyOf/isNoneOf), Definition 5
%
% ODRL Policy (Turtle):
%   ex:policyA a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isAnyOf ;
%         odrl:rightOperand ( geo:germany geo:france ) ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isNoneOf ;
%         odrl:rightOperand ( geo:westernEurope ) ] ] .
%
% Formal:
%   ⟦isAnyOf({de,fr})⟧  = ↓germany ∪ ↓france
%   ⟦isNoneOf({wE})⟧ = C \ ↓wE
%   leq(germany, westernEurope) → germany ∈ ↓wE → excluded
%   leq(france,  westernEurope) → france  ∈ ↓wE → excluded
%   All elements of isAnyOf are excluded → ∅ → Conflict
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Problem-specific axioms ─────────────────────────────────────
fof(list_anyList025_1, axiom, in_value_list(germany, anyList025)).
fof(list_anyList025_2, axiom, in_value_list(france, anyList025)).
fof(list_anyList025_closed, axiom,
    ![G]: (in_value_list(G, anyList025) => (G = germany | G = france))).
fof(list_noneList025_1, axiom, in_value_list(westernEurope, noneList025)).
fof(list_noneList025_closed, axiom,
    ![G]: (in_value_list(G, noneList025) => (G = westernEurope))).
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl025, conjecture,
    ![X]: ~( in_denotation_set(X, anyList025, isAnyOf)
           & in_denotation_set(X, noneList025, isNoneOf) )).
%--------------------------------------------------------------------------
