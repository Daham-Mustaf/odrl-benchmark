%--------------------------------------------------------------------------
% File     : ODRL200-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : isNoneOf × isNoneOf — Double Complement Overlap
% Expected : Theorem
% Verdict  : Compatible
% Paper    : isNoneOf × isNoneOf — Double Complement Overlap
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
%   %         odrl:rightOperand ( geo:easternEurope ) ] ] .
%
% Formal test:
%   Double complement: (C \ ↓wE) ∩ (C \ ↓eE)
%   %   europe: ¬leq(europe, wE) ∧ ¬leq(europe, eE)
%   %   Witness: europe ∈ isNoneOf({wE}) ∩ isNoneOf({eE})
%   %   Hard: prover must show ¬leq(europe, wE) — requires CWA over leq.
%
% One-liner : Double complement: isNoneOf({wE}) ∩ isNoneOf({eE}) ≠ ∅ (witness: europe)
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_extreme_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Problem-specific axioms ─────────────────────────────────────────
fof(list_200a, axiom, in_value_list(westernEurope, noneListA200)).
fof(list_noneListA200_closed, axiom,
    ![G]: (in_value_list(G, noneListA200) => (G = westernEurope))).
fof(list_200b, axiom, in_value_list(easternEurope, noneListB200)).
fof(list_noneListB200_closed, axiom,
    ![G]: (in_value_list(G, noneListB200) => (G = easternEurope))).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl200, conjecture,
    ?[X]: ( in_denotation_set(X, noneListA200, isNoneOf)
          & in_denotation_set(X, noneListB200, isNoneOf) )).

%--------------------------------------------------------------------------