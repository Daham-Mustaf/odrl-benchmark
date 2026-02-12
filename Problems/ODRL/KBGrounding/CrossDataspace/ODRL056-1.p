%--------------------------------------------------------------------------
% File     : ODRL056-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : Diagnostic: language is the blocking operand
% Status   : Theorem
% Expected : Conflict — fr ⊄ de (disjointness in LNG KB)
%
% Scenario : Follow-up from ODRL055-1. Overall compatibility failed.
%            Test language pair in isolation → confirms language
%            is the blocking dimension.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/LNG000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c5_def, axiom, has_operand(c5, language) & has_operator(c5, isA) & has_value(c5, de)).
fof(c6_def, axiom, has_operand(c6, language) & has_operator(c6, eq) & has_value(c6, fr)).

fof(conflict, conjecture, ~?[Z]: (in_denotation(Z, c5) & in_denotation(Z, c6))).
%--------------------------------------------------------------------------
