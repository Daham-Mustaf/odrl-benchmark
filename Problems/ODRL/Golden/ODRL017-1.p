%--------------------------------------------------------------------------
% File     : ODRL017-1.p : TPTP v0.3.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : isAnyOf({france, germany}) ∩ eq(bavaria) — Compatible
% Version  : 0.3.0, GEO000-0.ax
% Expected : Theorem (Compatible — witness: bavaria)
% Verdict  : Compatible
% Paper    : Definition 3 (isAnyOf = union of downward closures)
% Notes    : Denotation of isAnyOf({france, germany})
%              = {x | x ≤ france} ∪ {x | x ≤ germany}
%              = {france} ∪ {germany, bavaria}
%              = {france, germany, bavaria}
%            Denotation of eq(bavaria) = {bavaria}
%            Intersection = {bavaria} ≠ ∅
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Problems/ODRL/Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Problems/ODRL/Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% Value list for isAnyOf: {france, germany}
fof(vl_france,  axiom, in_value_list(france, list_anyof_1)).
fof(vl_germany, axiom, in_value_list(germany, list_anyof_1)).

fof(compatible_isAnyOf, conjecture,
    ?[X]: ( in_denotation_set(X, list_anyof_1, isAnyOf)
          & in_denotation(X, bavaria, eq) )).

%--------------------------------------------------------------------------
