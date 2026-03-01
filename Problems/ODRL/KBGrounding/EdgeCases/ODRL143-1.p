%--------------------------------------------------------------------------
% File     : ODRL143-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Reflexivity — Every Concept Is In Its Own isPartOf
% Expected : Theorem
% Verdict  : Tautology
% Paper    : Reflexivity — Every Concept Is In Its Own isPartOf
%
% ODRL Policy (Conceptual):
%   (Meta-property: ∀G: G ∈ ⟦isPartOf(G)⟧)
%
% Formal test:
%   leq_refl: leq(G, G) [reflexivity in KB]
%   %   → den_isPartOf_if: in_denotation(G, G, isPartOf)
%   %   Universally quantified over all KB concepts.
%
% One-liner : Reflexivity: ∀G: concept(G) → G ∈ ⟦isPartOf(G)⟧
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl143, conjecture,
    ![G]: ( concept(G)
        => in_denotation(G, G, isPartOf) )).

%--------------------------------------------------------------------------