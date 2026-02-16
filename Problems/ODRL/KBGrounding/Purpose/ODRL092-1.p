%--------------------------------------------------------------------------
% File     : ODRL092-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Conflict: eq(advertising) ∩ isNoneOf({marketing}) — child excluded by ancestor
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 3 (isNoneOf), Definition 5
% Category : set
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   eq(advertising) ∩ isNoneOf({marketing})
%
% Denotation analysis:
%   advertising ≤ marketing → advertising ∈ ↓mkt → excluded → ∅
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(l092_1, axiom, in_value_list(marketing, none092)).

fof(odrl092, conjecture,
    ![X]: ~( in_denotation(X, advertising, eq)
           & in_denotation_set(X, none092, isNoneOf) )).
%--------------------------------------------------------------------------
