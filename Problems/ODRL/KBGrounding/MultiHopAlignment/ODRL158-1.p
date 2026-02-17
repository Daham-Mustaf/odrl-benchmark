%--------------------------------------------------------------------------
% File     : ODRL158-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Proposition 2(2) Baseline — Compatible in Source KB
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Proposition 2(2) Baseline — Compatible in Source KB
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:hasPurpose ;
%   %         odrl:operator odrl:isA ;
%   %         odrl:rightOperand wit:witB ] ] .
%   %
%   %   ex:policyB a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:hasPurpose ;
%   %         odrl:operator odrl:isA ;
%   %         odrl:rightOperand wit:witC ] ] .
%
% Formal test:
%   Baseline for Prop 2(2) counterexample.
%   %   Source KB: witA ≤ witB, witA ≤ witC, no disjoint(witB, witC).
%   %   ⟦isA(witB)⟧ = {witA, witB}, ⟦isA(witC)⟧ = {witA, witC}
%   %   Intersection = {witA} ≠ ∅ → Compatible.
%   %   Witness: witA (shared descendant of both witB and witC).
%
% One-liner : Prop 2(2) baseline: witA witnesses isA(witB) ∩ isA(witC) ≠ ∅
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Problem-specific axioms ─────────────────────────────────────────
% --- Witness-Loss Source KB ---
% Counterexample for Proposition 2(2) (Graceful Degradation).
% witA is the shared descendant (witness): witA ≤ witB ∧ witA ≤ witC.
% witB, witC are incomparable — no disjointness asserted.
fof(wit_src_c1, axiom, concept(witA)).
fof(wit_src_c2, axiom, concept(witB)).
fof(wit_src_c3, axiom, concept(witC)).

fof(wit_src_leq1, axiom, leq(witA, witB)).
fof(wit_src_leq2, axiom, leq(witA, witC)).
fof(wit_src_refl1, axiom, leq(witA, witA)).
fof(wit_src_refl2, axiom, leq(witB, witB)).
fof(wit_src_refl3, axiom, leq(witC, witC)).

% NO disjoint(witB, witC) — incomparable, not disjoint.
fof(wit_src_una, axiom, $distinct(witA, witB, witC)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl158, conjecture,
    ?[X]: ( in_denotation(X, witB, isA)
          & in_denotation(X, witC, isA) )).

%--------------------------------------------------------------------------