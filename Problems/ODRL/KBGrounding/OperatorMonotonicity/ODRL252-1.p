%--------------------------------------------------------------------------
% File     : ODRL252-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Corollary — isNoneOf Anti-Monotonicity (Concrete)
% Expected : Theorem
% Verdict  : AntiMonotone
% Paper    : Corollary — isNoneOf Anti-Monotonicity (Concrete)
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isNoneOf ;
%   %         odrl:rightOperand ( geo:westernEurope ) ] ] .
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
%   isNoneOf anti-monotonicity: leq(de, wE) → isNoneOf({wE}) ⊆ isNoneOf({de})
%   %   Contrapositive of isPartOf monotonicity.
%   %   ∀X: (concept(X) ∧ ¬leq(X,wE)) → (concept(X) ∧ ¬leq(X,de))
%   %   Tests: negation + set operator + hierarchy reasoning combined.
%
% One-liner : isNoneOf anti-monotone: de ≤ wE → isNoneOf({wE}) ⊆ isNoneOf({de})
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Problem-specific axioms ─────────────────────────────────────────
fof(list_252a, axiom, in_value_list(westernEurope, noneListWE252)).
fof(list_noneListWE252_closed, axiom,
    ![G]: (in_value_list(G, noneListWE252) => (G = westernEurope))).
fof(list_252b, axiom, in_value_list(germany, noneListDE252)).
fof(list_noneListDE252_closed, axiom,
    ![G]: (in_value_list(G, noneListDE252) => (G = germany))).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl252, conjecture,
    ![X]: (
        in_denotation_set(X, noneListWE252, isNoneOf)
      => in_denotation_set(X, noneListDE252, isNoneOf) )).

%--------------------------------------------------------------------------