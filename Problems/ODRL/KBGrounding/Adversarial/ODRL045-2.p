%--------------------------------------------------------------------------
% File     : ODRL045-2.p : TPTP-ODRL Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : ATTACK RESOLUTION: isNoneOf + enriched KB — false Unknown fixed
% Status   : Theorem
% Expected : Compatible — KB enrichment resolves the gap
%
% This is ODRL045-1.p with ONE added axiom:
%   ~subClassOf(scientificResearch, commercialPurpose)
%
% Proof trace (why Theorem):
%   1. Negated conjecture: ∀X: ~in_denotation(X,c1) ∨ ~in_denotation(X,c2)
%   2. For X = scientificResearch: eq forces in_denotation(X,c2)
%   3. So ~in_denotation(scientificResearch, c1) is forced
%   4. Contrapositive of isNoneOf if-direction forces:
%      subClassOf(scientificResearch, commercialPurpose)
%   5. But the enriched KB has: ~subClassOf(scientificResearch, commercialPurpose)
%   6. CONTRADICTION → Refutation → Theorem → Compatible
%
%   This demonstrates the paper's core workflow:
%   (a) Run analysis → Unknown
%   (b) Identify KB gap (which negative fact is missing?)
%   (c) Enrich KB → rerun → definite verdict
%--------------------------------------------------------------------------

include('Axioms/Layer0-DomainKB/DPV000-0.ax').
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

% === KB ENRICHMENT: the missing negative fact ===
fof(kb_enrichment, axiom,
    ~subClassOf(scientificResearch, commercialPurpose)).

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

fof(compatible, conjecture,
    ?[X]: (in_denotation(X, c1) & in_denotation(X, c2))).
%--------------------------------------------------------------------------
