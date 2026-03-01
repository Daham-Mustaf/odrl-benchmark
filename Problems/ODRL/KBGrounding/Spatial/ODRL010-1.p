%--------------------------------------------------------------------------
% File     : ODRL010-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : KB property: leq transitivity — germany ⪯ europe
% Expected : Theorem
% Verdict  : Subsumption
% Paper    : Definition 2 (KB: leq transitivity)
%
% ODRL Policy (Turtle):
% (No ODRL policy — pure KB property test)
%
% Formal:
%   leq(germany, westernEurope) ∧ leq(westernEurope, europe)
%   ⟹ leq(germany, europe)  [leq_trans]
%
% Notes    : Validates leq_trans before any operator denotation tests.
% Difficulty: Trivial
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl010, conjecture, leq(germany, europe)).
%--------------------------------------------------------------------------
