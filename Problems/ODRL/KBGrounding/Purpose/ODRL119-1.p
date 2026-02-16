%--------------------------------------------------------------------------
% File     : ODRL119-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : XONE-Unknown: purpose ✓ ⊕ spatial ✓ → Unknown (exclusivity fails)
% Expected : Theorem
% Verdict  : Unknown
% Paper    : Definition 6 (XONE)
% Category : composition
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   V_purpose=Compatible, V_spatial=Compatible → both branches overlap → Unknown
%
% Denotation analysis:
%   XONE requires exclusive satisfaction — both Compatible fails exclusivity
%
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl119, conjecture,
    ( ?[Xp]: ( in_denotation(Xp, marketing, isA)
             & in_denotation(Xp, advertising, isA) )
    & ?[Xs]: ( in_denotation(Xs, europe, isPartOf)
             & in_denotation(Xs, germany, eq) ) )).
%--------------------------------------------------------------------------
