%--------------------------------------------------------------------------
% File     : ODRL221-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : isAnyOf Singleton = isPartOf — Operator Equivalence
% Expected : Theorem
% Verdict  : Equivalence
% Paper    : isAnyOf Singleton = isPartOf — Operator Equivalence
%
% ODRL Policy (Conceptual):
%   (Meta-property: isAnyOf({G}) ≡ isPartOf(G))
%
% Formal test:
%   isAnyOf({G}) = ↓G (single-element union) = isPartOf(G).
%   %   Prove: ∀X: in_denotation_set(X, {de}, isAnyOf) ↔ in_denotation(X, de, isPartOf)
%
% One-liner : Operator equivalence: isAnyOf({de}) ≡ isPartOf(de)
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_extreme_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Problem-specific axioms ─────────────────────────────────────────
fof(list_221, axiom, in_value_list(germany, anyList221)).
fof(list_anyList221_closed, axiom,
    ![G]: (in_value_list(G, anyList221) => (G = germany))).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl221, conjecture,
    ![X]: ( in_denotation_set(X, anyList221, isAnyOf)
        <=> in_denotation(X, germany, isPartOf) )).

%--------------------------------------------------------------------------