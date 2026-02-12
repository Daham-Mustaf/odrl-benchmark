%--------------------------------------------------------------------------
% File     : ODRL059-2.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection — Cross-KB Alignment
% Problem  : No false conflict: de_AT unmapped → NOT provably conflicting
% Status   : CounterSatisfiable
% Expected : Unknown — cannot prove conflict either (no false Conflict)
%
% Validates: Proposition 1(2) — alignment never fabricates conflicts
%
% Companion: ODRL059-1.p (cannot prove compatible either → truly Unknown)
%
% Together ODRL059-1 + ODRL059-2 prove the verdict is genuinely Unknown:
%   059-1: ¬Theorem → not provably Compatible
%   059-2: ¬Theorem → not provably Conflict
%   Both CounterSat → Unknown (neither compatible nor conflicting)
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/LNG001-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_def, axiom, has_operand(c1, language) & has_operator(c1, isA) & has_value(c1, deu)).
fof(c2_def, axiom, has_operand(c2, language) & has_operator(c2, eq) & has_value(c2, de_AT)).

fof(conflict, conjecture, ~?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).

%--------------------------------------------------------------------------
