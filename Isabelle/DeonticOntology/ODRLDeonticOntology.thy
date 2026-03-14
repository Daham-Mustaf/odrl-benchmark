(* ============================================================
   ODRLDeonticOntology.thy
   FOIS 2026 — "What Does ODRL Mean?"
   Mechanized verification of the formal deontic grounding
   of ODRL in UFO-L and Input/Output Logic.

   **Axioms:**
   - rfr_irreflexive, rfr_injective
   - decl_injective, decl_rfr_disjoint
   - perm_relator_basic     (Paper Axiom 5.1)
   - perm_relator_strong    (Paper Axiom 5.2)
   - proh_relator_basic     (Paper Axiom 5.3)
   - proh_relator_remedy    (Paper Axiom 5.4)
   - unique_founding        (Paper Axiom 5.5)
   - unique_relator_per_event (converse of 5.5)
   - obl_relator            (Paper Axiom 5.6)
   - correlativity_liberty/duty/power/immunity (Paper Axiom 5.7)
   - conflict_detection     (Paper Axiom 5.8)
   - cross_relator_consistency (Paper Axiom 5.9)
   - disability_block       (Paper Axiom 5.10)
   - A1, A2, A3             (Appendix A.0 cross-level axioms)
   - B1, B2, B3             (Appendix A.0 bridge axioms)

   **Lemmas (11 groups):**
   - 1:    perm_creates_liberty
   - 2:    proh_creates_duty
   - 3:    proh_remedy_creates_power
   - 4:    disability_blocks_proh
   - 5/5b: conflict_is_unsat, conflict_cross_relator
   - 6a/b: immunity_blocks_duty, strong_perm_persists
   - 7a-d: violation_triggers_normstate,
           normstate_requires_event,
           event_requires_competence,
           competence_grounds_power
   - 8:    full_lifecycle
   - 9:    liberty_unique_noright, duty_unique_claim,
           power_unique_subj, immunity_unique_disability
   - 10:   unique_founding_determines_relator,
           two_activations_two_relators
   - 11:   grounding_surfaces_noright/claim/immunity/disability

   Build:
     isabelle build -D Isabelle/
   ============================================================ *)

theory ODRLDeonticOntology
  imports Main
begin

(* ── Sorts ──────────────────────────────────────────────────
   Seven base types covering the ODRL signature.
   All are abstract (typedecl) -- no structure assumed
   beyond what the axioms impose.
   ─────────────────────────────────────────────────────────── *)
typedecl Agent
typedecl Action
typedecl Target
typedecl Rule
typedecl Position
typedecl LegalRelator
typedecl Event

(* ── Position classifiers ───────────────────────────────────
   Eight Hohfeldian positions at two levels:
     Conduct:    Liberty, Duty, Claim, NoRight
     Competence: Power, Subj, Immunity, Disability
   ─────────────────────────────────────────────────────────── *)
consts
  Liberty    :: "Position => bool"
  Duty       :: "Position => bool"
  Claim      :: "Position => bool"
  NoRight    :: "Position => bool"
  Power      :: "Position => bool"
  Subj       :: "Position => bool"
  Immunity   :: "Position => bool"
  Disability :: "Position => bool"

(* ── Rule classifiers ───────────────────────────────────────
   ODRL rule types and flags.
   ─────────────────────────────────────────────────────────── *)
consts
  Perm   :: "Rule => bool"
  Proh   :: "Rule => bool"
  Obl    :: "Rule => bool"
  rem    :: "Rule => bool"
  strong :: "Rule => bool"

(* ── Structural relations ───────────────────────────────────
   Core predicates connecting rules, positions, relators,
   events, agents, actions, and targets.
   ─────────────────────────────────────────────────────────── *)
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

(* ── rfr function (injective, irreflexive) ──────────────────
   rfr : Action -> Action maps an act to its forbearance.
   Declared over Action -> Action; irreflexivity enforces the
   Act/Forbearance distinction semantically.
   Prohibitions impose Duty over rfr(a), not a directly.
   ─────────────────────────────────────────────────────────── *)
consts rfr :: "Action => Action"

axiomatization where
  rfr_irreflexive : "ALL a.   rfr a ~= a" and
  rfr_injective   : "ALL a b. rfr a = rfr b --> a = b"

(* ── decl function (injective, disjoint from rfr) ───────────
   decl : Action -> Action maps a regulated action to the
   institutional act of declaring its violation.
   Must be disjoint from rfr to prevent collapse between
   proh_relator_basic and proh_relator_remedy.
   ─────────────────────────────────────────────────────────── *)
consts decl :: "Action => Action"

axiomatization where
  decl_injective   : "ALL a b. decl a = decl b --> a = b" and
  decl_rfr_disjoint: "ALL a.   decl a ~= rfr a"

(* ══════════════════════════════════════════════════════════════
   ax:perm-relator-basic  (Paper Axiom 5.1)

   When a Permission activates, it founds a fresh relator with:
     - Liberty borne by assignee over (a, t)
     - NoRight borne by assigner over (a, t)

   ODRL example:
     ex:perm1 odrl:Permission Alice read D1
   --> Liberty(Alice, read, D1), NoRight(Acme, read, D1) in rho

   NoRight is a surfaced correlative absent from any
   ODRL evaluator output (Table 2, row 2).
   ══════════════════════════════════════════════════════════════ *)
axiomatization where
  perm_relator_basic:
  "ALL p x y a t e.
     Perm p & aee p x & aer p y & act p a & tgt p t & activates e p
     --> (EX rho l n.
           isRel rho & founds e rho
         & Liberty l & bearer l x & cnt l a t & partOf l rho
         & NoRight n & bearer n y & cnt n a t & partOf n rho)"

(* ══════════════════════════════════════════════════════════════
   ax:perm-relator-strong  (Paper Axiom 5.2)

   When a strongly-permitted Permission activates and rho
   already exists (founded by perm_relator_basic), adds to rho:
     - Immunity borne by assignee over (a, t)
     - Disability borne by assigner over (a, t)

   The Disability prevents the assigner from later issuing a
   conflicting prohibition (ax:disability-block fires).
   rho is universally quantified -- this EXTENDS an existing
   relator. Caller must supply founds e rho.

   ODRL example:
     ex:perm2 odrl:Permission + ex:stronglyPermitted true
   --> Immunity(Alice, read, D1), Disability(Acme, read, D1)
   ══════════════════════════════════════════════════════════════ *)
axiomatization where
  perm_relator_strong:
  "ALL p x y a t e rho.
     Perm p & strong p & aee p x & aer p y & act p a & tgt p t
     & activates e p & founds e rho
     --> (EX im db.
           Immunity im & bearer im x & cnt im a t & partOf im rho
         & Disability db & bearer db y & cnt db a t & partOf db rho)"

(* ══════════════════════════════════════════════════════════════
   ax:proh-relator-basic  (Paper Axiom 5.3)

   When a Prohibition activates, it founds a fresh relator with:
     - Duty borne by assignee over (rfr(a), t)  -- duty to REFRAIN
     - Claim borne by assigner over (rfr(a), t)

   Key: cnt takes rfr(a) not a. Prohibitions regulate the
   omission (forbearance), not the act itself.
   Contrast with obl_relator which uses cnt du a t.

   ODRL example:
     ex:proh1 odrl:Prohibition Alice distribute D1
   --> Duty(Alice, rfr(distribute), D1),
       Claim(Acme, rfr(distribute), D1) in rho
   ══════════════════════════════════════════════════════════════ *)
axiomatization where
  proh_relator_basic:
  "ALL f x y a t e.
     Proh f & aee f x & aer f y & act f a & tgt f t & activates e f
     --> (EX rho d c.
           isRel rho & founds e rho
         & Duty d & bearer d x & cnt d (rfr a) t & partOf d rho
         & Claim c & bearer c y & cnt c (rfr a) t & partOf c rho)"

(* ══════════════════════════════════════════════════════════════
   ax:proh-relator-remedy  (Paper Axiom 5.4)

   When a Prohibition with remedy activates and rho already
   exists (from proh_relator_basic), adds to rho:
     - Power borne by assigner over (decl(a), t)
     - Subj borne by assignee over (decl(a), t)

   TIMING: Power is constituted at ACTIVATION, not at violation.
   It is a standing position licensing a future institutional
   act. rho is universally quantified -- EXTENDS existing relator.

   ODRL example:
     ex:proh1 odrl:Prohibition ... odrl:remedy ex:remedy1
   --> Power(Acme, decl(distribute), D1),
       Subj(Alice, decl(distribute), D1) added to rho

   Without rem(f): only proh_relator_basic fires.
   ══════════════════════════════════════════════════════════════ *)
axiomatization where
  proh_relator_remedy:
  "ALL f x y a t e rho.
     Proh f & rem f & aee f x & aer f y & act f a & tgt f t
     & activates e f & founds e rho
     --> (EX pw s.
           Power pw & bearer pw y & cnt pw (decl a) t & partOf pw rho
         & Subj s  & bearer s  x & cnt s  (decl a) t & partOf s  rho)"

(* ══════════════════════════════════════════════════════════════
   ax:unique-founding  (Paper Axiom 5.5)

   Every legal relator was founded by exactly one activation
   event. Direction: same relator -> same event.

   UFO-L basis (UFO axiom a77): a relator is founded by a
   unique event. Two distinct activations of the same rule
   produce TWO distinct relators.

   ODRL example:
     Alice requests D1 Monday --> e1 --> rho1
     Alice requests D1 Friday --> e2 --> rho2
   rho1 ~= rho2: Skolem terms are fresh per activation event.
   ══════════════════════════════════════════════════════════════ *)
axiomatization where
  unique_founding:
  "ALL rho e1 e2.
     founds e1 rho & founds e2 rho --> e1 = e2"

(* ── unique_relator_per_event ────────────────────────────────
   Converse of unique_founding.
   Direction: same event -> same relator.

   Needed in full_lifecycle (Lemma 8) to identify the fresh
   rho' introduced by proh_relator_basic with the assumed rho:
     founds e rho' & founds e rho --> rho' = rho

   In UFO-L: an activation event is a complete founding cause
   of exactly one relator instance.
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  unique_relator_per_event:
  "ALL e rho1 rho2.
     founds e rho1 & founds e rho2 --> rho1 = rho2"

(* ══════════════════════════════════════════════════════════════
   ax:obl-relator  (Paper Axiom 5.6)

   When an ODRL Duty rule activates, it founds a fresh relator:
     - Duty borne by assignee over (a, t)  -- duty to PERFORM
     - Claim borne by assigner over (a, t)

   Key contrast with proh_relator_basic:
     proh_relator_basic : cnt d (rfr a) t  -- duty to REFRAIN
     obl_relator        : cnt du a t       -- duty to PERFORM

   Variable 'du' (Hohfeldian Duty position) distinct from
   'd' (ODRL Duty rule variable) to avoid shadowing.

   ODRL example:
     ex:duty1 odrl:Duty Alice compensate D1
   --> Duty(Alice, compensate, D1), Claim(Acme, compensate, D1)
   ══════════════════════════════════════════════════════════════ *)
axiomatization where
  obl_relator:
  "ALL d x y a t e.
     Obl d & aee d x & aer d y & act d a & tgt d t & activates e d
     --> (EX rho du c.
           isRel rho & founds e rho
         & Duty du & bearer du x & cnt du a t & partOf du rho
         & Claim c  & bearer c  y & cnt c  a t & partOf c  rho)"

(* ══════════════════════════════════════════════════════════════
   ax:correlativity  (Paper Axiom 5.7)

   Every Hohfeldian position in a relator has exactly ONE
   correlative partner in that relator -- not zero, not two.

   Four biconditional pairs:
     Liberty  <-> NoRight    (conduct level)
     Duty     <-> Claim      (conduct level)
     Power    <-> Subj       (competence level)
     Immunity <-> Disability (competence level)

   Biconditional (=) enforces BOTH directions:
     --> position in rho requires exactly one correlative
     <-- correlative in rho requires its partner

   EX! expanded manually to avoid Isabelle parsing issues.
   UFO-L: correlatives are co-constituted parts of a relator.
   ══════════════════════════════════════════════════════════════ *)
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
              & (ALL s2. Subj s2 & partOf s2 rho --> s2 = s))"
and
  correlativity_immunity:
  "ALL im rho.
     (Immunity im & partOf im rho)
     = (EX db. Disability db & partOf db rho
               & (ALL db2. Disability db2 & partOf db2 rho --> db2 = db))"

(* ══════════════════════════════════════════════════════════════
   ax:conflict  (Paper Axiom 5.8)

   No relator can bundle Liberty and Duty-to-refrain over the
   same (a, t) for the same bearer. Single-relator conflict.

   Why rfr(a) is essential:
     Liberty over a    = licensed to perform
     Duty over rfr(a)  = obliged to refrain
     Only Liberty + Duty-to-refrain is a conflict.
     Liberty + Duty-to-perform is NOT.

   ODRL example:
     perm_relator_basic: Liberty(Alice, read, D1) in rho
     proh_relator_basic: Duty(Alice, rfr(read), D1) in rho
   Both in same rho --> False (Vampire: SZS Unsatisfiable).

   Contrast with ax:disability-block:
     ax:conflict      -- post-hoc (within a relator)
     disability-block -- up front (prevents creation)
   ══════════════════════════════════════════════════════════════ *)
axiomatization where
  conflict_detection:
  "ALL rho l d x a t.
     partOf l rho & partOf d rho
     & Liberty l & Duty d
     & bearer l x & bearer d x
     & cnt l a t & cnt d (rfr a) t
     --> False"

(* ══════════════════════════════════════════════════════════════
   ax:cross-relator  (Paper Axiom 5.9)

   Strengthens ax:conflict to model-level: Liberty and
   Duty-to-refrain cannot be co-borne by the same agent in
   ANY relators -- not just within one relator.

   Needed for Theorem 4.1 / Appendix A.2 Part 1:
     rho1 (permission) --> Liberty(Alice, read, D1)
     rho2 (prohibition) --> Duty(Alice, rfr(read), D1)
   rho1 ~= rho2, so conflict_detection cannot fire.
   But cross_relator_consistency still derives False.

   UFO: Liberty and Duty are disjoint moment types.
   An agent cannot bear both over the same (a,t).

   [simp del] prevents blast from looping on this axiom
   when Liberty and Duty facts are in context (full_lifecycle).
   Always cite explicitly.
   ══════════════════════════════════════════════════════════════ *)
axiomatization where
  cross_relator_consistency [simp del]:
  "Liberty l --> bearer l x --> cnt l a t -->
   Duty d    --> bearer d x --> cnt d (rfr a) t -->
   False"

(* ══════════════════════════════════════════════════════════════
   ax:disability-block  (Paper Axiom 5.10)

   If a Prohibition by y over (a, t) exists, then y cannot
   simultaneously hold a Disability over the same (a, t).
   Disability means y lacks competence to create that
   prohibition -- the two cannot coexist.

   ODRL example:
     perm_relator_strong adds Disability(Acme, read, D1).
     Acme tries: ex:proh1 odrl:Prohibition Alice read D1.
     --> False: the prohibition is blocked.

   Mechanized basis for Theorem 4.1:
     H1 = {Liberty, NoRight}: inadequate (prohibition can be added).
     H2 = H1 + {Immunity, Disability}: adequate (this axiom
     blocks the prohibition from being created).
   ══════════════════════════════════════════════════════════════ *)
axiomatization where
  disability_block:
  "ALL f x y a t.
     Proh f & aee f x & aer f y & act f a & tgt f t
     --> ~(EX db. Disability db & bearer db y & cnt db a t)"

(* ══════════════════════════════════════════════════════════════
   A.0 — Appendix predicates: A1--A3 + bridges B1--B3

   Paper: Appendix A.0. These predicates and axioms underlie
   the cross-level design principle (Section 4, Theorems
   4.1--4.3). Imported into the TPTP/FOF and SMT-LIB encodings.

   New sort:
     NormPos  -- abstract witness type for normative positions

   New predicates:
     NormStateChange(x,a,t,q) -- position q changes for x
     InstEvent(e)             -- e is an institutional event
     triggers(e,x,a,t,q)     -- e triggers the change of q
     competentFor(y,e)        -- y is competent to perform e
     aboutEvent(pw,e)         -- Power/Subj pw concerns event e
     does(x,a,t)              -- x performs a on t
     Duty_rem                 -- witness token for remedy-duty
   ══════════════════════════════════════════════════════════════ *)
typedecl NormPos

consts
  NormStateChange :: "Agent => Action => Target => NormPos => bool"
  InstEvent       :: "Event => bool"
  triggers        :: "Event => Agent => Action => Target => NormPos => bool"
  competentFor    :: "Agent => Event => bool"
  aboutEvent      :: "Position => Event => bool"
  does            :: "Agent => Action => Target => bool"
  Duty_rem        :: NormPos

(* ── A1: Normative State Changes Require an Institutional Event
   A normative state change requires a triggering institutional
   event. The change cannot happen spontaneously.

   ODRL motivation: Alice distributes D1 despite ex:proh1.
   The remedy duty must become active. A1 requires a triggering
   event -- specifically, Acme performing declareViolation.
   Forces WHO triggers it --> A2.

   Used in: normstate_requires_event (Lemma 7b), full_lifecycle.
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  A1:
  "ALL x a t q.
     NormStateChange x a t q
     --> (EX e. InstEvent e & triggers e x a t q)"

(* ── A2: Institutional Events Require a Competent Agent
   No institutional event without a competent agent.

   ODRL motivation: declareViolation cannot occur in a vacuum.
   Some y must be competentFor(y, e). In the ODRL scenario,
   y = Acme. In multi-party spaces: forces delegation questions.
   Forces WHAT is that competence --> A3.

   Used in: event_requires_competence (Lemma 7c), full_lifecycle.
   ─────────────────────────────────────────────────────────── *)
and A2:
  "ALL e.
     InstEvent e
     --> (EX y. competentFor y e)"

(* ── A3: Competence Is a Power-Subjection Pair
   Competence is grounded in a Power-Subjection pair.
   The competent agent y holds the Power; some x holds the
   correlative Subjection. Not a primitive.

   ODRL motivation: Acme competentFor declareViolation.
   A3 grounds this in the Power/Subj pair from
   proh_relator_remedy -- created at activation time.

   Key step in Theorem 4.2: conduct-level positions alone
   cannot provide this Power-Subjection pair.

   Used in: competence_grounds_power (Lemma 7d), full_lifecycle.
   ─────────────────────────────────────────────────────────── *)
and A3:
  "ALL y e.
     competentFor y e
     --> (EX pw s x.
           Power pw & bearer pw y &
           Subj s   & bearer s  x &
           aboutEvent pw e & aboutEvent s e)"

(* ── B1: Performing a Prohibited Action Is a NormStateChange
   Bridge connecting does() to A1. Performing a prohibited
   action with remedy constitutes a NormStateChange.

   Without B1: A1 never fires for ODRL violations.
   B1 is the entry point of the B1->A1->A2->A3 chain.

   ODRL example: does(Alice, distribute, D1) with rem(f)
   --> NormStateChange(Alice, distribute, D1, Duty_rem)

   Used in: violation_triggers_normstate (Lemma 7), full_lifecycle.
   ─────────────────────────────────────────────────────────── *)
and B1:
  "ALL f x a t b.
     Proh f & rem f & act f a & tgt f t & aee f x &
     does x a t
     --> NormStateChange x b t Duty_rem"

(* ── B2: Power Content Links to Founding Event
   Bridge connecting relator structure (partOf/founds) to
   the event structure (aboutEvent) required by A3.

   proh_relator_remedy created: Power pw, partOf pw rho, founds e rho
   B2 derives: aboutEvent(pw, e)

   Without B2: the chain B1->A1->A2->A3 breaks at A3 because
   the Power from proh_relator_remedy is not connected to
   the institutional event.

   Used in: full_lifecycle (Lemma 8) implicitly via A3.
   ─────────────────────────────────────────────────────────── *)
and B2:
  "ALL pw a t rho e.
     Power pw & cnt pw (decl a) t &
     partOf pw rho & founds e rho
     --> aboutEvent pw e"

(* ── B3: Subjection Content Links to Founding Event
   Mirror of B2 for the Subj position. Together B2 and B3
   ensure the Power-Subjection pair in the relator is the
   same pair A3 identifies as grounding competence.

   Without B3: A3 could introduce a fresh unrelated pair
   disconnected from the ODRL policy structure.

   Used in: full_lifecycle (Lemma 8) implicitly via A3.
   ─────────────────────────────────────────────────────────── *)
and B3:
  "ALL s a t rho e.
     Subj s & cnt s (decl a) t &
     partOf s rho & founds e rho
     --> aboutEvent s e"

(* ══════════════════════════════════════════════════════════════
   Lemma 1: Permission creates Liberty
   Paper: Proposition 5.1 (Faithfulness, direction i)

   Evaluator permits a for x on t
   --> Liberty(x,a,t) in Ground(pi,e)

   Proof: direct unfolding of perm_relator_basic.
   NoRight n also exists in rho but is dropped here.
   ══════════════════════════════════════════════════════════════ *)
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

(* ══════════════════════════════════════════════════════════════
   Lemma 2: Prohibition creates Duty + Claim
   Paper: Proposition 5.1 (Faithfulness, direction ii)

   Evaluator activates prohibition on a for x on t
   --> Duty(x, rfr(a), t)  in Ground(pi,e)
   --> Claim(y, rfr(a), t) in Ground(pi,e)

   Both over rfr(a): prohibition regulates the forbearance.
   Both Duty and Claim retained (both are correlatives).
   Mechanized basis for conflict detection (if Liberty also
   exists in rho, conflict_detection fires --> False).
   ══════════════════════════════════════════════════════════════ *)
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

(* ══════════════════════════════════════════════════════════════
   Lemma 3: Prohibition with remedy creates Power + Subj
   Paper: Proposition 5.1 (Faithfulness, direction iii)

   Evaluator activates prohibition with remedy
   --> Power(y, decl(a), t) in Ground(pi,e)
   --> Subj(x, decl(a), t)  in Ground(pi,e)

   rho is given in assumptions -- EXTENDS the relator from
   Lemma 2. Caller must supply founds e rho.
   TIMING: Power is constituted at activation, not violation.
   Mechanized basis for Theorem 4.2 (H4 adequacy).
   ══════════════════════════════════════════════════════════════ *)
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

(* ══════════════════════════════════════════════════════════════
   Lemma 4: Disability precludes prohibition creation
   Paper: Theorem 4.1 mechanized consequence (ax:disability-block)

   If y holds Disability over (a,t) then no prohibition by y
   over (a,t) can exist -- they are mutually inconsistent.

   Proof: disability_block gives ~(EX db. Disability db & ...)
   Assumptions give a witness db. Contradiction by blast.

   Key step in Theorem 4.1: H2 = {Liberty, NoRight, Immunity,
   Disability} is adequate because this lemma blocks the
   prohibition from being created.
   ══════════════════════════════════════════════════════════════ *)
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

(* ══════════════════════════════════════════════════════════════
   Lemma 5: Liberty-Duty conflict within one relator
   Paper: ax:conflict (Axiom 5.8) mechanized

   If Liberty(x,a,t) and Duty(x,rfr(a),t) are in the SAME
   relator rho, derives False. Single-relator conflict.
   Vampire gives SZS Unsatisfiable.

   For cross-relator conflict, see Lemma 5b.
   ══════════════════════════════════════════════════════════════ *)
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

(* ══════════════════════════════════════════════════════════════
   Lemma 5b: Liberty-Duty conflict across any relators
   Paper: ax:cross-relator (Axiom 5.9) / Appendix A.2 Part 1

   Strengthens Lemma 5 to model-level. Liberty and
   Duty-to-refrain cannot be co-borne regardless of relators.

   Mechanized basis for Appendix A.2 Part 1:
   "extending H1 with a prohibition makes the model
   inconsistent -- even across separate relators."

   Note: cross_relator_consistency is [simp del] -- must cite
   explicitly (prevents blast looping in full_lifecycle).
   ══════════════════════════════════════════════════════════════ *)
lemma conflict_cross_relator:
  assumes "Liberty l" "bearer l x" "cnt l a t"
          "Duty d"    "bearer d x" "cnt d (rfr a) t"
  shows "False"
  using assms cross_relator_consistency by blast

(* ══════════════════════════════════════════════════════════════
   Lemma 6a: Immunity + Disability blocks new Duty
   Paper: Appendix A.2 Part 2 (intermediate step)

   When x holds Immunity and y holds Disability over (a,t),
   y cannot issue a prohibition (Disability fires, Lemma 4).
   Immunity in assumptions confirms H2 is fully in scope.
   ══════════════════════════════════════════════════════════════ *)
lemma immunity_blocks_duty:
  assumes "Immunity im" "bearer im x" "cnt im a t"
          "Disability db" "bearer db y" "cnt db a t"
          "Proh f" "aee f x" "aer f y" "act f a" "tgt f t"
  shows "False"
  using assms disability_blocks_proh by blast

(* ══════════════════════════════════════════════════════════════
   Lemma 6b: Strong permission persists under model extension
   Paper: Theorem 4.1 / Appendix A.2 Part 2

   H2 = {Liberty, NoRight, Immunity, Disability} is adequate:
   no prohibition by y over (a,t) can coexist with H2.
   Liberty survives under ANY model extension.

   Contrast with H1 (Lemma 5b -- inadequacy):
     H1: extension with prohibition makes model inconsistent
         POST-HOC. Liberty destroyed. H1 inadequate.
     H2: prohibition cannot be CREATED. H2 adequate.
   ══════════════════════════════════════════════════════════════ *)
lemma strong_perm_persists:
  assumes
    "Liberty l"     "bearer l x"  "cnt l a t"
    "Immunity im"   "bearer im x" "cnt im a t"
    "Disability db" "bearer db y" "cnt db a t"
    "Proh f" "aee f x" "aer f y" "act f a" "tgt f t"
    "activates e f"
  shows "False"
  using assms disability_blocks_proh by blast

(* ══════════════════════════════════════════════════════════════
   Lemma 7: Violation triggers NormStateChange  (B1)
   Paper: Appendix A.3 Part 1 -- B1 entry point

   First step in B1->A1->A2->A3.
   does(x,a,t) with Proh + rem(f) --> NormStateChange via B1.
   Without B1: A1 never fires for ODRL violations.
   ══════════════════════════════════════════════════════════════ *)
lemma violation_triggers_normstate:
  assumes "Proh f" "rem f"
          "act f a" "tgt f t" "aee f x"
          "does x a t"
  shows "NormStateChange x b t Duty_rem"
  using assms B1 by blast

(* ══════════════════════════════════════════════════════════════
   Lemma 7b: NormStateChange requires institutional event  (A1)
   Paper: Appendix A.3 Part 1 -- A1 step

   NormStateChange requires a triggering institutional event.
   Forces: WHO performs it? --> Lemma 7c (A2).
   ══════════════════════════════════════════════════════════════ *)
lemma normstate_requires_event:
  assumes "NormStateChange x b t Duty_rem"
  shows "EX e. InstEvent e & triggers e x b t Duty_rem"
  using assms A1 by blast

(* ══════════════════════════════════════════════════════════════
   Lemma 7c: Institutional event requires competent agent  (A2)
   Paper: Appendix A.3 Part 1 -- A2 step

   No institutional event without a competent agent.
   Forces: WHAT IS that competence? --> Lemma 7d (A3).
   ══════════════════════════════════════════════════════════════ *)
lemma event_requires_competence:
  assumes "InstEvent e"
  shows "EX y. competentFor y e"
  using assms A2 by blast

(* ══════════════════════════════════════════════════════════════
   Lemma 7d: Competence grounded in Power-Subjection  (A3)
   Paper: Appendix A.3 Part 1 -- A3 step (final link)

   Competence is grounded in a Power-Subjection pair via A3.
   This Power is what proh_relator_remedy created at activation.

   Full chain:
     does(x,a,t)              [Lemma 7 / B1]
     --> NormStateChange       [A1, Lemma 7b]
     --> InstEvent(e')         [A2, Lemma 7c]
     --> competentFor(y', e') [A3, Lemma 7d]
     --> Power(y') + Subj(x')

   H3 = {Duty, Claim} cannot provide this --> H3 inadequate.
   H4 = H3 + {Power, Subj} IS adequate (Lemma 8).
   ══════════════════════════════════════════════════════════════ *)
lemma competence_grounds_power:
  assumes "competentFor y e"
  shows "EX pw s x. Power pw & bearer pw y &
                    Subj s   & bearer s  x &
                    aboutEvent pw e & aboutEvent s e"
  using assms A3 by blast

(* ══════════════════════════════════════════════════════════════
   Lemma 8: Full sanctioned-prohibition lifecycle
   Paper: Theorem 4.2 / Appendix A.3 Part 2 (adequacy of H4)

   Master lemma combining Lemmas 2, 3, 7a--7d.
   Witnesses all six steps: duty -> violation -> declaration
   -> remedy active.

   ODRL example:
     ex:proh1 Prohibition Alice distribute D1 + remedy
     Activation e fires. Alice performs does(Alice,distribute,D1).

   Six conclusions:
     (1) Duty + Claim in rho          [proh_relator_basic]
     (2) Power + Subj in rho          [proh_relator_remedy]
     (3) NormStateChange(Alice,...)   [B1 / Lemma 7]
     (4) InstEvent(e')                [A1 / Lemma 7b]
     (5) competentFor(y', e')         [A2 / Lemma 7c]
     (6) Power(y') + Subj aboutEvent  [A3 / Lemma 7d]

   Proof strategy:
     - proh_relator_basic introduces fresh rho'; unify with
       assumed rho via unique_relator_per_event.
     - Pre-substitute into dc_rho/ps_rho (isolates from
       Liberty/Duty facts to prevent cross_relator looping).
     - Name each conjunction part g1..g6.
     - Final blast on g1..g6 assembles the conjunction.
     - cross_relator_consistency is [simp del] so never fires
       automatically in this proof context.
   ══════════════════════════════════════════════════════════════ *)
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
    (EX e'. InstEvent e' & triggers e' x a t Duty_rem &
            (EX y'. competentFor y' e' &
                    (EX pw' s' x''.
                       Power pw' & bearer pw' y' &
                       Subj s'   & bearer s'  x'' &
                       aboutEvent pw' e' & aboutEvent s' e')))"
proof -
  (* Step 1: Duty + Claim from proh_relator_basic *)
  obtain rho' d c where dc:
    "isRel rho'" "founds e rho'"
    "Duty d"  "bearer d x" "cnt d (rfr a) t" "partOf d rho'"
    "Claim c" "bearer c y" "cnt c (rfr a) t" "partOf c rho'"
    using assms proh_relator_basic by blast
  have rho_eq: "rho' = rho"
    using dc(2) assms(8) unique_relator_per_event by blast
  have dc_rho:
    "Duty d & bearer d x & cnt d (rfr a) t & partOf d rho &
     Claim c & bearer c y & cnt c (rfr a) t & partOf c rho"
    using dc rho_eq by simp
  (* Step 2: Power + Subj from proh_relator_remedy *)
  obtain rho'' pw s where ps:
    "founds e rho''"
    "Power pw" "bearer pw y" "cnt pw (decl a) t" "partOf pw rho''"
    "Subj s"   "bearer s  x" "cnt s  (decl a) t" "partOf s  rho''"
    using assms proh_relator_remedy by blast
  have rho_eq2: "rho'' = rho"
    using ps(1) assms(8) unique_relator_per_event by blast
  have ps_rho:
    "Power pw & bearer pw y & cnt pw (decl a) t & partOf pw rho &
     Subj s & bearer s x & cnt s (decl a) t & partOf s rho"
    using ps rho_eq2 by simp
  (* Step 3: NormStateChange via B1 *)
  have nsc: "NormStateChange x a t Duty_rem"
    using assms violation_triggers_normstate by blast
  (* Step 4: institutional event via A1 *)
  obtain e' where ev:
    "InstEvent e'" "triggers e' x a t Duty_rem"
    using nsc normstate_requires_event by blast
  (* Step 5: competent agent via A2 *)
  obtain y' where comp: "competentFor y' e'"
    using ev(1) event_requires_competence by blast
  (* Step 6: Power-Subjection grounding via A3 *)
  obtain pw' s' x'' where psa:
    "Power pw'" "bearer pw' y'"
    "Subj s'"   "bearer s'  x''"
    "aboutEvent pw' e'" "aboutEvent s' e'"
    using comp competence_grounds_power by blast
  (* Assemble conjuncts -- each isolated to prevent
     cross_relator_consistency from firing *)
  have g1: "EX d c.
      Duty d  & bearer d x & cnt d (rfr a) t & partOf d rho &
      Claim c & bearer c y & cnt c (rfr a) t & partOf c rho"
    using dc_rho by blast
  have g2: "EX pw s.
      Power pw & bearer pw y & cnt pw (decl a) t & partOf pw rho &
      Subj s   & bearer s  x & cnt s  (decl a) t & partOf s  rho"
    using ps_rho by blast
  have g3: "NormStateChange x a t Duty_rem" using nsc .
  have g4: "EX e'. InstEvent e' & triggers e' x a t Duty_rem &
              (EX y'. competentFor y' e' &
                      (EX pw' s' x''.
                         Power pw' & bearer pw' y' &
                         Subj s'   & bearer s'  x'' &
                         aboutEvent pw' e' & aboutEvent s' e'))"
    using ev comp psa by blast
  show ?thesis
    apply (intro conjI)
    using g1 apply assumption
    using g2 apply assumption
    using g3 apply assumption
    using g4 apply assumption
    done
qed
(* ══════════════════════════════════════════════════════════════
   Lemma 9: Correlativity uniqueness
   Paper: ax:correlativity (Axiom 5.7) consequences

   Each Hohfeldian position has exactly ONE correlative partner
   in the same relator -- not zero, not two.

   Four sub-lemmas projecting biconditional axioms into
   existential-uniqueness direction.

   ODRL example: Liberty(l) in rho --> exactly one NoRight in rho.
   Two NoRights would be structurally incoherent in UFO-L.
   ══════════════════════════════════════════════════════════════ *)
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

(* ══════════════════════════════════════════════════════════════
   Lemma 10: Unique founding consequences
   Paper: ax:unique-founding (Axiom 5.5) mechanized

   10a: same event founds same relator (deterministic founding)
   10b: distinct events produce distinct relators (freshness)

   ODRL example:
     Alice requests D1 Monday --> e1 --> rho1
     Alice requests D1 Friday --> e2 --> rho2
     e1 ~= e2 --> rho1 ~= rho2
   Each activation creates fresh position individuals per
   UFO axiom a77. Essential for Skolem term freshness.

   10b uses BOTH unique_relator_per_event (e -> rho) and
   unique_founding (rho -> e) to derive rho1 ~= rho2.
   ══════════════════════════════════════════════════════════════ *)
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

(* ══════════════════════════════════════════════════════════════
   Lemma 11: Grounding strictly richer than ODRL evaluator
   Paper: Proposition 5.1 converse / Table 2 rows 2, 4, 7, 8

   ODRL evaluator produces (rows 1, 3, 5):
     Permission  --> Liberty
     Prohibition --> Duty
     Remedy      --> Power

   Grounding additionally entails (rows 2, 4, 7, 8):
     NoRight    -- surfaced correlative of Liberty
     Claim      -- surfaced correlative of Duty
     Immunity   -- added for strong permission
     Disability -- added for strong permission

   ODRL examples:
     ex:perm1  --> Evaluator: PERMITTED
                   Grounding: + NoRight(Acme, read, D1)
     ex:proh1  --> Evaluator: PROHIBITED
                   Grounding: + Claim(Acme, rfr(distribute), D1)
     ex:perm2 + strong
               --> Evaluator: PERMITTED
                   Grounding: + Immunity(Alice) + Disability(Acme)
   ══════════════════════════════════════════════════════════════ *)
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
