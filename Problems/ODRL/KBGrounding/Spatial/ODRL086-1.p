%--------------------------------------------------------------------------
% File     : ODRL086-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Cross-KB conflict: eq(dE) ∩ eq(fR) = ∅ via UNA
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 5 — Cross-KB Conflict via UNA
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   Dataspace A (GEO): permission spatial eq germany
%   Dataspace B (ISO): prohibition spatial eq fR
%
% Denotation analysis:
%   eq(dE) = {dE}, eq(fR) = {fR}, dE ≠ fR (ISO $distinct) → ∅ → Conflict
%   Basic test: UNA between ISO 3166 constants enables conflict detection.
%
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/ISO3166-0.ax').
include('Axioms/Alignment/ALIGN-GEO-ISO.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer1-ODRLCore/ALIGN000-0.ax').

fof(odrl086, conjecture,
    ![X]: ~( in_denotation(X, dE, eq)
           & in_denotation(X, fR, eq) )).
%--------------------------------------------------------------------------
