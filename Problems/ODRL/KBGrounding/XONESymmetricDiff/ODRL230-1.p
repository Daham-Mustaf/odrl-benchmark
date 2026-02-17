%--------------------------------------------------------------------------
% File     : ODRL230-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : XONE — Basic Symmetric Difference (Disjoint Siblings)
% Expected : Theorem
% Verdict  : XONESuccess
% Paper    : XONE — Basic Symmetric Difference (Disjoint Siblings)
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
%
% Formal test:
%   XONE: ∃X in exactly one of ↓de, ↓fr (symmetric difference).
%   %   Witness: germany ∈ ↓de ∧ germany ∉ ↓fr.
%   %   Negative proof: leq(de,fr) → disj_downward(de,fr,de,de) → disj(de,de) → ⊥
%   %   Tests: ATP proof by contradiction for negative denotation membership.
%
% One-liner : XONE: ↓de △ ↓fr ≠ ∅ via sibling disjointness
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl230, conjecture,
    ?[X]: ( ( in_denotation(X, germany, isPartOf)
            & ~in_denotation(X, france, isPartOf) )
          | ( ~in_denotation(X, germany, isPartOf)
            & in_denotation(X, france, isPartOf) ) )).

%--------------------------------------------------------------------------