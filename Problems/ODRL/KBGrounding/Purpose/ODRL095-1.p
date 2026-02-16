%--------------------------------------------------------------------------
% File     : ODRL095-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Multi-parent: personalisedAdvertising bridges marketing ⊥⊥ personalisation
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3, Multi-parent
% Category : multiparent
%
% ODRL Policy (Turtle):
%   personalisedAdvertising ≤ advertising(≤marketing) ∧ personalisedAdvertising ≤ personalisation
%   disjoint(marketing, personalisation) [d_0181]
%   Under disj_downward: contradiction (Lemma 1)
%
% Denotation analysis:
%   isA(marketing) ∩ isA(personalisation)
%   Witness: personalisedAdvertising (if consistent)
%   KB inconsistency: ex falso if disj_downward propagates
%
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl095, conjecture,
    ?[X]: ( in_denotation(X, marketing, isA)
          & in_denotation(X, personalisation, isA) )).
%--------------------------------------------------------------------------
