%--------------------------------------------------------------------------
% File     : ODRL132-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Definition 6 — 5-Way Existential Witness
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 6 — 5-Way Existential Witness
%
% ODRL Policy (Conceptual):
%   (5 compatible pairs in a single conjecture)
%   %   Tests large-scale existential witness construction.
%
% Formal test:
%   5 overlap witnesses — each pair from different GEO hierarchy branch.
%   %   Tests: Vampire's ability to find 5 independent witnesses.
%   %   All witnesses are grounded in the GEO KB.
%
% One-liner : 5-way existential: 5 independent compatible pairs
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl132, conjecture,
    ( ?[X1]: ( in_denotation(X1, europe, isPartOf)
             & in_denotation(X1, germany, eq) )
    & ?[X2]: ( in_denotation(X2, westernEurope, isPartOf)
             & in_denotation(X2, france, eq) )
    & ?[X3]: ( in_denotation(X3, europe, hasPart)
             & in_denotation(X3, germany, hasPart) )
    & ?[X4]: ( in_denotation(X4, westernEurope, isPartOf)
             & in_denotation(X4, bavaria, isPartOf) )
    & ?[X5]: ( in_denotation(X5, europe, isPartOf)
             & in_denotation(X5, poland, eq) ) )).

%--------------------------------------------------------------------------