%--------------------------------------------------------------------------
% File     : ODRL019-1.p : TPTP v0.3.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : isNoneOf({france}) ∩ eq(germany) — Compatible
% Version  : 0.3.0, GEO000-0.ax
% Expected : Theorem (Compatible — witness: germany)
% Verdict  : Compatible
% Paper    : Definition 3 (isNoneOf = C \ union of downward closures)
% Notes    : Denotation of isNoneOf({france})
%              = C \ {x | x ≤ france}
%              = {europe, france, germany, bavaria} \ {france}
%              = {europe, germany, bavaria}
%            Denotation of eq(germany) = {germany}
%            Intersection = {germany} ≠ ∅
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Problems/ODRL/Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Problems/ODRL/Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% Value list for isNoneOf: {france}
fof(vl_france, axiom, in_value_list(france, list_noneof_1)).

fof(compatible_isNoneOf, conjecture,
    ?[X]: ( in_denotation_set(X, list_noneof_1, isNoneOf)
          & in_denotation(X, germany, eq) )).

%--------------------------------------------------------------------------
% Domain closure for value list
fof(vl_closure, axiom,
    ![G]: (in_value_list(G, list_noneof_1) => G = france)).
