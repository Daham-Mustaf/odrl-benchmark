%--------------------------------------------------------------------------
% File     : ODRL042-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : OR-Compatible: V_spatial=Conflict ∨ V_purpose=Compatible
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 6 (Composition, or)
%
% ODRL Policy (Turtle):
%   (see problem description)
%
% Formal:
%   spatial: isPartOf(wE) ∩ isPartOf(eE) = ∅  [disjoint siblings]
%   purpose: isA(R&D) ∩ isA(aR) ≠ ∅  [aR ≤ R&D, witness: academicResearch]
%   OR: purpose ✓ → Compatible despite spatial ✗
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl042, conjecture,
    ( ?[Xs]: ( in_denotation(Xs, westernEurope, isPartOf)
             & in_denotation(Xs, easternEurope, isPartOf) )
    | ?[Xp]: ( in_denotation(Xp, researchAndDevelopment, isA)
             & in_denotation(Xp, academicResearch, isA) ) )).
%--------------------------------------------------------------------------
