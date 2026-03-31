(* ============================================================
   ODRLDeonticOntology.thy  —  Stage 1
   FOIS 2026 — "What Does ODRL Mean?"
   run isabelle build -D /Users/dahammhamad/Desktop/tptp-odrl/Isabelle/ -v
   ============================================================ *)
   
theory ODRLDeonticOntology
  imports Main
begin

(* ── Sorts ──────────────────────────────────────────────────
   Seven base types.  All abstract — no structure beyond
   what axioms impose.
   ─────────────────────────────────────────────────────────── *)
typedecl Agent
typedecl Action
typedecl Target
typedecl Rule
typedecl Position
typedecl LegalRelator
typedecl Event

(* ── Hohfeldian position classifiers ────────────────────────
   Conduct:    Permission  Duty  Right  NoRight
   Competence: Power    Subj  Immunity  Disability
   ─────────────────────────────────────────────────────────── *)
consts
  Permission    :: "Position => bool"
  Duty       :: "Position => bool"
  Right      :: "Position => bool"
  NoRight    :: "Position => bool"
  Power      :: "Position => bool"
  Subj       :: "Position => bool"
  Immunity   :: "Position => bool"
  Disability :: "Position => bool"

consts
  remAct :: "Rule => Action => bool"
(* ── Rule classifiers ───────────────────────────────────────
   Perm / Proh / obl: ODRL rule types
     obl:     ODRL Duty rule (lowercase: distinct from the
              Hohfeldian Duty position above)
   has_rem:   prohibition carries odrl:remedy
              (paper: \hasrem, abbreviation list §5)
   strong:    permission marked as strongly-permitted
              (profile extension point, not in ODRL 2.2 core)
   ─────────────────────────────────────────────────────────── *)
consts
  Perm    :: "Rule => bool"
  Proh    :: "Rule => bool"
  obl     :: "Rule => bool"
  has_rem :: "Rule => bool"
  strong  :: "Rule => bool"

(* ── Relator classifiers ────────────────────────────────────
   Rel:      ρ is a legal relator
             (paper: \mathit{Rel}(\rho) in every relator axiom)
   ODRLRel:  ρ is a relator founded by an ODRL rule activation.
             Required by ax:odrl-rel-typing (Ax5.6) to gate
             correlativity (Ax5.7).  Without this predicate
             correlativity applies to all relators universally,
             which is unsound.
   ─────────────────────────────────────────────────────────── *)
consts
  Rel     :: "LegalRelator => bool"
  ODRLRel :: "LegalRelator => bool"

(* ── Structural relations ───────────────────────────────────
   aee / aer / act / tgt: rule parameters
   activates:  event e activates rule r
               (all constraints of r satisfied at e)
   founds:     Event => LegalRelator => Rule => bool
               TERNARY — paper uses founds(e, ρ, r):
                 e   = activation event
                 ρ   = legal relator founded
                 r   = ODRL rule
               The rule argument is essential:
               two distinct rules activated by the SAME event
               must found TWO distinct relators.
               Binary founds would collapse them to one.
   bearer:     position p is borne by agent x
   cnt:        position p has content (action a, target t)
   partOf:     position p is a mereological part of relator ρ
   ─────────────────────────────────────────────────────────── *)
consts
  aee       :: "Rule => Agent => bool"
  aer       :: "Rule => Agent => bool"
  act       :: "Rule => Action => bool"
  tgt       :: "Rule => Target => bool"
  activates :: "Event => Rule => bool"
  founds    :: "Event => LegalRelator => Rule => bool"
  bearer    :: "Position => Agent => bool"
  cnt       :: "Position => Action => Target => bool"
  partOf    :: "Position => LegalRelator => bool"

(* ── rfr : Action -> Action  (injective, irreflexive) ───────
   Maps a regulated action to its forbearance.
   rfr(a) ≠ a enforces Act/Forbearance sort disjointness
   that UFO-L presupposes but FOF/HOL cannot express as types.
   Prohibitions impose Duty over rfr(a), not a directly.
   ─────────────────────────────────────────────────────────── *)
consts rfr :: "Action => Action"

axiomatization where
  rfr_irreflexive : "ALL a.   rfr a ~= a"       and
  rfr_injective   : "ALL a b. rfr a = rfr b --> a = b"

(* ── decl : Action -> Action  (injective, disjoint from rfr) ─
   Maps a regulated action to the institutional act of
   declaring its violation.
   decl(a) ≠ rfr(a) prevents collapse between
   proh_relator_basic (Duty/Right over rfr(a)) and
   proh_relator_remedy (Power/Subj over decl(a)).
   ─────────────────────────────────────────────────────────── *)
consts decl :: "Action => Action"

axiomatization where
  decl_injective    : "ALL a b. decl a = decl b --> a = b" and
  decl_rfr_disjoint : "ALL a.   decl a ~= rfr a"

(* ── Ax 5.1  Permission Relator — Weak ─────────────────────
   Paper: ax:perm-relator-basic
   Perm(p) activated at e founds a relator ρ containing:
     - Permission  l  borne by assignee x over ⟨a,t⟩
     - NoRight  n  borne by assigner y over ⟨a,t⟩
   NoRight is a surfaced correlative absent from any
   ODRL evaluator output (Table 2, row 2).
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_perm_relator_weak :
    "ALL p x y a t e.
       Perm p & aee p x & aer p y & act p a & tgt p t & activates e p
       -->
       (EX rho l n.
          Rel rho & founds e rho p
          & Permission l & bearer l x & cnt l a t & partOf l rho
          & NoRight n & bearer n y & cnt n a t & partOf n rho)"

(* ── Ax 5.2  Permission Relator — Strong ───────────────────
   Paper: ax:perm-relator-strong
   If Perm(p) is strongly-permitted and already founds ρ,
   that same ρ additionally contains:
     - Immunity   im  borne by assignee x over ⟨a,t⟩
     - Disability db  borne by assigner y over ⟨a,t⟩
   Note: ρ is universally quantified (not existential) —
   the relator is already given by ax_perm_relator_weak;
   this axiom augments it with competence-level positions.
   strong(p) is a profile extension point, not in ODRL 2.2.
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_perm_relator_strong :
    "ALL p x y a t e rho.
       Perm p & strong p & aee p x & aer p y & act p a & tgt p t
       & activates e p & founds e rho p
       -->
       (EX im db.
          Immunity im & bearer im x & cnt im a t & partOf im rho
          & Disability db & bearer db y & cnt db a t & partOf db rho)"
(* ── Ax 5.3  Prohibition Relator — Conduct ─────────────────
    When a Prohibition activates, it founds a fresh relator with:
    Proh(f) activated at e founds a relator ρ containing:
     - Duty borne by assignee over (rfr(a), t)  -- duty to REFRAIN
     - Right borne by assigner over (rfr(a), t)
   Key: cnt takes rfr(a) not a. Prohibitions regulate the
   omission (forbearance), not the act itself.
   Contrast with obl_relator which uses cnt du a t.
   ODRL example:
     ex:proh1 odrl:Prohibition Alice distribute D1
   --> Duty(Alice, rfr(distribute), D1),
       Right(Acme, rfr(distribute), D1) in rho
   Note: content is rfr(a), not a directly.
   rfr(a) ≠ a guaranteed by rfr_irreflexive (Stage 1).
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_proh_relator_conduct :
    "ALL f x y a t e.
       Proh f & aee f x & aer f y & act f a & tgt f t & activates e f
       -->
       (EX rho d c.
          Rel rho & founds e rho f
          & Duty d & bearer d x & cnt d (rfr a) t & partOf d rho
          & Right c & bearer c y & cnt c (rfr a) t & partOf c rho)"
(* ── Ax 5.4  Prohibition Relator — Remedy ──────────────────
   Paper: ax:proh-relator-remedy
   If Proh(f) carries has_rem and already founds ρ,
   that same ρ additionally contains:
     - Power pw  borne by assigner y over ⟨decl(a),t⟩
     - Subj  s   borne by assignee x over ⟨decl(a),t⟩
   Note: ρ is universally quantified — relator already exists
   from ax_proh_relator_conduct; this axiom augments it with
   competence-level positions gated on has_rem(f).
   Content is decl(a), not rfr(a) or a:
     rfr(a)  = duty to refrain       (conduct level, Ax 5.3)
     decl(a) = power to declare viol (competence level, Ax 5.4)
   decl(a) ≠ rfr(a) guaranteed by decl_rfr_disjoint (Stage 1).
   Power constituted at activation, not at violation.
   TIMING: Power is constituted at ACTIVATION, not at violation.
   It is a standing position licensing a future institutional
   act. rho is universally quantified -- EXTENDS existing relator.

   ODRL example:
     ex:proh1 odrl:Prohibition ... odrl:remedy ex:remedy1
   --> Power(Acme, decl(distribute), D1),
       Subj(Alice, decl(distribute), D1) added to rho
   Without rem(f): only proh_relator_basic fires.
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_proh_relator_remedy :
    "ALL f x y a t e rho.
       Proh f & has_rem f & aee f x & aer f y & act f a & tgt f t
       & activates e f & founds e rho f
       -->
       (EX pw s.
          Power pw & bearer pw y & cnt pw (decl a) t & partOf pw rho
          & Subj s  & bearer s  x & cnt s  (decl a) t & partOf s  rho)"
(* ── Ax 5.5  Unique Founding ────────────────────────────────
   Paper: ax:unique-founding
   Two directions, one axiom:
   (1) each (e, r) pair founds at most one relator:
       founds(e,ρ1,r) ∧ founds(e,ρ2,r) → ρ1 = ρ2
   (2) each (ρ, r) pair is founded by at most one event:
       founds(e1,ρ,r) ∧ founds(e2,ρ,r) → e1 = e2
   Together: ρ is individuated by the (e,r) pair — UFO
   principle of particular individuation.
   Distinct rules activated by the same event found
   numerically distinct relators.
      ODRL example:
     Alice requests D1 Monday --> e1 --> rho1
     Alice requests D1 Friday --> e2 --> rho2
   rho1 ~= rho2: Skolem terms are fresh per activation event.
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_unique_founding_relator :
    "ALL r rho1 rho2 e.
       founds e rho1 r & founds e rho2 r
       --> rho1 = rho2"
  and
  ax_unique_founding_event :
    "ALL r e1 e2 rho.
       founds e1 rho r & founds e2 rho r
       --> e1 = e2"
(* ── Ax 5.6  ODRL Relator Typing ───────────────────────────
   Paper: ax:odrl-rel-typing
   Every relator founded by an ODRL rule activation is
   an ODRL relator:
     founds(e,ρ,r) ∧ (Perm(r) ∨ Proh(r) ∨ obl(r)) → ODRLRel(ρ)
   Required to gate ax:correlativity (Ax 5.7):
   without this predicate, correlativity would apply to
   all relators universally, which is unsound.
   Policy π:
  p1 = Permission [ Alice, DataProvider, read, MedicalDB ]
  f1 = Prohibition [ Alice, DataProvider, share, MedicalDB ]

Direction 1 — same rule, two events → two distinct relators
Monday:  Alice satisfies constraints of p1 → activation event e1 → founds e1 rho1 p1
Friday:  Alice satisfies constraints of p1 → activation event e2 → founds e2 rho2 p1

By ax_unique_founding_relator:
  founds e1 rho1 p1  ∧  founds e1 rho2 p1  →  rho1 = rho2   (same event, same rule)
But e1 ≠ e2, so no such collapse occurs.
rho1 ≠ rho2 — Monday's Permission is a distinct particular from Friday's Permission.

Direction 2 — same event, two rules → two distinct relators
Monday:  both p1 and f1 activate simultaneously at e1
  founds e1 rho_p p1   →  rho_p contains Permission(Alice, read,  MedicalDB)
  founds e1 rho_f f1   →  rho_f contains Duty(Alice,  rfr(share), MedicalDB)

By ax_unique_founding_event:
  founds e1 rho p1  ∧  founds e2 rho p1  →  e1 = e2   (same relator, same rule)

rho_p ≠ rho_f — the permission relator and prohibition relator
are numerically distinct even though born at the same moment.
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_odrl_rel_typing :
    "ALL e rho r.
       founds e rho r & (Perm r | Proh r | obl r)
       --> ODRLRel rho"
(* ── Ax 5.7  Obligation Relator ─────────────────────────────
   Paper: ax:obl-relator
   obl(d) activated at e founds a relator ρ containing:
     - Duty  du  borne by assignee x over ⟨a,t⟩
     - Right c   borne by assigner y over ⟨a,t⟩
   Note: content is a directly — duty to perform the action.
   Contrast with ax_proh_relator_conduct where content is
   rfr(a) — duty to refrain from the action.
   Policy π:
  d1 = Duty [ Alice, DataProvider, attributeSource, MedicalDB ]
Activation: constraints satisfied → event e1
founds e1 rho_d d1
rho_d contains:
  Duty  du  bearer=Alice        cnt=(attributeSource, MedicalDB)
  Right c   bearer=DataProvider cnt=(attributeSource, MedicalDB)
  f1 = Prohibition [ Alice, DataProvider, share, MedicalDB ]
  → rho_f: Duty over rfr(share)   ← duty to refrain

  d1 = Duty [ Alice, DataProvider, attributeSource, MedicalDB ]
  → rho_d: Duty over attributeSource  ← duty to perform
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_obl_relator :
    "ALL d x y a t e.
       obl d & aee d x & aer d y & act d a & tgt d t & activates e d
       -->
       (EX rho du c.
          Rel rho & founds e rho d
          & Duty du & bearer du x & cnt du a t & partOf du rho
          & Right c  & bearer c  y & cnt c  a t & partOf c  rho)"
(* ── Ax 5.8  Hohfeldian Correlativity ──────────────────────
   Paper: ax:correlativity
   Each ODRL legal relator ρ contains exactly one position
   from each correlative pair over the same ⟨a,t⟩ content.
   Four biconditionals — one per correlative pair:
     Permission   ↔ NoRight      (conduct)
     Duty      ↔ Right        (conduct)
     Power     ↔ Subj         (competence)
     Immunity  ↔ Disability   (competence)
   EX! = unique existence in Isabelle/HOL.
   Gated on ODRLRel(ρ) — set by ax_odrl_rel_typing (Ax 5.6).
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_correlativity_permission_noright :
    "ALL rho a t.
       ODRLRel rho -->
       ((EX! l. Permission l & partOf l rho & cnt l a t)
        =
        (EX! n. NoRight n & partOf n rho & cnt n a t))"
  and
  ax_correlativity_duty_right :
    "ALL rho a t.
       ODRLRel rho -->
       ((EX! d. Duty d  & partOf d rho & cnt d a t)
        =
        (EX! c. Right c & partOf c rho & cnt c a t))"
  and
  ax_correlativity_power_subj :
    "ALL rho a t.
       ODRLRel rho -->
       ((EX! pw. Power pw & partOf pw rho & cnt pw a t)
        =
        (EX! s.  Subj  s  & partOf s  rho & cnt s  a t))"
  and
  ax_correlativity_immunity_disability :
    "ALL rho a t.
       ODRLRel rho -->
       ((EX! im. Immunity   im & partOf im rho & cnt im a t)
        =
        (EX! db. Disability db & partOf db rho & cnt db a t))"
(* ── Ax 5.9  Cross-Relator Position Disjointness ───────────
   Paper: ax:cross-relator
   Foundational claim grounded in UFO disjointness of
   Permission and Duty as moment types.
   A Permission and a Duty-to-refrain over the same ⟨a,t⟩
   cannot be co-borne by the same agent in any relator:
     Permission(l) ∧ bearer(l,x) ∧ cnt(l,a,t)
     ∧ Duty(d)  ∧ bearer(d,x) ∧ cnt(d,rfr(a),t)
     → ⊥
   Content arguments a and rfr(a) are of distinct types
   (Act and Forbearance); rfr(a) ≠ a enforced by
   rfr_irreflexive (Stage 1).
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_cross_relator :
    "ALL l d x a t.
       Permission l & bearer l x & cnt l a t
       & Duty d  & bearer d x & cnt d (rfr a) t
       --> False"

(* ── Corollary 5.9a  Permission–Duty Conflict Within a Relator ─
   Paper: ax:conflict
   Within-relator instance of ax_cross_relator.
   partOf premises are additional constraints on the same
   antecedent: co-instantiation impossible in any bearer
   regardless of relator membership, hence impossible within
   a single relator in particular.
   Directly applicable to ODRL conflict detection when two
   rules activate under the same policy.
   ─────────────────────────────────────────────────────────── *)
lemma conflict_within_relator :
  "ALL rho l d x a t.
     ODRLRel rho
     & Permission l & bearer l x & cnt l a t & partOf l rho
     & Duty d    & bearer d x & cnt d (rfr a) t & partOf d rho
     --> False"
  using ax_cross_relator by blast
(* ── Ax 5.10  Disability Precludes Prohibition Creation ────
   Paper: ax:disability-block
   No prohibition by y over ⟨a,t⟩ can exist while y holds
   a Disability over that same pair.
   Disability denies y the competence to create such a
   position.
   Constraint axiom: does not generate positions but
   precludes combinations inconsistent with strong
   permission. Required for A to be complete with respect
   to the grounding of thm:strong-crosslevel.
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_disability_block :
    "ALL f x y a t.
       Proh f & aee f x & aer f y & act f a & tgt f t
       --> ~ (EX db. Disability db & bearer db y & cnt db a t)"

(* ── Proposition: Evaluator Faithfulness ───────────────────
   Paper: prop:faithfulness
   Three directions verified mechanically:
   (F1) closed-world permission activation → Permission(x,a,t)
   (F2) prohibition activation → Duty(x,rfr(a),t)
   (F3) prohibition + has_rem activation → Power(y,decl(a),t)
   The converse fails: grounding additionally entails
   NoRight, Right, Immunity, Disability.
   Open-world Permission requires a default axiom — future work.
Example — Ax 5.10
Strong permission:  p1 = Permission+strong [ Alice, DataProvider, read, MedicalDB ]
→ rho_p: Immunity(Alice) + Disability(DataProvider) over ⟨read, MedicalDB⟩

Now DataProvider tries to issue:
  f1 = Prohibition [ Alice, DataProvider, read, MedicalDB ]

ax_disability_block fires:
  Proh(f1) ∧ aer(f1, DataProvider) ∧ act(f1, read) ∧ tgt(f1, MedicalDB)
  → ¬∃db. Disability(db) ∧ bearer(db, DataProvider) ∧ cnt(db, read, MedicalDB)

But Disability(DataProvider, read, MedicalDB) already exists → contradiction.
Prohibition cannot be created. Alice's strong permission is preserved.
   ─────────────────────────────────────────────────────────── *)
lemma faithfulness_F1 :
  "ALL p x y a t e.
     Perm p & aee p x & aer p y & act p a & tgt p t & activates e p
     --> (EX l. Permission l & bearer l x & cnt l a t)"
  using ax_perm_relator_weak by blast

lemma faithfulness_F2 :
  "ALL f x y a t e.
     Proh f & aee f x & aer f y & act f a & tgt f t & activates e f
     --> (EX d. Duty d & bearer d x & cnt d (rfr a) t)"
  using ax_proh_relator_conduct by blast

lemma faithfulness_F3 :
  "ALL f x y a t e.
     Proh f & has_rem f & aee f x & aer f y & act f a & tgt f t
     & activates e f
     --> (EX rho. founds e rho f &
          (EX pw. Power pw & bearer pw y & cnt pw (decl a) t))"
  by (meson ax_proh_relator_conduct ax_proh_relator_remedy)

(* ── Appendix A.2 — Abstract normative position witness ────
   NormPos is the type of abstract normative position tokens
   used in A1--A3 and bridge axioms B1--B3.
   Distinct from Position (Hohfeldian individuals in §5):
     Position  = concrete Hohfeldian moment (Permission, Duty, ...)
     NormPos   = abstract witness for "a normative position
                 comes into or goes out of existence"
   ─────────────────────────────────────────────────────────── *)
typedecl NormPos

(* ── Appendix A.2 — Predicates for A1--A3 and B1--B3 ───────
   NormStateChange x a t q  :  position q over ⟨a,t⟩ changes for x
   InstEvent e              :  e is an institutional event
   triggers e x a t q       :  e triggers the change of q for x
   competentFor y e         :  y is competent to perform e
   aboutEvent pw e          :  Power/Subj pw concerns event e
   does x a t               :  x performs action a on target t
   Duty_rem                 :  abstract token for remedy-duty position
   ─────────────────────────────────────────────────────────── *)
consts
  NormStateChange :: "Agent => Action => Target => NormPos => bool"
  InstEvent       :: "Event => bool"
  triggers        :: "Event => Agent => Action => Target => NormPos => bool"
  competentFor    :: "Agent => Event => bool"
  aboutEvent      :: "Position => Event => bool"
  does            :: "Agent => Action => Target => bool"
  Duty_rem        :: NormPos

(* ── Appendix A.2 — Axiom A1 ───────────────────────────────
   Paper: ax:A1  "NormStateChange requires InstEvent"
   Any normative position q coming into or going out of
   existence for agent x over action a on target t requires
   a triggering institutional event e.
   Motivation: prohibitions are sanctioned (Prop. 3.2) —
   violation activates a remedy duty. A1 forces that
   activation to be grounded in a concrete institutional
   act rather than occurring spontaneously.
   Scope: regulative UFO-L reading only; does not apply
   to constitutive norm activation.
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_A1 :
    "ALL x a t q.
       NormStateChange x a t q
       --> (EX e. InstEvent e & triggers e x a t q)"
(* ── Appendix A.2 — Axiom A2 ───────────────────────────────
   Paper: ax:A2  "InstEvent requires competent agent"
   No institutional event occurs without an agent holding
   the relevant competence to bring it about.
   Note: the paper writes Agent(y) as a FOL predicate.
   In this theory Agent is a type (typedecl Agent), so
   y :: Agent already carries that constraint — the
   predicate is absorbed by the type system and dropped.
   Motivation: chains from A1 — once a normative state
   change requires an institutional event (A1), A2 forces
   that event to be anchored to a responsible agent.
   Together A1--A2 prevent normative changes from arising
   without an identifiable actor.
   Scope: regulative UFO-L reading only.
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_A2 :
    "ALL e.
       InstEvent e
       --> (EX y. competentFor y e)"

(* ── Appendix A.2 — Axiom A3 ───────────────────────────────
   Paper: ax:A3  "Competence is a Power--Subjection pair"
   Competence to perform institutional event e is grounded
   in a Power--Subjection pair: y holds the Power, some x
   holds the correlative Subjection. Both concern e via
   aboutEvent.
   Note: Power and Subj are Hohfeldian position individuals
   (type Position) declared in §5. aboutEvent links them to
   the institutional event, connecting the competence-level
   grounding (A3) back to the relator structure (Ax5.4).
   Motivation: closes the A1--A2--A3 chain —
     A1: normative change requires institutional event
     A2: institutional event requires competent agent
     A3: competence IS a Power--Subjection pair
   Together they force any normative state change to be
   grounded in an explicit competence-level relator structure,
   which is the ontological basis for Theorems 4.1--4.3.
   Scope: regulative UFO-L reading only.
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_A3 :
    "ALL y e.
       competentFor y e
       --> (EX pw s x.
              Power pw & bearer pw y & aboutEvent pw e
              & Subj s  & bearer s  x & aboutEvent s  e)"
(* ── Appendix A.2 — Bridge Axiom B1 ────────────────────────
   Paper: B1  "Violation is a normative state change"
   Performing action a in violation of prohibition f (which
   carries a remedy) constitutes a normative state change:
   the reparative duty over the remedy action b becomes active.
   remAct(f,b): b is the action of the remedy attached to f.
   Duty_rem:    abstract NormPos token for the remedy duty.
   Connects: does (main-body) --> NormStateChange (A1 chain).
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_B1 :
    "ALL f x a t.
       Proh f & has_rem f & act f a & tgt f t & aee f x
       & does x a t
       --> (EX b. remAct f b & NormStateChange x b t Duty_rem)"

(* ── Appendix A.2 — Bridge Axiom B2 ────────────────────────
   Paper: B2  "Power content links to founding event"
   A Power whose content is decl(a) over target t, bundled
   in relator rho founded by event e, concerns event e.
   Connects: partOf + founds (main-body) --> aboutEvent (A3).
   Note: f (the prohibition rule) added to quantifier prefix —
   the paper omits it from ∀ but uses it in founds(e,rho,f);
   universally quantifying f is required for well-formed FOL.
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_B2 :
    "ALL pw a t rho e f.
       Power pw & cnt pw (decl a) t
       & partOf pw rho & founds e rho f
       --> aboutEvent pw e"

(* ── Appendix A.2 — Bridge Axiom B3 ────────────────────────
   Paper: B3  "Subjection content links to founding event"
   A Subjection whose content is decl(a) over target t,
   bundled in relator rho founded by event e, concerns e.
   Connects: partOf + founds (main-body) --> aboutEvent (A3).
   Note: same f-quantifier fix as B2.
   ─────────────────────────────────────────────────────────── *)
axiomatization where
  ax_B3 :
    "ALL s a t rho e f.
       Subj s & cnt s (decl a) t
       & partOf s rho & founds e rho f
       --> aboutEvent s e"
(* ── Proposition prop:sanctioned — Sanctioned direction ────
   Paper: prop:sanctioned (§3)
   ODRL prohibition is SANCTIONED: performing the prohibited
   action triggers normative consequences (NormStateChange).
   This is the consequential direction of sanctioned vs.
   regimented. The non-regimented direction (does x a t is
   consistent with Proh f) is a satisfiability claim confirmed by Vampire GRND008-sanctioned (SZS: Theorem) — it cannot
   be proved as a theorem within this theory.
   Proof: direct chain B1 --> A1.
   ─────────────────────────────────────────────────────────── *)
lemma prop_sanctioned :
  assumes "Proh f" "has_rem f"
          "act f a" "tgt f t" "aee f x"
          "does x a t"
  shows "EX e b. InstEvent e & remAct f b
                 & NormStateChange x b t Duty_rem
                 & triggers e x b t Duty_rem"
proof -
  from assms ax_B1
    obtain b where B: "remAct f b & NormStateChange x b t Duty_rem"
      by blast
  from B ax_A1
    obtain e where E: "InstEvent e & triggers e x b t Duty_rem"
      by blast
  show ?thesis
    using B E by blast
qed

(* ── Proposition prop:weak-complete ────────────────────────
   Paper: prop:weak-complete (§4)
   Weak permission is adequately characterised at conduct
   level by {Permission(x,a,t), NoRight(y,a,t)}.
   No competence-level positions (Power, Immunity, Disability)
   are required.
   Two directions:
   (a) weak perm activation produces Permission + NoRight
       -- direct from ax_perm_relator_weak
   (b) weak perm activation does NOT produce Immunity or
       Disability -- ax_perm_relator_strong requires
       strong(p); without it no competence positions are
       generated. Disability is further blocked from
       coexisting with any prohibition by
       ax_disability_block.
   ─────────────────────────────────────────────────────────── *)

(* Direction (a): Permission and NoRight are entailed *)
lemma prop_weak_complete_conduct :
  assumes "Perm p" "aee p x" "aer p y"
          "act p a" "tgt p t" "activates e p"
  shows "EX rho l n.
           Permission l & bearer l x & cnt l a t & partOf l rho
           & NoRight n & bearer n y & cnt n a t & partOf n rho"
  using assms ax_perm_relator_weak by blast

(* Direction (b): conduct-level pair suffices — no competence
   axiom needed. The proof closes using only
   ax_perm_relator_weak, without invoking ax_perm_relator_strong,
   ax_A1, ax_A2, or ax_A3. *)
lemma prop_weak_complete_no_competence_needed :
  assumes "Perm p" "aee p x" "aer p y"
          "act p a" "tgt p t" "activates e p"
  shows "EX l n.
           Permission l & bearer l x & cnt l a t
           & NoRight n & bearer n y & cnt n a t"
  using assms ax_perm_relator_weak by blast

(* ── Theorem thm:strong-crosslevel ─────────────────────────
   Paper: thm:strong-crosslevel (§4)
   Strong permission is cross-level: no conduct-level
   characterization is adequate.
   Two parts matching the paper proof:
   Part 1 (H1 inadequate): Permission + NoRight alone fails.
     Extending with a prohibition by y adds Duty(x,rfr(a),t)
     via ax_proh_relator_conduct. Then Permission(x,a,t) and
     Duty(x,rfr(a),t) co-exist for same bearer x -- False
     by ax_cross_relator. H1 cannot persist.
   Part 2 (H2 adequate): adding Immunity + Disability
     blocks the prohibition entirely via ax_disability_block.
     Permission(x,a,t) is preserved under any extension.
   ─────────────────────────────────────────────────────────── *)

(* Part 1: H1 = {Permission, NoRight} is inadequate.
   Adding a prohibition by y destroys Permission via
   ax_proh_relator_conduct + ax_cross_relator.           *)
lemma thm_strong_crosslevel_H1_inadequate :
  assumes
    "Permission l" "bearer l x" "cnt l a t"
    "Proh f" "aee f x" "aer f y" "act f a" "tgt f t"
    "activates e f"
  shows "False"
proof -
  from assms ax_proh_relator_conduct
    obtain rho d c where
      D: "Duty d" "bearer d x" "cnt d (rfr a) t"
      by blast
  from assms(1,2,3) D ax_cross_relator
  show ?thesis by blast
qed

(* Part 2: H2 = {Permission, NoRight, Immunity, Disability}
   is adequate. Disability blocks any prohibition by y
   via ax_disability_block, preserving Permission.          *)
lemma thm_strong_crosslevel_H2_adequate :
  assumes
    "Permission l"     "bearer l x"  "cnt l a t"
    "Disability db" "bearer db y" "cnt db a t"
    "Proh f" "aee f x" "aer f y" "act f a" "tgt f t"
  shows "False"
proof -
  from assms ax_disability_block
  have "~ (EX db. Disability db & bearer db y & cnt db a t)"
    by blast
  with assms show ?thesis by blast
qed

(* ── Theorem thm:sanctioned-crosslevel ─────────────────────
   Paper: thm:sanctioned-crosslevel (§4)
   Sanctioned prohibition is cross-level: no conduct-level
   characterization is adequate.
   Part 1 (H3 inadequate): {Duty, Right} alone provides no
     mechanism for the violation-to-remedy transition.
     does(x,a,t) via B1 --> NormStateChange --> A1 requires
     InstEvent --> A2 requires competentFor --> A3 requires
     Power-Subjection pair. H3 contains none. Contradiction.
   Part 2 (H4 adequate): adding Power(y,decl(a),t) and
     Subj(x,decl(a),t) grounds the full chain via B1+A1.
     Part 1: H3 = {Duty, Right} is inadequate.
   violation occurs (B1) --> NormStateChange (A1) -->
   InstEvent --> competentFor (A2) --> Power-Subjection (A3).
   H3 provides no such Power -- contradiction via A3.
   ─────────────────────────────────────────────────────────── *)

   (* ── Theorem thm:sanctioned-crosslevel ─────────────────────
  Part 1: H3 = {Duty, Right} is inadequate.
   violation occurs (B1) --> NormStateChange (A1) -->
   InstEvent --> competentFor (A2) --> Power-Subjection (A3).
   H3 provides no such Power -- contradiction via A3.
   ─────────────────────────────────────────────────────────── *)

lemma thm_sanctioned_crosslevel_H3_inadequate :
  assumes
    "Proh f" "has_rem f"
    "act f a" "tgt f t" "aee f x"
    "does x a t"
    (* H3: conduct only — no Power with aboutEvent *)
    "ALL pw. ~ (Power pw & bearer pw y & aboutEvent pw e')"
    "InstEvent e'"
    "competentFor y e'"
  shows "False"
proof -
  from assms(9) ax_A3
    obtain pw s z where
      PW: "Power pw" "bearer pw y" "aboutEvent pw e'"
      by blast
  from assms(7) PW show ?thesis by blast
qed
  (* ── Theorem thm:sanctioned-crosslevel ─────────────────────
  Part 2: H4 = H3 + {Power, Subj} is adequate.
   Power pw with cnt pw (decl a) t in rho founded by e.
   Full chain: B1 --> A1 both grounded without contradiction. 
   ─────────────────────────────────────────────────────────── *)
lemma thm_sanctioned_crosslevel_H4_adequate :
  assumes
    "Proh f" "has_rem f"
    "act f a" "tgt f t" "aee f x" "aer f y"
    "activates e f" "founds e rho f"
    "does x a t"
    "Power pw" "bearer pw y" "cnt pw (decl a) t" "partOf pw rho"
    "Subj s"   "bearer s x"  "cnt s  (decl a) t" "partOf s  rho"
  shows
    "EX e' b. InstEvent e'
              & remAct f b
              & NormStateChange x b t Duty_rem
              & triggers e' x b t Duty_rem"
proof -
  from assms ax_B1
    obtain b where B1: "remAct f b" "NormStateChange x b t Duty_rem"
      by blast
  from B1(2) ax_A1
    obtain e' where A1: "InstEvent e'" "triggers e' x b t Duty_rem"
      by blast
  show ?thesis
    using B1 A1 by blast
qed

(* ── Theorem thm:crosslevel ─────────────────────────────────
   Paper: thm:crosslevel (§4)
   "Violable Norms Require Both Levels"
   Any norm that is (i) violable and (ii) consequential has
   no adequate characterization using conduct-level positions
   alone.
   Proof strategy:
     consequential norm --> violation activates reparative
     position --> NormStateChange (by definition of
     consequential). By A1: NormStateChange requires
     InstEvent. By A2: InstEvent requires competentFor.
     By A3: competentFor requires Power-Subjection pair.
     Power and Subj are competence-level. Contradiction
     with conduct-only assumption.
   ODRL instance: ODRL prohibition is sanctioned
     (prop:sanctioned) and remedies are normative
     consequences --> theorem applies directly to ODRL.
   ─────────────────────────────────────────────────────────── *)

(* Core: NormStateChange chains through A1-A2-A3 to
   force a Power-Subjection pair into existence.
   Any assumption that only conduct-level positions exist
   is refuted.     
                                           *)
lemma thm_crosslevel :
  assumes
    (* norm is consequential: violation gives NormStateChange *)
    "NormStateChange x a t q"
    (* conduct-only assumption: no Power exists *)
    "ALL pw. ~ (Power pw & bearer pw y & aboutEvent pw e)"
    (* A2 witness: competent agent exists for e *)
    "InstEvent e"
    "competentFor y e"
  shows "False"
proof -
  from assms(4) ax_A3
    obtain pw s z where
      PW: "Power pw" "bearer pw y" "aboutEvent pw e"
      by blast
  from assms(2) PW show ?thesis by blast
qed

(* ODRL instance: applies thm_crosslevel to ODRL prohibition.
   Combines prop:sanctioned (B1 chain) with thm_crosslevel.
   The evaluator implicitly plays the competent authority;
   this lemma makes that explicit.                         *)
lemma thm_crosslevel_odrl_instance :
  assumes
    "Proh f" "has_rem f"
    "act f a" "tgt f t" "aee f x"
    "does x a t"
    "InstEvent e" "competentFor y e"
    "ALL pw. ~ (Power pw & bearer pw y & aboutEvent pw e)"
  shows "False"
proof -
  from assms ax_B1
    obtain b where NSC: "NormStateChange x b t Duty_rem"
      by blast
  from NSC assms(7,8,9) thm_crosslevel
  show ?thesis by blast
qed

(* ══════════════════════════════════════════════════════════════
   Lemma 1: Permission creates Permission
   Paper: prop:faithfulness direction F1
   ══════════════════════════════════════════════════════════════ *)
lemma perm_creates_Permission:
  assumes "Perm p" "aee p x" "aer p y" "act p a" "tgt p t" "activates e p"
  shows "EX rho l. Rel rho & founds e rho p &
                   Permission l & bearer l x & cnt l a t & partOf l rho"
proof -
  from assms ax_perm_relator_weak
  obtain rho l n where
    "Rel rho" "founds e rho p"
    "Permission l" "bearer l x" "cnt l a t" "partOf l rho"
    "NoRight n" "bearer n y" "cnt n a t" "partOf n rho"
    by blast
  thus ?thesis by blast
qed

(* ══════════════════════════════════════════════════════════════
   Lemma 2: Prohibition creates Duty + Right
   Paper: prop:faithfulness direction F2
   ══════════════════════════════════════════════════════════════ *)
lemma proh_creates_duty:
  assumes "Proh f" "aee f x" "aer f y" "act f a" "tgt f t" "activates e f"
  shows "EX rho d c. Rel rho & founds e rho f &
                     Duty d & bearer d x & cnt d (rfr a) t & partOf d rho &
                     Right c & bearer c y & cnt c (rfr a) t & partOf c rho"
proof -
  from assms ax_proh_relator_conduct
  obtain rho d c where
    "Rel rho" "founds e rho f"
    "Duty d"  "bearer d x" "cnt d (rfr a) t" "partOf d rho"
    "Right c" "bearer c y" "cnt c (rfr a) t" "partOf c rho"
    by blast
  thus ?thesis by blast
qed

(* ══════════════════════════════════════════════════════════════
   Lemma 3: Prohibition with remedy creates Power + Subj
   Paper: prop:faithfulness direction F3
   ══════════════════════════════════════════════════════════════ *)
lemma proh_remedy_creates_power:
  assumes "Proh f" "has_rem f"
          "aee f x" "aer f y" "act f a" "tgt f t"
          "activates e f" "founds e rho f"
  shows "EX pw s. Power pw & bearer pw y & cnt pw (decl a) t & partOf pw rho &
                  Subj s  & bearer s  x & cnt s  (decl a) t & partOf s  rho"
proof -
  from assms ax_proh_relator_remedy
  obtain pw s where
    "Power pw" "bearer pw y" "cnt pw (decl a) t" "partOf pw rho"
    "Subj s"   "bearer s  x" "cnt s  (decl a) t" "partOf s  rho"
    by blast
  thus ?thesis by blast
qed

(* ══════════════════════════════════════════════════════════════
   Lemma 4: Disability precludes prohibition creation
   Paper: ax:disability-block consequence / thm:strong-crosslevel
   ══════════════════════════════════════════════════════════════ *)
lemma disability_blocks_proh:
  assumes "Proh f" "aee f x" "aer f y" "act f a" "tgt f t"
          "Disability db" "bearer db y" "cnt db a t"
  shows "False"
proof -
  from assms ax_disability_block
  have "~ (EX db. Disability db & bearer db y & cnt db a t)"
    by blast
  with assms show ?thesis by blast
qed

(* ══════════════════════════════════════════════════════════════
   Lemma 5: Permission-Duty conflict within one relator
   Paper: Corollary ax:conflict / GRND005
   ══════════════════════════════════════════════════════════════ *)
lemma conflict_is_unsat:
  assumes "partOf l rho" "partOf d rho"
          "Permission l" "Duty d"
          "bearer l x" "bearer d x"
          "cnt l a t" "cnt d (rfr a) t"
  shows "False"
  using assms ax_cross_relator by blast

(* ══════════════════════════════════════════════════════════════
   Lemma 5b: Permission-Duty conflict across any relators
   Paper: ax:cross-relator / Appendix A.4 Part 1
   ══════════════════════════════════════════════════════════════ *)
lemma conflict_cross_relator:
  assumes "Permission l" "bearer l x" "cnt l a t"
          "Duty d"    "bearer d x" "cnt d (rfr a) t"
  shows "False"
  using assms ax_cross_relator by blast

(* ══════════════════════════════════════════════════════════════
   Lemma 6a: Immunity + Disability blocks new Duty
   Paper: Appendix A.4 Part 2 intermediate step
   ══════════════════════════════════════════════════════════════ *)
lemma immunity_blocks_duty:
  assumes "Immunity im" "bearer im x" "cnt im a t"
          "Disability db" "bearer db y" "cnt db a t"
          "Proh f" "aee f x" "aer f y" "act f a" "tgt f t"
  shows "False"
  using assms disability_blocks_proh by blast

(* ══════════════════════════════════════════════════════════════
   Lemma 6b: Strong permission persists under model extension
   Paper: thm:strong-crosslevel / Appendix A.4 Part 2
   ══════════════════════════════════════════════════════════════ *)
lemma strong_perm_persists:
  assumes
    "Permission l"     "bearer l x"  "cnt l a t"
    "Immunity im"   "bearer im x" "cnt im a t"
    "Disability db" "bearer db y" "cnt db a t"
    "Proh f" "aee f x" "aer f y" "act f a" "tgt f t"
    "activates e f"
  shows "False"
  using assms disability_blocks_proh by blast

(* ══════════════════════════════════════════════════════════════
   Lemma 7: Violation triggers NormStateChange  (ax_B1)
   Paper: Appendix A.5 Part 1 -- B1 entry point
   ══════════════════════════════════════════════════════════════ *)
lemma violation_triggers_normstate:
  assumes "Proh f" "has_rem f"
          "act f a" "tgt f t" "aee f x"
          "does x a t"
  shows "EX b. remAct f b & NormStateChange x b t Duty_rem"
  using assms ax_B1 by blast

(* ══════════════════════════════════════════════════════════════
   Lemma 7b: NormStateChange requires institutional event (ax_A1)
   Paper: Appendix A.5 Part 1 -- A1 step
   ══════════════════════════════════════════════════════════════ *)
lemma normstate_requires_event:
  assumes "NormStateChange x b t Duty_rem"
  shows "EX e. InstEvent e & triggers e x b t Duty_rem"
  using assms ax_A1 by blast

(* ══════════════════════════════════════════════════════════════
   Lemma 7c: Institutional event requires competent agent (ax_A2)
   Paper: Appendix A.5 Part 1 -- A2 step
   ══════════════════════════════════════════════════════════════ *)
lemma event_requires_competence:
  assumes "InstEvent e"
  shows "EX y. competentFor y e"
  using assms ax_A2 by blast

(* ══════════════════════════════════════════════════════════════
   Lemma 7d: Competence grounded in Power-Subjection (ax_A3)
   Paper: Appendix A.5 Part 1 -- A3 step
   ══════════════════════════════════════════════════════════════ *)
lemma competence_grounds_power:
  assumes "competentFor y e"
  shows "EX pw s x. Power pw & bearer pw y &
                    Subj s   & bearer s  x &
                    aboutEvent pw e & aboutEvent s e"
  using assms ax_A3 by blast

(* ══════════════════════════════════════════════════════════════
   Lemma 8: Full sanctioned-prohibition lifecycle
   Paper: §6 Validation "Lemma 8" — explicitly named
   ══════════════════════════════════════════════════════════════ *)
lemma full_lifecycle:
  assumes
    "Proh f" "has_rem f"
    "aee f x" "aer f y" "act f a" "tgt f t"
    "activates e f" "founds e rho f"
    "does x a t"
  shows
    "(EX d c.
       Duty d  & bearer d x & cnt d (rfr a) t & partOf d rho &
       Right c & bearer c y & cnt c (rfr a) t & partOf c rho) &
    (EX pw s.
       Power pw & bearer pw y & cnt pw (decl a) t & partOf pw rho &
       Subj s   & bearer s  x & cnt s  (decl a) t & partOf s  rho) &
    (EX b. remAct f b & NormStateChange x b t Duty_rem) &
    (EX e' b. InstEvent e' & remAct f b & triggers e' x b t Duty_rem &
              (EX y'. competentFor y' e' &
                      (EX pw' s' x''.
                         Power pw' & bearer pw' y' &
                         Subj s'   & bearer s'  x'' &
                         aboutEvent pw' e' & aboutEvent s' e')))"
proof -
  obtain rho' d c where dc:
    "Rel rho'" "founds e rho' f"
    "Duty d"  "bearer d x" "cnt d (rfr a) t" "partOf d rho'"
    "Right c" "bearer c y" "cnt c (rfr a) t" "partOf c rho'"
    using assms ax_proh_relator_conduct by blast
  have rho_eq: "rho' = rho"
    using dc(2) assms(8) ax_unique_founding_relator by blast
  have dc_rho:
    "Duty d & bearer d x & cnt d (rfr a) t & partOf d rho &
     Right c & bearer c y & cnt c (rfr a) t & partOf c rho"
    using dc rho_eq by simp
  obtain rho'' pw s where ps:
    "founds e rho'' f"
    "Power pw" "bearer pw y" "cnt pw (decl a) t" "partOf pw rho''"
    "Subj s"   "bearer s  x" "cnt s  (decl a) t" "partOf s  rho''"
    using assms ax_proh_relator_remedy by blast
  have rho_eq2: "rho'' = rho"
    using ps(1) assms(8) ax_unique_founding_relator by blast
  have ps_rho:
    "Power pw & bearer pw y & cnt pw (decl a) t & partOf pw rho &
     Subj s & bearer s x & cnt s (decl a) t & partOf s rho"
    using ps rho_eq2 by simp
  obtain b where B:
    "remAct f b" "NormStateChange x b t Duty_rem"
    using assms ax_B1 by blast
  obtain e' where ev:
    "InstEvent e'" "triggers e' x b t Duty_rem"
    using B(2) ax_A1 by blast
  obtain y' where comp: "competentFor y' e'"
    using ev(1) ax_A2 by blast
  obtain pw' s' x'' where psa:
    "Power pw'" "bearer pw' y'"
    "Subj s'"   "bearer s'  x''"
    "aboutEvent pw' e'" "aboutEvent s' e'"
    using comp ax_A3 by blast
  have g1: "EX d c.
      Duty d  & bearer d x & cnt d (rfr a) t & partOf d rho &
      Right c & bearer c y & cnt c (rfr a) t & partOf c rho"
    using dc_rho by blast
  have g2: "EX pw s.
      Power pw & bearer pw y & cnt pw (decl a) t & partOf pw rho &
      Subj s   & bearer s  x & cnt s  (decl a) t & partOf s  rho"
    using ps_rho by blast
  have g3: "EX b. remAct f b & NormStateChange x b t Duty_rem"
    using B by blast
  have g4: "EX e' b. InstEvent e' & remAct f b &
              triggers e' x b t Duty_rem &
              (EX y'. competentFor y' e' &
                      (EX pw' s' x''.
                         Power pw' & bearer pw' y' &
                         Subj s'   & bearer s'  x'' &
                         aboutEvent pw' e' & aboutEvent s' e'))"
    using ev B comp psa by blast
  show ?thesis
    using g1 g2 g3 g4 by blast
qed

(* ══════════════════════════════════════════════════════════════
   Lemma 9: Correlativity uniqueness
   Paper: ax:correlativity (Ax5.8) / GRND006
   Assumes EX! on left side to fire the biconditional.
   ══════════════════════════════════════════════════════════════ *)
lemma permission_unique_noright:
  assumes "ODRLRel rho"
          "EX! l. Permission l & partOf l rho & cnt l a t"
  shows "EX! n. NoRight n & partOf n rho & cnt n a t"
proof -
  from ax_correlativity_permission_noright
  have inst: "ODRLRel rho -->
    ((EX! l. Permission l & partOf l rho & cnt l a t) =
     (EX! n. NoRight n & partOf n rho & cnt n a t))"
    by (elim allE[where x=rho] allE[where x=a] allE[where x=t])
  with assms show ?thesis by simp
qed

lemma duty_unique_right:
  assumes "ODRLRel rho"
          "EX! d. Duty d & partOf d rho & cnt d a t"
  shows "EX! c. Right c & partOf c rho & cnt c a t"
proof -
  from ax_correlativity_duty_right
  have inst: "ODRLRel rho -->
    ((EX! d. Duty d & partOf d rho & cnt d a t) =
     (EX! c. Right c & partOf c rho & cnt c a t))"
    by (elim allE[where x=rho] allE[where x=a] allE[where x=t])
  with assms show ?thesis by simp
qed

lemma power_unique_subj:
  assumes "ODRLRel rho"
          "EX! pw. Power pw & partOf pw rho & cnt pw a t"
  shows "EX! s. Subj s & partOf s rho & cnt s a t"
proof -
  from ax_correlativity_power_subj
  have inst: "ODRLRel rho -->
    ((EX! pw. Power pw & partOf pw rho & cnt pw a t) =
     (EX! s. Subj s & partOf s rho & cnt s a t))"
    by (elim allE[where x=rho] allE[where x=a] allE[where x=t])
  with assms show ?thesis by simp
qed

lemma immunity_unique_disability:
  assumes "ODRLRel rho"
          "EX! im. Immunity im & partOf im rho & cnt im a t"
  shows "EX! db. Disability db & partOf db rho & cnt db a t"
proof -
  from ax_correlativity_immunity_disability
  have inst: "ODRLRel rho -->
    ((EX! im. Immunity im & partOf im rho & cnt im a t) =
     (EX! db. Disability db & partOf db rho & cnt db a t))"
    by (elim allE[where x=rho] allE[where x=a] allE[where x=t])
  with assms show ?thesis by simp
qed
(* ══════════════════════════════════════════════════════════════
   Lemma 10: Unique founding consequences
   Paper: ax:unique-founding (Ax5.5)
   ══════════════════════════════════════════════════════════════ *)
lemma unique_founding_determines_relator:
  assumes "founds e rho1 r" "founds e rho2 r"
  shows "rho1 = rho2"
  using assms ax_unique_founding_relator by blast

lemma two_activations_two_relators:
  assumes "founds e1 rho1 r" "founds e2 rho2 r" "e1 ~= e2"
  shows "rho1 ~= rho2"
proof -
  from assms ax_unique_founding_relator
  have "rho1 = rho2 --> founds e1 rho2 r" by blast
  with assms ax_unique_founding_event
  have "rho1 = rho2 --> e1 = e2" by blast
  with assms show ?thesis by blast
qed

(* ══════════════════════════════════════════════════════════════
   Lemma 11: Grounding strictly richer than ODRL evaluator
   Paper: prop:faithfulness converse / Table 1 rows 2,4,7,8
   ══════════════════════════════════════════════════════════════ *)
lemma grounding_surfaces_noright:
  assumes "Perm p" "aee p x" "aer p y" "act p a" "tgt p t" "activates e p"
  shows "EX rho n. Rel rho & founds e rho p &
                   NoRight n & bearer n y & cnt n a t & partOf n rho"
proof -
  from assms ax_perm_relator_weak
  obtain rho l n where
    "Rel rho" "founds e rho p"
    "Permission l" "bearer l x" "cnt l a t" "partOf l rho"
    "NoRight n" "bearer n y" "cnt n a t" "partOf n rho"
    by blast
  thus ?thesis by blast
qed

lemma grounding_surfaces_right:
  assumes "Proh f" "aee f x" "aer f y" "act f a" "tgt f t" "activates e f"
  shows "EX rho c. Rel rho & founds e rho f &
                   Right c & bearer c y & cnt c (rfr a) t & partOf c rho"
proof -
  from assms ax_proh_relator_conduct
  obtain rho d c where
    "Rel rho" "founds e rho f"
    "Duty d"  "bearer d x" "cnt d (rfr a) t" "partOf d rho"
    "Right c" "bearer c y" "cnt c (rfr a) t" "partOf c rho"
    by blast
  thus ?thesis by blast
qed

lemma grounding_surfaces_immunity:
  assumes "Perm p" "strong p" "aee p x" "aer p y"
          "act p a" "tgt p t" "activates e p" "founds e rho p"
  shows "EX im. Immunity im & bearer im x & cnt im a t & partOf im rho"
proof -
  from assms ax_perm_relator_strong
  obtain im db where
    "Immunity im"   "bearer im x"  "cnt im a t"  "partOf im rho"
    "Disability db" "bearer db y"  "cnt db a t"  "partOf db rho"
    by blast
  thus ?thesis by blast
qed

lemma grounding_surfaces_disability:
  assumes "Perm p" "strong p" "aee p x" "aer p y"
          "act p a" "tgt p t" "activates e p" "founds e rho p"
  shows "EX db. Disability db & bearer db y & cnt db a t & partOf db rho"
proof -
  from assms ax_perm_relator_strong
  obtain im db where
    "Immunity im"   "bearer im x"  "cnt im a t"  "partOf im rho"
    "Disability db" "bearer db y"  "cnt db a t"  "partOf db rho"
    by blast
  thus ?thesis by blast
qed
end