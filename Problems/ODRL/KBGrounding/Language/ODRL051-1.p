%--------------------------------------------------------------------------
% File     : ODRL051-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : Language conflict: fr ⊄ de (cross-branch)
% Status   : Theorem
% Expected : Conflict — French not subsumable under German
%
% Scenario : Hamburger Kunsthalle permits metadata use in German.
%            Louvre requests in French. Languages are disjoint.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/LNG000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom, has_operand(c1, language) & has_operator(c1, isA) & has_value(c1, de)).
fof(c2_def, axiom, has_operand(c2, language) & has_operator(c2, eq) & has_value(c2, fr)).

fof(conflict, conjecture, ~?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).
%--------------------------------------------------------------------------
