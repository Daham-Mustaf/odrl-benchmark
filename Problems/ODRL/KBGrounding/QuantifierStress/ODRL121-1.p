%--------------------------------------------------------------------------
% File     : ODRL121-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : ∃∀ Pattern — Common Ancestor for Multiple Concepts
% Expected : Theorem
% Verdict  : Compatible
% Paper    : ∃∀ Pattern — Common Ancestor for Multiple Concepts
%
% ODRL Policy (Conceptual):
%   (∃X common to hasPart denotation of all three countries)
%
% Formal test:
%   ∃X: ∀G ∈ {de, fr, it}: leq(G, X) → in_denotation(X, G, hasPart)
%   %   Witness: europe (all three ≤ europe via regional hierarchy)
%   %   Tests: ∃∀ quantifier alternation with 3 conjuncts.
%
% One-liner : ∃∀ pattern: common ancestor europe for {de, fr, it}
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-16
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl121, conjecture,
    ?[X]: ( in_denotation(X, germany, hasPart)
          & in_denotation(X, france, hasPart)
          & in_denotation(X, italy, hasPart) )).

%--------------------------------------------------------------------------