%--------------------------------------------------------------------------
% File     : ODRL111-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Definition 3 (isAnyOf) — Union Compatible with isPartOf
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3 (isAnyOf) — Union Compatible with isPartOf
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isAnyOf ;
%   %         odrl:rightOperand ( geo:germany geo:france ) ] ] .
%   %
%   %   ex:policyB a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand geo:westernEurope ] ] .
%
% Formal test:
%   ⟦isAnyOf({de, fr})⟧ = ↓de ∪ ↓fr, both ⊆ ↓wE.
%   %   Witness: germany ∈ ↓de ∩ ↓wE.
%
% One-liner : isAnyOf({de,fr}) ∩ isPartOf(wE) ≠ ∅
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-16
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Problem-specific axioms ─────────────────────────────────────────
fof(list_111_1, axiom, in_value_list(germany, list111)).
fof(list_111_2, axiom, in_value_list(france, list111)).
fof(list_list111_closed, axiom,
    ![G]: (in_value_list(G, list111) => (G = germany | G = france))).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl111, conjecture,
    ?[X]: ( in_denotation_set(X, list111, isAnyOf)
          & in_denotation(X, westernEurope, isPartOf) )).

%--------------------------------------------------------------------------