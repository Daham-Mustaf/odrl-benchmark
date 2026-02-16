%--------------------------------------------------------------------------
% File     : ODRL090-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Compatible: eq(advertising) ∩ isAnyOf({marketing, enforceSecurity})
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3 (isAnyOf), Definition 5
% Category : set
%
% ODRL Policy (Turtle):
%   eq(advertising) ∩ isAnyOf({marketing, enforceSecurity})
%
% Denotation analysis:
%   advertising ∈ ↓marketing → Witness
%
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(l090_1, axiom, in_value_list(marketing, set090)).
fof(l090_2, axiom, in_value_list(enforceSecurity, set090)).

fof(odrl090, conjecture,
    ?[X]: ( in_denotation(X, advertising, eq)
          & in_denotation_set(X, set090, isAnyOf) )).
%--------------------------------------------------------------------------
