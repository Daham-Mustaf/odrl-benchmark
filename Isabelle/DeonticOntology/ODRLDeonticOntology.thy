theory ODRLDeonticOntology
  imports Main
begin

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


(* ══════════════════════════════════════════════════
   ax:perm-relator-basic
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
   ax:perm-relator-strong

   ODRL example:
     ex:perm2 a odrl:Permission ;
         odrl:assignee    ex:Alice ;
         odrl:assigner    ex:Acme ;
         odrl:action      odrl:read ;
         odrl:target      ex:dataset_D1 ;
         ex:stronglyPermitted true .          -- strong(p)

   When activation event e fires and relator rho already
   exists (founded by ax:perm-relator-basic), this axiom
   adds to rho:
     - Immunity borne by Alice over (read, D1)
         Alice cannot be stripped of this liberty by Acme
     - Disability borne by Acme over (read, D1)
         Acme lacks competence to create a conflicting
         prohibition (ax:disability-block blocks ex:proh1)

   Contrast with basic permission: without strong(p),
   Acme can issue ex:proh1 and override Alice's liberty.
   With strong(p), the Disability makes that impossible.
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
   ax:proh-relator-basic

   ODRL example:
     ex:proh1 a odrl:Prohibition ;
         odrl:assignee ex:Alice ;
         odrl:assigner ex:Acme ;
         odrl:action   odrl:distribute ;
         odrl:target   ex:dataset_D1 .

   When activation event e fires, this axiom creates
   a fresh relator rho containing:
     - Duty borne by Alice over (rfr(distribute), D1)
         Alice has a duty to REFRAIN from distributing
     - Claim borne by Acme over (rfr(distribute), D1)
         Acme has a correlative claim that Alice refrains

   rfr(distribute) is the forbearance: the omission of
   distributing, not the act itself. This is why cnt
   takes rfr(a) not a -- prohibitions regulate omissions,
   not performances.

   Contrast with ax:perm-relator-basic which takes act a
   directly: permissions license the act; prohibitions
   impose a duty on its forbearance.
   ══════════════════════════════════════════════════ *)
axiomatization where
  proh_relator_basic:
  "ALL f x y a t e.
     Proh f & aee f x & aer f y & act f a & tgt f t & activates e f
     --> (EX rho d c.
           isRel rho & founds e rho
         & Duty d & bearer d x & cnt d (rfr a) t & partOf d rho
         & Claim c & bearer c y & cnt c (rfr a) t & partOf c rho)"    

(* ── decl function (injective, disjoint from rfr) ── *)
consts decl :: "Action => Action"
axiomatization where
  decl_injective   : "ALL a b. decl a = decl b --> a = b" and
  decl_rfr_disjoint: "ALL a.   decl a ~= rfr a"

(* ══════════════════════════════════════════════════
   ax:proh-relator-remedy
   Paper: Axiom 5.4

   ODRL example:
     ex:proh1 a odrl:Prohibition ;
         odrl:assignee ex:Alice ;
         odrl:assigner ex:Acme ;
         odrl:action   odrl:distribute ;
         odrl:target   ex:dataset_D1 ;
         odrl:remedy   ex:remedy1 .      -- rem(f) flag

     ex:remedy1 a odrl:Duty ;
         odrl:action odrl:compensate .

   When activation event e fires and relator rho already
   exists (founded by ax:proh-relator-basic), this axiom
   adds to rho:
     - Power borne by Acme over (decl(distribute), D1)
         Acme has standing authority to declare a violation
         if Alice distributes D1 -- licensed BEFORE violation
     - Subj borne by Alice over (decl(distribute), D1)
         Alice is in subjection to that declaration

   Timing: Power is constituted at activation, not at
   violation. If Alice later distributes D1, Acme exercises
   this Power via an institutional act (declareViolation),
   which triggers ex:remedy1 (compensate).

   Without rem(f): ax:proh-relator-basic fires only,
   no Power/Subj created, violation authority unrepresented.
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
   ax:unique-founding
   Paper: Axiom 5.5
   Every legal relator was brought into existence by exactly one activation event — you cannot have two different events both founding the same relator.

   UFO-L basis: a relator is founded by a unique event
   (UFO axiom a77). Two distinct activation events e1, e2
   of the same rule produce TWO distinct relators, not one.

   ODRL example:
     Alice requests dataset D1 on Monday  --> event e1 --> relator rho1
     Alice requests dataset D1 on Friday  --> event e2 --> relator rho2

   rho1 and rho2 are distinct individuals even though they
   arise from the same rule. This axiom enforces the
   contrapositive: if founds(e1, rho) and founds(e2, rho)
   then e1 = e2, i.e. one relator cannot have two founding
   events.

   Consequence for the axiom set: Skolem terms introduced
   by ax:perm-relator-basic, ax:proh-relator-basic, and
   ax:proh-relator-remedy are fresh per activation event,
   consistent with this axiom.
   ══════════════════════════════════════════════════ *)
axiomatization where
  unique_founding:
  "ALL rho e1 e2.
     founds e1 rho & founds e2 rho --> e1 = e2" 

(* ══════════════════════════════════════════════════
   ax:obl-relator
   Paper: Axiom 5.6
   When an ODRL Duty rule is activated, it creates a legal relator bundling a Duty (on the assignee) and a Claim (on the assigner), both concerning performing the action directly.

   ODRL example:
     ex:policy1 a odrl:Agreement ;
         odrl:obligation ex:duty1 .

     ex:duty1 a odrl:Duty ;
         odrl:assignee ex:Alice ;
         odrl:assigner ex:Acme ;
         odrl:action   odrl:compensate ;
         odrl:target   ex:dataset_D1 .

   When activation event e fires, this axiom creates
   a fresh relator rho containing:
     - Duty borne by Alice over (compensate, D1)
         Alice has a duty to PERFORM the act directly
     - Claim borne by Acme over (compensate, D1)
         Acme has a correlative claim that Alice performs

   Key contrast with ax:proh-relator-basic:
     proh_relator_basic : cnt du (rfr a) t  -- duty to REFRAIN
     obl_relator        : cnt du a t        -- duty to PERFORM

   Prohibition imposes duty on the forbearance rfr(a).
   Obligation imposes duty on the act a itself.

   Note: variable du (Hohfeldian Duty position) is distinct
   from d (the ODRL Duty rule) to avoid shadowing.

   ODRL structural roles covered by this axiom:
     odrl:obligation  -- policy-level duty
     odrl:duty        -- permission condition
   Remedy and consequence roles are CTD structures
   handled via ax:proh-relator-remedy.
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
   ax:correlativity
   Paper: Axiom 5.7

   Every Hohfeldian position in a relator has exactly
   one correlative partner in that same relator:
     Liberty  (assignee) <-> NoRight    (assigner)
     Duty     (assignee) <-> Claim      (assigner)
     Power    (assigner) <-> Subj       (assignee)
     Immunity (assignee) <-> Disability (assigner)

   EX! = existence AND uniqueness: not zero, not two.
   Biconditional enforces both directions:
     --> Liberty in rho requires exactly one NoRight
     <-- NoRight in rho requires a Liberty

   Design note: <-- direction matches UFO-L relator
   mereology -- correlatives are co-constituted.
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
   ax:conflict
   Paper: Axiom 5.8
   No relator can simultaneously give the same agent a Liberty to do a AND a Duty to refrain from a on the same target.

   ODRL example — conflict scenario:
     ex:perm1 a odrl:Permission ;
         odrl:assignee ex:Alice ;
         odrl:assigner ex:Acme ;
         odrl:action   odrl:read ;
         odrl:target   ex:dataset_D1 .

     ex:proh1 a odrl:Prohibition ;
         odrl:assignee ex:Alice ;
         odrl:assigner ex:Acme ;
         odrl:action   odrl:read ;
         odrl:target   ex:dataset_D1 .

   ax:perm-relator-basic creates Liberty(Alice, read, D1)
   ax:proh-relator-basic creates Duty(Alice, rfr(read), D1)

   If both land in the same relator rho, this axiom
   fires and derives False -- the policy is inconsistent.

   This is the mechanized conflict detection result:
   Vampire derives False from the combined axiom set +
   the two activation facts, giving SZS status Unsatisfiable.

   Design: rfr(a) on the Duty side is essential.
   Liberty is over act a; Duty is over forbearance rfr(a).
   Without rfr the axiom would not fire -- a Liberty to
   perform and a Duty to perform are not a conflict.
   The conflict is Liberty(a) vs Duty(rfr(a)):
   licensed to act vs obliged to refrain.
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
   ax:disability-block
   Paper: Axiom 5.9
   If y has issued a prohibition over ⟨a, t⟩, then y cannot simultaneously hold a Disability over that same ⟨a, t⟩ — because Disability means y lacks the competence to create that prohibition in the first place.

   ODRL example -- blocked prohibition scenario:
     ex:perm2 a odrl:Permission ;
         odrl:assignee    ex:Alice ;
         odrl:assigner    ex:Acme ;
         odrl:action      odrl:read ;
         odrl:target      ex:dataset_D1 ;
         ex:stronglyPermitted true .

   ax:perm-relator-strong adds to rho:
     Disability(Acme, read, D1)  -- Acme cannot revoke

   Now Acme tries to issue:
     ex:proh1 a odrl:Prohibition ;
         odrl:assigner ex:Acme ;
         odrl:assignee ex:Alice ;
         odrl:action   odrl:read ;
         odrl:target   ex:dataset_D1 .

   This axiom fires: Proh(proh1) & aer(proh1, Acme)
   & Disability(Acme, read, D1) --> False.
   The prohibition cannot coexist -- blocked.

   Contrast with ax:conflict which detects conflict
   between positions inside a relator. This axiom
   blocks the prohibition from being created at all:
     ax:conflict      -- detects post-hoc inconsistency
     ax:disability-block -- prevents creation up front

   This is the mechanized proof of
   Theorem 4.1 (Strong Permission is Cross-Level):
   the Disability makes the conduct-only characterization
   inadequate by blocking any overriding prohibition.
   ══════════════════════════════════════════════════ *)
axiomatization where
  disability_block:
  "ALL f x y a t.
     Proh f & aee f x & aer f y & act f a & tgt f t
     --> ~(EX db. Disability db & bearer db y & cnt db a t)"

(* ══════════════════════════════════════════════════
   A.0 — Appendix predicates (A1–A3 + bridges B1–B3)
   Paper: Appendix A.0

   These predicates and axioms underlie the cross-level
   design principle (Section 4 / Theorems 4.1-4.3).
   They do not appear in the main-body axioms but are
   imported into the TPTP/FOF and SMT-LIB encodings.

   New sort:
     NormPos -- normative position token (witness type)

   New predicates:
     NormStateChange(x,a,t,q) -- position q changes for x
     InstEvent(e)             -- e is an institutional event
     triggers(e,x,a,t,q)     -- e triggers change of q
     competentFor(y,e)        -- y is competent to perform e
     aboutEvent(pw,e)         -- Power/Subj pw concerns e
     does(x,a,t)              -- x performs a on t
     Duty_rem                 -- witness token for remedy-duty
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

(* ══════════════════════════════════════════════════
   A1: Normative State Changes Require an
       Institutional Event

   ODRL example:
     ex:proh1 a odrl:Prohibition ;
         odrl:assignee ex:Alice ;
         odrl:assigner ex:Acme ;
         odrl:action   odrl:distribute ;
         odrl:target   ex:dataset_D1 ;
         odrl:remedy   ex:remedy1 .

   Alice distributes D1 despite the prohibition.
   This is a normative state change: the remedy duty
   ex:remedy1 must now become active.

   A1 says: this change cannot happen spontaneously.
   It requires a triggering institutional event e --
   specifically, Acme performing the act of declaring
   the violation (declareViolation).

   Without A1: the remedy just activates automatically,
   with no agent responsible for triggering it.
   With A1: an institutional event is required, forcing
   us to ask WHO triggers it and HOW -- answered by A2-A3.

   This is why ODRL's evaluator implicitly plays the
   role of normative authority: it performs the
   institutional act A1 requires.
   ══════════════════════════════════════════════════ *)
axiomatization where
  A1:
  "ALL x a t q.
     NormStateChange x a t q
     --> (EX e. InstEvent e & triggers e x a t q)"

(* ══════════════════════════════════════════════════
   A2: Institutional Events Require a Competent Agent

   ODRL example (continuing from A1):
   The institutional event e = declareViolation(Alice,
   distribute, D1) cannot occur in a vacuum.

   A2 says: some agent y must be competentFor(y, e).
   In the ODRL scenario, y = Acme (the assigner).
   Acme is the party competent to declare that Alice
   has violated the prohibition.

   Without A2: institutional events float free --
   no agent is accountable for normative state changes.
   With A2: the evaluator's implicit authority is made
   explicit -- there must be an agent who holds the
   competence to trigger this change.

   In multi-party data spaces this matters: if Acme
   and BetaCorp both prohibit distribute, A2 forces
   the question of which party is competent to declare
   Alice's violation -- they cannot both be without
   explicit delegation.
   ══════════════════════════════════════════════════ *)
and A2:
  "ALL e.
     InstEvent e
     --> (EX y. competentFor y e)"

(* ══════════════════════════════════════════════════
   A3: Competence Is a Power-Subjection Pair

   ODRL example (continuing from A2):
   Acme is competentFor(Acme, declareViolation_e).

   A3 says: this competence is not a primitive --
   it is grounded in a Power-Subjection pair:
     Power(pw)  bearer=Acme  aboutEvent=e
     Subj(s)    bearer=Alice aboutEvent=e

   This Power is exactly what ax:proh-relator-remedy
   creates at activation time (before any violation).
   A3 connects the abstract competence claim (A2) to
   the concrete relator structure (main-body axioms).

   Without A3: competence is an ungrounded primitive --
   we know someone is competent but not what that means
   ontologically.
   With A3: the Power-Subjection pair in relator rho
   IS the competence. The evaluator's authority is now
   a first-class ontological entity, not a black box.

   This is the key step in the proof of
   Theorem 4.2 (Sanctioned Prohibition is Cross-Level):
   conduct-level positions alone cannot provide this
   Power-Subjection pair.
   ══════════════════════════════════════════════════ *)
and A3:
  "ALL y e.
     competentFor y e
     --> (EX pw s x.
           Power pw & bearer pw y &
           Subj s   & bearer s  x &
           aboutEvent pw e & aboutEvent s e)"

(* ══════════════════════════════════════════════════
   B1: Performing a Prohibited Action Is a
       NormStateChange (bridge to A1)

   ODRL example:
     ex:proh1 a odrl:Prohibition ;
         odrl:assignee ex:Alice ;
         odrl:assigner ex:Acme ;
         odrl:action   odrl:distribute ;
         odrl:target   ex:dataset_D1 ;
         odrl:remedy   ex:remedy1 .     -- rem(f)

   Alice performs does(Alice, distribute, D1).
   The prohibition carries a remedy (rem f).

   B1 fires: this performance IS a NormStateChange --
   specifically, it activates the remedy duty Duty_rem.

   This is the bridge between:
     - the operational layer (Alice did the act)
     - the normative layer (a state change occurred)
   ...which A1 then requires to be triggered by an
   institutional event.

   Without B1: A1 never fires for ODRL violations --
   NormStateChange would never be instantiated.
   B1 is the entry point connecting ODRL's does()
   predicate to the A1-A2-A3 chain.
   ══════════════════════════════════════════════════ *)
and B1:
  "ALL f x a t b.
     Proh f & rem f & act f a & tgt f t & aee f x &
     does x a t
     --> NormStateChange x b t Duty_rem"

(* ══════════════════════════════════════════════════
   B2: Power Content Links to Founding Event
       (bridge from relator structure to aboutEvent)

   ODRL example:
     ax:proh-relator-remedy created:
       Power(pw) bearer=Acme cnt=(decl(distribute), D1)
       partOf pw rho
       founds e rho      -- e is the activation event

   B2 says: this Power concerns event e.
   I.e. aboutEvent(pw, e) holds.

   This is needed for A3 to fire: A3 requires
   aboutEvent(pw, e) to connect the Power in the
   relator to the institutional event in A1-A2.

   Without B2: the Power created by proh_relator_remedy
   and the Power required by A3 are never identified --
   the proof chain from B1 through A1-A2-A3 breaks.
   B2 closes the gap between the relator mereology
   (partOf, founds) and the event structure (aboutEvent).
   ══════════════════════════════════════════════════ *)
and B2:
  "ALL pw a t rho e.
     Power pw & cnt pw (decl a) t &
     partOf pw rho & founds e rho
     --> aboutEvent pw e"

(* ══════════════════════════════════════════════════
   B3: Subjection Content Links to Founding Event
       (bridge from relator structure to aboutEvent)

   ODRL example (mirror of B2):
     ax:proh-relator-remedy also created:
       Subj(s) bearer=Alice cnt=(decl(distribute), D1)
       partOf s rho
       founds e rho

   B3 says: this Subjection also concerns event e.
   I.e. aboutEvent(s, e) holds.

   Required by A3: the Subjection correlative of the
   Power must also be linked to the same event e,
   confirming that Alice is in subjection to exactly
   the institutional event that Acme is competent to
   perform.

   Together B2 and B3 ensure the Power-Subjection pair
   in the relator is the same pair that A3 identifies
   as grounding Acme's competence. Without both bridges,
   A3 could introduce a fresh unrelated Power-Subjection
   pair disconnected from the ODRL policy structure.
   ══════════════════════════════════════════════════ *)
and B3:
  "ALL s a t rho e.
     Subj s & cnt s (decl a) t &
     partOf s rho & founds e rho
     --> aboutEvent s e"    
end