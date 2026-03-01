%--------------------------------------------------------------------------
% File     : ODRL112-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Definition 3 (isNoneOf) — Conflict with Subsumed isPartOf
% Expected : CounterSatisfiable
% Verdict  : Conflict
% Paper    : Definition 3 (isNoneOf) — Conflict with Subsumed isPartOf
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isNoneOf ;
%   %         odrl:rightOperand ( geo:westernEurope ) ] ] .
%   %
%   %   ex:policyB a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand geo:germany ] ] .
%
% Formal test:
%   isNoneOf({wE}) = {X | ¬leq(X, wE)}, isPartOf(de) = {X | leq(X, de)}
%   %   germany ≤ wE → ↓de ⊆ ↓wE → every X ∈ isPartOf(de) is also ≤ wE
%   %   → X ∈ isNoneOf({wE}) requires ¬leq(X, wE) — contradiction.
%   %   ⟦isNoneOf({wE})⟧ ∩ ⟦isPartOf(de)⟧ = ∅ → Conflict
%
% One-liner : isNoneOf({wE}) ∩ isPartOf(de) = ∅: subsumed → conflict
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Problem-specific axioms ─────────────────────────────────────────
fof(list_112_1, axiom, in_value_list(westernEurope, list112)).
fof(list_list112_closed, axiom,
    ![G]: (in_value_list(G, list112) => (G = westernEurope))).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl112, conjecture,
    ?[X]: ( in_denotation_set(X, list112, isNoneOf)
          & in_denotation(X, germany, isPartOf) )).

%--------------------------------------------------------------------------