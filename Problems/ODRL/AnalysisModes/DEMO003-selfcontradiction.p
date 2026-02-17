%--------------------------------------------------------------------------
% File     : DEMO003-selfcontradiction.p
% Problem  : Intra-rule conflict: commercial AND nonCommercial
% Expected : Theorem (Conflict - authoring error)
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DEMO-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% Single rule requires BOTH:
%   constraint 1: purpose isA(commercial)
%   constraint 2: purpose isA(nonCommercial)
% Query: Can both be satisfied? (NO - disjoint branches!)

fof(demo003_selfcontradiction, conjecture,
    ?[X]: ( in_denotation(X, commercial, isA)
          & in_denotation(X, nonCommercial, isA) )).

%--------------------------------------------------------------------------