%--------------------------------------------------------------------------
% File     : ODRL083-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Aligned compatible: isPartOf(europe) ∩ eq(dE) ≠ ∅
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Proposition 2(1) — Compatible Verdict Preservation
%
% ODRL Policy (Turtle):
%   (see problem description)
%
% Formal:
%   ISO: leq(dE, europe)  → dE ∈ ⟦isPartOf(europe)⟧
%   eq(dE) = {dE}      → dE ∈ ⟦eq(dE)⟧
%   Witness: dE. Alignment preserves compatible verdict.
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-28
% Gen      : gen_hierarchy_suite.py
%--------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/ISO3166-0.ax').
include('Axioms/Alignment/ALIGN-GEO-ISO.ax').
include('Axioms/Layer1-ODRLCore/ALIGN000-0.ax').
% ─── Conjecture ──────────────────────────────────────────────────────
fof(odrl083, conjecture,
    ?[X]: ( in_denotation(X, europe, isPartOf)
          & in_denotation(X, dE, eq) )).
%--------------------------------------------------------------------------
