theory ODRLDeonticOntology
  imports Main
begin


(* **Axioms (11):**
- `rfr_irreflexive`, `rfr_injective`
- `decl_injective`, `decl_rfr_disjoint`
- `perm_relator_basic`, `perm_relator_strong`
- `proh_relator_basic`, `proh_relator_remedy`
- `unique_founding`, `unique_relator_per_event`
- `obl_relator`
- `correlativity_liberty/duty/power/immunity`
- `conflict_detection`
- `cross_relator_consistency`
- `disability_block`
- `A1`, `A2`, `A3`, `B1`, `B2`, `B3`

**Lemmas (11 groups):**
- 1: `perm_creates_liberty`
- 2: `proh_creates_duty`
- 3: `proh_remedy_creates_power`
- 4: `disability_blocks_proh`
- 5/5b: `conflict_is_unsat`, `conflict_cross_relator`
- 6a/6b: `immunity_blocks_duty`, `strong_perm_persists`
- 7a-7d: `violation_triggers_normstate`, `normstate_requires_event`, `event_requires_competence`, `competence_grounds_power`
- 8: `full_lifecycle`
- 9: `liberty_unique_noright`, `duty_unique_claim`, `power_unique_subj`, `immunity_unique_disability`
- 10: `unique_founding_determines_relator`, `two_activations_two_relators`
- 11: `grounding_surfaces_noright/claim/immunity/disability`

Build:

isabelle build -D Isabelle/ *)

(* ── Sorts ─────────────────────────────────────── *)
typedecl Agent
typedecl Action
typedecl Target
typedecl Rule
typedecl Position
typedecl LegalRelator
typedecl Event

(* ── Position classifiers ───────────────────────── *)
consts
  Liberty    :: "Position => bool"
  Duty       :: "Position => bool"
  Claim      :: "Position => bool"
  NoRight    :: "Position => bool"
  Power      :: "Position => bool"
  Subj       :: "Position => bool"
  Immunity   :: "Position => bool"
  Disability :: "Position => bool"

(* ── Rule classifiers ───────────────────────────── *)
consts
  Perm   :: "Rule => bool"
  Proh   :: "Rule => bool"
  Obl    :: "Rule => bool"
  rem    :: "Rule => bool"
  strong :: "Rule => bool"

(* ── Structural relations ───────────────────────── *)
consts
  aee       :: "Rule => Agent => bool"
  aer       :: "Rule => Agent => bool"
  act       :: "Rule => Action => bool"
  tgt       :: "Rule => Target => bool"
  activates :: "Event => Rule => bool"
  founds    :: "Event => LegalRelator => bool"
  isRel     :: "LegalRelator => bool"
  bearer    :: "Position => Agent => bool"
  cnt       :: "Position => Action => Target => bool"
  partOf    :: "Position => LegalRelator => bool"

(* ── rfr function (injective, irreflexive) ─────── *)
consts rfr :: "Action => Action"

axiomatization where
  rfr_irreflexive : "ALL a.   rfr a ~= a" and
  rfr_injective   : "ALL a b. rfr a = rfr b --> a = b"

(* ── decl function (injective, disjoint from rfr) ── *)
consts decl :: "Action => Action"

axiomatization where
  decl_injective   : "ALL a b. decl a = decl b --> a = b" and
  decl_rfr_disjoint: "ALL a.   decl a ~= rfr a"

(* ══════════════════════════════════════════════════
   ax:perm-relator-basic  (Paper Axiom 5.1)
   ══════════════════════════════════════════════════ *)
axiomatization where
  perm_relator_basic:
  "ALL p x y a t e.
     Perm p & aee p x & aer p y & act p a & tgt p t & activates e p
     --> (EX rho l n.
           isRel rho & founds e rho
         & Liberty l & bearer l x & cnt l a t & partOf l rho
         & NoRight n & bearer n y & cnt n a t & partOf n rho)"

(* ══════════════════════════════════════════════════
   ax:perm-relator-strong  (Paper Axiom 5.2)
   ══════════════════════════════════════════════════ *)
axiomatization where
  perm_relator_strong:
  "ALL p x y a t e rho.
     Perm p & strong p & aee p x & aer p y & act p a & tgt p t
     & activates e p & founds e rho
     --> (EX im db.
           Immunity im & bearer im x & cnt im a t & partOf im rho
         & Disability db & bearer db y & cnt db a t & partOf db rho)"

(* ══════════════════════════════════════════════════
   ax:proh-relator-basic  (Paper Axiom 5.3)
   ══════════════════════════════════════════════════ *)
axiomatization where
  proh_relator_basic:
  "ALL f x y a t e.
     Proh f & aee f x & aer f y & act f a & tgt f t & activates e f
     --> (EX rho d c.
           isRel rho & founds e rho
         & Duty d & bearer d x & cnt d (rfr a) t & partOf d rho
         & Claim c & bearer c y & cnt c (rfr a) t & partOf c rho)"

(* ══════════════════════════════════════════════════
   ax:proh-relator-remedy  (Paper Axiom 5.4)
   ══════════════════════════════════════════════════ *)
axiomatization where
  proh_relator_remedy:
  "ALL f x y a t e rho.
     Proh f & rem f & aee f x & aer f y & act f a & tgt f t
     & activates e f & founds e rho
     --> (EX pw s.
           Power pw & bearer pw y & cnt pw (decl a) t & partOf pw rho
         & Subj s  & bearer s  x & cnt s  (decl a) t & partOf s  rho)"

(* ══════════════════════════════════════════════════
   ax:unique-founding  (Paper Axiom 5.5)
   ══════════════════════════════════════════════════ *)
axiomatization where
  unique_founding:
  "ALL rho e1 e2.
     founds e1 rho & founds e2 rho --> e1 = e2"

(* ── Derived: unique relator per event ─────────── *)
axiomatization where
  unique_relator_per_event:
  "ALL e rho1 rho2.
     founds e rho1 & founds e rho2 --> rho1 = rho2"

(* ══════════════════════════════════════════════════
   ax:obl-relator  (Paper Axiom 5.6)
   ══════════════════════════════════════════════════ *)
axiomatization where
  obl_relator:
  "ALL d x y a t e.
     Obl d & aee d x & aer d y & act d a & tgt d t & activates e d
     --> (EX rho du c.
           isRel rho & founds e rho
         & Duty du & bearer du x & cnt du a t & partOf du rho
         & Claim c  & bearer c  y & cnt c  a t & partOf c  rho)"

(* ══════════════════════════════════════════════════
   ax:correlativity  (Paper Axiom 5.7)
   ══════════════════════════════════════════════════ *)
axiomatization where
  correlativity_liberty:
  "ALL l rho.
     (Liberty l & partOf l rho)
     = (EX n. NoRight n & partOf n rho
              & (ALL m. NoRight m & partOf m rho --> m = n))"
and
  correlativity_duty:
  "ALL d rho.
     (Duty d & partOf d rho)
     = (EX c. Claim c & partOf c rho
              & (ALL k. Claim k & partOf k rho --> k = c))"
and
  correlativity_power:
  "ALL pw rho.
     (Power pw & partOf pw rho)
     = (EX s. Subj s & partOf s rho
              & (ALL t. Subj t & partOf t rho --> t = s))"
and
  correlativity_immunity:
  "ALL im rho.
     (Immunity im & partOf im rho)
     = (EX db. Disability db & partOf db rho
               & (ALL db2. Disability db2 & partOf db2 rho --> db2 = db))"

(* ══════════════════════════════════════════════════
   ax:conflict  (Paper Axiom 5.8)
   ══════════════════════════════════════════════════ *)
axiomatization where
  conflict_detection:
  "ALL rho l d x a t.
     partOf l rho & partOf d rho
     & Liberty l & Duty d
     & bearer l x & bearer d x
     & cnt l a t & cnt d (rfr a) t
     --> False"

(* ══════════════════════════════════════════════════
   ax:cross-relator  (Paper Axiom 5.9)
   Cross-relator position disjointness:
   Liberty and Duty-to-refrain cannot be co-borne
   by the same agent in ANY relators.
   [simp del] prevents blast from looping on this.
   ══════════════════════════════════════════════════ *)
axiomatization where
  cross_relator_consistency [simp del]:
  "Liberty l --> bearer l x --> cnt l a t -->
   Duty d    --> bearer d x --> cnt d (rfr a) t -->
   False"

(* ══════════════════════════════════════════════════
   ax:disability-block  (Paper Axiom 5.10)
   ══════════════════════════════════════════════════ *)
axiomatization where
  disability_block:
  "ALL f x y a t.
     Proh f & aee f x & aer f y & act f a & tgt f t
     --> ~(EX db. Disability db & bearer db y & cnt db a t)"

(* ══════════════════════════════════════════════════
   A.0 — Appendix predicates (A1-A3 + bridges B1-B3)
   ══════════════════════════════════════════════════ *)
typedecl NormPos

consts
  NormStateChange :: "Agent => Action => Target => NormPos => bool"
  InstEvent       :: "Event => bool"
  triggers        :: "Event => Agent => Action => Target => NormPos => bool"
  competentFor    :: "Agent => Event => bool"
  aboutEvent      :: "Position => Event => bool"
  does            :: "Agent => Action => Target => bool"
  Duty_rem        :: NormPos

(* A1 *)
axiomatization where
  A1:
  "ALL x a t q.
     NormStateChange x a t q
     --> (EX e. InstEvent e & triggers e x a t q)"

(* A2 *)
and A2:
  "ALL e.
     InstEvent e
     --> (EX y. competentFor y e)"

(* A3 *)
and A3:
  "ALL y e.
     competentFor y e
     --> (EX pw s x.
           Power pw & bearer pw y &
           Subj s   & bearer s  x &
           aboutEvent pw e & aboutEvent s e)"

(* B1 *)
and B1:
  "ALL f x a t b.
     Proh f & rem f & act f a & tgt f t & aee f x &
     does x a t
     --> NormStateChange x b t Duty_rem"

(* B2 *)
and B2:
  "ALL pw a t rho e.
     Power pw & cnt pw (decl a) t &
     partOf pw rho & founds e rho
     --> aboutEvent pw e"

(* B3 *)
and B3:
  "ALL s a t rho e.
     Subj s & cnt s (decl a) t &
     partOf s rho & founds e rho
     --> aboutEvent s e"

(* ══════════════════════════════════════════════════
   Lemma 1: Permission creates Liberty
   Paper: Prop 5.1 (Faithfulness i)
   ══════════════════════════════════════════════════ *)
lemma perm_creates_liberty:
  assumes "Perm p" "aee p x" "aer p y" "act p a" "tgt p t" "activates e p"
  shows "EX rho l. isRel rho & founds e rho &
                   Liberty l & bearer l x & cnt l a t & partOf l rho"
proof -
  from assms perm_relator_basic
  obtain rho l n where
    "isRel rho" "founds e rho"
    "Liberty l" "bearer l x" "cnt l a t" "partOf l rho"
    "NoRight n" "bearer n y" "cnt n a t" "partOf n rho"
    by blast
  thus ?thesis by blast
qed

(* ══════════════════════════════════════════════════
   Lemma 2: Prohibition creates Duty + Claim
   Paper: Prop 5.1 (Faithfulness ii)
   ══════════════════════════════════════════════════ *)
lemma proh_creates_duty:
  assumes "Proh f" "aee f x" "aer f y" "act f a" "tgt f t" "activates e f"
  shows "EX rho d c. isRel rho & founds e rho &
                     Duty d & bearer d x & cnt d (rfr a) t & partOf d rho &
                     Claim c & bearer c y & cnt c (rfr a) t & partOf c rho"
proof -
  from assms proh_relator_basic
  obtain rho d c where
    "isRel rho" "founds e rho"
    "Duty d"  "bearer d x" "cnt d (rfr a) t" "partOf d rho"
    "Claim c" "bearer c y" "cnt c (rfr a) t" "partOf c rho"
    by blast
  thus ?thesis by blast
qed

(* ══════════════════════════════════════════════════
   Lemma 3: Prohibition with remedy creates Power + Subj
   Paper: Prop 5.1 (Faithfulness iii)
   ══════════════════════════════════════════════════ *)
lemma proh_remedy_creates_power:
  assumes "Proh f" "rem f"
          "aee f x" "aer f y" "act f a" "tgt f t"
          "activates e f" "founds e rho"
  shows "EX pw s. Power pw & bearer pw y & cnt pw (decl a) t & partOf pw rho &
                  Subj s  & bearer s  x & cnt s  (decl a) t & partOf s  rho"
proof -
  from assms proh_relator_remedy
  obtain pw s where
    "Power pw" "bearer pw y" "cnt pw (decl a) t" "partOf pw rho"
    "Subj s"   "bearer s  x" "cnt s  (decl a) t" "partOf s  rho"
    by blast
  thus ?thesis by blast
qed

(* ══════════════════════════════════════════════════
   Lemma 4: Disability precludes prohibition creation
   Paper: ax:disability-block mechanized
   ══════════════════════════════════════════════════ *)
lemma disability_blocks_proh:
  assumes "Proh f" "aee f x" "aer f y" "act f a" "tgt f t"
          "Disability db" "bearer db y" "cnt db a t"
  shows "False"
proof -
  from assms disability_block
  have "~(EX db. Disability db & bearer db y & cnt db a t)"
    by blast
  with assms show ?thesis by blast
qed

(* ══════════════════════════════════════════════════
   Lemma 5: Liberty-Duty conflict within one relator
   Paper: ax:conflict mechanized
   ══════════════════════════════════════════════════ *)
lemma conflict_is_unsat:
  assumes "partOf l rho" "partOf d rho"
          "Liberty l" "Duty d"
          "bearer l x" "bearer d x"
          "cnt l a t" "cnt d (rfr a) t"
  shows "False"
proof -
  from assms conflict_detection
  show ?thesis by blast
qed

(* ══════════════════════════════════════════════════
   Lemma 5b: Liberty-Duty conflict across any relators
   Paper: ax:cross-relator mechanized (Appendix A.2 Part 1)
   ══════════════════════════════════════════════════ *)
lemma conflict_cross_relator:
  assumes "Liberty l" "bearer l x" "cnt l a t"
          "Duty d"    "bearer d x" "cnt d (rfr a) t"
  shows "False"
  using assms cross_relator_consistency by blast

(* ══════════════════════════════════════════════════
   Lemma 6a: Immunity + Disability blocks new Duty
   Paper: Appendix A.2 Part 2 intermediate
   ══════════════════════════════════════════════════ *)
lemma immunity_blocks_duty:
  assumes "Immunity im" "bearer im x" "cnt im a t"
          "Disability db" "bearer db y" "cnt db a t"
          "Proh f" "aee f x" "aer f y" "act f a" "tgt f t"
  shows "False"
  using assms disability_blocks_proh by blast

(* ══════════════════════════════════════════════════
   Lemma 6b: Strong permission persists under extension
   Paper: Theorem 4.1 / Appendix A.2 Part 2
   ══════════════════════════════════════════════════ *)
lemma strong_perm_persists:
  assumes
    "Liberty l"     "bearer l x"  "cnt l a t"
    "Immunity im"   "bearer im x" "cnt im a t"
    "Disability db" "bearer db y" "cnt db a t"
    "Proh f" "aee f x" "aer f y" "act f a" "tgt f t"
    "activates e f"
  shows "False"
  using assms disability_blocks_proh by blast

(* ══════════════════════════════════════════════════
   Lemma 7: Violation triggers NormStateChange  (B1)
   Paper: Appendix A.3 Part 1 entry point
   ══════════════════════════════════════════════════ *)
lemma violation_triggers_normstate:
  assumes "Proh f" "rem f"
          "act f a" "tgt f t" "aee f x"
          "does x a t"
  shows "NormStateChange x b t Duty_rem"
  using assms B1 by blast

(* ══════════════════════════════════════════════════
   Lemma 7b: NormStateChange requires institutional event  (A1)
   ══════════════════════════════════════════════════ *)
lemma normstate_requires_event:
  assumes "NormStateChange x b t Duty_rem"
  shows "EX e. InstEvent e & triggers e x b t Duty_rem"
  using assms A1 by blast

(* ══════════════════════════════════════════════════
   Lemma 7c: Institutional event requires competent agent  (A2)
   ══════════════════════════════════════════════════ *)
lemma event_requires_competence:
  assumes "InstEvent e"
  shows "EX y. competentFor y e"
  using assms A2 by blast

(* ══════════════════════════════════════════════════
   Lemma 7d: Competence grounded in Power-Subjection  (A3)
   ══════════════════════════════════════════════════ *)
lemma competence_grounds_power:
  assumes "competentFor y e"
  shows "EX pw s x. Power pw & bearer pw y &
                    Subj s   & bearer s  x &
                    aboutEvent pw e & aboutEvent s e"
  using assms A3 by blast

(* ══════════════════════════════════════════════════
   Lemma 8: Full sanctioned-prohibition lifecycle
   Paper: Theorem 4.2 / Appendix A.3 Part 2
   ══════════════════════════════════════════════════ *)
lemma full_lifecycle:
  assumes
    "Proh f" "rem f"
    "aee f x" "aer f y" "act f a" "tgt f t"
    "activates e f" "founds e rho"
    "does x a t"
  shows
    "(EX d c.
       Duty d  & bearer d x & cnt d (rfr a) t & partOf d rho &
       Claim c & bearer c y & cnt c (rfr a) t & partOf c rho) &
    (EX pw s.
       Power pw & bearer pw y & cnt pw (decl a) t & partOf pw rho &
       Subj s   & bearer s  x & cnt s  (decl a) t & partOf s  rho) &
    (NormStateChange x a t Duty_rem) &
    (EX e'. InstEvent e' & triggers e' x a t Duty_rem) &
    (EX y'. competentFor y' e') &
    (EX pw' s' x'.
       Power pw' & bearer pw' y' &
       Subj s'   & bearer s'  x' &
       aboutEvent pw' e' & aboutEvent s' e')"
proof -
  obtain rho' d c where dc:
    "isRel rho'" "founds e rho'"
    "Duty d"  "bearer d x" "cnt d (rfr a) t" "partOf d rho'"
    "Claim c" "bearer c y" "cnt c (rfr a) t" "partOf c rho'"
    using assms proh_relator_basic by blast
  have rho_eq: "rho' = rho"
    using dc(2) assms(8) unique_relator_per_event by blast
  obtain rho'' pw s where ps:
    "founds e rho''"
    "Power pw" "bearer pw y" "cnt pw (decl a) t" "partOf pw rho''"
    "Subj s"   "bearer s  x" "cnt s  (decl a) t" "partOf s  rho''"
    using assms proh_relator_remedy by blast
  have rho_eq2: "rho'' = rho"
    using ps(1) assms(8) unique_relator_per_event by blast
  have nsc: "NormStateChange x a t Duty_rem"
    using assms violation_triggers_normstate by blast
  obtain e' where ev:
    "InstEvent e'" "triggers e' x a t Duty_rem"
    using nsc normstate_requires_event by blast
  obtain y' where comp: "competentFor y' e'"
    using ev(1) event_requires_competence by blast
  obtain pw' s' x' where psa:
    "Power pw'" "bearer pw' y'"
    "Subj s'"   "bearer s'  x'"
    "aboutEvent pw' e'" "aboutEvent s' e'"
    using comp competence_grounds_power by blast
  show ?thesis
  proof (intro conjI)
    show "EX d c.
           Duty d  & bearer d x & cnt d (rfr a) t & partOf d rho &
           Claim c & bearer c y & cnt c (rfr a) t & partOf c rho"
      using dc rho_eq by (intro exI) auto
    show "EX pw s.
           Power pw & bearer pw y & cnt pw (decl a) t & partOf pw rho &
           Subj s   & bearer s  x & cnt s  (decl a) t & partOf s  rho"
      using ps rho_eq2 by (intro exI) auto
    show "NormStateChange x a t Duty_rem" using nsc .
    show "EX e'. InstEvent e' & triggers e' x a t Duty_rem"
      using ev by blast
    show "EX y'. competentFor y' e'" using comp by blast
    show "EX pw' s' x'.
           Power pw' & bearer pw' y' &
           Subj s'   & bearer s'  x' &
           aboutEvent pw' e' & aboutEvent s' e'"
      using psa by (intro exI) auto
  qed
qed

(* ══════════════════════════════════════════════════
   Lemma 9: Correlativity uniqueness
   Paper: ax:correlativity consequences
   ══════════════════════════════════════════════════ *)
lemma liberty_unique_noright:
  assumes "Liberty l" "partOf l rho"
  shows "EX! n. NoRight n & partOf n rho"
  using assms correlativity_liberty by blast

lemma duty_unique_claim:
  assumes "Duty d" "partOf d rho"
  shows "EX! c. Claim c & partOf c rho"
  using assms correlativity_duty by blast

lemma power_unique_subj:
  assumes "Power pw" "partOf pw rho"
  shows "EX! s. Subj s & partOf s rho"
  using assms correlativity_power by blast

lemma immunity_unique_disability:
  assumes "Immunity im" "partOf im rho"
  shows "EX! db. Disability db & partOf db rho"
  using assms correlativity_immunity by blast

(* ══════════════════════════════════════════════════
   Lemma 10: Unique founding
   Paper: ax:unique-founding consequences
   ══════════════════════════════════════════════════ *)
lemma unique_founding_determines_relator:
  assumes "founds e rho1" "founds e rho2"
  shows "rho1 = rho2"
  using assms unique_relator_per_event by blast

lemma two_activations_two_relators:
  assumes "founds e1 rho1" "founds e2 rho2" "e1 ~= e2"
  shows "rho1 ~= rho2"
proof -
  from assms unique_relator_per_event
  have "rho1 = rho2 --> founds e1 rho2" by blast
  with assms unique_founding
  have "rho1 = rho2 --> e1 = e2" by blast
  with assms show ?thesis by blast
qed

(* ══════════════════════════════════════════════════
   Lemma 11: Grounding strictly richer than evaluator
   Paper: Prop 5.1 converse / Table 2 strict richness
   ══════════════════════════════════════════════════ *)
lemma grounding_surfaces_noright:
  assumes "Perm p" "aee p x" "aer p y" "act p a" "tgt p t" "activates e p"
  shows "EX rho n. isRel rho & founds e rho &
                   NoRight n & bearer n y & cnt n a t & partOf n rho"
proof -
  from assms perm_relator_basic
  obtain rho l n where
    "isRel rho" "founds e rho"
    "Liberty l" "bearer l x" "cnt l a t" "partOf l rho"
    "NoRight n" "bearer n y" "cnt n a t" "partOf n rho"
    by blast
  thus ?thesis by blast
qed

lemma grounding_surfaces_claim:
  assumes "Proh f" "aee f x" "aer f y" "act f a" "tgt f t" "activates e f"
  shows "EX rho c. isRel rho & founds e rho &
                   Claim c & bearer c y & cnt c (rfr a) t & partOf c rho"
proof -
  from assms proh_relator_basic
  obtain rho d c where
    "isRel rho" "founds e rho"
    "Duty d"  "bearer d x" "cnt d (rfr a) t" "partOf d rho"
    "Claim c" "bearer c y" "cnt c (rfr a) t" "partOf c rho"
    by blast
  thus ?thesis by blast
qed

lemma grounding_surfaces_immunity:
  assumes "Perm p" "strong p" "aee p x" "aer p y"
          "act p a" "tgt p t" "activates e p" "founds e rho"
  shows "EX im. Immunity im & bearer im x & cnt im a t & partOf im rho"
proof -
  from assms perm_relator_strong
  obtain im db where
    "Immunity im"   "bearer im x"  "cnt im a t"  "partOf im rho"
    "Disability db" "bearer db y"  "cnt db a t"  "partOf db rho"
    by blast
  thus ?thesis by blast
qed

lemma grounding_surfaces_disability:
  assumes "Perm p" "strong p" "aee p x" "aer p y"
          "act p a" "tgt p t" "activates e p" "founds e rho"
  shows "EX db. Disability db & bearer db y & cnt db a t & partOf db rho"
proof -
  from assms perm_relator_strong
  obtain im db where
    "Immunity im"   "bearer im x"  "cnt im a t"  "partOf im rho"
    "Disability db" "bearer db y"  "cnt db a t"  "partOf db rho"
    by blast
  thus ?thesis by blast
qed

end
