%--------------------------------------------------------------------------
% File     : ODRL096-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Multi-parent: servicePersonalisation bridges personalisation ⊥⊥ serviceProvision
% Expected : Theorem
% Verdict  : Compatible
% Paper    : Definition 3, Multi-parent
% Category : multiparent
%
% ODRL Policy (Turtle):
%   servicePersonalisation ≤ personalisation ∧ servicePersonalisation ≤ serviceProvision
%   disjoint(personalisation, serviceProvision) [d_0218]
%
% Denotation analysis:
%   isA(personalisation) ∩ isA(serviceProvision)
%   Witness: servicePersonalisation (if consistent)
%
% Difficulty: Very Hard
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl096, conjecture,
    ?[X]: ( in_denotation(X, personalisation, isA)
          & in_denotation(X, serviceProvision, isA) )).
%--------------------------------------------------------------------------
