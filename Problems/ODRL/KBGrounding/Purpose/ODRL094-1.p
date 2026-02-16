%--------------------------------------------------------------------------
% File     : ODRL094-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Multi-parent: commercialResearch bridges disjoint subtrees (KB consistency test)
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3, Multi-parent
% Category : multiparent
%
% ODRL Policy (Turtle):
%   commercialResearch ≤ commercialPurpose ∧ commercialResearch ≤ researchAndDevelopment
%   disjoint(commercialPurpose, researchAndDevelopment) [d_0044]
%   Under disj_downward: commercialResearch ⊥⊥ researchAndDevelopment AND
%   commercialResearch ≤ researchAndDevelopment → Lemma 1 contradiction!
%   THIS PROBLEM TESTS WHETHER THE KB IS CONSISTENT.
%
% Denotation analysis:
%   isA(commercialPurpose) ∩ isA(researchAndDevelopment)
%   Expected: Compatible (commercialResearch is witness)
%   BUT: with disj_downward, KB becomes inconsistent → Theorem trivially
%
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl094, conjecture,
    ?[X]: ( in_denotation(X, commercialPurpose, isA)
          & in_denotation(X, researchAndDevelopment, isA) )).
%--------------------------------------------------------------------------
