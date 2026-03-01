theory ODRL_Analysis_Modes imports Main begin

(* ================================================================= *)
(* Core machinery (from ODRL_Grounding.thy)                          *)
(* ================================================================= *)

datatype 'c denotation = Classical "'c set" | Top
datatype verdict = Conflict | Compatible | Unknown
datatype subsum_verdict = Confirmed | Refuted | SubUnknown

fun verdict_of :: "'c denotation \<Rightarrow> 'c denotation \<Rightarrow> verdict" where
  "verdict_of (Classical s1) (Classical s2) =
     (if s1 \<inter> s2 = {} then Conflict else Compatible)"
| "verdict_of _ _ = Unknown"

fun verdict_and :: "verdict list \<Rightarrow> verdict" where
  "verdict_and vs =
    (if Conflict \<in> set vs then Conflict
     else if \<forall>v \<in> set vs. v = Compatible then Compatible
     else Unknown)"

fun subsumption_verdict :: "'c denotation \<Rightarrow> 'c denotation \<Rightarrow> subsum_verdict" where
  "subsumption_verdict (Classical s1) (Classical s2) =
     (if s1 \<subseteq> s2 then Confirmed else Refuted)"
| "subsumption_verdict _ _ = SubUnknown"


(* ================================================================= *)
(* MODE 1: INTRA-POLICY SELF-CONTRADICTION                           *)
(* "Can this policy ever be satisfied?"                              *)
(* ================================================================= *)

(*
  A museum publishes this ODRL policy:
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

  The author intended: "allow use for commercial OR academic."
  But wrote AND instead of OR.
  
  This policy requires a SINGLE purpose value to be BOTH 
  commercial AND academic simultaneously.

  KB_purpose (DPV):
    dpv:Purpose
      \<ge> dpv:ServiceProvision  \<ge> dpv:Marketing
      \<ge> dpv:AcademicResearch  \<ge> dpv:ScientificResearch
    ServiceProvision \<bottom> AcademicResearch (disjoint branches)

  c1 = (purpose, isA, dpv:ServiceProvision)
  \<llbracket>c1\<rrbracket> = {ServiceProvision, Marketing}

  c2 = (purpose, isA, dpv:AcademicResearch)
  \<llbracket>c2\<rrbracket> = {AcademicResearch, ScientificResearch}

  Same operand (purpose), two constraints, AND composition.
*)

(* Step 1: per-operand verdict on purpose *)
lemma selfcon_purpose_verdict:
  "verdict_of 
     (Classical {ServiceProvision, Marketing}) 
     (Classical {AcademicResearch, ScientificResearch}) 
   = Conflict"
  by simp

(* Step 2: AND composition — one Conflict kills the policy *)
lemma selfcon_and_verdict:
  "verdict_and [Conflict] = Conflict"
  by simp

(* Result: This policy is UNSATISFIABLE.
   No request can ever trigger this permission.
   The administrator is told at authoring time:
   "Your policy can never be satisfied — did you mean OR?" *)


(* A more complex self-contradiction: two operands, one conflicts *)
(*
  Permission:
    constraint1: (purpose, isA, dpv:ServiceProvision)
    constraint2: (purpose, isA, dpv:AcademicResearch)
    constraint3: (spatial, isPartOf, gn:Europe)
    constraint4: (spatial, isPartOf, gn:France)
    composition: and

  Purpose: Conflict (disjoint branches)
  Spatial: Compatible (France \<subseteq> Europe)
  verdict_and: one Conflict present \<longrightarrow> Conflict
*)

lemma selfcon_multi_operand:
  "verdict_and [Conflict, Compatible] = Conflict"
  by simp

(* Even though spatial is fine, purpose kills the whole policy. *)


(* A policy that is NOT self-contradictory *)
(*
  Permission:
    constraint1: (purpose, isA, dpv:ServiceProvision)
    constraint2: (spatial, isPartOf, gn:France)
    composition: and

  Different operands \<longrightarrow> operand independence \<longrightarrow> no conflict.
  verdict_and [Compatible] would only arise if same-operand 
  constraints conflict. Here there are none, so no self-contradiction.
  A request for (Marketing, Paris) satisfies both. \<checkmark>
*)


(* ================================================================= *)
(* MODE 2: CONSTRAINT REDUNDANCY                                     *)
(* "Is this constraint already implied by another?"                  *)
(* ================================================================= *)

(*
  A policy has two spatial constraints:
  {
    "odrl:constraint": [
      {
        "odrl:leftOperand": "odrl:spatial",
        "odrl:operator": "odrl:isPartOf",
        "odrl:rightOperand": "gn:Europe"
      },
      {
        "odrl:leftOperand": "odrl:spatial",
        "odrl:operator": "odrl:isPartOf",
        "odrl:rightOperand": "gn:France"
      }
    ],
    "odrl:operand": "odrl:and"
  }

  KB_spatial (GeoNames):
    gn:Europe \<ge> gn:France \<ge> gn:Paris \<ge> ...
    gn:Europe \<ge> gn:Germany \<ge> gn:Berlin \<ge> ...

  c1 = (spatial, isPartOf, gn:France)
  \<llbracket>c1\<rrbracket> = {France, Paris, Lyon}

  c2 = (spatial, isPartOf, gn:Europe)
  \<llbracket>c2\<rrbracket> = {Europe, France, Paris, Lyon, Germany, Berlin}

  Question: Is c2 redundant given c1?
  \<llbracket>c1\<rrbracket> \<subseteq> \<llbracket>c2\<rrbracket>? 
  {France, Paris, Lyon} \<subseteq> {Europe, France, Paris, Lyon, Germany, Berlin}?
  YES \<longrightarrow> c1 \<sqsubseteq>_c c2 (c1 refines c2)
  
  Meaning: anything satisfying "isPartOf France" automatically 
  satisfies "isPartOf Europe." Under AND, the Europe constraint 
  is redundant — it can be removed without changing behavior.
*)

lemma redundancy_spatial:
  "subsumption_verdict 
     (Classical {France, Paris, Lyon}) 
     (Classical {Europe, France, Paris, Lyon, Germany, Berlin}) 
   = Confirmed"
  by simp

(* c1 \<sqsubseteq>_c c2: France refines Europe.
   The Europe constraint adds nothing under AND.
   Administrator can simplify the policy. *)


(* The reverse: is the France constraint redundant given Europe? *)
lemma not_redundant_reverse:
  "subsumption_verdict 
     (Classical {Europe, France, Paris, Lyon, Germany, Berlin}) 
     (Classical {France, Paris, Lyon}) 
   = Refuted"
  by simp

(* No! Europe does NOT refine France. Germany is in Europe but 
   not in France. The France constraint is the restrictive one. *)


(* Purpose example: is ScientificResearch redundant given Research? *)
(*
  KB_purpose (DPV):
    dpv:ResearchAndDevelopment
      \<ge> dpv:ScientificResearch
      \<ge> dpv:CommercialResearch

  c3 = (purpose, isA, dpv:ScientificResearch)
  \<llbracket>c3\<rrbracket> = {ScientificResearch}

  c4 = (purpose, isA, dpv:ResearchAndDevelopment)
  \<llbracket>c4\<rrbracket> = {ResearchAndDevelopment, ScientificResearch, CommercialResearch}

  \<llbracket>c3\<rrbracket> \<subseteq> \<llbracket>c4\<rrbracket>? YES.
*)

lemma redundancy_purpose:
  "subsumption_verdict 
     (Classical {ScientificResearch}) 
     (Classical {ResearchAndDevelopment, ScientificResearch, CommercialResearch}) 
   = Confirmed"
  by simp

(* ScientificResearch refines ResearchAndDevelopment.
   Under AND, the broader constraint is redundant. *)


(* Language: eq German vs isA Germanic *)
(*
  c5 = (language, eq, deu)        \<llbracket>c5\<rrbracket> = {German}
  c6 = (language, isA, Germanic)  \<llbracket>c6\<rrbracket> = {Germanic, German, English}
  
  {German} \<subseteq> {Germanic, German, English}? YES.
  eq German refines isA Germanic.
*)

lemma redundancy_language:
  "subsumption_verdict 
     (Classical {German}) 
     (Classical {Germanic, German, English}) 
   = Confirmed"
  by simp


(* ================================================================= *)
(* MODE 3: POLICY REFINEMENT VERIFICATION                            *)
(* "Does downstream validly restrict upstream?"                      *)
(* ================================================================= *)

(*
  DSSC blueprint: data flows through a supply chain.
  Each intermediary can RESTRICT but never WEAKEN the policy.
  
  Upstream policy: 
    (purpose, isA, dpv:ResearchAndDevelopment)
    "Data may be used for any research purpose"
    \<llbracket>upstream\<rrbracket> = {ResearchAndDevelopment, ScientificResearch, CommercialResearch}

  Downstream policy A (valid refinement):
    (purpose, isA, dpv:ScientificResearch)
    "Data may be used for scientific research only"
    \<llbracket>downstream_A\<rrbracket> = {ScientificResearch}

  Question: Is downstream_A a valid refinement of upstream?
  \<llbracket>downstream_A\<rrbracket> \<subseteq> \<llbracket>upstream\<rrbracket>?
*)

lemma refinement_valid:
  "subsumption_verdict 
     (Classical {ScientificResearch}) 
     (Classical {ResearchAndDevelopment, ScientificResearch, CommercialResearch}) 
   = Confirmed"
  by simp

(* YES. ScientificResearch \<sqsubseteq>_c ResearchAndDevelopment.
   Downstream only allows a subset of what upstream allows.
   This is a valid restriction. DSSC compliant. \<checkmark> *)


(*
  Downstream policy B (INVALID — widens scope):
    (purpose, isA, dpv:ServiceProvision)
    "Data may be used for commercial services"
    \<llbracket>downstream_B\<rrbracket> = {ServiceProvision, Marketing}

  \<llbracket>downstream_B\<rrbracket> \<subseteq> \<llbracket>upstream\<rrbracket>?
  {ServiceProvision, Marketing} \<subseteq> {ResearchAndDevelopment, ScientificResearch, CommercialResearch}?
*)

lemma refinement_invalid:
  "subsumption_verdict 
     (Classical {ServiceProvision, Marketing}) 
     (Classical {ResearchAndDevelopment, ScientificResearch, CommercialResearch}) 
   = Refuted"
  by simp

(* NO. ServiceProvision is NOT a subconcept of ResearchAndDevelopment.
   Downstream allows uses (Marketing) that upstream does not.
   This VIOLATES the supply chain restriction.
   The administrator is told: "Policy B widens scope — rejected." *)


(*
  Downstream policy C (valid — restricts spatially):
  
  Upstream: (spatial, isPartOf, gn:Europe)
  \<llbracket>upstream_spatial\<rrbracket> = {Europe, France, Paris, Lyon, Germany, Berlin}

  Downstream: (spatial, isPartOf, gn:France)
  \<llbracket>downstream_spatial\<rrbracket> = {France, Paris, Lyon}
*)

lemma refinement_spatial_valid:
  "subsumption_verdict 
     (Classical {France, Paris, Lyon}) 
     (Classical {Europe, France, Paris, Lyon, Germany, Berlin}) 
   = Confirmed"
  by simp

(* France \<sqsubseteq>_c Europe. 
   Downstream restricts from all of Europe to only France.
   Valid refinement. \<checkmark> *)


(*
  Downstream policy D (INVALID — widens spatially):

  Upstream: (spatial, isPartOf, gn:France)
  \<llbracket>upstream_fr\<rrbracket> = {France, Paris, Lyon}

  Downstream: (spatial, isPartOf, gn:Europe)
  \<llbracket>downstream_eu\<rrbracket> = {Europe, France, Paris, Lyon, Germany, Berlin}
*)

lemma refinement_spatial_invalid:
  "subsumption_verdict 
     (Classical {Europe, France, Paris, Lyon, Germany, Berlin}) 
     (Classical {France, Paris, Lyon}) 
   = Refuted"
  by simp

(* Europe does NOT refine France. 
   Downstream allows Germany, which upstream forbids. 
   DSSC violation. *)


(* ================================================================= *)
(* COMBINED: Conflict propagation through refinement                 *)
(* If c1 refines c2 and c2 conflicts with c3,                       *)
(* then c1 conflicts with c3.                                       *)
(* ================================================================= *)

(*
  Upstream: (purpose, isA, ResearchAndDevelopment)
    \<llbracket>upstream\<rrbracket> = {R&D, Scientific, Commercial}

  Downstream (valid refinement): (purpose, isA, ScientificResearch)
    \<llbracket>downstream\<rrbracket> = {ScientificResearch}

  Third party prohibition: (purpose, isA, ServiceProvision)
    \<llbracket>prohibition\<rrbracket> = {ServiceProvision, Marketing}

  upstream conflicts with prohibition? 
    {R&D, Scientific, Commercial} \<inter> {ServiceProvision, Marketing} = {} \<longrightarrow> Conflict

  Does downstream also conflict with prohibition?
    {ScientificResearch} \<inter> {ServiceProvision, Marketing} = {} \<longrightarrow> Conflict \<checkmark>

  Conflict propagates: if upstream conflicts, any valid 
  refinement also conflicts. This is Lemma conflict-propagation.
*)

lemma conflict_propagation_example:
  assumes sub: "subsumption_verdict (Classical s_down) (Classical s_up) = Confirmed"
    and conf: "verdict_of (Classical s_up) (Classical s_prohib) = Conflict"
  shows "verdict_of (Classical s_down) (Classical s_prohib) = Conflict"
proof -
  from sub have "s_down \<subseteq> s_up" by (simp split: if_splits)
  from conf have "s_up \<inter> s_prohib = {}" by (simp split: if_splits)
  from \<open>s_down \<subseteq> s_up\<close> \<open>s_up \<inter> s_prohib = {}\<close> 
  have "s_down \<inter> s_prohib = {}" by blast
  then show ?thesis by simp
qed

(* Concrete instance *)
lemma conflict_propagation_concrete:
  "verdict_of (Classical {ScientificResearch}) 
              (Classical {ServiceProvision, Marketing}) = Conflict"
  by simp


(* ================================================================= *)
(* SUMMARY                                                           *)
(* All three modes use the same machinery:                           *)
(*   Mode 1 (self-contradiction): verdict_of + verdict_and           *)
(*   Mode 2 (redundancy):         subsumption_verdict                *)
(*   Mode 3 (refinement):         subsumption_verdict                *)
(* Same denotations, same soundness, same Isabelle proofs.           *)
(* ================================================================= *)

end
