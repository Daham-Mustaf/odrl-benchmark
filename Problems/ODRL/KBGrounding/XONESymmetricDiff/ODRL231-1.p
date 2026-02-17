%--------------------------------------------------------------------------
% File     : ODRL231-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : XONE — Symmetric Difference (Derived Disjointness)
% Expected : Theorem
% Verdict  : XONESuccess
% Paper    : XONE — Symmetric Difference (Derived Disjointness)
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
%   %         odrl:rightOperand geo:poland ] ] .
%
% Formal test:
%   XONE via derived disjointness:
%   %   de ≤ wE, pl ≤ eE, disjoint(wE,eE)
%   %   → disj_downward → disjoint(de, pl) [derived, not asserted]
%   %   Witness: germany ∈ ↓de ∧ germany ∉ ↓pl.
%   %   Harder: negative proof requires multi-step derivation chain.
%
% One-liner : XONE: ↓de △ ↓pl ≠ ∅ via derived disjointness (wE⊥eE)
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl231, conjecture,
    ?[X]: ( ( in_denotation(X, germany, isPartOf)
            & ~in_denotation(X, poland, isPartOf) )
          | ( ~in_denotation(X, germany, isPartOf)
            & in_denotation(X, poland, isPartOf) ) )).

%--------------------------------------------------------------------------