%--------------------------------------------------------------------------
% File     : ODRL097-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Multi-parent: communicationForCustomerCare bridges commMgmt ⊥⊥ custMgmt
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3, Multi-parent
% Category : multiparent
%
% ODRL Policy (Turtle):
%   communicationForCustomerCare ≤ communicationManagement ∧
%   communicationForCustomerCare ≤ customerCare ≤ customerManagement
%   disjoint(communicationManagement, customerManagement) [d_0049]
%
% Denotation analysis:
%   isA(communicationManagement) ∩ isA(customerManagement)
%   Witness: communicationForCustomerCare (if consistent)
%
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl097, conjecture,
    ?[X]: ( in_denotation(X, communicationManagement, isA)
          & in_denotation(X, customerManagement, isA) )).
%--------------------------------------------------------------------------
