%------------------------------------------------------------------------------
% File     : ODRL214-2.p : TPTP-ODRL Killer Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : Full BSB/French Archive scenario in ENRICHED DPV KB
% Version  : [Semantics] : Denotational
% English  : Same scenario as ODRL214-1.p, but with enriched DPV KB that adds
%            explicit negative axiom: ¬(scientificResearch ⊑ commercialPurpose).
%            This resolves the knowledge gap → Compatible verdict.
%
% Refs     : [MS26] Mustafa & Sutcliffe (2026), Formal Foundations for ODRL
% Source   : [DM]
% Names    : Killer benchmark (enriched KB)
%
% Status   : Theorem
% Rating   : 1.00 v0.1.0
%
% Comments : Demonstrates how ONE NEGATIVE AXIOM resolves XONE verdict.
%            This validates the paper's claim (Table 3, p.20):
%            "XONE requires strictly stronger KB axioms than conjunction or
%            disjunction: open-world semantics blocks exclusivity even when
%            positive evidence appears to satisfy exactly one branch."
%------------------------------------------------------------------------------

%------------------------------------------------------------------------------
% Layer 0: Domain Knowledge Bases
%------------------------------------------------------------------------------

% Purpose taxonomy (W3C DPV v2.2 + enrichment)
% CRITICAL CHANGE: Includes ¬(scientificResearch ⊑ commercialPurpose)
include('Axioms/Layer0-DomainKB/DPV004-0.ax').

% Spatial hierarchy (same as ODRL214-1)
include('Axioms/Layer0-DomainKB/GEO003-0.ax').

%------------------------------------------------------------------------------
% Layer 1: ODRL Operator Semantics
%------------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

%------------------------------------------------------------------------------
% Layer 2: Grounding Function
%------------------------------------------------------------------------------
include('Axioms/Layer2-Grounding/GROUND000-1.ax').

%------------------------------------------------------------------------------
% Policy Definition: BSB XONE Policy (same as ODRL214-1)
%------------------------------------------------------------------------------

fof(branch_a_purpose_def, axiom,
    has_operand(c_branch_a_purpose, purpose) &
    has_operator(c_branch_a_purpose, isNoneOf) &
    has_value_set(c_branch_a_purpose, [commercialPurpose])).

fof(branch_a_spatial_def, axiom,
    has_operand(c_branch_a_spatial, spatial) &
    has_operator(c_branch_a_spatial, isPartOf) &
    has_value(c_branch_a_spatial, westernEurope)).

fof(branch_b_purpose_def, axiom,
    has_operand(c_branch_b_purpose, purpose) &
    has_operator(c_branch_b_purpose, isA) &
    has_value(c_branch_b_purpose, commercialPurpose)).

fof(branch_b_spatial_def, axiom,
    has_operand(c_branch_b_spatial, spatial) &
    has_operator(c_branch_b_spatial, eq) &
    has_value(c_branch_b_spatial, germany)).

%------------------------------------------------------------------------------
% Request Definition (same as ODRL214-1)
%------------------------------------------------------------------------------

fof(request_purpose_def, axiom,
    has_operand(c_request_purpose, purpose) &
    has_operator(c_request_purpose, eq) &
    has_value(c_request_purpose, scientificResearch)).

fof(request_spatial_def, axiom,
    has_operand(c_request_spatial, spatial) &
    has_operator(c_request_spatial, eq) &
    has_value(c_request_spatial, france)).

%------------------------------------------------------------------------------
% Per-Problem Denotation Rules
%------------------------------------------------------------------------------

fof(branch_a_purpose_only_if, axiom,
    ![X]: (in_denotation(X, c_branch_a_purpose)
          => ~subClassOf(X, commercialPurpose))).

%------------------------------------------------------------------------------
% XONE Conjecture (same as ODRL214-1)
%------------------------------------------------------------------------------

fof(xone_branch_a_compatible, conjecture,
    (?[P_a]: (in_denotation(P_a, c_branch_a_purpose) &
              in_denotation(P_a, c_request_purpose)))
    & (?[S_a]: (in_denotation(S_a, c_branch_a_spatial) &
                in_denotation(S_a, c_request_spatial)))
    & (~?[P_b]: (in_denotation(P_b, c_branch_b_purpose) &
                 in_denotation(P_b, c_request_purpose)))
    & (~?[S_b]: (in_denotation(S_b, c_branch_b_spatial) &
                 in_denotation(S_b, c_request_spatial)))
).

%------------------------------------------------------------------------------
% Expected Result: Theorem (Compatible)
%------------------------------------------------------------------------------

% Denotation analysis:
%
% With DPV004-0.ax, we now have:
%   fof(dpv_sci_not_comm, axiom, ~subClassOf(scientificResearch, commercialPurpose)).
%
% This enables the if-direction to populate the denotation:
%   scientificResearch is a concept ✓
%   ~subClassOf(scientificResearch, commercialPurpose) ✓ (new axiom!)
%   → in_denotation(scientificResearch, c_branch_a_purpose) ✓
%
% Now all four conjuncts are PROVABLE:
%
% 1. Branch A purpose: 
%    P_a = scientificResearch witnesses:
%      - in_denotation(scientificResearch, c_branch_a_purpose) ✓ (if-direction + new axiom)
%      - in_denotation(scientificResearch, c_request_purpose) ✓ (eq operator)
%    → ∃P_a: ... ✓ PROVABLE
%
% 2. Branch A spatial:
%    S_a = france witnesses:
%      - france ⪯ westernEurope ✓ (GEO003-0.ax)
%      - in_denotation(france, c_branch_a_spatial) ✓
%      - in_denotation(france, c_request_spatial) ✓
%    → ∃S_a: ... ✓ PROVABLE
%
% 3. Branch B purpose conflict:
%    ⟦c_branch_b_purpose⟧ = {x | x ⊑ commercialPurpose}
%                          = {commercialPurpose, commercialResearch, advertising}
%    ⟦c_request_purpose⟧ = {scientificResearch}
%    scientificResearch ⊑ commercialPurpose? 
%      NO! (explicit negative axiom)
%    → {commercialPurpose, commercialResearch, advertising} ∩ {scientificResearch} = ∅
%    → ~∃P_b: ... ✓ PROVABLE
%
% 4. Branch B spatial conflict:
%    {germany} ∩ {france} = ∅ (UNA)
%    → ~∃S_b: ... ✓ PROVABLE
%
% All four conjuncts proven → XONE conjecture is a Theorem → Compatible ✓
%
%------------------------------------------------------------------------------
% Validates:
%   - Impact of negative axiom enrichment on XONE verdict
%   - Lemma 2 (XONE witness): All four conditions satisfied
%   - Def 6 (XONE): Exactly one branch (A) holds, other (B) conflicts
%   - Thm 1 (Soundness): Compatible verdict has runtime witness
%------------------------------------------------------------------------------
