%--------------------------------------------------------------------------
% File     : ODRL038-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Unknown: unknownRegion not in hierarchy → verdict Unknown
% Expected : CounterSatisfiable
% Verdict  : Unknown
% Paper    : Definition 3 (grounding), Definition 5 (Unknown verdict)
%
% ODRL Policy (Turtle):
%   (see problem description)
%
% Formal:
%   γ(unknownRegion) = ⊥  (not grounded)
%   ⟦isPartOf(unknownRegion)⟧ = ⊤
%   verdict_of(⊤, classical_set) = Unknown
%
% Notes    : Demonstrates open-world semantics: missing concept → Unknown, not Conflict.
% Difficulty: Trivial
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl038, conjecture,
    ![X]: ~( in_denotation(X, europe, isPartOf)
           & in_denotation(X, unknownRegion, isPartOf) )).
%--------------------------------------------------------------------------
