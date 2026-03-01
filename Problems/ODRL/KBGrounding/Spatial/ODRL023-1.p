%--------------------------------------------------------------------------
% File     : ODRL023-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Conflict: isAllOf({wE,eE}) ∩ eq(germany) = ∅ [empty isAllOf]
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 3 (isAllOf), Definition 5
%
% ODRL Policy (Turtle):
%   ex:policyA a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isAllOf ;
%         odrl:rightOperand ( geo:westernEurope geo:easternEurope ) ] ] .
%
%   ex:policyB a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:eq ;
%         odrl:rightOperand geo:germany ] ] .
%
% Formal:
%   ⟦isAllOf({wE,eE})⟧ = {X | leq(X,wE) ∧ leq(X,eE)}
%   disjoint(wE,eE) → disj_downward → ∀X: leq(X,wE) ∧ leq(X,eE) → disj(X,X)
%   disj_irrefl → contradiction → ⟦isAllOf⟧ = ∅
%   ∅ ∩ {germany} = ∅  →  Conflict
%
% Notes    : isAllOf requires membership in ALL listed closures. Disjoint pair → empty.
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Problem-specific axioms ─────────────────────────────────────
fof(list_allRegions023_1, axiom, in_value_list(westernEurope, allRegions023)).
fof(list_allRegions023_2, axiom, in_value_list(easternEurope, allRegions023)).
fof(list_allRegions023_closed, axiom,
    ![G]: (in_value_list(G, allRegions023) => (G = westernEurope | G = easternEurope))).
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl023, conjecture,
    ![X]: ~( in_denotation_set(X, allRegions023, isAllOf)
           & in_denotation(X, germany, eq) )).
%--------------------------------------------------------------------------
