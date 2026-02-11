%--------------------------------------------------------------------------
% File     : ODRL042-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : ATTACK: isNoneOf vs isA — forced contradiction
% Status   : Theorem
% Expected : Conflict — denotations provably disjoint
%
% Attack vector: Do only-if rules from DIFFERENT operators compose
%   to produce a contradiction?
%
%   c1: purpose isA researchAndDevelopment
%       only-if: in_denotation(X,c1) => subClassOf(X, R&D)
%
%   c2: purpose isNoneOf {researchAndDevelopment}
%       only-if: in_denotation(X,c2) => ~subClassOf(X, R&D)
%
%   Any witness X would need: subClassOf(X, R&D) ∧ ~subClassOf(X, R&D)
%   This is a logical contradiction — denotations are provably disjoint.
%
%   Conjecture: ~∃X(overlap) — Theorem confirms conflict.
%   Failure mode: CounterSat would mean only-if rules don't compose
%   across operators, leaving the intersection unconstrained.
%
%   Note: isNoneOf only-if is in Layer 2. isNoneOf if-direction is
%   per-problem (grounded). For conflict proof, we only need only-if.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_operand, axiom, has_operand(c1, purpose)).
fof(c1_operator, axiom, has_operator(c1, isA)).
fof(c1_value,    axiom, has_value(c1, researchAndDevelopment)).

fof(c2_operand, axiom, has_operand(c2, purpose)).
fof(c2_operator, axiom, has_operator(c2, isNoneOf)).
fof(c2_value,    axiom, has_value(c2, researchAndDevelopment)).

% Conjecture: denotations are disjoint (negated compatibility = conflict)
fof(conflict, conjecture,
    ~?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).
%--------------------------------------------------------------------------
