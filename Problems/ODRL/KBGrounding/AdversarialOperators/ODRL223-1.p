%--------------------------------------------------------------------------
% File     : ODRL223-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : isAllOf ⊆ isAnyOf — Intersection Subsumes Union
% Expected : Theorem
% Verdict  : Subsumption
% Paper    : isAllOf ⊆ isAnyOf — Intersection Subsumes Union
%
% ODRL Policy (Conceptual):
%   (Meta-property: ∀L: isAllOf(L) ⊆ isAnyOf(L))
%
% Formal test:
%   isAllOf(L) = ∩ᵢ ↓gᵢ ⊆ ∪ᵢ ↓gᵢ = isAnyOf(L).
%   %   For L = {wE, europe}: ↓wE ∩ ↓europe ⊆ ↓wE ∪ ↓europe
%   %   Very Hard: biconditional over set operator semantics.
%
% One-liner : Set containment: isAllOf({wE,europe}) ⊆ isAnyOf({wE,europe})
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_extreme_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Problem-specific axioms ─────────────────────────────────────────
fof(list_223_1, axiom, in_value_list(westernEurope, sharedList223)).
fof(list_223_2, axiom, in_value_list(europe, sharedList223)).
fof(list_sharedList223_closed, axiom,
    ![G]: (in_value_list(G, sharedList223) => (G = westernEurope | G = europe))).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl223, conjecture,
    ![X]: ( in_denotation_set(X, sharedList223, isAllOf)
        => in_denotation_set(X, sharedList223, isAnyOf) )).

%--------------------------------------------------------------------------