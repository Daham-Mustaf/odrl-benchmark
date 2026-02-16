%--------------------------------------------------------------------------
% File     : ODRL132-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection (DPV Purpose)
% Problem  : Conflict: neq(purpose) ∩ eq(purpose) = ∅ — root exclusion
% Expected : Theorem
% Verdict  : Conflict
% Paper    : Definition 3 (neq, same value x2)
% Category : edge
% Encoding : prover-friendly (flipped for refutation provers)
%
% ODRL Policy (Turtle):
%   neq(purpose) ∩ eq(purpose)
%
% Denotation analysis:
%   purpose ∈ ⟦eq(purpose)⟧, purpose ∉ ⟦neq(purpose)⟧
%   All other X: X ∈ ⟦neq(purpose)⟧ but X ∉ ⟦eq(purpose)⟧ → ∅
%
% Difficulty: Easy
% Authors  : Mustafa, D. & Sutcliffe, G.
% Date     : 2026-02-15
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl132, conjecture,
    ![X]: ~( in_denotation(X, purpose, neq)
           & in_denotation(X, purpose, eq) )).
%--------------------------------------------------------------------------
