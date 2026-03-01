%--------------------------------------------------------------------------
% File     : ODRL220-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : isAllOf Singleton = isPartOf — Operator Equivalence
% Expected : Theorem
% Verdict  : Equivalence
% Paper    : isAllOf Singleton = isPartOf — Operator Equivalence
%
% ODRL Policy (Conceptual):
%   (Meta-property: isAllOf({G}) ≡ isPartOf(G))
%
% Formal test:
%   isAllOf({G}) = ↓G (single-element intersection) = isPartOf(G).
%   %   Prove: ∀X: in_denotation_set(X, {de}, isAllOf) ↔ in_denotation(X, de, isPartOf)
%   %   Very Hard: biconditional requires proving BOTH directions.
%
% One-liner : Operator equivalence: isAllOf({de}) ≡ isPartOf(de)
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_extreme_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Problem-specific axioms ─────────────────────────────────────────
fof(list_220, axiom, in_value_list(germany, allList220)).
fof(list_allList220_closed, axiom,
    ![G]: (in_value_list(G, allList220) => (G = germany))).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl220, conjecture,
    ![X]: ( in_denotation_set(X, allList220, isAllOf)
        <=> in_denotation(X, germany, isPartOf) )).

%--------------------------------------------------------------------------