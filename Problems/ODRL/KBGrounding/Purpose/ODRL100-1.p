%--------------------------------------------------------------------------
% File     : ODRL100-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : KB consistency: ¬∃(X≤Y ∧ X⊥⊥Y) — Lemma 1 meta-test
% Expected : Theorem
% Verdict  : Consistent
% Paper    : Lemma 1 (disj-order consistency)
% Category : multiparent
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   META-TEST: Can we derive ⊥ from the KB?
%   If disj_downward is active, multi-parent nodes create contradictions.
%
% Denotation analysis:
%   Conjecture: ∃ concept that is both ≤ X and ⊥⊥ X → should be impossible
%   by Lemma 1. If Theorem: KB is INCONSISTENT.
%
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl100, conjecture,
    ![X,Y]: ~( leq(X, Y) & disjoint(X, Y) )).
%--------------------------------------------------------------------------
