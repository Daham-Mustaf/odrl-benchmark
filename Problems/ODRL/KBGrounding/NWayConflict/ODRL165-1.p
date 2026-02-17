%--------------------------------------------------------------------------
% File     : ODRL165-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : N-Way — 4-Policy One Spoiler
% Expected : Theorem
% Verdict  : MixedNWay
% Paper    : N-Way — 4-Policy One Spoiler
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand geo:europe ] ] .
%   %
%   %   ex:policyB a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand geo:westernEurope ] ] .
%   %
%   %   ex:policyC a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:eq ;
%   %         odrl:rightOperand geo:germany ] ] .
%   %
%   %   ex:policyD a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand geo:easternEurope ] ] .
%
% Formal test:
%   4-policy one spoiler: D conflicts with B,C but NOT with A.
%   %   Compatible(A,D): ↓europe ∩ ↓eE = ↓eE ≠ ∅    [witness: poland]
%   %   Conflict(B,D):   ↓wE ∩ ↓eE = ∅                [wE ⊥ eE]
%   %   Conflict(C,D):   {de} ∩ ↓eE = ∅                [de ≤ wE, wE ⊥ eE → de ⊥ eE]
%   %   Shows: spoiler analysis — every pair must be checked independently.
%
% One-liner : 4-policy spoiler: Compatible(A,D) ∧ Conflict(B,D) ∧ Conflict(C,D)
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl165, conjecture,
    ( ?[X]: ( in_denotation(X, europe, isPartOf)
            & in_denotation(X, easternEurope, isPartOf) )
    & ![Y]: ~( in_denotation(Y, westernEurope, isPartOf)
             & in_denotation(Y, easternEurope, isPartOf) )
    & ![Z]: ~( in_denotation(Z, germany, eq)
             & in_denotation(Z, easternEurope, isPartOf) ) )).

%--------------------------------------------------------------------------