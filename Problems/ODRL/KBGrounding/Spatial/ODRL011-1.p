%--------------------------------------------------------------------------
% File     : ODRL011-1.p : TPTP v0.1.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Spatial non-containment: germany ⊄ france
% Version  : GEO000-0.ax
% Expected : Theorem
% Source   : Mustafa & Sutcliffe, 
% Notes    : Tests negative containment (conflict basis).
%            Policy: spatial isPartOf france
%            Request: spatial eq germany
%            Proves disjoint denotations → Conflict.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').

fof(odrl011_non_containment, conjecture,
    ~partOf(germany, france)).
%--------------------------------------------------------------------------
