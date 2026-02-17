%--------------------------------------------------------------------------
% File     : DEMO004-redundancy.p
% Problem  : Constraint redundancy: targetedAds ⊆ advertising
% Expected : Theorem (c₂ redundant - remove it)
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DEMO-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% Rule has two constraints:
%   c1: purpose isA(targetedAds)  [specific]
%   c2: purpose isA(advertising)   [general]
% Query: Does c1 ⊆ c2? (YES - c2 is redundant!)

fof(demo004_redundancy, conjecture,
    ![X]: ( in_denotation(X, targetedAds, isA)
        => in_denotation(X, advertising, isA) )).

%--------------------------------------------------------------------------