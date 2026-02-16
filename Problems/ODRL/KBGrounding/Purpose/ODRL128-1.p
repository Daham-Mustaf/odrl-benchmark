%--------------------------------------------------------------------------
% File     : ODRL128-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Conflict: sibling leaves isA — disjoint by axiom
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 3, Definition 5
% Category : edge
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   Same parent's children are disjoint — isA goes downward.
%
% Denotation analysis:
%   sellDataToThirdParties ⊥⊥ sellInsightsFromData [d_0263]
%   ↓sellData ∩ ↓sellInsights = ∅ (both are leaves)
%
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl128, conjecture,
    ![X]: ~( in_denotation(X, sellDataToThirdParties, isA)
           & in_denotation(X, sellInsightsFromData, isA) )).
%--------------------------------------------------------------------------
