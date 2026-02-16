%--------------------------------------------------------------------------
% File     : ODRL098-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Multi-parent: nonCommercialResearch bridges nonCommPurpose ⊥⊥ R&D
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3, Multi-parent
% Category : multiparent
%
% ODRL Policy (Turtle):
%   nonCommercialResearch ≤ nonCommercialPurpose ∧ nonCommercialResearch ≤ researchAndDevelopment
%   disjoint(nonCommercialPurpose, researchAndDevelopment) [d_0194]
%
% Denotation analysis:
%   isA(nonCommercialPurpose) ∩ isA(researchAndDevelopment)
%
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl098, conjecture,
    ?[X]: ( in_denotation(X, nonCommercialPurpose, isA)
          & in_denotation(X, researchAndDevelopment, isA) )).
%--------------------------------------------------------------------------
