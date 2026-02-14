%--------------------------------------------------------------------------
% File     : ODRL010-1.p : TPTP v0.3.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Spatial compatibility: isPartOf(europe) ∩ eq(germany) ≠ ∅
% Version  : 0.3.0, GEO000-0.ax
% Expected : Theorem (Compatible — witness exists)
% Verdict  : Compatible
% Paper    : Definition 3 (denotation), Definition 5 (conflict)
% Notes    : Rule 1 constrains spatial isPartOf europe.
%            Rule 2 constrains spatial eq germany.
%            Denotation of isPartOf(europe) = {x | x ≤ europe}
%              = {europe, france, germany, bavaria}
%            Denotation of eq(germany) = {germany}
%            Intersection = {germany} ≠ ∅ → Compatible
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Problems/ODRL/Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Problems/ODRL/Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% Conjecture: ∃x in both denotations (Table 2, Compatible pattern)
fof(compatible_spatial, conjecture,
    ?[X]: ( in_denotation(X, europe, isPartOf)
          & in_denotation(X, germany, eq) )).

%--------------------------------------------------------------------------
