%--------------------------------------------------------------------------
% File     : ODRL113-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Definition 3 — isAnyOf ∩ isNoneOf Partial Overlap
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3 — isAnyOf ∩ isNoneOf Partial Overlap
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isAnyOf ;
%   %         odrl:rightOperand ( geo:germany geo:poland ) ] ] .
%   %
%   %   ex:policyB a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isNoneOf ;
%   %         odrl:rightOperand ( geo:easternEurope ) ] ] .
%
% Formal test:
%   isAnyOf({de,pl}) ∩ isNoneOf({eE})
%   %   germany ∈ ↓de ∧ ¬leq(de, eE) → germany ∈ isNoneOf({eE})
%   %   Witness: germany → Compatible
%
% One-liner : isAnyOf({de,pl}) ∩ isNoneOf({eE}): partial overlap → Compatible
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-16
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Problem-specific axioms ─────────────────────────────────────────
fof(list_113a_1, axiom, in_value_list(germany, anyList113)).
fof(list_113a_2, axiom, in_value_list(poland, anyList113)).
fof(list_anyList113_closed, axiom,
    ![G]: (in_value_list(G, anyList113) => (G = germany | G = poland))).
fof(list_113b_1, axiom, in_value_list(easternEurope, noneList113)).
fof(list_noneList113_closed, axiom,
    ![G]: (in_value_list(G, noneList113) => (G = easternEurope))).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl113, conjecture,
    ?[X]: ( in_denotation_set(X, anyList113, isAnyOf)
          & in_denotation_set(X, noneList113, isNoneOf) )).

%--------------------------------------------------------------------------