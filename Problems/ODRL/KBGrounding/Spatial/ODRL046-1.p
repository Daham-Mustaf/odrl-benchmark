%--------------------------------------------------------------------------
% File     : ODRL046-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : XONE-Unknown: both dims compatible → exclusivity fails
% Expected : Theorem
% Verdict  : Unknown
% Paper    : Definition 6 (Composition, xone)
%
% ODRL Policy (Turtle):
%   (see problem description)
%
% Formal:
%   spatial: isPartOf(europe) ∩ eq(germany) ≠ ∅  ✓  [germany]
%   purpose: isA(R&D) ∩ isA(aR) ≠ ∅            ✓  [academicResearch]
%   XONE: both ✓ → neither exclusively satisfies → Unknown
%   Test: flip_conj proves both compatible simultaneously
%
% Notes    : flip_conj is Theorem; main XONE form is CounterSatisfiable.
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
% XONE exclusivity fails — test that both dims are simultaneously compatible
fof(odrl046, conjecture,
    ( ?[Xs]: ( in_denotation(Xs, europe, isPartOf)
             & in_denotation(Xs, germany, eq) )
    & ?[Xp]: ( in_denotation(Xp, researchAndDevelopment, isA)
             & in_denotation(Xp, academicResearch, isA) ) )).
%--------------------------------------------------------------------------
