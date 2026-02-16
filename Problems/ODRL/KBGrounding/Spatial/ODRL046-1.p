%--------------------------------------------------------------------------
% File     : ODRL046-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : XONE-Unknown: spatial ✓ ⊕ purpose ✓ → Unknown
% Expected : Theorem
% Verdict  : Unknown
% Paper    : Definition 6 (Composition, xone)
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   V_spatial=Compatible, V_purpose=Compatible → exclusivity fails → Unknown
%
% Denotation analysis:
%   XONE=(spatial∧¬purpose)∨(purpose∧¬spatial) — both disjuncts fail.
%
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl046, conjecture,
    ( ?[Xs]: ( in_denotation(Xs, europe, isPartOf)
             & in_denotation(Xs, germany, eq) )
    & ?[Xp]: ( in_denotation(Xp, researchAndDevelopment, isA)
             & in_denotation(Xp, academicResearch, isA) ) )).
%--------------------------------------------------------------------------
