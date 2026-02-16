%--------------------------------------------------------------------------
% File     : ODRL091-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Compatible: eq(legalCompliance) ∩ isNoneOf({marketing, enforceSecurity})
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3 (isNoneOf), Definition 5
% Category : set
%
% ODRL Policy (Turtle):
%   eq(legalCompliance) ∩ isNoneOf({marketing, enforceSecurity})
%
% Denotation analysis:
%   legalCompliance ≤ fulfilmentOfObligation, disjoint from both → Witness
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(l091_1, axiom, in_value_list(marketing, none091)).
fof(l091_2, axiom, in_value_list(enforceSecurity, none091)).

fof(odrl091, conjecture,
    ?[X]: ( in_denotation(X, legalCompliance, eq)
          & in_denotation_set(X, none091, isNoneOf) )).
%--------------------------------------------------------------------------
