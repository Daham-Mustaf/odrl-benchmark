%--------------------------------------------------------------------------
% File     : ODRL250-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Lemma 2 (universal) — isPartOf Monotonicity
% Expected : Theorem
% Verdict  : Monotone
% Paper    : Lemma 2 (universal) — isPartOf Monotonicity
%
% ODRL Policy (Conceptual):
%   (Meta-property: no ODRL policy — operator characterization)
%
% Formal test:
%   ∀A,B,X: leq(A,B) → (in_den(X,A,isPartOf) → in_den(X,B,isPartOf))
%   %   Proof chain: den_isPartOf_onlyif → leq_trans → den_isPartOf_if
%   %   Tests: universally quantified operator property over arbitrary concepts.
%
% One-liner : isPartOf monotonicity: leq(A,B) → ↓A ⊆ ↓B (universal)
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl250, conjecture,
    ![A,B,X]: (
        (leq(A, B) & in_denotation(X, A, isPartOf))
      => in_denotation(X, B, isPartOf) )).

%--------------------------------------------------------------------------