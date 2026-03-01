%--------------------------------------------------------------------------
% File     : ODRL021-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Compatible: isNoneOf({eE,sE}) ∩ isPartOf(wE) ≠ ∅
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3 (isNoneOf), Definition 5
%
% ODRL Policy (Turtle):
%   ex:policyA a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:spatial ;
%         odrl:operator odrl:isNoneOf ;
%         odrl:rightOperand ( geo:easternEurope geo:southernEurope ) ] ] .
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
%   ⟦isNoneOf({eE,sE})⟧ = C \ (↓eE ∪ ↓sE)
%   Witness: germany
%     leq(germany, westernEurope)  → germany ∈ isPartOf(wE)
%     disj(wE,eE) → ¬leq(germany,eE) → germany ∉ ↓eE
%     disj(wE,sE) → ¬leq(germany,sE) → germany ∉ ↓sE
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Problem-specific axioms ─────────────────────────────────────
fof(list_excluded021_1, axiom, in_value_list(easternEurope, excluded021)).
fof(list_excluded021_2, axiom, in_value_list(southernEurope, excluded021)).
fof(list_excluded021_closed, axiom,
    ![G]: (in_value_list(G, excluded021) => (G = easternEurope | G = southernEurope))).
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl021, conjecture,
    ?[X]: ( in_denotation_set(X, excluded021, isNoneOf)
          & in_denotation(X, westernEurope, isPartOf) )).
%--------------------------------------------------------------------------
