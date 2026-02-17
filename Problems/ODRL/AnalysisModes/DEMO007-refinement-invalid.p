%--------------------------------------------------------------------------
% File     : DEMO007-refinement-invalid.p
% Problem  : Invalid refinement: downstream widens upstream
% Expected : CounterSatisfiable (DSSC violation - reverse direction)
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DEMO-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% Upstream policy:   permission for sales (narrow)
% Downstream policy: permission for commercial (broad)
% Query: Is downstream ⊆ upstream? (NO - downstream widens!)
% This VIOLATES DSSC supply chain rules.

fof(demo007_refinement_invalid, conjecture,
    ![X]: ( in_denotation(X, commercial, isA)
        => in_denotation(X, sales, isA) )).

%--------------------------------------------------------------------------