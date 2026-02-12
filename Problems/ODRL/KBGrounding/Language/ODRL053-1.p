%--------------------------------------------------------------------------
% File     : ODRL053-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : Language compatible: arz ⊑ ar (macrolanguage)
% Status   : Theorem
% Expected : Compatible — witness = arz (Egyptian Arabic)
%
% Scenario : BSB Arabic manuscript collection permits access for
%            Arabic-language research. Egyptian university requests
%            in Egyptian Arabic (arz). ISO 639-3 macrolanguage
%            containment: arz ⊑ ar.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/LNG000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom, has_operand(c1, language) & has_operator(c1, isA) & has_value(c1, ar)).
fof(c2_def, axiom, has_operand(c2, language) & has_operator(c2, eq) & has_value(c2, arz)).

fof(compatible, conjecture, ?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).
%--------------------------------------------------------------------------
