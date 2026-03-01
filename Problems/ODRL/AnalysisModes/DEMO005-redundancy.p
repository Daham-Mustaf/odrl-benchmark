%--------------------------------------------------------------------------
% File     : DEMO005-redundancy.p
% Problem  : Constraint redundancy: sales ⊆ commercial
% Expected : Theorem (c₂ redundant - remove it)
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DEMO-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% Rule has:
%   c1: purpose isA(sales)      [specific]
%   c2: purpose isA(commercial) [general - parent]
% Query: c1 ⊆ c2? (YES - c2 adds nothing!)

fof(demo005_redundancy, conjecture,
    ![X]: ( in_denotation(X, sales, isA)
        => in_denotation(X, commercial, isA) )).

%--------------------------------------------------------------------------