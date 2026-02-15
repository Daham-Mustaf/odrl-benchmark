%--------------------------------------------------------------------------
% File     : ODRL020-1.p : TPTP v0.3.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : isNoneOf({france, germany}) ∩ isPartOf(germany) — Conflict
% Version  : 0.3.0, GEO000-0.ax
% Expected : Theorem (Conflict — no witness)
% Verdict  : Conflict
% Paper    : Definition 3 (isNoneOf exclusion + isPartOf downward)
% Notes    : Denotation of isNoneOf({france, germany})
%              = C \ ({x | x ≤ france} ∪ {x | x ≤ germany})
%              = {europe, france, germany, bavaria} \ {france, germany, bavaria}
%              = {europe}
%            Denotation of isPartOf(germany) = {x | x ≤ germany}
%              = {germany, bavaria}
%            Intersection: europe ∉ {germany, bavaria}
%              (europe != germany, europe != bavaria by UNA)
%              → ∅ → Conflict
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Problems/ODRL/Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Problems/ODRL/Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% Value list for isNoneOf: {france, germany}
fof(vl_france,  axiom, in_value_list(france, list_noneof_2)).
fof(vl_germany, axiom, in_value_list(germany, list_noneof_2)).

fof(conflict_isNoneOf, conjecture,
    ~?[X]: ( in_denotation_set(X, list_noneof_2, isNoneOf)
           & in_denotation(X, germany, isPartOf) )).

%--------------------------------------------------------------------------
