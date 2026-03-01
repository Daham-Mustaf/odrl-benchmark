theory ODRL_Scenarios imports Main begin

(* ================================================================= *)
(* Core verdict machinery (minimal, from ODRL_Grounding.thy)         *)
(* ================================================================= *)

datatype 'c denotation = Classical "'c set" | Top

datatype verdict = Conflict | Compatible | Unknown

fun verdict_of :: "'c denotation \<Rightarrow> 'c denotation \<Rightarrow> verdict" where
  "verdict_of (Classical s1) (Classical s2) =
     (if s1 \<inter> s2 = {} then Conflict else Compatible)"
| "verdict_of _ _ = Unknown"

fun verdict_and :: "verdict list \<Rightarrow> verdict" where
  "verdict_and vs =
    (if Conflict \<in> set vs then Conflict
     else if \<forall>v \<in> set vs. v = Compatible then Compatible
     else Unknown)"

definition satisfies :: "'c \<Rightarrow> 'c denotation \<Rightarrow> bool" where
  "satisfies val d = (case d of Top \<Rightarrow> True | Classical s \<Rightarrow> val \<in> s)"


(* ================================================================= *)
(* SCENARIO 1: Permission vs Prohibition (cross-rule conflict)       *)
(* ================================================================= *)

(* 
   Policy A — Permission:
   {
     "@type": "odrl:Permission",
     "odrl:action": "odrl:use",
     "odrl:constraint": {
       "odrl:leftOperand": "odrl:purpose",
       "odrl:operator": "odrl:isA",
       "odrl:rightOperand": "dpv:ServiceProvision"
     }
   }

   Policy B — Prohibition:
   {
     "@type": "odrl:Prohibition",
     "odrl:action": "odrl:use",
     "odrl:constraint": {
       "odrl:leftOperand": "odrl:purpose",
       "odrl:operator": "odrl:isA",
       "odrl:rightOperand": "dpv:AcademicResearch"
     }
   }

   Question: Do these two rules conflict?

   KB_purpose (DPV):
     dpv:Purpose
       \<ge> dpv:ServiceProvision
       |     \<ge> dpv:Marketing
       \<ge> dpv:AcademicResearch
             \<ge> dpv:ScientificResearch

   c1 = (purpose, isA, dpv:ServiceProvision)
   c2 = (purpose, isA, dpv:AcademicResearch)

   \<gamma>(dpv:ServiceProvision) = ServiceProvision   \<checkmark>
   \<gamma>(dpv:AcademicResearch) = AcademicResearch   \<checkmark>

   \<llbracket>c1\<rrbracket> = {x \<in> C | x \<le> ServiceProvision} = {ServiceProvision, Marketing}
   \<llbracket>c2\<rrbracket> = {x \<in> C | x \<le> AcademicResearch} = {AcademicResearch, ScientificResearch}
*)

(* Step 1: Denotations have empty intersection *)
lemma scenario1_sets:
  "{ServiceProvision, Marketing} 
 \<inter> {AcademicResearch, ScientificResearch} = {}"
  by simp

(* Step 2: Therefore verdict is Conflict *)
lemma scenario1_verdict:
  "verdict_of 
     (Classical {ServiceProvision, Marketing}) 
     (Classical {AcademicResearch, ScientificResearch}) 
   = Conflict"
  by simp

(* Meaning: A permission for commercial use and a prohibition
   for academic use do NOT conflict — they govern different 
   purposes. Wait — that's Compatible, not Conflict!

   Actually let's check: the PERMISSION says "use is allowed 
   when purpose isA ServiceProvision." The PROHIBITION says 
   "use is forbidden when purpose isA AcademicResearch."

   These constrain DIFFERENT purposes. No purpose value falls
   in both sets. So a request for Marketing satisfies the 
   permission but not the prohibition. No contradiction.

   The Conflict verdict means: no single purpose value can
   simultaneously be ServiceProvision-or-below AND 
   AcademicResearch-or-below. This is correct.

   For a TRUE cross-rule conflict, both must constrain the
   SAME values:
*)

(* 
   Permission: (purpose, isA, dpv:ServiceProvision)
   Prohibition: (purpose, isA, dpv:ServiceProvision)
   Same constraint, opposite deontic → real policy conflict!
*)

lemma scenario1_real_conflict:
  "verdict_of 
     (Classical {ServiceProvision, Marketing}) 
     (Classical {ServiceProvision, Marketing}) 
   = Compatible"
  by simp

(* Compatible! Because the denotations overlap (they're identical).
   This means: there EXISTS a purpose value (e.g. Marketing) that
   is simultaneously permitted and prohibited. THAT is the real
   conflict — detected by Compatible denotations under opposite
   deontic operators. *)


(* ================================================================= *)
(* SCENARIO 2: Intra-policy self-contradiction                       *)
(* ================================================================= *)

(*
   One policy with two constraints joined by AND:
   {
     "@type": "odrl:Permission",
     "odrl:action": "odrl:use",
     "odrl:constraint": [
       {
         "odrl:leftOperand": "odrl:purpose",
         "odrl:operator": "odrl:isA",
         "odrl:rightOperand": "dpv:ServiceProvision"
       },
       {
         "odrl:leftOperand": "odrl:purpose",
         "odrl:operator": "odrl:isA",
         "odrl:rightOperand": "dpv:AcademicResearch"
       }
     ],
     "odrl:operand": "odrl:and"
   }

   This says: "allow use when purpose is BOTH commercial 
   AND academic simultaneously."

   c1 = (purpose, isA, dpv:ServiceProvision)
   c2 = (purpose, isA, dpv:AcademicResearch)
   composition: and

   \<llbracket>c1\<rrbracket> = {ServiceProvision, Marketing}
   \<llbracket>c2\<rrbracket> = {AcademicResearch, ScientificResearch}
*)

(* Step 1: Per-operand verdict *)
lemma scenario2_per_operand:
  "verdict_of 
     (Classical {ServiceProvision, Marketing}) 
     (Classical {AcademicResearch, ScientificResearch}) 
   = Conflict"
  by simp

(* Step 2: Composition under AND *)
lemma scenario2_composition:
  "verdict_and [Conflict] = Conflict"
  by simp

(* The policy is self-contradictory. No request can ever 
   satisfy it. The administrator should fix the policy 
   before publishing it. This is caught at authoring time. *)

(* A multi-operand example: purpose conflicts but spatial is fine *)
(*
   constraint1: (purpose, isA, dpv:ServiceProvision)
   constraint2: (purpose, isA, dpv:AcademicResearch)
   constraint3: (spatial, isPartOf, gn:France)
   constraint4: (spatial, isPartOf, gn:Europe)
   composition: and

   Purpose: Conflict (no overlap)
   Spatial: Compatible (France \<subseteq> Europe)
   verdict_and [Conflict, Compatible] = Conflict
*)

lemma scenario2_multi_operand:
  "verdict_and [Conflict, Compatible] = Conflict"
  by simp

(* One Conflict in AND is enough — the whole policy fails. *)


(* ================================================================= *)
(* SCENARIO 3: Policy vs Request (runtime satisfaction)              *)
(* ================================================================= *)

(*
   Policy constraint:
   {
     "odrl:leftOperand": "odrl:purpose",
     "odrl:operator": "odrl:isA",
     "odrl:rightOperand": "dpv:ServiceProvision"
   }

   c = (purpose, isA, dpv:ServiceProvision)
   \<llbracket>c\<rrbracket> = {ServiceProvision, Marketing}

   Now requests arrive at runtime:

   Request 1: \<omega>(purpose) = dpv:Marketing
   \<gamma>(dpv:Marketing) = Marketing
   Marketing \<in> {ServiceProvision, Marketing}?

   Request 2: \<omega>(purpose) = dpv:ScientificResearch
   \<gamma>(dpv:ScientificResearch) = ScientificResearch
   ScientificResearch \<in> {ServiceProvision, Marketing}?
*)

(* Request 1: Marketing satisfies the constraint *)
lemma scenario3_request1:
  "satisfies Marketing (Classical {ServiceProvision, Marketing})"
  by (simp add: satisfies_def)

(* Request 2: ScientificResearch does NOT satisfy *)
lemma scenario3_request2:
  "\<not> satisfies ScientificResearch (Classical {ServiceProvision, Marketing})"
  by (simp add: satisfies_def)

(* What if the constraint has ungrounded value? ⟦c⟧ = Top *)
(* Top is permissive: any grounded value satisfies *)
lemma scenario3_top_permissive:
  "satisfies AnyValue Top"
  by (simp add: satisfies_def)


(* ================================================================= *)
(* THE KEY BRIDGE: Theorem 3 (Runtime Soundness)                     *)
(* Static Conflict \<longrightarrow> no request can satisfy both               *)
(* ================================================================= *)

(*
   Permission:  c1 = (purpose, isA, dpv:ServiceProvision)
   Prohibition: c2 = (purpose, isA, dpv:AcademicResearch)

   \<llbracket>c1\<rrbracket> = {ServiceProvision, Marketing}
   \<llbracket>c2\<rrbracket> = {AcademicResearch, ScientificResearch}

   Static analysis says: Conflict.
   Runtime guarantee: no request value can satisfy both.
*)

lemma runtime_soundness_example:
  assumes "verdict_of (Classical s1) (Classical s2) = Conflict"
  shows "\<not>(\<exists>val. satisfies val (Classical s1) \<and> satisfies val (Classical s2))"
proof -
  from assms have "s1 \<inter> s2 = {}" by (simp split: if_splits)
  then show ?thesis by (auto simp: satisfies_def)
qed

(* Concrete instance *)
lemma runtime_soundness_concrete:
  "\<not>(\<exists>val. satisfies val (Classical {ServiceProvision, Marketing}) 
         \<and> satisfies val (Classical {AcademicResearch, ScientificResearch}))"
  by (auto simp: satisfies_def)

(* This is why static analysis works: you don't need to wait 
   for requests. Check policies at authoring time. If Conflict,
   no data use can ever satisfy both. Guaranteed. *)

end
