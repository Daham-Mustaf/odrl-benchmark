%--------------------------------------------------------------------------
% File     : ODRL066-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection — Cross-KB Alignment
% Problem  : Three-domain cross-KB: alternative standards, language blocks
% Status   : CounterSatisfiable
% Expected : Unknown — language conflict blocks overall conjunction
%
% Validates: Proposition 1 + Definition 5 (conjunctive semantics)
%            End-to-end: cross-dataspace × cross-KB × three-valued
%
% Parallel : ODRL055-1.p (same scenario, original KBs: GEO000+DPV000+LNG000)
%
% Scenario : Same as ODRL055-1 but EVERY KB is the alternative standard:
%            - Spatial:  ISO 3166 (GEO001) instead of GeoNames
%            - Purpose:  GDPR-based (DPV001) instead of W3C DPV
%            - Language: ISO 639-3 (LNG001) instead of BCP 47
%
%            BSB equivalent permits European access to German-language
%            manuscripts for non-commercial use. French archive
%            equivalent requests from France, in French, for
%            scientific research.
%
%   Spatial:  fra ⊑ eur                            → Compatible ✓
%   Purpose:  scientificResearch ⊑? nichtKomm      → Unknown   ?
%             (scientificResearch not in DPV001)
%   Language: fra ⊄ deu                             → Conflict  ✗
%
%   Overall: language blocks → CounterSat
%
% KBs used: GEO001-0.ax (ISO 3166), DPV001-0.ax (GDPR), LNG001-0.ax (ISO 639-3)
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO001-0.ax').
include('Axioms/Layer0-DomainKB/DPV001-0.ax').
include('Axioms/Layer0-DomainKB/LNG001-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

% BSB-equivalent policy (alternative standard identifiers)
fof(c1_def, axiom, has_operand(c1, spatial)  & has_operator(c1, isPartOf) & has_value(c1, eur)).
fof(c3_def, axiom, has_operand(c3, purpose)  & has_operator(c3, isA)      & has_value(c3, nichtKommerziellerZweck)).
fof(c5_def, axiom, has_operand(c5, language)  & has_operator(c5, isA)      & has_value(c5, deu)).

% French archive-equivalent request (alternative standard identifiers)
fof(c2_def, axiom, has_operand(c2, spatial)  & has_operator(c2, eq) & has_value(c2, fra)).
fof(c4_def, axiom, has_operand(c4, purpose)  & has_operator(c4, eq) & has_value(c4, scientificResearch)).
fof(c6_def, axiom, has_operand(c6, language)  & has_operator(c6, eq) & has_value(c6, fra)).

% All three operand pairs must overlap
fof(compatible, conjecture,
    (?[X]: (in_denotation(X, c1) & in_denotation(X, c2)))
  & (?[Y]: (in_denotation(Y, c3) & in_denotation(Y, c4)))
  & (?[Z]: (in_denotation(Z, c5) & in_denotation(Z, c6)))).

%--------------------------------------------------------------------------
