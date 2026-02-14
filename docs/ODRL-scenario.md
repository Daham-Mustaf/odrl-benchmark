The deepest realistic ODRL scenario that exercises every definition.


╔══════════════════════════════════════════════════════════════════════════════╗
║                    THE KILLER BENCHMARK: ODRL-ALIGN-XONE                     ║
║         Cross-KB Aligned Exclusive Composition with Unmapped Witness         ║
╚══════════════════════════════════════════════════════════════════════════════╝

SCENARIO: BSB (Munich) offers digitized manuscripts.
          French Archive requests access.
          Each side uses DIFFERENT knowledge bases.

┌─────────────────────────────────────────────────────────────────────────────┐
│  BSB POLICY (Permission)                                                    │
│                                                                             │
│  odrl:permission [                                                          │
│    odrl:target    <bsb:manuscripts> ;                                       │
│    odrl:action    odrl:use ;                                                │
│    odrl:constraint [                                                        │
│      odrl:xone (                                                            │
│        ┌─── Branch A ───────────────────────────────────┐                   │
│        │  odrl:and (                                    │                   │
│        │    [ odrl:leftOperand  odrl:purpose ;          │                   │
│        │      odrl:operator     odrl:isNoneOf ;         │                   │
│        │      odrl:rightOperand (dpv:Commercial) ]      │                   │
│        │    [ odrl:leftOperand  odrl:spatial ;          │                   │
│        │      odrl:operator     odrl:isPartOf ;         │                   │
│        │      odrl:rightOperand gn:WesternEurope ]      │                   │
│        │  )                                             │                   │
│        └────────────────────────────────────────────────┘                   │
│        ┌─── Branch B ───────────────────────────────────┐                   │
│        │  odrl:and (                                    │                   │
│        │    [ odrl:leftOperand  odrl:purpose ;          │                   │
│        │      odrl:operator     odrl:isA ;              │                   │
│        │      odrl:rightOperand dpv:Commercial ]        │                   │
│        │    [ odrl:leftOperand  odrl:spatial ;          │                   │
│        │      odrl:operator     odrl:eq ;               │                   │
│        │      odrl:rightOperand gn:Germany ]            │                   │
│        │  )                                             │                   │
│        └────────────────────────────────────────────────┘                   │
│      )                                                                      │
│    ]                                                                        │
│  ]                                                                          │
│                                                                             │
│  MEANING: "You may use manuscripts under EXACTLY ONE of:                    │
│    A) Non-commercial purpose + anywhere in Western Europe                   │
│    B) Commercial purpose + only in Germany"                                 │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  FRENCH ARCHIVE REQUEST                                                     │
│                                                                             │
│  odrl:request [                                                             │
│    odrl:target    <bsb:manuscripts> ;                                       │
│    odrl:action    odrl:use ;                                                │
│    odrl:constraint [                                                        │
│      odrl:and (                                                             │
│        [ odrl:leftOperand  odrl:purpose ;                                   │
│          odrl:operator     odrl:eq ;                                        │
│          odrl:rightOperand dpv:ScientificResearch ]                         │
│        [ odrl:leftOperand  odrl:spatial ;                                   │
│          odrl:operator     odrl:eq ;                                        │
│          odrl:rightOperand gn:France ]                                      │
│      )                                                                      │
│    ]                                                                        │
│  ]                                                                          │
│                                                                             │
│  MEANING: "We want to use manuscripts for scientific research in France"    │
└─────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
 KNOWLEDGE BASE A: BSB's KBs (DPV + GeoNames)
═══════════════════════════════════════════════════════════════════════════════

  KB_A PURPOSE (W3C DPV — depth 4):

                            purpose
                         ╱    │     ╲
                       ╱      │       ╲
              Commercial    R&D    NonCommercial
                ╱    ╲      ╱ │ ╲       ╱    ╲
              ╱       ╲   ╱  │   ╲    ╱       ╲
        Advertising  CommRes │  NonCommRes  Education
                           │
                    ScientificRes    ← NOT under Commercial
                                     ← NOT under NonCommercial
                                     ← ONLY under R&D

  Positive axioms (⊑):
    Commercial ⊑ Purpose           NonCommercial ⊑ Purpose
    R&D ⊑ Purpose                  Advertising ⊑ Commercial
    CommRes ⊑ R&D                  CommRes ⊑ Commercial
    NonCommRes ⊑ R&D               NonCommRes ⊑ NonCommercial
    ScientificRes ⊑ R&D            Education ⊑ NonCommercial

  Negative axioms (¬⊑) — CRITICAL for xone:
    ¬(Commercial ⊑ NonCommercial)     ✓ present
    ¬(NonCommercial ⊑ Commercial)     ✓ present
    ¬(NonCommRes ⊑ Commercial)        ✓ present (leaf)
    ¬(Education ⊑ Commercial)         ✓ present (leaf)

  ABSENT negative axioms — cause Unknown:
    ¬(ScientificRes ⊑ Commercial)     ✗ NOT STATED
    ¬(ScientificRes ⊑ NonCommercial)  ✗ NOT STATED
    ¬(R&D ⊑ Commercial)              ✗ NOT STATED
    ¬(R&D ⊑ NonCommercial)           ✗ NOT STATED


  KB_A SPATIAL (GeoNames — depth 4):

                             World
                            ╱     ╲
                          ╱         ╲
                    Europe            Asia
                   ╱      ╲
                 ╱          ╲
          WesternEurope   EasternEurope
            ╱   │   ╲
          ╱     │     ╲
      France Germany  Austria
        │
      Paris

  Positive axioms (⪯ = partOf):
    Europe ⪯ World              Asia ⪯ World
    WesternEurope ⪯ Europe      EasternEurope ⪯ Europe
    France ⪯ WesternEurope      Germany ⪯ WesternEurope
    Austria ⪯ WesternEurope     Paris ⪯ France

  Negative axioms:
    ¬(Europe ⪯ Asia)  ¬(Asia ⪯ Europe)
    ¬(WesternEurope ⪯ EasternEurope)  etc.


═══════════════════════════════════════════════════════════════════════════════
 KNOWLEDGE BASE B: French Archive's KBs (GDPR taxonomy + ISO 3166)
═══════════════════════════════════════════════════════════════════════════════

  KB_B PURPOSE (GDPR-derived — SHALLOWER, missing ScientificRes):

                         purpose
                        ╱       ╲
                      ╱           ╲
              Commercial      NonCommercial
                  │                  │
              CommRes          NonCommRes

  ⚠ ScientificRes DOES NOT EXIST in KB_B
  ⚠ R&D DOES NOT EXIST in KB_B
  ⚠ Education DOES NOT EXIST in KB_B
  ⚠ Advertising DOES NOT EXIST in KB_B


  KB_B SPATIAL (ISO 3166 — FLATTER, no Paris, no WesternEurope):

                          World
                         ╱     ╲
                       ╱         ╲
                  Europe          Asia
                 ╱  │  ╲
               ╱    │    ╲
          France Germany Austria

  ⚠ WesternEurope DOES NOT EXIST in KB_B
  ⚠ EasternEurope DOES NOT EXIST in KB_B
  ⚠ Paris DOES NOT EXIST in KB_B


═══════════════════════════════════════════════════════════════════════════════
 ALIGNMENT MAPS
═══════════════════════════════════════════════════════════════════════════════

  α_purpose: KB_A → KB_B (PARTIAL)
  ┌──────────────────┬──────────────────┬──────────┐
  │ KB_A concept     │ KB_B concept     │ Status   │
  ├──────────────────┼──────────────────┼──────────┤
  │ purpose          │ purpose'         │ ✓ mapped │
  │ Commercial       │ Commercial'      │ ✓ mapped │
  │ NonCommercial    │ NonCommercial'   │ ✓ mapped │
  │ CommRes          │ CommRes'         │ ✓ mapped │
  │ NonCommRes       │ NonCommRes'      │ ✓ mapped │
  │ R&D             │ ⊥                │ ✗ LOST   │
  │ ScientificRes   │ ⊥                │ ✗ LOST   │
  │ Education       │ ⊥                │ ✗ LOST   │
  │ Advertising     │ ⊥                │ ✗ LOST   │
  └──────────────────┴──────────────────┴──────────┘

  α_spatial: KB_A → KB_B (PARTIAL)
  ┌──────────────────┬──────────────────┬──────────┐
  │ KB_A concept     │ KB_B concept     │ Status   │
  ├──────────────────┼──────────────────┼──────────┤
  │ World            │ World'           │ ✓ mapped │
  │ Europe           │ Europe'          │ ✓ mapped │
  │ Asia             │ Asia'            │ ✓ mapped │
  │ France           │ France'          │ ✓ mapped │
  │ Germany          │ Germany'         │ ✓ mapped │
  │ Austria          │ Austria'         │ ✓ mapped │
  │ WesternEurope   │ ⊥                │ ✗ LOST   │
  │ EasternEurope   │ ⊥                │ ✗ LOST   │
  │ Paris           │ ⊥                │ ✗ LOST   │
  └──────────────────┴──────────────────┴──────────┘


═══════════════════════════════════════════════════════════════════════════════
 STEP-BY-STEP PIPELINE TRACE (Definition by Definition)
═══════════════════════════════════════════════════════════════════════════════

 ┌─ Def 1: Constraints ──────────────────────────────────────────────────────┐
 │                                                                           │
 │  POLICY (xone of two branches, each with and):                            │
 │                                                                           │
 │  Branch A:                                                                │
 │    c_A1 = (purpose,  isNoneOf, {Commercial})                              │
 │    c_A2 = (spatial,  isPartOf, WesternEurope)                             │
 │                                                                           │
 │  Branch B:                                                                │
 │    c_B1 = (purpose,  isA,      Commercial)                                │
 │    c_B2 = (spatial,  eq,       Germany)                                    │
 │                                                                           │
 │  REQUEST:                                                                 │
 │    c_R1 = (purpose,  eq,       ScientificResearch)                        │
 │    c_R2 = (spatial,  eq,       France)                                    │
 └───────────────────────────────────────────────────────────────────────────┘

 ┌─ Def 2: KB structures ───────────────────────────────────────────────────┐
 │                                                                           │
 │  KB_purpose = ({purpose, Comm, NonComm, R&D, CommRes, NonCommRes,         │
 │                  SciRes, Edu, Adv},  ⊑,  γ)                               │
 │  |C| = 9,  ≤ = ⊑ (taxonomic)                                             │
 │                                                                           │
 │  KB_spatial = ({World, Europe, Asia, WEurope, EEurope,                    │
 │                  France, Germany, Austria, Paris},  ⪯,  γ)                │
 │  |C| = 9,  ≤ = ⪯ (mereological)                                          │
 └───────────────────────────────────────────────────────────────────────────┘

 ┌─ Def 3: Denotations in KB_A ─────────────────────────────────────────────┐
 │                                                                           │
 │  POLICY BRANCH A:                                                         │
 │                                                                           │
 │  ⟦c_A1⟧ = ⟦purpose isNoneOf {Commercial}⟧                               │
 │         = C \ {x | x ⊑ Commercial}                                       │
 │         = C \ {Commercial, CommRes, Advertising}                          │
 │         = {purpose, NonComm, R&D, NonCommRes, SciRes, Edu}                │
 │         6 elements                                                        │
 │                                                                           │
 │  ⟦c_A2⟧ = ⟦spatial isPartOf WesternEurope⟧                              │
 │         = {x | x ⪯ WesternEurope}                                        │
 │         = {WEurope, France, Germany, Austria, Paris}                      │
 │         5 elements                                                        │
 │                                                                           │
 │  POLICY BRANCH B:                                                         │
 │                                                                           │
 │  ⟦c_B1⟧ = ⟦purpose isA Commercial⟧                                      │
 │         = {x | x ⊑ Commercial}                                           │
 │         = {Commercial, CommRes, Advertising}                              │
 │         3 elements                                                        │
 │                                                                           │
 │  ⟦c_B2⟧ = ⟦spatial eq Germany⟧                                           │
 │         = {Germany}                                                       │
 │         1 element                                                         │
 │                                                                           │
 │  REQUEST:                                                                 │
 │                                                                           │
 │  ⟦c_R1⟧ = ⟦purpose eq ScientificResearch⟧ = {SciRes}                    │
 │  ⟦c_R2⟧ = ⟦spatial eq France⟧             = {France}                    │
 └───────────────────────────────────────────────────────────────────────────┘

 ┌─ Def 4+5: Per-operand verdicts ──────────────────────────────────────────┐
 │                                                                           │
 │  BRANCH A vs REQUEST:                                                     │
 │                                                                           │
 │  purpose: ⟦c_A1⟧ ⊓ ⟦c_R1⟧                                               │
 │    = {purpose,NonComm,R&D,NonCommRes,SciRes,Edu} ∩ {SciRes}              │
 │    = {SciRes}                                                             │
 │    ≠ ∅ ... BUT can Vampire PROVE SciRes ∈ ⟦isNoneOf {Comm}⟧?             │
 │                                                                           │
 │    if-direction needs: ¬subClassOf(SciRes, Commercial)                    │
 │    THIS AXIOM IS ✗ ABSENT → Vampire cannot populate the denotation        │
 │    → CounterSatisfiable → UNKNOWN                                         │
 │                                                                           │
 │  spatial: ⟦c_A2⟧ ⊓ ⟦c_R2⟧                                               │
 │    = {WEurope,France,Germany,Austria,Paris} ∩ {France}                    │
 │    = {France}                                                             │
 │    France ⪯ WesternEurope ✓ (explicit axiom)                             │
 │    → Vampire proves witness → COMPATIBLE ✓                                │
 │                                                                           │
 │  BRANCH A overall (and): purpose=Unknown, spatial=Compatible              │
 │    → Def 6 (and): ∃ Unknown → UNKNOWN                                    │
 │                                                                           │
 │  ─────────────────────────────────────────────────────                    │
 │                                                                           │
 │  BRANCH B vs REQUEST:                                                     │
 │                                                                           │
 │  purpose: ⟦c_B1⟧ ⊓ ⟦c_R1⟧                                               │
 │    = {Commercial, CommRes, Advertising} ∩ {SciRes}                        │
 │    SciRes ⊑ Commercial? NOT asserted, NOT denied                          │
 │    → CounterSatisfiable → UNKNOWN                                         │
 │                                                                           │
 │  spatial: ⟦c_B2⟧ ⊓ ⟦c_R2⟧                                               │
 │    = {Germany} ∩ {France}                                                 │
 │    Germany = France? No. Germany ⊑ France? No.                            │
 │    UNA: Germany ≠ France (explicit)                                       │
 │    → empty intersection → CONFLICT ✓                                      │
 │                                                                           │
 │  BRANCH B overall (and): purpose=Unknown, spatial=Conflict                │
 │    → Def 6 (and): ∃ Conflict → CONFLICT                                  │
 └───────────────────────────────────────────────────────────────────────────┘

 ┌─ Def 6: XONE composition ────────────────────────────────────────────────┐
 │                                                                           │
 │  V_A = Unknown    (purpose unknown, spatial compatible)                   │
 │  V_B = Conflict   (spatial conflict kills branch)                         │
 │                                                                           │
 │  xone requires:                                                           │
 │    Compatible if ∃!k: V_k=Compatible AND ∀j≠k: V_j=Conflict              │
 │    Conflict   if ∀k: V_k=Conflict                                        │
 │    Unknown    otherwise                                                   │
 │                                                                           │
 │  V_A=Unknown, V_B=Conflict → "otherwise" → UNKNOWN                       │
 │                                                                           │
 │  ┌───────────────────────────────────────────────────────────────┐        │
 │  │  VERDICT IN KB_A: UNKNOWN                                     │        │
 │  │                                                               │        │
 │  │  Root cause: ScientificResearch's position relative to        │        │
 │  │  Commercial is underdetermined in W3C DPV.                    │        │
 │  │  The KB gap is REAL — DPV genuinely doesn't commit.           │        │
 │  └───────────────────────────────────────────────────────────────┘        │
 └───────────────────────────────────────────────────────────────────────────┘


 NOW: What if we ADD the missing axiom?
 ¬(ScientificRes ⊑ Commercial) — "scientific research is NOT commercial"

 ┌─ RECOMPUTE with enriched KB_A ───────────────────────────────────────────┐
 │                                                                           │
 │  BRANCH A purpose: ⟦isNoneOf {Comm}⟧ ⊓ {SciRes}                            │
 │    ¬(SciRes ⊑ Comm) now explicit → SciRes ∈ ⟦isNoneOf {Comm}⟧              │
 │    → {SciRes} ≠ ∅ → COMPATIBLE ✓                                          │
 │                                                                           │
 │  BRANCH A spatial: unchanged → COMPATIBLE ✓                               │
 │  BRANCH A overall (and): both Compatible → COMPATIBLE ✓                   │
 │                                                                           │
 │  BRANCH B purpose: ⟦isA Comm⟧ ⊓ {SciRes}                                   │
 │    SciRes ⊑ Comm? only-if says: if in_den(SciRes,c_B1) then               │
 │    subClassOf(SciRes, Commercial). But ¬(SciRes ⊑ Comm) blocks.           │
 │    → empty → CONFLICT ✓                                                   │
 │                                                                           │
 │  BRANCH B spatial: unchanged → CONFLICT ✓                                 │
 │  BRANCH B overall (and): Conflict → CONFLICT ✓                            │
 │                                                                           │
 │  XONE: V_A=Compatible, V_B=Conflict                                      │
 │    ∃!k Compatible (A) AND ∀j≠k Conflict (B) → COMPATIBLE ✓               │
 │                                                                           │
 │  ┌───────────────────────────────────────────────────────────────┐        │
 │  │  VERDICT IN ENRICHED KB_A: COMPATIBLE                         │        │
 │  │                                                               │        │
 │  │  One negative axiom resolves the entire xone.                 │        │
 │  │  This is the paper's key finding about xone.                  │        │
 │  └───────────────────────────────────────────────────────────────┘        │
 └───────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
 NOW: CROSS-KB ALIGNMENT (The Killer Case)
═══════════════════════════════════════════════════════════════════════════════

 Using the ENRICHED KB_A (with ¬(SciRes ⊑ Comm)).
 Verdict in KB_A = COMPATIBLE.
 Now translate to KB_B via alignment α.

 ┌─ Def 7: Alignment check ─────────────────────────────────────────────────┐
 │                                                                           │
 │  α_purpose: partial (5 mapped, 4 unmapped)                                │
 │  α_spatial: partial (6 mapped, 3 unmapped)                                │
 └───────────────────────────────────────────────────────────────────────────┘

 ┌─ Def 8 (STRENGTHENED): Aligned constraints ──────────────────────────────┐
 │                                                                           │
 │  α(c_A1) = α(purpose isNoneOf {Commercial}):                              │
 │    α(Commercial) = Commercial' ≠ ⊥  ✓                                     │
 │    ⟦c_A1⟧_A = {purpose, NonComm, R&D, NonCommRes, SciRes, Edu}           │
 │    dom(α_purpose) = {purpose, Comm, NonComm, CommRes, NonCommRes}         │
 │    R&D ∉ dom(α) ✗  SciRes ∉ dom(α) ✗  Edu ∉ dom(α) ✗                    │
 │    ⟦c_A1⟧_A ⊄ dom(α)  →  α(c_A1) = ⊤                                    │
 │                                                                           │
 │  α(c_A2) = α(spatial isPartOf WesternEurope):                             │
 │    α(WesternEurope) = ⊥  →  α(c_A2) = ⊤                                  │
 │                                                                           │
 │  α(c_B1) = α(purpose isA Commercial):                                     │
 │    α(Commercial) = Commercial' ≠ ⊥  ✓                                     │
 │    ⟦c_B1⟧_A = {Commercial, CommRes, Advertising}                          │
 │    Advertising ∉ dom(α) ✗                                                 │
 │    ⟦c_B1⟧_A ⊄ dom(α)  →  α(c_B1) = ⊤                                    │
 │                                                                           │
 │  α(c_B2) = α(spatial eq Germany):                                         │
 │    α(Germany) = Germany' ≠ ⊥  ✓                                           │
 │    ⟦c_B2⟧_A = {Germany}                                                   │
 │    {Germany} ⊆ dom(α) ✓                                                   │
 │    →  α(c_B2) = (spatial, eq, Germany')  ✓                                │
 │                                                                           │
 │  α(c_R1) = α(purpose eq ScientificResearch):                              │
 │    α(SciRes) = ⊥  →  α(c_R1) = ⊤                                         │
 │                                                                           │
 │  α(c_R2) = α(spatial eq France):                                          │
 │    α(France) = France' ≠ ⊥  ✓                                             │
 │    ⟦c_R2⟧_A = {France}                                                    │
 │    {France} ⊆ dom(α) ✓                                                   │
 │    →  α(c_R2) = (spatial, eq, France')  ✓                                 │
 └───────────────────────────────────────────────────────────────────────────┘

 ┌─ Def 4+5: Verdicts in KB_B ──────────────────────────────────────────────┐
 │                                                                           │
 │  BRANCH A in KB_B:                                                        │
 │    purpose: α(c_A1) = ⊤, α(c_R1) = ⊤  →  ⊤ ⊓ ⊤ = ⊤  →  UNKNOWN        │
 │    spatial: α(c_A2) = ⊤               →  ⊤ ⊓ D = ⊤  →  UNKNOWN         │
 │    and(Unknown, Unknown) → UNKNOWN                                        │
 │                                                                           │
 │  BRANCH B in KB_B:                                                        │
 │    purpose: α(c_B1) = ⊤, α(c_R1) = ⊤  →  ⊤ ⊓ ⊤ = ⊤  →  UNKNOWN        │
 │    spatial: α(c_B2) = (eq, Germany'), α(c_R2) = (eq, France')            │
 │      {Germany'} ∩ {France'} = ∅ (UNA) →  CONFLICT ✓                       │
 │    and(Unknown, Conflict) → CONFLICT                                      │
 │                                                                           │
 │  XONE in KB_B: V_A=Unknown, V_B=Conflict → UNKNOWN                       │
 │                                                                           │
 │  ┌───────────────────────────────────────────────────────────────┐        │
 │  │  KB_A verdict:  COMPATIBLE                                    │        │
 │  │  KB_B verdict:  UNKNOWN                                       │        │
 │  │                                                               │        │
 │  │  Prop 1.2: Compatible → Unknown  ✓  (graceful degradation)    │        │
 │  │  No false Conflict.                                           │        │
 │  └───────────────────────────────────────────────────────────────┘        │
 └───────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
 WHAT OLD DEF 8 WOULD HAVE DONE (THE BUG)
═══════════════════════════════════════════════════════════════════════════════

 ┌─ Old Def 8: only checks α(g) ≠ ⊥ ───────────────────────────────────────┐
 │                                                                           │
 │  α(c_A1) = α(purpose isNoneOf {Commercial}):                              │
 │    α(Commercial) ≠ ⊥  → PROCEED (old Def 8 doesn't check denotation)     │
 │    ⟦α(c_A1)⟧_B over {purpose', Comm', NonComm', CommRes', NonCommRes'}   │
 │    isNoneOf {Commercial'} = C_B \ {x ⊑ Commercial'}                      │
 │                           = C_B \ {Commercial', CommRes'}                 │
 │                           = {purpose', NonComm', NonCommRes'}             │
 │                                                                           │
 │    MISSING: R&D, SciRes, Edu — all were in ⟦c_A1⟧_A                      │
 │    Denotation SHRANK from 6 to 3 elements                                │
 │                                                                           │
 │  In this specific scenario, the request value SciRes is also              │
 │  unmapped (α(SciRes) = ⊥), so α(c_R1) = ⊤ regardless.                   │
 │  → Same Unknown result by accident.                                       │
 │                                                                           │
 │  BUT with a different request (e.g., NonCommRes which IS mapped):         │
 │  The shrunken denotation could lose the only witness and                  │
 │  fabricate a Conflict. See the minimal killer example below.              │
 └───────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
 MINIMAL KILLER: Where Old Def 8 Fabricates a False Conflict
═══════════════════════════════════════════════════════════════════════════════

  KB_A: {root, a, b, d}          KB_B: {a', b'}
        a ⊑ root                       (flat, no hierarchy)
        b ⊑ root
        d ⊑ root                 α: a→a', b→b', root→⊥, d→⊥
        all siblings disjoint

  c₁ = (ℓ, isNoneOf, {a})    ⟦c₁⟧_A = {root, b, d}
  c₂ = (ℓ, isNoneOf, {b})    ⟦c₂⟧_A = {root, a, d}

  Intersection in KB_A: {root, d} → COMPATIBLE ✓

  ┌── Old Def 8 ───────────────────┐  ┌── New Def 8 ──────────────────────┐
  │ α(a) ≠ ⊥ → proceed             │  │ ⟦c₁⟧={root,b,d}                    │
  │ ⟦α(c₁)⟧_B = isNoneOf{a'}        │  │ root ∉ dom(α), d ∉ dom(α)         │
  │           = {b'}                │  │ ⟦c₁⟧ ⊄ dom(α) → ⊤                 │
  │ ⟦α(c₂)⟧_B = isNoneOf{b'}        │  │                                   │
  │           = {a'}               │  │ Similarly α(c₂) = ⊤               │
  │                                │  │                                   │
  │ {b'} ∩ {a'} = ∅                │  │ ⊤ ⊓ ⊤ = ⊤                        │
  │                                │  │                                   │
  │ → 💥 FALSE CONFLICT            │  │ → ✓ UNKNOWN                       │
  │                                │  │                                   │
  │ Compatible became Conflict!    │  │ Graceful degradation.             │
  └────────────────────────────────┘  └────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
 DEFINITIONS EXERCISED
═══════════════════════════════════════════════════════════════════════════════

  ✓ Def 1  Constraint              — 6 constraints across 2 operands
  ✓ Def 2  KB                      — taxonomic + mereological + depth 4
  ✓ Def 3  Denotation              — isNoneOf, isA, isPartOf, eq
  ✓ Def 4  Conservative ⊓          — classical and ⊤ cases
  ✓ Def 5  Verdict                 — all three: Conflict, Compatible, Unknown
  ✓ Def 6  Composition             — xone(and(...), and(...))
  ✓ Assm 1 KB Correctness          — grounded values correct
  ✓ Assm 2 Operand Independence    — purpose × spatial decomposed
  ✓ Def 7  Alignment               — partial, injective, order-preserving
  ✓ Def 8  Aligned Constraint      — ⊤ from unmapped denotation elements
  ✓ Lem 1  Denotation Preservation — eq constraints fully covered
  ✓ Prop 1.1 Conflict Preservation — spatial Conflict preserved
  ✓ Prop 1.2 Graceful Degradation  — Compatible → Unknown
  ✓ Thm 1  Soundness               — Conflict verdict = no witness
  ✓ Thm 2  Runtime Soundness       — no ω satisfies both in conflict pair
