%--------------------------------------------------------------------------
% File     : ODRL034-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Redundancy detection: isPartOf(westernEurope) ∩ eq(germany) = isPartOf(westernEurope) restricted
% Expected : Theorem (eq(germany) ⊆ isPartOf(westernEurope))
% Verdict  : Confirmed (germany constraint is redundant)
% Paper    : Definition 7, practical application: policy simplification
%
% ODRL Scenario:
%   A policy has two spatial constraints on the same rule:
%     Constraint A: { "operator": "isPartOf",
%                     "rightOperand": "westernEurope" }
%     Constraint B: { "operator": "eq",
%                     "rightOperand": "germany" }
%   Since eq(germany) ⊆ isPartOf(westernEurope), constraint B is
%   redundant — it adds no additional restriction beyond what A
%   already covers. Policy can be simplified by removing B.
%
% Denotation analysis:
%   ⟦eq(germany)⟧ = {germany}
%   ⟦isPartOf(westernEurope)⟧ = {x | x ≤ westernEurope} ⊇ {germany}
%   {germany} ⊆ {x | x ≤ westernEurope} → Confirmed
%
% Encoding: ∀X: in_denotation(X, germany, eq) → in_denotation(X, westernEurope, isPartOf)
% Difficulty: Easy — direct edge in KB
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl034, conjecture,
    ![X]: ( in_denotation(X, germany, eq)
          => in_denotation(X, westernEurope, isPartOf) )).
%--------------------------------------------------------------------------
