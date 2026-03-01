%--------------------------------------------------------------------------
% File     : ODRL201-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : isNoneOf × isAllOf — Complement Meets Intersection
% Expected : Theorem
% Verdict  : Compatible
% Paper    : isNoneOf × isAllOf — Complement Meets Intersection
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isNoneOf ;
%   %         odrl:rightOperand ( geo:easternEurope ) ] ] .
%   %
%   %   ex:policyB a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isAllOf ;
%   %         odrl:rightOperand ( geo:europe geo:westernEurope ) ] ] .
%
% Formal test:
%   Complement ∩ intersection:
%   %   isNoneOf({eE}) = C \ ↓eE, isAllOf({europe, wE}) = ↓wE
%   %   wE⊥eE → ↓wE ⊆ (C \ ↓eE) → overlap = ↓wE ≠ ∅
%   %   Hard: prover must chain disjointness → non-membership → complement inclusion.
%
% One-liner : Complement ∩ intersection: isNoneOf({eE}) ∩ isAllOf({europe,wE}) = ↓wE
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Problem-specific axioms ─────────────────────────────────────────
fof(list_201a, axiom, in_value_list(easternEurope, noneList201)).
fof(list_noneList201_closed, axiom,
    ![G]: (in_value_list(G, noneList201) => (G = easternEurope))).
fof(list_201b_1, axiom, in_value_list(europe, allList201)).
fof(list_201b_2, axiom, in_value_list(westernEurope, allList201)).
fof(list_allList201_closed, axiom,
    ![G]: (in_value_list(G, allList201) => (G = europe | G = westernEurope))).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl201, conjecture,
    ?[X]: ( in_denotation_set(X, noneList201, isNoneOf)
          & in_denotation_set(X, allList201, isAllOf) )).

%--------------------------------------------------------------------------