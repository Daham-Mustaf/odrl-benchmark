%--------------------------------------------------------------------------
% File     : ODRL014-1.p : TPTP v0.3.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : neq(france) ∩ eq(france) — Conflict
% Version  : 0.3.0, GEO000-0.ax
% Expected : Theorem (Conflict — no witness)
% Verdict  : Conflict
% Paper    : Definition 3 (neq denotation = C \ {g})
% Notes    : Denotation of neq(france) = C \ {france}
%            Denotation of eq(france) = {france}
%            Intersection = ∅ → Conflict
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Problems/ODRL/Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Problems/ODRL/Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(conflict_neq_eq, conjecture,
    ~?[X]: ( in_denotation(X, france, neq)
           & in_denotation(X, france, eq) )).

%--------------------------------------------------------------------------
