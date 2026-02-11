%--------------------------------------------------------------------------
% File     : ODRL045-1.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : ATTACK: isNoneOf + KB gap — false Unknown
% Status   : CounterSatisfiable
% Expected : Unknown — but REAL answer is Compatible
%
% Attack vector: Does a missing negative fact cause a false Unknown?
%
%   c1: purpose isNoneOf {commercialPurpose}
%       Intended denotation: everything NOT under commercialPurpose
%   c2: purpose eq scientificResearch
%
%   Real-world truth: scientificResearch ⊑ R&D, NOT ⊑ commercialPurpose
%   So the policies ARE compatible.
%
%   However, the DPV KB lacks: ~subClassOf(scientificResearch, commercialPurpose)
%   Without this negative fact, the prover cannot determine that
%   scientificResearch satisfies the isNoneOf constraint.
%
%   Proof trace (why CounterSat):
%   1. Negated conjecture: ∀X: ~in_denotation(X,c1) ∨ ~in_denotation(X,c2)
%   2. For X = scientificResearch: in_denotation via eq forces ~in_denotation(X,c1)
%   3. Contrapositive of isNoneOf if-direction: forces subClassOf(scientificResearch, commercialPurpose)
%   4. This is consistent with KB (no negative fact prevents it)
%   5. Model found → CounterSatisfiable → Unknown
%
%   Failure mode: If Theorem → the prover somehow proved
%   ~subClassOf(scientificResearch, commercialPurpose) from thin air.
%   This would mean the encoding smuggles in closed-world reasoning.
%
%   This is the KEY paper finding: open-world is CONSERVATIVE.
%   It reports Unknown rather than risking false Compatible.
%   The fix is KB enrichment: add ~subClassOf(scientificResearch, commercialPurpose).
%
%   See ODRL045-2.p for the enriched KB version that resolves to Compatible.
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

fof(c1_operand, axiom, has_operand(c1, purpose)).
fof(c1_operator, axiom, has_operator(c1, isNoneOf)).
fof(c1_value,    axiom, has_value(c1, commercialPurpose)).

% isNoneOf if-direction (grounded for this problem)
fof(isNoneOf_if_c1, axiom,
    ![X]: ((~subClassOf(X, commercialPurpose) & taxonomic(purpose))
        => in_denotation(X, c1))).

fof(c2_operand, axiom, has_operand(c2, purpose)).
fof(c2_operator, axiom, has_operator(c2, eq)).
fof(c2_value,    axiom, has_value(c2, scientificResearch)).

% Conjecture: compatible? Should FAIL — KB gap
fof(compatible, conjecture,
    ?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).
%--------------------------------------------------------------------------
