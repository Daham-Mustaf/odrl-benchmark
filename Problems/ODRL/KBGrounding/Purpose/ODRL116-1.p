%--------------------------------------------------------------------------
% File     : ODRL116-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : OR-Compatible: purpose ✗ ∨ spatial ✓ → Compatible
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 6 (OR)
% Category : composition
%
% ODRL Policy (Turtle):
%   V_purpose=Conflict(mkt⊥sec), V_spatial=Compatible(de≤eu) → OR=Compatible
%
% Denotation analysis:
%   Disjunction: ∃k:V_k=Compatible → Compatible
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl116, conjecture,
    ( ?[Xp]: ( in_denotation(Xp, marketing, isA)
             & in_denotation(Xp, enforceSecurity, isA) )
    | ?[Xs]: ( in_denotation(Xs, europe, isPartOf)
             & in_denotation(Xs, germany, eq) ) )).
%--------------------------------------------------------------------------
