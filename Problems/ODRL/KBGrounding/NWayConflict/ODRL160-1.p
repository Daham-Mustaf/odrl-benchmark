%--------------------------------------------------------------------------
% File     : ODRL160-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : N-Way — 3-Policy Mutual Exclusion
% Expected : Theorem
% Verdict  : Conflict
% Paper    : N-Way — 3-Policy Mutual Exclusion
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand geo:germany ] ] .
%   %
%   %   ex:policyB a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand geo:france ] ] .
%   %
%   %   ex:policyC a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand geo:poland ] ] .
%
% Formal test:
%   3-policy mutual exclusion: all C(3,2) = 3 pairs conflict.
%   %   de ⊥ fr [siblings under wE]
%   %   de ⊥ pl [disj_downward from wE ⊥ eE + leq(de,wE) + leq(pl,eE)]
%   %   fr ⊥ pl [disj_downward from wE ⊥ eE + leq(fr,wE) + leq(pl,eE)]
%   %   Proves: pairwise analysis scales — all 3 pairs are independently empty.
%
% One-liner : 3-policy mutual exclusion: all 3 pairs conflict (de⊥fr, de⊥pl, fr⊥pl)
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl160, conjecture,
    ( ![X]: ~( in_denotation(X, germany, isPartOf)
             & in_denotation(X, france, isPartOf) )
    & ![Y]: ~( in_denotation(Y, germany, isPartOf)
             & in_denotation(Y, poland, isPartOf) )
    & ![Z]: ~( in_denotation(Z, france, isPartOf)
             & in_denotation(Z, poland, isPartOf) ) )).

%--------------------------------------------------------------------------