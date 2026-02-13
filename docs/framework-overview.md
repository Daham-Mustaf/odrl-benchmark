# ODRL Semantic Grounding Framework — Big Picture

```
═══════════════════════════════════════════════════════════════════════════
                        ODRL POLICY LAYER
═══════════════════════════════════════════════════════════════════════════

  BSB Policy (Munich)                    French Archive (Paris)
  ┌──────────────────────┐               ┌──────────────────────┐
  │ Permission: display  │               │ Request: display     │
  │                      │               │                      │
  │ c1: spatial isPartOf │               │ c4: spatial eq       │
  │     europe           │               │     france           │
  │ c2: purpose isA      │               │ c5: purpose eq       │
  │     nonCommercial    │               │     scientificRes    │
  │ c3: language isA     │               │ c6: language eq      │
  │     de               │               │     fr               │
  │                      │               │                      │
  │ Composition: AND     │               │                      │
  └──────────┬───────────┘               └──────────┬───────────┘
             │                                      │
             ▼                                      ▼
═══════════════════════════════════════════════════════════════════════════
                   STEP 1: KB GROUNDING  (Def. 3 — Denotation)
              "What set of concepts satisfies each constraint?"
═══════════════════════════════════════════════════════════════════════════

  Three Semantic Domains (Def. 2 — KB):
  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
  │   TAXONOMIC     │  │  MEREOLOGICAL   │  │    NOMINAL      │
  │   ≤ = ⊑         │  │  ≤ = ⪯          │  │   ≤ = =         │
  │                 │  │                 │  │                 │
  │  purpose        │  │  spatial        │  │  device         │
  │  language       │  │  virtualLoc     │  │  event          │
  │  industry       │  │                 │  │  channel        │
  │  fileFormat     │  │                 │  │  product        │
  │  media          │  │                 │  │  system         │
  │  recipient      │  │                 │  │  unitOfCount    │
  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘
           │                    │                     │
           ▼                    ▼                     ▼

  Grounding against KBs:
  ┌─────────────────────────────────────────────────────────────┐
  │                                                             │
  │  c1: spatial isPartOf europe                                │
  │      KB = GeoNames:  europe ──⪯── germany ──⪯── bavaria    │
  │                         └──⪯── france                       │
  │                                                             │
  │      ⟦c1⟧ = {x ∈ C | x ⪯ europe}                          │
  │           = {europe, germany, france, bavaria}              │
  │                                                             │
  │  c4: spatial eq france                                      │
  │      ⟦c4⟧ = {france}                                       │
  │                                                             │
  │  c2: purpose isA nonCommercial                              │
  │      KB = W3C DPV:  nonComm ──⊑── nonCommRes               │
  │                     commercial ──⊑── commRes                │
  │                     research ──⊑── nonCommRes               │
  │                              └──⊑── commRes                 │
  │                                                             │
  │      ⟦c2⟧ = {x | x ⊑ nonComm} = {nonComm, nonCommRes}     │
  │                                                             │
  │  c5: purpose eq scientificRes                               │
  │      KB silent on scientificRes ⊑ nonComm ?                 │
  │      γ(scientificRes) maps, but position unclear            │
  │      ⟦c5⟧ = {scientificRes}  ... but is it ⊑ nonComm?      │
  │                                                             │
  │  c3: language isA de                                        │
  │      KB = BCP 47:  de ──⊑── de-AT, de-CH                   │
  │      ⟦c3⟧ = {de, de-AT, de-CH}                             │
  │                                                             │
  │  c6: language eq fr                                         │
  │      ⟦c6⟧ = {fr}                                           │
  │                                                             │
  │  UNGROUNDED VALUE?  γ(v) = ⊥  →  ⟦c⟧ = ⊤ (indeterminate)  │
  └─────────────────────────────────────────────────────────────┘
                              │
                              ▼
═══════════════════════════════════════════════════════════════════════════
              STEP 2: CONFLICT DETECTION  (Def. 4 — Verdicts)
                "Do two denotations overlap?"
═══════════════════════════════════════════════════════════════════════════

  Conservative Intersection (Def. 3):
  ┌───────────────────────────────────────────────────────────┐
  │                                                           │
  │   D₁ ⊓ D₂ = D₁ ∩ D₂    if both grounded                │
  │   D₁ ⊓ D₂ = ⊤           if either is ⊤                  │
  │                                                           │
  └───────────────────────────────────────────────────────────┘

  Per-operand verdicts:

  SPATIAL:   ⟦c1⟧ ⊓ ⟦c4⟧ = {eur,ger,fra,bav} ∩ {fra} = {fra} ≠ ∅
             ┌─────────────────┐
             │   ✓ COMPATIBLE  │   witness: france
             └─────────────────┘

  PURPOSE:   ⟦c2⟧ ⊓ ⟦c5⟧ = {nonComm,nonCommRes} ∩ {sciRes}
             KB doesn't say sciRes ⊑ nonComm or sciRes ⋢ nonComm
             ┌─────────────────┐
             │   ? UNKNOWN     │   KB gap — honest about ignorance
             └─────────────────┘

  LANGUAGE:  ⟦c3⟧ ⊓ ⟦c6⟧ = {de, de-AT, de-CH} ∩ {fr} = ∅
             ┌─────────────────┐
             │   ✗ CONFLICT    │   fr is not a German dialect
             └─────────────────┘
                              │
                              ▼
═══════════════════════════════════════════════════════════════════════════
           STEP 3: COMPOSITION  (Def. 5 — and/or/xone)
            "How do per-operand verdicts combine?"
═══════════════════════════════════════════════════════════════════════════

  BSB uses AND (all dimensions must overlap):

  ┌──────────┐   ┌──────────┐   ┌──────────┐
  │spatial: ✓│   │purpose: ?│   │language: ✗│
  │Compatible│   │ Unknown  │   │ Conflict  │
  └────┬─────┘   └────┬─────┘   └────┬─────┘
       │              │              │
       └──────────────┼──────────────┘
                      ▼
              ┌──────────────┐
              │  AND:        │
              │  ∃ Conflict  │──→  CONFLICT (language blocks all)
              │  → Conflict  │
              └──────────────┘

  Comparison of composition modes:
  ┌─────────────────────────────────────────────────────────┐
  │                                                         │
  │  AND:   All must be Compatible                          │
  │         One Conflict → whole is Conflict                │
  │         One Unknown (no Conflict) → whole is Unknown    │
  │                                                         │
  │  OR:    One Compatible → whole is Compatible            │
  │         All Conflict → whole is Conflict                │
  │         Mix without Compatible → Unknown                │
  │                                                         │
  │  XONE:  Exactly one Compatible                          │
  │         AND all others provably Conflict  ← STRICT!     │
  │         Anything else → Unknown                         │
  │                                                         │
  │  KEY INSIGHT: xone needs NEGATIVE axioms in KB          │
  │  (ODRL085 vs ODRL086)                                   │
  └─────────────────────────────────────────────────────────┘
                              │
                              ▼
═══════════════════════════════════════════════════════════════════════════
          STEP 4: CROSS-KB ALIGNMENT  (Def. 6, Prop. 1)
           "What if each side uses a different KB?"
═══════════════════════════════════════════════════════════════════════════

  Dataspace A (GeoNames)          Dataspace B (ISO 3166)
  ┌──────────────────┐            ┌──────────────────┐
  │     europe       │───α───────▶│     europe       │
  │    ╱     ╲       │            │    ╱     ╲       │
  │ germany  france  │───α───────▶│ germany  france  │
  │    │             │            │                  │
  │ bavaria          │───α──▶ ⊥   │  (no bavaria)   │
  └──────────────────┘            └──────────────────┘

  Alignment α: order-preserving injection (Def. 6)
  ┌───────────────────────────────────────────────────────┐
  │  x ≤_A y  ↔  α(x) ≤_B α(y)   (biconditional!)      │
  │                                                       │
  │  Injective: distinct concepts stay distinct            │
  │  Partial: α(bavaria) = ⊥  (no counterpart)            │
  └───────────────────────────────────────────────────────┘

  Guarantees (Prop. 1):
  ┌───────────────────────────────────────────────────────┐
  │                                                       │
  │  CONFLICT in KB_A ──────────▶ CONFLICT in KB_B        │
  │                   preserved                           │
  │                                                       │
  │  Unmapped concept ─────────▶ UNKNOWN                  │
  │                   degrades     (never false Conflict)  │
  │                                                       │
  │  Safety: alignment can only WEAKEN toward Unknown     │
  │          never FABRICATE conflicts                     │
  │                                                       │
  └───────────────────────────────────────────────────────┘

  Three configurations:
  ┌────────────┬──────────────────────┬──────────────────┐
  │ Total      │ dom(α) = C_A         │ Verdicts fully   │
  │            │ BCP47 ↔ ISO 639-3    │ preserved        │
  ├────────────┼──────────────────────┼──────────────────┤
  │ Partial    │ dom(α) ⊂ C_A         │ Unmapped → ⊤     │
  │            │ GeoNames → ISO 3166  │ No false Conflict│
  ├────────────┼──────────────────────┼──────────────────┤
  │ Empty      │ dom(α) = ∅           │ All → Unknown    │
  │            │ Incompatible KBs     │ (status quo)     │
  └────────────┴──────────────────────┴──────────────────┘
                              │
                              ▼
═══════════════════════════════════════════════════════════════════════════
            STEP 5: RUNTIME SOUNDNESS  (Thm. 2)
          "Do design-time verdicts hold at runtime?"
═══════════════════════════════════════════════════════════════════════════

  DESIGN TIME                           RUNTIME
  (concepts)                            (concrete values)
  ┌─────────────┐                       ┌─────────────────┐
  │ Analyze:    │                       │ Request arrives: │
  │ c1 vs c2   │                       │ ω(spatial)=FR    │
  │             │                       │ ω(purpose)=sci   │
  │ Verdict:    │                       │ ω(language)=fr   │
  │ CONFLICT    │──── guarantees ──────▶│                   │
  │             │                       │ No ω can satisfy │
  │             │                       │ both c1 and c2   │
  └─────────────┘                       └─────────────────┘

  Thm 2: verdict(c1,c2) = Conflict  →  ¬∃ω: (ω ⊨ c1 ∧ ω ⊨ c2)

  This justifies STATIC POLICY ANALYSIS:
  reject incompatible policies at authoring time,
  before any data flows.

═══════════════════════════════════════════════════════════════════════════
                    PROVER VALIDATION LAYER
═══════════════════════════════════════════════════════════════════════════

  ┌──────────────────────────────────────────────────────────────┐
  │                                                              │
  │  Encoding: EPR fragment (decidable!)                         │
  │                                                              │
  │  TPTP format ──▶ Vampire (superposition) ──▶ SZS status     │
  │       │                                          │           │
  │       │         154 problems                     │ 100%      │
  │       │                                          │ agree     │
  │  SMT-LIB ─────▶ Z3 (DPLL(T)) ────────────▶ sat/unsat       │
  │                                                              │
  │  Verdict mapping:                                            │
  │  ┌────────────┬────────────────┬───────────┐                 │
  │  │ CONFLICT   │ Theorem        │ unsat     │                 │
  │  │ COMPATIBLE │ Theorem        │ unsat     │                 │
  │  │ UNKNOWN    │ CounterSat     │ sat       │                 │
  │  └────────────┴────────────────┴───────────┘                 │
  │                                                              │
  │  Bidirectional denotation rules:                             │
  │  IF-direction:  KB facts → in_denotation  (proves compat)   │
  │  ONLY-IF:       in_denotation → KB facts  (proves conflict) │
  │  Both needed — neither alone suffices!                       │
  │                                                              │
  └──────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════
                        FULL PIPELINE SUMMARY
═══════════════════════════════════════════════════════════════════════════

  ODRL Policy + Request
         │
         ▼
  ┌─────────────────┐
  │ 1. GROUND       │  Def. 3: constraint → denotation (set of concepts)
  │    against KB   │  Three domains: taxonomic / mereological / nominal
  │    γ(v) = ⊥?    │──── yes ────▶ ⟦c⟧ = ⊤
  └────────┬────────┘
           │ no
           ▼
  ┌─────────────────┐
  │ 2. INTERSECT    │  Def. 3+4: ⟦c1⟧ ⊓ ⟦c2⟧
  │    denotations  │  = ∅ → Conflict | ≠ ∅ → Compatible | ⊤ → Unknown
  └────────┬────────┘
           ▼
  ┌─────────────────┐
  │ 3. COMPOSE      │  Def. 5: combine per-operand verdicts
  │    and/or/xone  │  xone needs negative axioms!
  └────────┬────────┘
           ▼
  ┌─────────────────┐
  │ 4. ALIGN?       │  Def. 6 + Prop. 1: cross-KB translation
  │    (if needed)  │  Preserves conflicts, degrades gracefully
  └────────┬────────┘
           ▼
  ┌─────────────────┐
  │ 5. ENFORCE      │  Thm. 2: design-time verdict → runtime guarantee
  │    at runtime   │  Static analysis justified
  └─────────────────┘
```
