%--------------------------------------------------------------------------
% File     : ODRL033-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Tautological equivalence: isA(germany) ≡ isPartOf(germany) 
% Expected : Theorem (Equivalence — identical denotations)
% Verdict  : Confirmed (both directions)
% Paper    : Definition 3 (isA = isPartOf), Definition 7
%
% ODRL Scenario:
%   Constraint c1:
%     { "leftOperand": "spatial",
%       "operator": "isA",
%       "rightOperand": "http://example.org/geo/germany" }
%   Constraint c2:
%     { "leftOperand": "spatial",
%       "operator": "isPartOf",
%       "rightOperand": "http://example.org/geo/germany" }
%
% Denotation analysis:
%   ⟦isA(germany)⟧ = {x | x ≤ germany} = ⟦isPartOf(germany)⟧
%   The paper (Definition 3, footnote) notes isA and isPartOf have
%   identical denotations — semantic distinction is in the KB, not operator.
%   This is a TAUTOLOGY: the two constraints are interchangeable.
%
% Encoding: ∀X: in_denotation(X, germany, isA) ↔ in_denotation(X, germany, isPartOf)
% Proof: Both den_isA and den_isPartOf reduce to leq(X, germany).
% Difficulty: Trivial — tests operator equivalence
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(odrl033, conjecture,
    ![X]: ( in_denotation(X, germany, isA)
        <=> in_denotation(X, germany, isPartOf) )).
%--------------------------------------------------------------------------
