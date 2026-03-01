%--------------------------------------------------------------------------
% File     : ODRL063-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Redundancy: isPartOf(europe) redundant under ∧ with isPartOf(germany)
% Expected : Theorem
% Verdict  : Derivable
% Paper    : Redundancy Detection (intra-rule ∧)
%
% ODRL Policy (Turtle):
%   ex:rule a odrl:Permission ; odrl:action odrl:use ;
%     odrl:constraint [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:germany ] ;
%     odrl:constraint [ odrl:operator odrl:isPartOf ; odrl:rightOperand geo:europe ] .
%
% Formal:
%   ⟦isPartOf(germany)⟧ ⊆ ⟦isPartOf(europe)⟧
%   Chain: leq(X,germany) → leq(germany,wE) → leq(wE,europe) → leq(X,europe)
%   → the europe constraint adds no restriction under conjunction
%   The STRICTER constraint makes the WEAKER one redundant
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl063, conjecture,
    ![X]: ( in_denotation(X, germany, isPartOf)
          => in_denotation(X, europe, isPartOf) )).
%--------------------------------------------------------------------------
