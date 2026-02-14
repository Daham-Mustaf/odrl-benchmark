%--------------------------------------------------------------------------
% File     : ODRL011-1.p : TPTP v0.3.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Spatial conflict: eq(france) ∩ eq(germany) = ∅
% Version  : 0.3.0, GEO000-0.ax
% Expected : Theorem (Conflict — no witness exists)
% Verdict  : Conflict
% Paper    : Definition 3 (denotation), Definition 5 (conflict)
% Notes    : Rule 1 constrains spatial eq france.
%            Rule 2 constrains spatial eq germany.
%            Denotation of eq(france) = {france}
%            Denotation of eq(germany) = {germany}
%            france ≠ germany (UNA) → Intersection = ∅ → Conflict
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Problems/ODRL/Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Problems/ODRL/Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% Conjecture: ¬∃x in both denotations (Table 2, Conflict pattern)
fof(conflict_spatial, conjecture,
    ~?[X]: ( in_denotation(X, france, eq)
           & in_denotation(X, germany, eq) )).

%--------------------------------------------------------------------------
