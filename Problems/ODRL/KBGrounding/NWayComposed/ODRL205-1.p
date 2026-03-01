%--------------------------------------------------------------------------
% File     : ODRL205-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : isAnyOf(5) × isNoneOf(2) — Large Union vs Large Exclusion
% Expected : CounterSatisfiable
% Verdict  : Conflict
% Paper    : isAnyOf(5) × isNoneOf(2) — Large Union vs Large Exclusion
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isAnyOf ;
%   %         odrl:rightOperand ( geo:germany geo:france geo:italy geo:spain geo:netherlands ) ] ] .
%   %
%   %   ex:policyB a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isNoneOf ;
%   %         odrl:rightOperand ( geo:westernEurope geo:easternEurope ) ] ] .
%
% Formal test:
%   Large union ∩ large complement:
%   %   isAnyOf({de,fr,it,es,nl}): all ≤ wE → all ∈ ↓wE
%   %   isNoneOf({wE,eE}): C \ (↓wE ∪ ↓eE) ≈ {europe}
%   %   → Union ∩ Complement = ∅ (all union members excluded)
%   %   Extreme: 5-element list + 2-element exclusion + CWA reasoning.
%
% One-liner : Large union vs large complement: isAnyOf(5) ∩ isNoneOf(2) = ∅
% Difficulty: Extreme
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Problem-specific axioms ─────────────────────────────────────────
fof(list_205a_1, axiom, in_value_list(germany, anyList205)).
fof(list_205a_2, axiom, in_value_list(france, anyList205)).
fof(list_205a_3, axiom, in_value_list(italy, anyList205)).
fof(list_205a_4, axiom, in_value_list(spain, anyList205)).
fof(list_205a_5, axiom, in_value_list(netherlands, anyList205)).
fof(list_anyList205_closed, axiom,
    ![G]: (in_value_list(G, anyList205) => (G = germany | G = france | G = italy | G = spain | G = netherlands))).
fof(list_205b_1, axiom, in_value_list(westernEurope, noneList205)).
fof(list_205b_2, axiom, in_value_list(easternEurope, noneList205)).
fof(list_noneList205_closed, axiom,
    ![G]: (in_value_list(G, noneList205) => (G = westernEurope | G = easternEurope))).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl205, conjecture,
    ?[X]: ( in_denotation_set(X, anyList205, isAnyOf)
          & in_denotation_set(X, noneList205, isNoneOf) )).

%--------------------------------------------------------------------------