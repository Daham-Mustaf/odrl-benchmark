%--------------------------------------------------------------------------
% File     : ODRL120-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Definition 5 (universal) — All Descendant Pairs Conflict
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 5 (universal) — All Descendant Pairs Conflict
%
% ODRL Policy (Conceptual):
%   (Universal variant of ODRL013)
%   %   ∀G1 ∈ ↓wE, ∀G2 ∈ ↓eE: disjoint overlap → Conflict
%
% Formal test:
%   For any G1 ≤ wE and G2 ≤ eE:
%   %   disj_downward(wE ⊥ eE, G1 ≤ wE, G2 ≤ eE) → disjoint(G1, G2)
%   %   → ⟦isPartOf(G1)⟧ ∩ ⟦isPartOf(G2)⟧ = ∅ → Conflict for ALL pairs.
%
% One-liner : Universal conflict: ∀G1∈↓wE, ∀G2∈↓eE: overlap = ∅
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl120, conjecture,
    ![G1,G2,X]: (
        (leq(G1, westernEurope) & leq(G2, easternEurope))
      => ~( in_denotation(X, G1, isPartOf)
          & in_denotation(X, G2, isPartOf) ))).

%--------------------------------------------------------------------------