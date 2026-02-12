%--------------------------------------------------------------------------
% File     : ODRL060-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection — Cross-KB Alignment
% Problem  : Spatial conflict preservation: GeoNames → ISO 3166
% Status   : Theorem
% Expected : Conflict — fra ⊄ deu (countries disjoint)
%
% Validates: Proposition 1(1) — Verdict Preservation (total alignment)
%
% Parallel : ODRL015-1.p (GeoNames: germany vs france → Conflict)
%
% Scenario : Dataspace A (GeoNames) detected conflict between German
%            spatial policy and French request. Dataspace B (ISO 3166)
%            uses three-letter codes. Alignment α: germany→deu, france→fra.
%
% Alignment: α(germany)=deu, α(france)=fra (total for relevant concepts)
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO001-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom, has_operand(c1, spatial) & has_operator(c1, isPartOf) & has_value(c1, deu)).
fof(c2_def, axiom, has_operand(c2, spatial) & has_operator(c2, eq) & has_value(c2, fra)).

fof(conflict, conjecture, ~?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).

%--------------------------------------------------------------------------
