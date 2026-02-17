%--------------------------------------------------------------------------
% File     : ODRL204-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : isNoneOf × isPartOf — Universal Complement Conflict
% Expected : Theorem
% Verdict  : Conflict
% Paper    : isNoneOf × isPartOf — Universal Complement Conflict
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isNoneOf ;
%   %         odrl:rightOperand ( geo:europe ) ] ] .
%   %
%   %   ex:policyB a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand geo:germany ] ] .
%
% Formal test:
%   isNoneOf({europe}) ∩ isPartOf(germany) = ∅
%   %   ↓de ⊆ ↓europe → every X ∈ isPartOf(de) has leq(X, europe)
%   %   → X ∉ isNoneOf({europe})
%   %   Universal proof: ∀X: ¬(complement ∧ descendant)
%
% One-liner : Complement conflict: isNoneOf({europe}) ∩ isPartOf(de) = ∅
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_extreme_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Problem-specific axioms ─────────────────────────────────────────
fof(list_204, axiom, in_value_list(europe, noneList204)).
fof(list_noneList204_closed, axiom,
    ![G]: (in_value_list(G, noneList204) => (G = europe))).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl204, conjecture,
    ![X]: ~( in_denotation_set(X, noneList204, isNoneOf)
           & in_denotation(X, germany, isPartOf) )).

%--------------------------------------------------------------------------