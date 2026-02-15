%--------------------------------------------------------------------------
% File     : ODRL013-1.p : TPTP v0.3.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : neq(france) ∩ isPartOf(europe) — Compatible
% Version  : 0.3.0, GEO000-0.ax
% Expected : Theorem (Compatible — witness: germany)
% Verdict  : Compatible
% Paper    : Definition 3 (neq denotation = C \ {g})
% Notes    : Denotation of neq(france) = C \ {france}
%              = {europe, germany, bavaria}
%            Denotation of isPartOf(europe) = {x | x ≤ europe}
%              = {europe, france, germany, bavaria}
%            Intersection = {europe, germany, bavaria} ≠ ∅
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Problems/ODRL/Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Problems/ODRL/Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(compatible_neq, conjecture,
    ?[X]: ( in_denotation(X, france, neq)
          & in_denotation(X, europe, isPartOf) )).

%--------------------------------------------------------------------------
