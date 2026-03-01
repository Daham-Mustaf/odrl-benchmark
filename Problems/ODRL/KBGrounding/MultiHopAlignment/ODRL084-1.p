%--------------------------------------------------------------------------
% File     : ODRL084-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Subsumption preservation: isPartOf(dE) ⊆ isPartOf(europe)
% Expected : Theorem
% Verdict  : Subsumption
% Paper    : Corollary 1 — Subsumption Preservation
%
% ODRL Policy (Turtle):
%   (see problem description)
%
% Formal:
%   ⟦isPartOf(dE)⟧ ⊆ ⟦isPartOf(europe)⟧
%   leq(dE, europe) in ISO3166 → leq_trans → subsumption
%   Tests Corollary 1: subsumption preserved under alignment
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
fof(odrl084, conjecture,
    ![X]: ( in_denotation(X, dE, isPartOf)
          => in_denotation(X, europe, isPartOf) )).
%--------------------------------------------------------------------------
