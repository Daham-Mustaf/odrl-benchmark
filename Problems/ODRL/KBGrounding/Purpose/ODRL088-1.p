%--------------------------------------------------------------------------
% File     : ODRL088-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Compatible: isNoneOf × isNoneOf — large exclusions still overlap
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3 (isNoneOf), Definition 5
% Category : set
%
% ODRL Policy (Turtle):
%   isNoneOf({marketing}) ∩ isNoneOf({enforceSecurity})
%
% Denotation analysis:
%   C\↓mkt ∩ C\↓sec. Witness: legalCompliance (under fulfilmentOfObligation,
%   disjoint from both marketing and enforceSecurity)
%
% Difficulty: Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(l088a_1, axiom, in_value_list(marketing, none088a)).
fof(l088b_1, axiom, in_value_list(enforceSecurity, none088b)).

fof(odrl088, conjecture,
    ?[X]: ( in_denotation_set(X, none088a, isNoneOf)
          & in_denotation_set(X, none088b, isNoneOf) )).
%--------------------------------------------------------------------------
