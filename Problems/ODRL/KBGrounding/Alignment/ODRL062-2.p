%--------------------------------------------------------------------------
% File     : ODRL062-2.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection — Cross-KB Alignment
% Problem  : No false conflict: bavaria unmapped → NOT provably conflicting
% Status   : CounterSatisfiable
% Expected : Unknown — cannot prove conflict either (no false Conflict)
%
% Validates: Proposition 1(2) — alignment never fabricates conflicts
%
% Companion: ODRL062-1.p (cannot prove compatible either → truly Unknown)
%
% Together ODRL062-1 + ODRL062-2 prove genuine Unknown:
%   062-1: ¬Theorem → not provably Compatible
%   062-2: ¬Theorem → not provably Conflict
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/GEO001-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom, has_operand(c1, spatial) & has_operator(c1, isPartOf) & has_value(c1, deu)).
fof(c2_def, axiom, has_operand(c2, spatial) & has_operator(c2, eq) & has_value(c2, bavaria)).

fof(conflict, conjecture, ~?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).

%--------------------------------------------------------------------------
