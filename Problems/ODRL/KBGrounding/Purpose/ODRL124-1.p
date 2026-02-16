%--------------------------------------------------------------------------
% File     : ODRL124-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : AND-3-operand: purpose ✓ ∧ spatial ✓ ∧ language ✓ → Compatible
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 6 (AND, all compatible)
% Category : composition
%
% ODRL Policy (Turtle):
%   AND: all 3 operands compatible → Compatible
%
% Denotation analysis:
%   V_purpose=Compatible, V_spatial=Compatible, V_language=Compatible
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/LANG000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl124, conjecture,
    ( ?[Xp]: ( in_denotation(Xp, marketing, isA)
             & in_denotation(Xp, advertising, isA) )
    & ?[Xs]: ( in_denotation(Xs, europe, isPartOf)
             & in_denotation(Xs, germany, eq) )
    & ?[Xl]: ( in_denotation(Xl, english, isA)
             & in_denotation(Xl, english, eq) ) )).
%--------------------------------------------------------------------------
