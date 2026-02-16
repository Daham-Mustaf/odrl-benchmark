%--------------------------------------------------------------------------
% File     : ODRL130-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Compatible: isAnyOf 3-element set ∩ eq — one subtree matches
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3 (isAnyOf, 3-element)
% Category : edge
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   isAnyOf({advertising, customerCare, legalCompliance}) ∩ eq(directMarketing)
%
% Denotation analysis:
%   directMarketing ≤ marketing, advertising ≤ marketing, but directMarketing ∉ ↓adv
%   directMarketing ∉ ↓customerCare, directMarketing ∉ ↓legalCompliance
%   BUT: is directMarketing ≤ advertising? NO (siblings under marketing)
%   So: directMarketing NOT in union → Conflict? Wait...
%   directMarketing ∉ ↓adv (sibling), ∉ ↓custCare (disjoint subtree), ∉ ↓legal (disjoint)
%   → Actually CONFLICT. Let me pick a better witness.
%   Use isAnyOf({marketing, customerCare, legalCompliance}) ∩ eq(advertising) instead.
%
% Difficulty: Medium
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(l130_1, axiom, in_value_list(marketing, set130)).
fof(l130_2, axiom, in_value_list(customerCare, set130)).
fof(l130_3, axiom, in_value_list(legalCompliance, set130)).

fof(odrl130, conjecture,
    ?[X]: ( in_denotation_set(X, set130, isAnyOf)
          & in_denotation(X, advertising, eq) )).
%--------------------------------------------------------------------------
