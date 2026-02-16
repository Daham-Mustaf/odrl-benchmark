%--------------------------------------------------------------------------
% File     : ODRL082-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Compatible: isAnyOf × isAnyOf with subtree overlap
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3 (isAnyOf), Definition 5
% Category : set
%
% ODRL Policy (Turtle):
%   isAnyOf({marketing, customerManagement}) ∩ isAnyOf({advertising, customerCare})
%
% Denotation analysis:
%   advertising ≤ marketing → advertising ∈ both → Compatible
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(l082a_1, axiom, in_value_list(marketing, set082a)).
fof(l082a_2, axiom, in_value_list(customerManagement, set082a)).
fof(l082b_1, axiom, in_value_list(advertising, set082b)).
fof(l082b_2, axiom, in_value_list(customerCare, set082b)).

fof(odrl082, conjecture,
    ?[X]: ( in_denotation_set(X, set082a, isAnyOf)
          & in_denotation_set(X, set082b, isAnyOf) )).
%--------------------------------------------------------------------------
