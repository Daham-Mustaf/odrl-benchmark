%--------------------------------------------------------------------------
% File     : ODRL232-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : XONE — 3-Way Exactly-One (Mutual Exclusion)
% Expected : Theorem
% Verdict  : XONEThreeWay
% Paper    : XONE — 3-Way Exactly-One (Mutual Exclusion)
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
%   3-way XONE: ∃X in exactly one of {↓de, ↓fr, ↓pl}.
%   %   de ⊥ fr [sibling], de ⊥ pl [derived wE⊥eE], fr ⊥ pl [derived wE⊥eE]
%   %   Witness: germany (∈ ↓de, ∉ ↓fr, ∉ ↓pl)
%   %   Requires: 1 positive proof + 2 negative proofs (contradiction chains).
%   %   Tests: 3-way symmetric difference with mixed direct/derived disjointness.
%
% One-liner : 3-way XONE: exactly one of {↓de, ↓fr, ↓pl}
% Difficulty: Extreme
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl232, conjecture,
    ?[X]: ( ( in_denotation(X, germany, isPartOf)
            & ~in_denotation(X, france, isPartOf)
            & ~in_denotation(X, poland, isPartOf) )
          | ( ~in_denotation(X, germany, isPartOf)
            & in_denotation(X, france, isPartOf)
            & ~in_denotation(X, poland, isPartOf) )
          | ( ~in_denotation(X, germany, isPartOf)
            & ~in_denotation(X, france, isPartOf)
            & in_denotation(X, poland, isPartOf) ) )).

%--------------------------------------------------------------------------