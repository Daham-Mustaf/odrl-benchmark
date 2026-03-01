%--------------------------------------------------------------------------
% File     : ODRL095-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Lemma 2 + Theorem 3: runtime conflict propagation via subsumption
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Lemma 2 + Theorem 3 — Runtime Conflict Propagation
%
% ODRL Policy (Turtle):
%   (see problem description)
%
% Formal:
%   Lemma 2: isPartOf(germany) ⊑ isPartOf(wE)  [germany ≤ wE in GEO]
%   disj(wE, eE) + leq(germany, wE) → conflict(germany, eE)
%   Theorem 3: ∀Ω: ¬(satisfies(Ω,germany,isPartOf)∧satisfies(Ω,eE,isPartOf))
%   7-step refutation: ODRL090 proof + one extra leq_trans at step 5
%
% Notes    : Hardest runtime problem: requires Vampire to chain leq_trans before disj_downward. The 7-step proof requires deeper search than ODRL090.
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/RUNTIME000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl095, conjecture,
    ![Omega]: ~( satisfies(Omega, germany, isPartOf)
              & satisfies(Omega, easternEurope, isPartOf) )).
%--------------------------------------------------------------------------
