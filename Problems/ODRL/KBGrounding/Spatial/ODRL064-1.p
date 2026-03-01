%--------------------------------------------------------------------------
% File     : ODRL064-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Redundancy: isAnyOf({germany,france}) ⊆ isPartOf(westernEurope)
% Expected : Theorem
% Verdict  : Derivable
% Paper    : Redundancy Detection (set-valued)
%
% ODRL Policy (Turtle):
%   ex:rule a odrl:Permission ;
%     odrl:constraint [ odrl:operator odrl:isAnyOf ;
%       odrl:rightOperand ( geo:germany geo:france ) ] ;
%     odrl:constraint [ odrl:operator odrl:isPartOf ;
%       odrl:rightOperand geo:westernEurope ] .
%
% Formal:
%   ⟦isAnyOf({de,fr})⟧ = ↓germany ∪ ↓france
%   leq(germany,wE) → ↓germany ⊆ ↓wE
%   leq(france,wE)  → ↓france  ⊆ ↓wE
%   → isAnyOf({de,fr}) ⊆ isPartOf(wE) → wE constraint redundant
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Problem-specific axioms ─────────────────────────────────────
fof(list_anyList064_1, axiom, in_value_list(germany, anyList064)).
fof(list_anyList064_2, axiom, in_value_list(france, anyList064)).
fof(list_anyList064_closed, axiom,
    ![G]: (in_value_list(G, anyList064) => (G = germany | G = france))).
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl064, conjecture,
    ![X]: ( in_denotation_set(X, anyList064, isAnyOf)
          => in_denotation(X, westernEurope, isPartOf) )).
%--------------------------------------------------------------------------
