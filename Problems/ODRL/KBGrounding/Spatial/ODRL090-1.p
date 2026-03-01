%--------------------------------------------------------------------------
% File     : ODRL090-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Theorem 3 (forward): static Conflict → no runtime context satisfies both
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Theorem 3 — Runtime Soundness (Conflict → no context)
%
% ODRL Policy (Turtle):
%   (see problem description)
%
% Formal:
%   Static: ⟦isPartOf(wE)⟧ ∩ ⟦isPartOf(eE)⟧ = ∅  [Conflict, ODRL013]
%   Runtime: ∀Ω: ¬(satisfies(Ω,wE,isPartOf) ∧ satisfies(Ω,eE,isPartOf))
%   6-step refutation via satisfies_needs_assignment + backward bridge
%
% Notes    : Key: Part D (satisfies_needs_assignment) provides assigns(ω_sk,X) for the Skolem context; without it, the backward bridge cannot fire.
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/RUNTIME000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl090, conjecture,
    ![Omega]: ~( satisfies(Omega, westernEurope, isPartOf)
              & satisfies(Omega, easternEurope, isPartOf) )).
%--------------------------------------------------------------------------
