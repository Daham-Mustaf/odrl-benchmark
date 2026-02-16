%--------------------------------------------------------------------------
% File     : ODRL123-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : OR-3-operand: purpose ✗ ∨ spatial ✗ ∨ language ✓ → Compatible
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 6 (OR, 3-operand)
% Category : composition
%
% ODRL Policy (Turtle):
%   OR over 3 operands: purpose=Conflict, spatial=Conflict, language=Compatible
%   OR: ∃k:Compatible → Compatible
%
% Denotation analysis:
%   One compatible among three operands suffices for OR-Compatible
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/LANG000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl123, conjecture,
    ( ?[Xp]: ( in_denotation(Xp, marketing, isA)
             & in_denotation(Xp, enforceSecurity, isA) )
    | ?[Xs]: ( in_denotation(Xs, westernEurope, isPartOf)
             & in_denotation(Xs, easternEurope, isPartOf) )
    | ?[Xl]: ( in_denotation(Xl, english, isA)
             & in_denotation(Xl, english, eq) ) )).
%--------------------------------------------------------------------------
