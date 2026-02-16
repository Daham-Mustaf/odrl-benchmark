%--------------------------------------------------------------------------
% File     : ODRL099-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Multi-parent: improveInternalCRMProcesses bridges custMgmt ⊥⊥ servProv (deepest)
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3, Multi-parent
% Category : multiparent
%
% ODRL Policy (Turtle):
%   improveInternalCRMProcesses ≤ customerRelationshipManagement(≤customerManagement)
%   ∧ improveInternalCRMProcesses ≤ optimisationForController(≤serviceOptimisation≤serviceProvision)
%   disjoint(customerManagement, serviceProvision) [d_0090]
%
% Denotation analysis:
%   isA(customerManagement) ∩ isA(serviceProvision)
%   Witness: improveInternalCRMProcesses (longest chain, 2 hops each side)
%
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl099, conjecture,
    ?[X]: ( in_denotation(X, customerManagement, isA)
          & in_denotation(X, serviceProvision, isA) )).
%--------------------------------------------------------------------------
