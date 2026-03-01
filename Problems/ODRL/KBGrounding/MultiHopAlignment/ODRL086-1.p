%--------------------------------------------------------------------------
% File     : ODRL086-1.p : TPTP v0.1.0.
% Domain   : ODRL Policy Conflict Detection
% Problem  : Cross-KB conflict: eq(dE) ∩ eq(fR) = ∅ via UNA
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 5 — Cross-KB Conflict via UNA
%
% ODRL Policy (Turtle):
%   (see problem description)
%
% Formal:
%   eq(dE) = {dE}, eq(fR) = {fR}
%   dE ≠ fR  [ISO $distinct / UNA]
%   → intersection = ∅ → Conflict
%
% Difficulty: Easy
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
fof(odrl086, conjecture,
    ![X]: ~( in_denotation(X, dE, eq)
           & in_denotation(X, fR, eq) )).
%--------------------------------------------------------------------------
