%--------------------------------------------------------------------------
% File     : ODRL062-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection — Cross-KB Alignment
% Problem  : Spatial graceful degradation: bavaria unmapped in ISO 3166
% Status   : CounterSatisfiable
% Expected : Unknown — bavaria has no grounding in ISO 3166 KB
%
% Validates: Proposition 1(2) — Graceful Degradation (partial alignment)
%
% Parallel : ODRL011-1.p (GeoNames: bavaria ⊑ germany → Compatible)
%
% Scenario : Dataspace A (GeoNames) found German policy compatible
%            with Bavarian request (bavaria ⊑ germany). Dataspace B
%            (ISO 3166) has no sub-national regions — bavaria is
%            unmappable. Compatible degrades to Unknown.
%
% Alignment: α(germany)=deu, α(bavaria)=⊥ (partial — region lost)
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO001-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom, has_operand(c1, spatial) & has_operator(c1, isPartOf) & has_value(c1, deu)).
fof(c2_def, axiom, has_operand(c2, spatial) & has_operator(c2, eq) & has_value(c2, bavaria)).

fof(compatible, conjecture, ?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).

%--------------------------------------------------------------------------
