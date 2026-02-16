%--------------------------------------------------------------------------
% File     : ODRL050-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Self-compatible: isPartOf(europe) ∩ isPartOf(europe) ≠ ∅
% Expected : Theorem (Trivially Compatible — same constraint)
% Verdict  : Compatible (tautological overlap)
% Paper    : Definition 5 (identity case)
%
% ODRL Scenario:
%   Two rules with IDENTICAL spatial constraints:
%     Rule 1: { "operator": "isPartOf", "rightOperand": "europe" }
%     Rule 2: { "operator": "isPartOf", "rightOperand": "europe" }
%
%   ⟦isPartOf(europe)⟧ ∩ ⟦isPartOf(europe)⟧ = ⟦isPartOf(europe)⟧ ≠ ∅
%   Trivially compatible — any non-empty denotation intersects itself.
%
% Proof: X=europe by reflexivity. Instant.
% Difficulty: Trivial — identity/tautology
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl050, conjecture,
    ?[X]: ( in_denotation(X, europe, isPartOf)
          & in_denotation(X, europe, isPartOf) )).
%--------------------------------------------------------------------------
