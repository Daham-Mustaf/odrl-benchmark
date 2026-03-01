%--------------------------------------------------------------------------
% File     : ODRL203-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : 3-Way Set Operators — isAnyOf × isNoneOf × isAllOf
% Expected : Theorem
% Verdict  : MixedNWay
% Paper    : 3-Way Set Operators — isAnyOf × isNoneOf × isAllOf
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isAnyOf ;
%   %         odrl:rightOperand ( geo:germany geo:france ) ] ] .
%   %
%   %   ex:policyB a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isNoneOf ;
%   %         odrl:rightOperand ( geo:westernEurope ) ] ] .
%   %
%   %   ex:policyC a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isAllOf ;
%   %         odrl:rightOperand ( geo:europe geo:germany ) ] ] .
%
% Formal test:
%   3-way set operator non-transitivity:
%   %   Conflict(A,B): isAnyOf({de,fr}) ∩ isNoneOf({wE}) = ∅
%   %     (de,fr both ≤ wE → excluded from complement)
%   %   Compatible(A,C): isAnyOf({de,fr}) ∩ isAllOf({europe,de}) = ↓de ≠ ∅
%   %   Conflict(B,C): isNoneOf({wE}) ∩ isAllOf({europe,de}) = (C\↓wE) ∩ ↓de = ∅
%   %   Extreme: 3 different set operators, non-transitive via complement.
%
% One-liner : 3-way set ops: isAnyOf × isNoneOf × isAllOf, non-transitive
% Difficulty: Extreme
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Problem-specific axioms ─────────────────────────────────────────
fof(list_203a_1, axiom, in_value_list(germany, anyList203)).
fof(list_203a_2, axiom, in_value_list(france, anyList203)).
fof(list_anyList203_closed, axiom,
    ![G]: (in_value_list(G, anyList203) => (G = germany | G = france))).
fof(list_203b, axiom, in_value_list(westernEurope, noneList203)).
fof(list_noneList203_closed, axiom,
    ![G]: (in_value_list(G, noneList203) => (G = westernEurope))).
fof(list_203c_1, axiom, in_value_list(europe, allList203)).
fof(list_203c_2, axiom, in_value_list(germany, allList203)).
fof(list_allList203_closed, axiom,
    ![G]: (in_value_list(G, allList203) => (G = europe | G = germany))).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl203, conjecture,
    ( ![X]: ~( in_denotation_set(X, anyList203, isAnyOf)
             & in_denotation_set(X, noneList203, isNoneOf) )
    & ?[Y]: ( in_denotation_set(Y, anyList203, isAnyOf)
            & in_denotation_set(Y, allList203, isAllOf) )
    & ![Z]: ~( in_denotation_set(Z, noneList203, isNoneOf)
             & in_denotation_set(Z, allList203, isAllOf) ) )).

%--------------------------------------------------------------------------