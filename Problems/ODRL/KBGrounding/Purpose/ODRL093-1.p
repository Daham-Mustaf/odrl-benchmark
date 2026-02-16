%--------------------------------------------------------------------------
% File     : ODRL093-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Compatible: isAnyOf({advertising, customerCare}) ∩ isPartOf(customerMgmt)
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3, Definition 5
% Category : set
%
% ODRL Policy (Turtle):
%   isAnyOf({advertising, customerCare}) ∩ isPartOf(customerManagement)
%
% Denotation analysis:
%   customerCare ≤ customerManagement → customerCare ∈ both → Witness
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(l093_1, axiom, in_value_list(advertising, set093)).
fof(l093_2, axiom, in_value_list(customerCare, set093)).

fof(odrl093, conjecture,
    ?[X]: ( in_denotation_set(X, set093, isAnyOf)
          & in_denotation(X, customerManagement, isPartOf) )).
%--------------------------------------------------------------------------
