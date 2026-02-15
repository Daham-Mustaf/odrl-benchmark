%--------------------------------------------------------------------------
% File     : ODRL016-1.p : TPTP v0.3.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : hasPart(europe) ∩ isPartOf(france) — Conflict
% Version  : 0.3.0, GEO000-0.ax
% Expected : Theorem (Conflict — no witness)
% Verdict  : Conflict
% Paper    : Definition 3 (hasPart = upward, isPartOf = downward)
% Notes    : Denotation of hasPart(europe) = {x | europe ≤ x}
%              = {europe}  (nothing above europe in this KB)
%            Denotation of isPartOf(france) = {x | x ≤ france}
%              = {france}  (nothing below france in this KB)
%            europe ≠ france (UNA) → Intersection = ∅ → Conflict
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Problems/ODRL/Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Problems/ODRL/Axioms/Layer1-ODRLCore/ODRL000-0.ax').

fof(conflict_hasPart_isPartOf, conjecture,
    ~?[X]: ( in_denotation(X, europe, hasPart)
           & in_denotation(X, france, isPartOf) )).

%--------------------------------------------------------------------------
