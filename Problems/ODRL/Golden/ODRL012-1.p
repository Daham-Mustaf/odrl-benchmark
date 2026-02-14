%--------------------------------------------------------------------------
% File     : ODRL012-1.p : TPTP v0.3.0
% Domain   : ODRL Policy Conflict Detection
% Problem  : Spatial conflict: isPartOf(france) ∩ isPartOf(germany) = ∅
% Version  : 0.3.0, GEO000-0.ax
% Expected : Theorem (Conflict — disjointness blocks overlap)
% Verdict  : Conflict
% Paper    : Definition 2 (⊥⊥ downward closure), Definition 3, 5
% Notes    : Rule 1 constrains spatial isPartOf france.
%            Rule 2 constrains spatial isPartOf germany.
%            Denotation of isPartOf(france) = {x | x ≤ france}
%              = {france}  (france has no sub-regions in this KB)
%            Denotation of isPartOf(germany) = {x | x ≤ germany}
%              = {germany, bavaria}
%            disjoint(france, germany) is asserted.
%            disj_downward derives: disjoint(france, bavaria).
%            So france ∉ {germany, bavaria} and
%              {germany, bavaria} ∩ {france} = ∅ → Conflict
% Authors  : Mustafa, D. & Sutcliffe, G.
%--------------------------------------------------------------------------
include('Problems/ODRL/Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Problems/ODRL/Axioms/Layer1-ODRLCore/ODRL000-0.ax').

% Conjecture: ¬∃x in both denotations (Table 2, Conflict pattern)
fof(conflict_disjoint, conjecture,
    ~?[X]: ( in_denotation(X, france, isPartOf)
           & in_denotation(X, germany, isPartOf) )).

%--------------------------------------------------------------------------
