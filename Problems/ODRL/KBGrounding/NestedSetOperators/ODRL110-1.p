%--------------------------------------------------------------------------
% File     : ODRL110-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Definition 3 (isAllOf) — Empty Denotation from Disjoint Members
% Expected : Theorem
% Verdict  : EmptyDenotation
% Paper    : Definition 3 (isAllOf) — Empty Denotation from Disjoint Members
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isAllOf ;
%   %         odrl:rightOperand ( geo:westernEurope geo:easternEurope ) ] ] .
%
% Formal test:
%   ⟦isAllOf({wE, eE})⟧ = ↓wE ∩ ↓eE.
%   %   wE ⊥ eE [sibling disjointness in GEO KB]
%   %   → disj_downward: ∀X: leq(X,wE) ∧ leq(X,eE) → disjoint(X,X)
%   %   → disj_irrefl: ¬disjoint(X,X) → no such X exists.
%   %   ⟦isAllOf({wE,eE})⟧ = ∅ (vacuously true constraint).
%
% One-liner : isAllOf({wE,eE}) = ∅: disjoint members → empty denotation
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Problem-specific axioms ─────────────────────────────────────────
fof(list_110_1, axiom, in_value_list(westernEurope, list110)).
fof(list_110_2, axiom, in_value_list(easternEurope, list110)).
fof(list_list110_closed, axiom,
    ![G]: (in_value_list(G, list110) => (G = westernEurope | G = easternEurope))).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl110, conjecture,
    ![X]: ~in_denotation_set(X, list110, isAllOf)).

%--------------------------------------------------------------------------