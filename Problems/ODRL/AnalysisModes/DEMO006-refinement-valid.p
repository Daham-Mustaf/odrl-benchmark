%--------------------------------------------------------------------------
% File     : DEMO006-refinement-valid.p
% Problem  : Valid refinement: downstream narrows upstream
% Expected : Theorem (Valid - sales narrows commercial)
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DEMO-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% Upstream policy:   permission for commercial (broad)
% Downstream policy: permission for sales (narrow)
% Query: Is downstream ⊆ upstream? (YES - valid refinement!)

fof(demo006_refinement_valid, conjecture,
    ![X]: ( in_denotation(X, sales, isA)
        => in_denotation(X, commercial, isA) )).

%--------------------------------------------------------------------------