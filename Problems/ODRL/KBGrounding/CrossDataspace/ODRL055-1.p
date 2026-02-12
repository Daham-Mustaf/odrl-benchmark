%--------------------------------------------------------------------------
% File     : ODRL055-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : Three-KB cross-dataspace: language blocks compatibility
% Status   : CounterSatisfiable
% Expected : Unknown — language conflict blocks overall conjunction
%
% Scenario : Bayerische Staatsbibliothek permits European access
%            to German-language manuscripts for non-commercial use.
%            French archive requests from France in French for
%            scientific research.
%
%   Spatial:  france ⊑ europe              → Compatible ✓
%   Purpose:  scientificResearch ⊑? nonComm → Unknown   ?
%   Language: fr ⊄ de                       → Conflict  ✗
%
%   Overall: language blocks → CounterSat
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO000-0.ax').
include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer0-DomainKB/LNG000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

% BSB Policy
fof(c1_def, axiom, has_operand(c1, spatial)  & has_operator(c1, isPartOf) & has_value(c1, europe)).
fof(c3_def, axiom, has_operand(c3, purpose)  & has_operator(c3, isA)      & has_value(c3, nonCommercialPurpose)).
fof(c5_def, axiom, has_operand(c5, language)  & has_operator(c5, isA)      & has_value(c5, de)).

% French Archive Request
fof(c2_def, axiom, has_operand(c2, spatial)  & has_operator(c2, eq) & has_value(c2, france)).
fof(c4_def, axiom, has_operand(c4, purpose)  & has_operator(c4, eq) & has_value(c4, scientificResearch)).
fof(c6_def, axiom, has_operand(c6, language)  & has_operator(c6, eq) & has_value(c6, fr)).

% All three operand pairs must overlap
fof(compatible, conjecture,
    (?[X]: (in_denotation(X, c1) & in_denotation(X, c2)))
  & (?[Y]: (in_denotation(Y, c3) & in_denotation(Y, c4)))
  & (?[Z]: (in_denotation(Z, c5) & in_denotation(Z, c6)))).
%--------------------------------------------------------------------------
