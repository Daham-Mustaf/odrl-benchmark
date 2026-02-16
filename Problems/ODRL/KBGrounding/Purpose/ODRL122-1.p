%--------------------------------------------------------------------------
% File     : ODRL122-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : AND-3-operand: purpose ✗ ∧ spatial ✓ ∧ language ✓ → Conflict
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 6 (AND, 3-operand)
% Category : composition
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   AND over 3 operands: purpose=Conflict, spatial=Compatible, language=Compatible
%   AND: ∃k:Conflict → Conflict (purpose alone kills it)
%
% Denotation analysis:
%   One conflict among three operands suffices for AND-Conflict
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/LANG000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl122, conjecture,
    ![Xp]: ~( in_denotation(Xp, marketing, isA)
            & in_denotation(Xp, enforceSecurity, isA) )).
%--------------------------------------------------------------------------
