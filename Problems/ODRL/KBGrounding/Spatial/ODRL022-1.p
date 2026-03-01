%--------------------------------------------------------------------------
% File     : ODRL022-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Conflict: isNoneOf({europe}) ∩ isPartOf(wE) = ∅
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 3 (isNoneOf), Definition 5
%
% ODRL Policy (Turtle):
%   ex:policyA a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isNoneOf ;
%         odrl:rightOperand ( geo:europe ) ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isPartOf ;
%         odrl:rightOperand geo:westernEurope ] ] .
%
% Formal:
%   ∀X: leq(X, westernEurope) → leq(X, europe)  [leq_trans: wE ≤ europe]
%   → every X ∈ ⟦isPartOf(wE)⟧ satisfies leq(X,europe)
%   → X is excluded by isNoneOf({europe})
%   → intersection = ∅  →  Conflict
%
% Notes    : Requires leq_trans to establish that wE ⊆ ↓europe, then contradiction.
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Problem-specific axioms ─────────────────────────────────────
fof(list_excluded022_1, axiom, in_value_list(europe, excluded022)).
fof(list_excluded022_closed, axiom,
    ![G]: (in_value_list(G, excluded022) => (G = europe))).
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl022, conjecture,
    ![X]: ~( in_denotation_set(X, excluded022, isNoneOf)
           & in_denotation(X, westernEurope, isPartOf) )).
%--------------------------------------------------------------------------
