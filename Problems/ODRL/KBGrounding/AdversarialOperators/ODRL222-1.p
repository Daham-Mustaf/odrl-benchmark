%--------------------------------------------------------------------------
% File     : ODRL222-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : isNoneOf({root}) = ∅ — Root Complement Is Empty
% Expected : Theorem
% Verdict  : EmptyComplement
% Paper    : isNoneOf({root}) = ∅ — Root Complement Is Empty
%
% ODRL Policy (Conceptual):
%   (Meta-property: complement of root concept is empty)
%
% Formal test:
%   isNoneOf({europe}) = C_geo \ ↓europe.
%   %   europe is the root → all concepts ≤ europe → complement = ∅.
%   %   Very Hard: requires ∀X: concept(X) → leq(X, europe) (root reachability).
%
% One-liner : Root complement empty: isNoneOf({europe}) = ∅
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_extreme_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Problem-specific axioms ─────────────────────────────────────────
fof(list_222, axiom, in_value_list(europe, noneList222)).
fof(list_noneList222_closed, axiom,
    ![G]: (in_value_list(G, noneList222) => (G = europe))).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl222, conjecture,
    ![X]: ( concept(X)
        => ~in_denotation_set(X, noneList222, isNoneOf) )).

%--------------------------------------------------------------------------