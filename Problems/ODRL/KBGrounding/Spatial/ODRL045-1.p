%--------------------------------------------------------------------------
% File     : ODRL045-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : XONE-Compatible: purpose ✓ ⊕ spatial ✗ → Compatible
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 6 (Composition, xone)
%
% ODRL Policy (Turtle):
%   V_spatial=Conflict(provable), V_purpose=Compatible
%
% Denotation analysis:
%   XONE: ∃!k:V_k=Compatible ∧ ∀j≠k:V_j=Conflict → Compatible
%
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl045, conjecture,
    ( ?[Xp]: ( in_denotation(Xp, researchAndDevelopment, isA)
             & in_denotation(Xp, academicResearch, isA) )
    & ~( ?[Xs]: ( in_denotation(Xs, westernEurope, isPartOf)
                & in_denotation(Xs, easternEurope, isPartOf) ) ) )).
%--------------------------------------------------------------------------
