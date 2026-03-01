%--------------------------------------------------------------------------
% File     : ODRL122-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Lemma 2 (universal) — Denotation Subsumption Chain
% Expected : Theorem
% Verdict  : Subsumption
% Paper    : Lemma 2 (universal) — Denotation Subsumption Chain
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand geo:bavaria ] ] .
%   %
%   %   ex:policyB a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:spatial ;
%   %         odrl:operator odrl:isPartOf ;
%   %         odrl:rightOperand geo:europe ] ] .
%
% Formal test:
%   bavaria ≤ germany ≤ westernEurope ≤ europe [3-hop chain]
%   %   → leq_trans: leq(bavaria, europe)
%   %   → ⟦isPartOf(bavaria)⟧ ⊆ ⟦isPartOf(europe)⟧
%
% One-liner : Subsumption chain: ↓bavaria ⊆ ↓europe via 3-hop leq
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl122, conjecture,
    ![X]: ( in_denotation(X, bavaria, isPartOf)
        => in_denotation(X, europe, isPartOf) )).

%--------------------------------------------------------------------------