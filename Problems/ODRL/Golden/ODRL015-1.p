%--------------------------------------------------------------------------
% File     : ODRL015-1.p : TPTP v0.3.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : hasPart(bavaria) ∩ eq(germany) — Compatible
% Version  : 0.3.0, GEO000-0.ax
% Expected : Theorem (Compatible — witness: germany)
% Verdict  : Compatible
% Paper    : Definition 3 (hasPart denotation = {x | g ≤ x})
% Notes    : Denotation of hasPart(bavaria) = {x | bavaria ≤ x}
%              = {bavaria, germany, europe}
%            Denotation of eq(germany) = {germany}
%            Intersection = {germany} ≠ ∅
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Problems/ODRL/Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Problems/ODRL/Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(compatible_hasPart, conjecture,
    ?[X]: ( in_denotation(X, bavaria, hasPart)
          & in_denotation(X, germany, eq) )).

%--------------------------------------------------------------------------
