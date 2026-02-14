%------------------------------------------------------------------------------
% File     : ODRL214-1.p : TPTP-ODRL Killer Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : Full BSB/French Archive scenario in base DPV KB
% Version  : [Semantics] : Denotational
% English  : BSB permits cultural data use under XONE policy with two branches:
%            Branch A: non-commercial purpose AND within Western Europe
%            Branch B: commercial purpose AND only in Germany
%            French Archive requests access for scientific research from France.
%            
%            In base DPV KB (without explicit ¬(sciRes ⊑ commercial)), the
%            position of scientificResearch relative to commercialPurpose is
%            underdetermined → Unknown verdict.
%
% Refs     : [MS26] Mustafa & Sutcliffe (2026), Formal Foundations for ODRL
% Source   : [DM]
% Names    : Killer benchmark (base KB)
%
% Status   : CounterSatisfiable
% Rating   : 1.00 v0.1.0
%
% Comments : This is the ACTUAL killer benchmark that exercises all definitions,
%            lemmas, propositions, and theorems from Section 3 of the paper.
%            Compare with:
%            - ODRL214-2.p (enriched KB → Theorem/Compatible)
%            - ODRL214-3.p (aligned KB → CounterSat/Unknown)
%------------------------------------------------------------------------------

%------------------------------------------------------------------------------
% Layer 0: Domain Knowledge Bases
%------------------------------------------------------------------------------

% Purpose taxonomy (W3C DPV v2.2, 10 concepts, DAG structure)
% NOTE: Base version WITHOUT explicit ¬(scientificResearch ⊑ commercialPurpose)
include('Axioms/Layer0-DomainKB/DPV000-0.ax').

% Spatial hierarchy (GeoNames fragment, 9 concepts, depth 4)
% Includes: World > Europe > WesternEurope > {France, Germany, Austria}
%           and Europe > EasternEurope
%           and France > Paris
include('Axioms/Layer0-DomainKB/GEO003-0.ax').

%------------------------------------------------------------------------------
% Layer 1: ODRL Operator Semantics (Bidirectional Denotation Rules)
%------------------------------------------------------------------------------

% Defines in_denotation/2 predicate for:
% - eq, neq (equality operators)
% - isA, isPartOf, hasPart (hierarchical operators)
% - isAnyOf, isAllOf, isNoneOf (set-valued operators)
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

%------------------------------------------------------------------------------
% Layer 2: Grounding Function γ: V → C
%------------------------------------------------------------------------------

% Maps ODRL right operand values to KB concepts
% Handles unmapped values: γ(v) = ⊥ → ⟦c⟧ = ⊤
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

%------------------------------------------------------------------------------
% Policy Definition: BSB XONE Policy
%------------------------------------------------------------------------------

% Branch A: Non-commercial use within Western Europe
% Formalized as: and(purpose isNoneOf {commercialPurpose},
%                     spatial isPartOf westernEurope)

fof(branch_a_purpose_def, axiom,
    has_operand(c_branch_a_purpose, purpose) &
    has_operator(c_branch_a_purpose, isNoneOf) &
    has_value_set(c_branch_a_purpose, [commercialPurpose])).

fof(branch_a_spatial_def, axiom,
    has_operand(c_branch_a_spatial, spatial) &
    has_operator(c_branch_a_spatial, isPartOf) &
    has_value(c_branch_a_spatial, westernEurope)).

% Branch B: Commercial use only in Germany
% Formalized as: and(purpose isA commercialPurpose,
%                     spatial eq germany)

fof(branch_b_purpose_def, axiom,
    has_operand(c_branch_b_purpose, purpose) &
    has_operator(c_branch_b_purpose, isA) &
    has_value(c_branch_b_purpose, commercialPurpose)).

fof(branch_b_spatial_def, axiom,
    has_operand(c_branch_b_spatial, spatial) &
    has_operator(c_branch_b_spatial, eq) &
    has_value(c_branch_b_spatial, germany)).

%------------------------------------------------------------------------------
% Request Definition: French National Archive
%------------------------------------------------------------------------------

% Scientific research from France
% Formalized as: and(purpose eq scientificResearch,
%                     spatial eq france)

fof(request_purpose_def, axiom,
    has_operand(c_request_purpose, purpose) &
    has_operator(c_request_purpose, eq) &
    has_value(c_request_purpose, scientificResearch)).

fof(request_spatial_def, axiom,
    has_operand(c_request_spatial, spatial) &
    has_operator(c_request_spatial, eq) &
    has_value(c_request_spatial, france)).

%------------------------------------------------------------------------------
% Per-Problem Denotation Rules for Set-Valued Operators
%------------------------------------------------------------------------------

% For isNoneOf{commercialPurpose}, the only-if direction needs grounding:
% "If X is in the denotation, then X is NOT under commercialPurpose"
fof(branch_a_purpose_only_if, axiom,
    ![X]: (in_denotation(X, c_branch_a_purpose)
          => ~subClassOf(X, commercialPurpose))).

% The if-direction is in the shared layer (ODRL000-0.ax):
% "If X is a concept AND X is NOT under commercialPurpose, then X is in denotation"

%------------------------------------------------------------------------------
% XONE Conjecture (Lemma 2: Witness Characterization for Binary XONE)
%------------------------------------------------------------------------------

% XONE is Compatible if exactly one branch holds (all operands) AND
% the other branch provably conflicts (at least one operand).
%
% For multi-operand branches, we need BOTH operands to witness compatibility:
% - Branch A needs: purpose witness AND spatial witness
% - Branch B needs: purpose conflict OR spatial conflict (at least one)
%
% We test Branch A holds exclusively:

fof(xone_branch_a_compatible, conjecture,
    % Branch A purpose: witness exists
    (?[P_a]: (in_denotation(P_a, c_branch_a_purpose) &
              in_denotation(P_a, c_request_purpose)))
    
    % AND Branch A spatial: witness exists  
    & (?[S_a]: (in_denotation(S_a, c_branch_a_spatial) &
                in_denotation(S_a, c_request_spatial)))
    
    % AND Branch B purpose: intersection empty
    & (~?[P_b]: (in_denotation(P_b, c_branch_b_purpose) &
                 in_denotation(P_b, c_request_purpose)))
    
    % AND Branch B spatial: intersection empty
    & (~?[S_b]: (in_denotation(S_b, c_branch_b_spatial) &
                 in_denotation(S_b, c_request_spatial)))
).

%------------------------------------------------------------------------------
% Expected Result: CounterSatisfiable (Unknown)
%------------------------------------------------------------------------------

% Denotation analysis:
%
% ⟦c_branch_a_purpose⟧ = ⟦isNoneOf {commercialPurpose}⟧
%   = C \ {x | x ⊑ commercialPurpose}
%   = C \ {commercialPurpose, commercialResearch, advertising}
%   = {purpose, nonCommercialPurpose, researchAndDevelopment,
%      academicResearch, scientificResearch, nonCommercialResearch,
%      marketing, directMarketing}
%   (8 concepts)
%
% ⟦c_request_purpose⟧ = {scientificResearch} (singleton)
%
% Question: Is scientificResearch ∈ ⟦c_branch_a_purpose⟧?
%
% Only-if direction (branch_a_purpose_only_if) requires:
%   in_denotation(scientificResearch, c_branch_a_purpose)
%   → ~subClassOf(scientificResearch, commercialPurpose)
%
% But DPV000-0.ax does NOT have this axiom!
% KB has: scientificResearch ⊑ researchAndDevelopment ✓
% KB has: researchAndDevelopment ⊑ purpose ✓
% KB lacks: ~(scientificResearch ⊑ commercialPurpose) ✗
%
% Open-world reasoning: Could scientificResearch be under commercialPurpose?
% Without explicit negative axiom, the prover CANNOT confirm it's not.
%
% → First conjunct (Branch A purpose) is UNPROVABLE
% → Entire XONE conjecture fails
% → CounterSatisfiable (Unknown)
%
% ⟦c_branch_a_spatial⟧ = ⟦isPartOf westernEurope⟧
%   = {x | x ⪯ westernEurope}
%   = {westernEurope, france, germany, austria, paris}
%   (5 concepts)
%
% ⟦c_request_spatial⟧ = {france} (singleton)
%
% france ⪯ westernEurope? YES (explicit in GEO003-0.ax)
% → Second conjunct (Branch A spatial) is PROVABLE ✓
%
% ⟦c_branch_b_spatial⟧ = {germany}
% ⟦c_request_spatial⟧ = {france}
% {germany} ∩ {france} = ∅ (UNA in GEO003-0.ax)
% → Fourth conjunct (Branch B spatial conflict) is PROVABLE ✓
%
% But first conjunct fails → overall Unknown.
%
%------------------------------------------------------------------------------
% Validates:
%   - Def 3 (Denotation): isNoneOf, isPartOf, isA, eq across 2 operands
%   - Def 4 (Conservative ⊓): classical intersections + ⊤ cases
%   - Def 5 (Verdict): Unknown when KB incomplete
%   - Def 6 (Composition): AND within branches + XONE across branches
%   - Lemma 2 (XONE witness): Multi-operand witness requirement
%   - Assm 2 (Operand independence): purpose × spatial decomposition
%   - Thm 1 (Soundness): Unknown reflects genuine knowledge gap
%------------------------------------------------------------------------------
