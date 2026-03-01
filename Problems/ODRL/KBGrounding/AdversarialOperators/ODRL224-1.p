%--------------------------------------------------------------------------
% File     : ODRL224-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : isAnyOf ∩ isNoneOf Same List — Self-Annihilation
% Expected : Theorem
% Verdict  : Conflict
% Paper    : isAnyOf ∩ isNoneOf Same List — Self-Annihilation
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isAnyOf ;
%   %         odrl:rightOperand ( geo:germany ) ] ] .
%   %
%   %   ex:policyB a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isNoneOf ;
%   %         odrl:rightOperand ( geo:germany ) ] ] .
%
% Formal test:
%   Self-annihilation: isAnyOf({de}) ∩ isNoneOf({de}) = ↓de ∩ (C\↓de) = ∅.
%   %   Very Hard: prover must show ∀X: leq(X,de) → ¬(¬leq(X,de))
%   %   i.e., set membership and complement are contradictory.
%
% One-liner : Self-annihilation: isAnyOf({de}) ∩ isNoneOf({de}) = ∅
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_extreme_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Problem-specific axioms ─────────────────────────────────────────
fof(list_224a, axiom, in_value_list(germany, anyList224)).
fof(list_anyList224_closed, axiom,
    ![G]: (in_value_list(G, anyList224) => (G = germany))).
fof(list_224b, axiom, in_value_list(germany, noneList224)).
fof(list_noneList224_closed, axiom,
    ![G]: (in_value_list(G, noneList224) => (G = germany))).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl224, conjecture,
    ![X]: ~( in_denotation_set(X, anyList224, isAnyOf)
           & in_denotation_set(X, noneList224, isNoneOf) )).

%--------------------------------------------------------------------------