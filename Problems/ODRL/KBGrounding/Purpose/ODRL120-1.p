%--------------------------------------------------------------------------
% File     : ODRL120-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : XONE-Conflict: purpose ✗ ⊕ spatial ✗ → Conflict
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 6 (XONE)
% Category : composition
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   V_purpose=Conflict, V_spatial=Conflict → XONE=Conflict
%
% Denotation analysis:
%   ∀k:V_k=Conflict → Conflict
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl120, conjecture,
    ( ![Xp]: ~( in_denotation(Xp, marketing, isA)
              & in_denotation(Xp, enforceSecurity, isA) )
    & ![Xs]: ~( in_denotation(Xs, westernEurope, isPartOf)
              & in_denotation(Xs, easternEurope, isPartOf) ) )).
%--------------------------------------------------------------------------
