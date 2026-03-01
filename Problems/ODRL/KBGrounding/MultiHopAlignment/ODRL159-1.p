%--------------------------------------------------------------------------
% File     : ODRL159-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Proposition 2(2) Bug — Fabricated Conflict from Partial Alignment
% Expected : CounterSatisfiable
% Verdict  : FabricatedConflict
% Paper    : Proposition 2(2) Bug — Fabricated Conflict from Partial Alignment
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
%   Proposition 2(2) COUNTEREXAMPLE: partial alignment creates false Conflict.
%   %   Partial alignment α: dom(α) = {witB, witC}. Witness witA is UNMAPPED.
%   %   Target KB: {tgtB, tgtC} only (no concept for witA).
%   %   ⟦isA(tgtB)⟧ = {tgtB}, ⟦isA(tgtC)⟧ = {tgtC}
%   %   Intersection = ∅ (tgtB ≠ tgtC by UNA) → FABRICATED Conflict!
%   %   Source was Compatible (ODRL158), target is Conflict → verdict NOT preserved.
%   %   Disproves: 'partial alignment can only weaken toward Unknown, never fabricate'.
%
% One-liner : Prop 2(2) BUG: partial alignment loses witness → fabricated Conflict
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_advanced_suite.py
%--------------------------------------------------------------------------

include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% ─── Problem-specific axioms ─────────────────────────────────────────
% --- Witness-Loss Target KB (after partial alignment) ---
% dom(α) = {witB, witC}. Witness witA is UNMAPPED → lost.
% Target concepts: tgtB = α(witB), tgtC = α(witC).
fof(wit_tgt_c1, axiom, concept(tgtB)).
fof(wit_tgt_c2, axiom, concept(tgtC)).

fof(wit_tgt_refl1, axiom, leq(tgtB, tgtB)).
fof(wit_tgt_refl2, axiom, leq(tgtC, tgtC)).

% NO leq(tgtB, tgtC) or leq(tgtC, tgtB) — incomparable (matching source).
% NO concept corresponding to witA — it was lost in alignment!
fof(wit_tgt_una, axiom, $distinct(tgtB, tgtC)).

% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl159, conjecture,
    ?[X]: ( in_denotation(X, tgtB, isA)
          & in_denotation(X, tgtC, isA) )).

%--------------------------------------------------------------------------