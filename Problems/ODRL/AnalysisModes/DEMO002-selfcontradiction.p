%--------------------------------------------------------------------------
% File     : DEMO002-selfcontradiction.p
% Problem  : Intra-rule conflict: eq vs neq same concept
% Expected : Theorem (Conflict - authoring error)
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DEMO-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% Single rule with contradictory constraints:
%   constraint 1: purpose eq(sales)
%   constraint 2: purpose neq(sales)
% Query: Can both be satisfied?

fof(demo002_selfcontradiction, conjecture,
    ?[X]: ( in_denotation(X, sales, eq)
          & in_denotation(X, sales, neq) )).

%--------------------------------------------------------------------------