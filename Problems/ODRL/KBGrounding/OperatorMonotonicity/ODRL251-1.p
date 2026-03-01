%--------------------------------------------------------------------------
% File     : ODRL251-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Lemma 2 (universal) — hasPart Anti-Monotonicity
% Expected : Theorem
% Verdict  : AntiMonotone
% Paper    : Lemma 2 (universal) — hasPart Anti-Monotonicity
%
% ODRL Policy (Conceptual):
%   (Meta-property: no ODRL policy — operator characterization)
%
% Formal test:
%   ∀A,B,X: leq(A,B) → (in_den(X,B,hasPart) → in_den(X,A,hasPart))
%   %   Proof chain: den_hasPart_onlyif → leq_trans → den_hasPart_if
%   %   Direction reverses: A ≤ B → ↑B ⊆ ↑A (smaller concept, more ancestors).
%   %   Tests: anti-monotone reasoning with universally quantified hasPart.
%
% One-liner : hasPart anti-monotonicity: leq(A,B) → ↑B ⊆ ↑A (universal)
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl251, conjecture,
    ![A,B,X]: (
        (leq(A, B) & in_denotation(X, B, hasPart))
      => in_denotation(X, A, hasPart) )).

%--------------------------------------------------------------------------