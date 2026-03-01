%--------------------------------------------------------------------------
% File     : ODRL162-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : N-Way — Non-Transitive Compatibility
% Expected : Theorem
% Verdict  : NonTransitive
% Paper    : N-Way — Non-Transitive Compatibility
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand geo:westernEurope ] ] .
%   %
%   %   ex:policyB a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand geo:europe ] ] .
%   %
%   %   ex:policyC a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand geo:easternEurope ] ] .
%
% Formal test:
%   Non-transitive compatibility — the key N-way insight.
%   %   Compatible(A,B): ↓wE ∩ ↓europe = ↓wE ≠ ∅  [witness: germany]
%   %   Compatible(B,C): ↓europe ∩ ↓eE = ↓eE ≠ ∅   [witness: poland]
%   %   Conflict(A,C):   ↓wE ∩ ↓eE = ∅              [wE ⊥ eE]
%   %   Proves: Compatible(A,B) ∧ Compatible(B,C) ⊬ Compatible(A,C)
%
% One-liner : Non-transitive: Compatible(A,B) ∧ Compatible(B,C) but Conflict(A,C)
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl162, conjecture,
    ( ?[X]: ( in_denotation(X, westernEurope, isPartOf)
            & in_denotation(X, europe, isPartOf) )
    & ?[Y]: ( in_denotation(Y, europe, isPartOf)
            & in_denotation(Y, easternEurope, isPartOf) )
    & ![Z]: ~( in_denotation(Z, westernEurope, isPartOf)
             & in_denotation(Z, easternEurope, isPartOf) ) )).

%--------------------------------------------------------------------------