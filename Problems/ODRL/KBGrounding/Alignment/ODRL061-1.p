%--------------------------------------------------------------------------
% File     : ODRL061-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection — Cross-KB Alignment
% Problem  : Spatial compatible preservation: GeoNames → ISO 3166
% Status   : Theorem
% Expected : Compatible — witness = fra (fra ⊑ eur)
%
% Validates: Proposition 1(1) — Verdict Preservation (total alignment)
%
% Parallel : ODRL010-1.p (GeoNames: france ⊑ europe → Compatible)
%
% Scenario : Dataspace A (GeoNames) found European policy compatible
%            with French request. Dataspace B (ISO 3166) uses
%            three-letter codes. Alignment α: europe→eur, france→fra.
%
% Alignment: α(europe)=eur, α(france)=fra (total for relevant concepts)
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO001-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom, has_operand(c1, spatial) & has_operator(c1, isPartOf) & has_value(c1, eur)).
fof(c2_def, axiom, has_operand(c2, spatial) & has_operator(c2, eq) & has_value(c2, fra)).

fof(compatible, conjecture, ?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).

%--------------------------------------------------------------------------
