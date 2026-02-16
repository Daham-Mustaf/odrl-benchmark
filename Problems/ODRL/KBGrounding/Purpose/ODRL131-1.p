%--------------------------------------------------------------------------
% File     : ODRL131-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Compatible: isAllOf({marketing, purpose}) — ancestor chain, non-empty
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3 (isAllOf, ancestor chain)
% Category : edge
%
% ODRL Policy (Turtle):
%   isAllOf({marketing, purpose}) ∩ eq(advertising)
%
% Denotation analysis:
%   advertising ≤ marketing ≤ purpose → advertising ∈ ↓mkt ∩ ↓purpose = ↓marketing
%   Witness: advertising
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(l131_1, axiom, in_value_list(marketing, all131)).
fof(l131_2, axiom, in_value_list(purpose, all131)).

fof(odrl131, conjecture,
    ?[X]: ( in_denotation_set(X, all131, isAllOf)
          & in_denotation(X, advertising, eq) )).
%--------------------------------------------------------------------------
