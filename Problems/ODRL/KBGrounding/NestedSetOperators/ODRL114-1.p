%--------------------------------------------------------------------------
% File     : ODRL114-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Definition 3 (isAllOf) — Compatible Members Non-Empty
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3 (isAllOf) — Compatible Members Non-Empty
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isAllOf ;
%   %         odrl:rightOperand ( geo:westernEurope geo:europe ) ] ] .
%
% Formal test:
%   ⟦isAllOf({wE, europe})⟧ = ↓wE ∩ ↓europe = ↓wE (since wE ≤ europe)
%   %   Witness: germany ∈ ↓wE.
%
% One-liner : isAllOf({wE, europe}) ≠ ∅: compatible members → non-empty
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Problem-specific axioms ─────────────────────────────────────────
fof(list_114_1, axiom, in_value_list(westernEurope, list114)).
fof(list_114_2, axiom, in_value_list(europe, list114)).
fof(list_list114_closed, axiom,
    ![G]: (in_value_list(G, list114) => (G = westernEurope | G = europe))).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl114, conjecture,
    ?[X]: in_denotation_set(X, list114, isAllOf)).

%--------------------------------------------------------------------------