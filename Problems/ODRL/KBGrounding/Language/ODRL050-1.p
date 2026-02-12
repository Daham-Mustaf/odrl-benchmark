%--------------------------------------------------------------------------
% File     : ODRL050-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : Language compatible: de_AT ⊑ de (regional refinement)
% Status   : Theorem
% Expected : Compatible — witness = de_AT
%
% Scenario : Bayerische Staatsbibliothek permits manuscript access
%            for German-language contexts. Austrian National Library
%            requests in Austrian German (de-AT).
%            BCP 47: de-AT refines de → compatible.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/LNG000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

% BSB: language isA de
fof(c1_def, axiom, has_operand(c1, language) & has_operator(c1, isA) & has_value(c1, de)).

% Austrian Library: language eq de_AT
fof(c2_def, axiom, has_operand(c2, language) & has_operator(c2, eq) & has_value(c2, de_AT)).

fof(compatible, conjecture, ?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).
%--------------------------------------------------------------------------
