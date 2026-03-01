%--------------------------------------------------------------------------
% File     : ODRL225-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : De Morgan-like — isNoneOf and isAllOf Don't Partition C
% Expected : Theorem
% Verdict  : NonPartition
% Paper    : De Morgan-like — isNoneOf and isAllOf Don't Partition C
%
% ODRL Policy (Conceptual):
%   (Meta-property: complement-of-union and intersection don't cover C)
%
% Formal test:
%   isNoneOf({wE,eE}) = C \ (↓wE∪↓eE), isAllOf({wE,eE}) = ↓wE∩↓eE = ∅.
%   %   These DON'T partition C: ∃X neither in complement nor in intersection.
%   %   Witness: germany ∈ ↓wE (so not in complement) but ¬∈ ↓eE (so not in isAllOf).
%   %   Extreme: prover must reason about 3 regions: complement, intersection, remainder.
%
% One-liner : Non-partition: ∃X: X ∉ isNoneOf({wE,eE}) ∧ X ∉ isAllOf({wE,eE})
% Difficulty: Extreme
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_extreme_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Problem-specific axioms ─────────────────────────────────────────
fof(list_225_1, axiom, in_value_list(westernEurope, sharedList225)).
fof(list_225_2, axiom, in_value_list(easternEurope, sharedList225)).
fof(list_sharedList225_closed, axiom,
    ![G]: (in_value_list(G, sharedList225) => (G = westernEurope | G = easternEurope))).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl225, conjecture,
    ?[X]: ( concept(X)
          & ~in_denotation_set(X, sharedList225, isNoneOf)
          & ~in_denotation_set(X, sharedList225, isAllOf) )).

%--------------------------------------------------------------------------