%--------------------------------------------------------------------------
% File     : ODRL018-1.p : TPTP v0.3.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : isAllOf({france, germany}) ∩ eq(bavaria) — Conflict
% Version  : 0.3.0, GEO000-0.ax
% Expected : Theorem (Conflict — no witness)
% Verdict  : Conflict
% Paper    : Definition 3 (isAllOf = intersection of downward closures)
% Notes    : Denotation of isAllOf({france, germany})
%              = {x | x ≤ france} ∩ {x | x ≤ germany}
%              = {france} ∩ {germany, bavaria}
%              = ∅  (france and germany are disjoint)
%            Since denotation itself is empty, conflict with anything.
%            More precisely: no X can satisfy isAllOf({france, germany})
%            because disjoint(france, germany) + disj_downward blocks
%            any concept from being ≤ both.
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Problems/ODRL/Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Problems/ODRL/Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% Value list for isAllOf: {france, germany}
fof(vl_france,  axiom, in_value_list(france, list_allof_1)).
fof(vl_germany, axiom, in_value_list(germany, list_allof_1)).

fof(conflict_isAllOf, conjecture,
    ~?[X]: ( in_denotation_set(X, list_allof_1, isAllOf)
           & concept(X) )).

%--------------------------------------------------------------------------
