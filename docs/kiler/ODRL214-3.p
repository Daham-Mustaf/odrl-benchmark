%------------------------------------------------------------------------------
% File     : ODRL214-3.p : TPTP-ODRL Killer Benchmark
% Domain   : ODRL Policy Conflict Detection
% Problem  : Full BSB/French Archive scenario in ALIGNED KB (GDPR + ISO3166)
% Version  : [Semantics] : Denotational
% English  : Same scenario as ODRL214-2.p, but constraints are interpreted over
%            KB_B (GDPR purpose taxonomy + ISO 3166 spatial) via alignment.
%            
%            CRITICAL: KB_B is SMALLER and lacks several concepts:
%            Purpose KB_B: Missing scientificResearch, researchAndDevelopment,
%                         academicResearch, marketing, advertising (6 missing)
%            Spatial KB_B: Missing westernEurope, easternEurope, paris (3 missing)
%            
%            Strengthened Definition 8 check:
%            For c_branch_a_spatial = (spatial, isPartOf, westernEurope):
%              α(westernEurope) = ⊥ (not in ISO 3166)
%              → α(c_branch_a_spatial) = ⊤ (unmapped grounding value)
%            
%            For c_request_purpose = (purpose, eq, scientificResearch):
%              α(scientificResearch) = ⊥ (not in GDPR taxonomy)
%              → α(c_request_purpose) = ⊤ (unmapped grounding value)
%            
%            Result: Compatible in KB_A degrades to Unknown in KB_B ✓
%
% Refs     : [MS26] Mustafa & Sutcliffe (2026), Formal Foundations for ODRL
% Source   : [DM]
% Names    : Killer benchmark (aligned KB)
%
% Status   : CounterSatisfiable
% Rating   : 1.00 v0.1.0
%
% Comments : Validates Proposition 1.2 (Graceful Degradation):
%            "If ⟦c⟧_A ⊄ dom(α), then verdict degrades to Unknown, never to
%            false Conflict."
%            Compare verdicts:
%              ODRL214-2 (KB_A enriched): Theorem (Compatible) ✓
%              ODRL214-3 (KB_B aligned):  CounterSat (Unknown) ✓
%------------------------------------------------------------------------------

%------------------------------------------------------------------------------
% Layer 0: Domain Knowledge Bases (KB_B — smaller, aligned KBs)
%------------------------------------------------------------------------------

% Purpose taxonomy (GDPR-derived, 6 concepts vs. DPV's 11)
% Structure:
%   purpose
%   ├── commercialPurpose
%   │   └── commercialResearch
%   └── nonCommercialPurpose
%       └── nonCommercialResearch
%
% MISSING from DPV004:
%   - researchAndDevelopment (R&D)
%   - scientificResearch ← REQUEST VALUE!
%   - academicResearch
%   - marketing
%   - advertising
include('Axioms/Layer0-DomainKB/GDPR001-0.ax').

% Spatial hierarchy (ISO 3166, 6 concepts vs. GeoNames' 9)
% Structure:
%   world
%   ├── europe
%   │   ├── france
%   │   ├── germany
%   │   └── austria
%   └── asia
%
% MISSING from GEO003:
%   - westernEurope ← BRANCH A VALUE!
%   - easternEurope
%   - paris
include('Axioms/Layer0-DomainKB/ISO3166-0.ax').

%------------------------------------------------------------------------------
% Layer 3: Alignment Declarations
%------------------------------------------------------------------------------

% α_purpose: DPV004 → GDPR001
% Mapped (5):   purpose, commercialPurpose, nonCommercialPurpose,
%               commercialResearch, nonCommercialResearch
% Unmapped (6): R&D, scientificResearch, academicResearch,
%               marketing, advertising, directMarketing
include('Axioms/Layer3-Alignment/ALIGN-DPV-GDPR.ax').

% α_spatial: GEO003 → ISO3166
% Mapped (6):   world, europe, asia, france, germany, austria
% Unmapped (3): westernEurope, easternEurope, paris
include('Axioms/Layer3-Alignment/ALIGN-GEO-ISO.ax').

%------------------------------------------------------------------------------
% Layer 1: ODRL Operator Semantics
%------------------------------------------------------------------------------
include('Axioms/Layer1-ODRLCore/ODRL000-0.ax').

%------------------------------------------------------------------------------
% Layer 2: Grounding Function (KB_B version)
%------------------------------------------------------------------------------

% γ_B: V → C_B ∪ {⊥}
% For unmapped values, returns ⊥, which triggers ⟦c⟧ = ⊤ per Def 3
include('Axioms/Layer2-Grounding/GROUND-KB-B.ax').

%------------------------------------------------------------------------------
% Policy Definition: BSB XONE Policy (values from KB_A, interpreted over KB_B)
%------------------------------------------------------------------------------

% CRITICAL ENCODING DECISION:
% The constraint VALUES reference KB_A concepts (westernEurope, scientificResearch),
% but we're evaluating over KB_B via alignment.
% 
% Per Def 8, for each constraint c from KB_A:
%   α(c) = ⊤ if:
%     - α(g) = ⊥ (grounding value unmapped)
%     OR
%     - ⟦c⟧_A ⊄ dom(α) (denotation has unmapped elements)

fof(branch_a_purpose_def, axiom,
    has_operand(c_branch_a_purpose, purpose) &
    has_operator(c_branch_a_purpose, isNoneOf) &
    has_value_set(c_branch_a_purpose, [commercialPurpose])).
% NOTE: commercialPurpose IS mapped: α(commercialPurpose) = commercialPurpose' ✓
% But ⟦isNoneOf{comm}⟧_A has unmapped elements (R&D, sciRes, acadRes, marketing, adv)
% → Strengthened Def 8 forces α(c_branch_a_purpose) = ⊤

fof(branch_a_spatial_def, axiom,
    has_operand(c_branch_a_spatial, spatial) &
    has_operator(c_branch_a_spatial, isPartOf) &
    has_value(c_branch_a_spatial, westernEurope)).
% NOTE: westernEurope NOT in ISO 3166: α(westernEurope) = ⊥
% → Def 8 forces α(c_branch_a_spatial) = ⊤

fof(branch_b_purpose_def, axiom,
    has_operand(c_branch_b_purpose, purpose) &
    has_operator(c_branch_b_purpose, isA) &
    has_value(c_branch_b_purpose, commercialPurpose)).
% NOTE: commercialPurpose IS mapped ✓
% ⟦isA comm⟧_A = {comm, commRes, advertising}
% advertising NOT mapped → ⟦c⟧_A ⊄ dom(α)
% → α(c_branch_b_purpose) = ⊤

fof(branch_b_spatial_def, axiom,
    has_operand(c_branch_b_spatial, spatial) &
    has_operator(c_branch_b_spatial, eq) &
    has_value(c_branch_b_spatial, germany)).
% NOTE: germany IS mapped: α(germany) = germany' ✓
% ⟦eq germany⟧_A = {germany} (singleton)
% {germany} ⊆ dom(α) ✓
% → α(c_branch_b_spatial) = (spatial, eq, germany') ✓ NOT ⊤!

fof(request_purpose_def, axiom,
    has_operand(c_request_purpose, purpose) &
    has_operator(c_request_purpose, eq) &
    has_value(c_request_purpose, scientificResearch)).
% NOTE: scientificResearch NOT in GDPR001: α(scientificResearch) = ⊥
% → α(c_request_purpose) = ⊤

fof(request_spatial_def, axiom,
    has_operand(c_request_spatial, spatial) &
    has_operator(c_request_spatial, eq) &
    has_value(c_request_spatial, france)).
% NOTE: france IS mapped: α(france) = france' ✓
% ⟦eq france⟧_A = {france} ⊆ dom(α) ✓
% → α(c_request_spatial) = (spatial, eq, france') ✓ NOT ⊤!

%------------------------------------------------------------------------------
% Per-Problem Denotation Rules
%------------------------------------------------------------------------------

% For the constraints that survived alignment (not ⊤), apply standard rules
% For constraints that became ⊤, no denotation rules needed (⊤ ⊓ D = ⊤)

fof(branch_a_purpose_only_if, axiom,
    ![X]: (in_denotation(X, c_branch_a_purpose)
          => ~subClassOf(X, commercialPurpose))).
% But this won't help since c_branch_a_purpose = ⊤ in KB_B

%------------------------------------------------------------------------------
% XONE Conjecture (same encoding as ODRL214-1/2)
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
% Expected Result: CounterSatisfiable (Unknown)
%------------------------------------------------------------------------------

% Aligned constraint analysis (applying Def 8):
%
% c_branch_a_purpose: ⊤ (unmapped denotation elements)
% c_branch_a_spatial: ⊤ (unmapped grounding value westernEurope)
% c_branch_b_purpose: ⊤ (unmapped denotation element advertising)
% c_branch_b_spatial: (spatial, eq, germany') ✓ grounded in KB_B
% c_request_purpose:  ⊤ (unmapped grounding value scientificResearch)
% c_request_spatial:  (spatial, eq, france') ✓ grounded in KB_B
%
% Conjunct evaluation:
%
% 1. Branch A purpose: in_den(P_a, ⊤) & in_den(P_a, ⊤)
%    Definition 4: ⊤ ⊓ ⊤ = ⊤
%    Can't prove ∃P_a from ⊤ → UNPROVABLE
%
% 2. Branch A spatial: in_den(S_a, ⊤) & in_den(S_a, france')
%    ⊤ ⊓ {france'} = ⊤
%    → UNPROVABLE
%
% 3. Branch B purpose: ~∃P_b: in_den(P_b, ⊤) & in_den(P_b, ⊤)
%    ⊤ ⊓ ⊤ = ⊤
%    Can't prove emptiness of ⊤ → UNPROVABLE
%
% 4. Branch B spatial: ~∃S_b: in_den(S_b, {germany'}) & in_den(S_b, {france'})
%    {germany'} ∩ {france'} = ∅ (UNA in ISO3166-0.ax)
%    → PROVABLE ✓
%
% Only one of four conjuncts is provable → overall conjecture UNPROVABLE
% → CounterSatisfiable (Unknown)
%
% VALIDATION OF PROPOSITION 1.2:
%
% Verdict in KB_A (ODRL214-2): Compatible (Theorem)
% Verdict in KB_B (ODRL214-3): Unknown (CounterSat)
%
% Graceful degradation: ✓
%   Compatible → Unknown (never → false Conflict)
%
% WHY no false Conflict?
%   Old Def 8 would have:
%     ⟦α(c_branch_a_purpose)⟧_B = {purpose', nonComm', nonCommRes'}
%       (SHRUNKEN from KB_A's 8 elements to 3)
%     Could create false Conflict if intersection became empty
%   
%   New Def 8 prevents shrinkage:
%     α(c_branch_a_purpose) = ⊤ (not a classical set)
%     ⊤ ⊓ anything = ⊤ (never ∅)
%     → Guaranteed no false Conflict ✓
%
%------------------------------------------------------------------------------
% Validates:
%   - Def 7 (Alignment): Partial injection DPV→GDPR, GEO→ISO
%   - Def 8 (Aligned Constraint, strengthened): ⊤ assignment prevents shrinkage
%   - Def 4 (Conservative ⊓): ⊤ propagation through intersections
%   - Prop 1.2 (Graceful Degradation): Compatible → Unknown under alignment
%   - Thm 1 (Soundness): No false Conflict introduced by alignment
%------------------------------------------------------------------------------
