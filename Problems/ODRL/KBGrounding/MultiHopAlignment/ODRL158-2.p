%--------------------------------------------------------------------------
% File     : ODRL158-2.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Proposition 2(2) Fix — Downward-Closed Alignment Preserves Verdict
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Proposition 2(2) Fix — Downward-Closed Alignment Preserves Verdict
%
% ODRL Policy (Conceptual):
%   ex:policyA a odrl:Set ;
%   %     odrl:permission [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:hasPurpose ;
%   %         odrl:operator odrl:isA ;
%   %         odrl:rightOperand tgt:tgtB ] ] .
%   %
%   %   ex:policyB a odrl:Set ;
%   %     odrl:prohibition [
%   %       odrl:action odrl:use ;
%   %       odrl:constraint [
%   %         odrl:leftOperand odrl:hasPurpose ;
%   %         odrl:operator odrl:isA ;
%   %         odrl:rightOperand tgt:tgtC ] ] .
%
% Formal test:
%   Proposition 2(2) FIX: downward-closed alignment preserves Compatible.
%   %   Total alignment β: dom(β) = {witA, witB, witC}. ALL concepts mapped.
%   %   Target KB: {tgtA, tgtB, tgtC} with tgtA ≤ tgtB, tgtA ≤ tgtC.
%   %   ⟦isA(tgtB)⟧ = {tgtA, tgtB}, ⟦isA(tgtC)⟧ = {tgtA, tgtC}
%   %   Intersection = {tgtA} ≠ ∅ → Compatible PRESERVED.
%   %   Compare: ODRL158 (source), ODRL159 (partial → fabricated Conflict).
%   %   Fix: require dom(α) ⊇ ↓g for each grounding value g.
%
% One-liner : Prop 2(2) FIX: downward-closed alignment → Compatible preserved
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-17
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Problem-specific axioms ─────────────────────────────────────────
% --- Witness-Loss Target KB (downward-closed alignment) ---
% dom(β) = {witA, witB, witC}. Witness witA IS mapped → preserved.
% Target concepts: tgtA = β(witA), tgtB = β(witB), tgtC = β(witC).
fof(wit_full_c1, axiom, concept(tgtA)).
fof(wit_full_c2, axiom, concept(tgtB)).
fof(wit_full_c3, axiom, concept(tgtC)).

fof(wit_full_leq1, axiom, leq(tgtA, tgtB)).
fof(wit_full_leq2, axiom, leq(tgtA, tgtC)).
fof(wit_full_refl1, axiom, leq(tgtA, tgtA)).
fof(wit_full_refl2, axiom, leq(tgtB, tgtB)).
fof(wit_full_refl3, axiom, leq(tgtC, tgtC)).

% Structure preserved: tgtA ≤ tgtB, tgtA ≤ tgtC (mirrors source).
fof(wit_full_una, axiom, $distinct(tgtA, tgtB, tgtC)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl158b, conjecture,
    ?[X]: ( in_denotation(X, tgtB, isA)
          & in_denotation(X, tgtC, isA) )).

%--------------------------------------------------------------------------