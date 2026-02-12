%--------------------------------------------------------------------------
% File     : ODRL065-2.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection — Cross-KB Alignment
% Problem  : No false conflict: scientificResearch unmapped → NOT conflict
% Status   : CounterSatisfiable
% Expected : Unknown — cannot prove conflict either (no false Conflict)
%
% Validates: Proposition 1(2) — alignment never fabricates conflicts
%
% Companion: ODRL065-1.p (cannot prove compatible either → truly Unknown)
%
% Together ODRL065-1 + ODRL065-2 prove genuine Unknown:
%   065-1: ¬Theorem → not provably Compatible
%   065-2: ¬Theorem → not provably Conflict
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV001-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom, has_operand(c1, purpose) & has_operator(c1, isA) & has_value(c1, forschungUndEntwicklung)).
fof(c2_def, axiom, has_operand(c2, purpose) & has_operator(c2, eq) & has_value(c2, scientificResearch)).

fof(conflict, conjecture, ~?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).

%--------------------------------------------------------------------------
