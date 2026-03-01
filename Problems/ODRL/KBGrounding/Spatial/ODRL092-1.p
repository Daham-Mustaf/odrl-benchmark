%--------------------------------------------------------------------------
% File     : ODRL092-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Theorem 3 (contrapositive): runtime witness → verdict ≠ Conflict
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Theorem 3 (contrapositive) — Runtime Witness → Static Compatible
%
% ODRL Policy (Turtle):
%   (see problem description)
%
% Formal:
%   assigns(ω, france).
%   france ≤ wE  [GEO] → in_den(france, wE, isPartOf)
%   france ≠ germany  [UNA in GEO] → in_den(france, germany, neq)
%   → ∃X: in_den(X, wE, isPartOf) ∧ in_den(X, germany, neq)
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/RUNTIME000-0.ax').
% ─── Problem-specific axioms ─────────────────────────────────────
fof(runtime_context_092, axiom, assigns(omega092, france)).
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl092, conjecture,
    ?[X]: ( in_denotation(X, westernEurope, isPartOf)
          & in_denotation(X, germany, neq) )).
%--------------------------------------------------------------------------
