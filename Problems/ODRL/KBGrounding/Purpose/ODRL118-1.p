%--------------------------------------------------------------------------
% File     : ODRL118-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : XONE-Compatible: purpose ✓ ⊕ spatial ✗ → Compatible
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 6 (XONE)
% Category : composition
%
% ODRL Policy (Turtle):
%   V_purpose=Compatible, V_spatial=Conflict (provable via ⊥⊥)
%   XONE: ∃!k:Compat ∧ ∀j≠k:Conflict → Compatible
%
% Denotation analysis:
%   Exactly one branch satisfiable + other provably empty
%
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl118, conjecture,
    ( ?[Xp]: ( in_denotation(Xp, marketing, isA)
             & in_denotation(Xp, advertising, isA) )
    & ~( ?[Xs]: ( in_denotation(Xs, westernEurope, isPartOf)
                & in_denotation(Xs, easternEurope, isPartOf) ) ) )).
%--------------------------------------------------------------------------
