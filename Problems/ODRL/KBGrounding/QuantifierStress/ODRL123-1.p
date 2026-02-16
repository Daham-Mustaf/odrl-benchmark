%--------------------------------------------------------------------------
% File     : ODRL123-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : ∀∃ Pattern — Every Descendant Has an Ancestor
% Expected : Theorem
% Verdict  : Sound
% Paper    : ∀∃ Pattern — Every Descendant Has an Ancestor
%
% ODRL Policy (Conceptual):
%   (∀G ≤ wE: ∃X such that X ∈ hasPart(G))
%
% Formal test:
%   For all G ≤ wE: leq(G, westernEurope) → in_denotation(westernEurope, G, hasPart)
%   %   Witness: X = westernEurope (leq(G, wE) → den_hasPart_if → in_den(wE, G, hasPart))
%   %   Tests: universal-existential with quantified KB concepts.
%
% One-liner : ∀∃ pattern: every G ≤ wE has ancestor in hasPart(G)
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-16
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl123, conjecture,
    ![G]: ( leq(G, westernEurope)
        => ?[X]: in_denotation(X, G, hasPart) )).

%--------------------------------------------------------------------------