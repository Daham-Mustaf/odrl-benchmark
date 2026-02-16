%--------------------------------------------------------------------------
% File     : ODRL087-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Conflict: isNoneOf({purpose}) = ∅ (root exclusion)
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 3 (isNoneOf), Definition 5
% Category : set
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   ex:p1 a odrl:Set ;
%     odrl:permission [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:purpose ;
%         odrl:operator odrl:isNoneOf ;
%         odrl:rightOperand ( dpv:Purpose ) ] ] .
%
%   ex:p2 a odrl:Set ;
%     odrl:prohibition [
%       odrl:action odrl:use ;
%       odrl:constraint [
%         odrl:leftOperand odrl:purpose ;
%         odrl:operator odrl:isA ;
%         odrl:rightOperand dpv:Marketing ] ] .
%
% Denotation analysis:
%   isNoneOf({purpose}) = C \ ↓purpose = C \ C = ∅ (purpose is root)
%   ∅ ∩ anything = ∅ → Conflict
%
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(list_087_1, axiom, in_value_list(purpose, none087)).

fof(odrl087, conjecture,
    ![X]: ~( in_denotation_set(X, none087, isNoneOf)
           & in_denotation(X, marketing, isA) )).
%--------------------------------------------------------------------------
