%--------------------------------------------------------------------------
% File     : ODRL065-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Non-redundant: isPartOf(europe) ⊄ neq(germany)
% Expected : CounterSatisfiable
% Verdict  : Refuted
% Paper    : Redundancy Refuted
%
% ODRL Policy (Turtle):
%   ex:rule a odrl:Permission ;
%     odrl:constraint [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:europe ] ;
%     odrl:constraint [ odrl:operator odrl:neq ; odrl:rightOperand geo:germany ] .
%
% Formal:
%   ⟦isPartOf(europe)⟧ ⊄ ⟦neq(germany)⟧
%   Counterexample: germany
%     leq(germany, europe)  → germany ∈ ⟦isPartOf(europe)⟧
%     germany = germany     → germany ∉ ⟦neq(germany)⟧
%   → neq(germany) genuinely restricts (removes germany from scope)
%
% Notes    : flip_conj: find X ∈ isPartOf(europe) but X ∉ neq(germany). germany witnesses.
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl065, conjecture,
    ?[X]: ( in_denotation(X, europe, isPartOf)
          & ~in_denotation(X, germany, neq) )).
%--------------------------------------------------------------------------
