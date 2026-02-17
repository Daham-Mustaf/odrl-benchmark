%--------------------------------------------------------------------------
% File     : ODRL234-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : XONE + isNoneOf — Set Negation × Symmetric Difference
% Expected : Theorem
% Verdict  : XONESetOp
% Paper    : XONE + isNoneOf — Set Negation × Symmetric Difference
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
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand geo:easternEurope ] ] .
%
% Formal test:
%   XONE: isNoneOf({wE}) △ isPartOf(eE)
%   %   Second disjunct (X ≤ wE ∧ X ≤ eE): impossible (wE ⊥ eE)
%   %   First disjunct: ∃X: X ∉ ↓wE ∧ X ∉ ↓eE
%   %   Witness: europe (~leq(europe,wE) via eE-collapse, ~leq(europe,eE) via wE-collapse)
%   %   Tests: XONE with set-theoretic complement (isNoneOf) + negative root reasoning.
%
% One-liner : XONE: isNoneOf({wE}) △ isPartOf(eE), witness = europe (root)
% Difficulty: Extreme
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Problem-specific axioms ─────────────────────────────────────────
fof(list_234_1, axiom, in_value_list(westernEurope, noneList234)).
fof(list_noneList234_closed, axiom,
    ![G]: (in_value_list(G, noneList234) => (G = westernEurope))).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl234, conjecture,
    ?[X]: ( ( in_denotation_set(X, noneList234, isNoneOf)
            & ~in_denotation(X, easternEurope, isPartOf) )
          | ( ~in_denotation_set(X, noneList234, isNoneOf)
            & in_denotation(X, easternEurope, isPartOf) ) )).

%--------------------------------------------------------------------------