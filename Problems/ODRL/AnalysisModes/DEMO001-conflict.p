%--------------------------------------------------------------------------
% File     : DEMO001-conflict.p
% Problem  : Cross-rule conflict: advertising vs research
% Expected : Theorem (Conflict - disjoint branches)
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DEMO-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% Policy 1: permission for advertising
% Policy 2: prohibition for research
% Query: Can they overlap?

fof(demo001_conflict, conjecture,
    ?[X]: ( in_denotation(X, advertising, isA)
          & in_denotation(X, research, isA) )).

%--------------------------------------------------------------------------