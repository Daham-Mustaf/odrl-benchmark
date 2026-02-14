theory ODRL_Grounding
  imports Main
begin

section \<open>ODRL Semantic Grounding Framework — Machine-Verified Meta-Theorems\<close>

text \<open>
  This theory mechanically verifies the meta-theorems of the ODRL
  semantic grounding framework for KB-dependent constraint conflict
  detection. It covers: soundness, composition soundness, runtime
  soundness, conflict propagation, KB monotonicity, decidability,
  and cross-dataspace alignment preservation.
\<close>

(* ================================================================= *)
(* Section 1: Core Datatypes                                         *)
(* ================================================================= *)

datatype 'c denotation = Classical "'c set" | Top

datatype verdict = Conflict | Compatible | Unknown

datatype subsum_verdict = Confirmed | Refuted | SubUnknown

(* ================================================================= *)
(* Section 2: Knowledge Base (Definition 2)                          *)
(* ================================================================= *)

locale knowledge_base =
  fixes C :: "'c set"
    and leq :: "'c \<Rightarrow> 'c \<Rightarrow> bool"
    and disj :: "'c \<Rightarrow> 'c \<Rightarrow> bool"
    and \<gamma> :: "'v \<Rightarrow> 'c option"
  assumes finite_C: "finite C"
    and leq_refl: "x \<in> C \<Longrightarrow> leq x x"
    and leq_trans: "\<lbrakk>leq x y; leq y z\<rbrakk> \<Longrightarrow> leq x z"
    and disj_sym: "disj x y \<Longrightarrow> disj y x"
    and disj_irrefl: "x \<in> C \<Longrightarrow> \<not> disj x x"
    and disj_down: "\<lbrakk>disj x y; leq x' x; leq y' y\<rbrakk> \<Longrightarrow> disj x' y'"
    and gamma_range: "\<gamma> v = Some c \<Longrightarrow> c \<in> C"

(* ================================================================= *)
(* Section 3: Lemma — Disjointness-Order Consistency                 *)
(* (Lemma lem:disj-consistency)                                      *)
(* ================================================================= *)

context knowledge_base
begin

lemma disj_order_consistency:
  assumes "leq x y" and "x \<in> C"
  shows "\<not> disj x y"
proof
  assume "disj x y"
  from disj_down[OF this leq_refl[OF assms(2)] assms(1)]
  have "disj x x" .
  with disj_irrefl[OF assms(2)] show False by contradiction
qed

(* ================================================================= *)
(* Section 4: Conservative Intersection (Definition 4)               *)
(* ================================================================= *)

fun conservative_meet :: "'c denotation \<Rightarrow> 'c denotation \<Rightarrow> 'c denotation"
  where
    "conservative_meet (Classical s1) (Classical s2) = Classical (s1 \<inter> s2)"
  | "conservative_meet _ _ = Top"

(* ================================================================= *)
(* Section 5: Conflict Detection (Definition 5)                      *)
(* ================================================================= *)

fun verdict_of :: "'c denotation \<Rightarrow> 'c denotation \<Rightarrow> verdict"
  where
    "verdict_of (Classical s1) (Classical s2) =
       (if s1 \<inter> s2 = {} then Conflict
        else Compatible)"
  | "verdict_of _ _ = Unknown"

lemma verdict_meet_equiv:
  "verdict_of d1 d2 =
     (case conservative_meet d1 d2 of
        Classical s \<Rightarrow> (if s = {} then Conflict else Compatible)
      | Top \<Rightarrow> Unknown)"
  by (cases d1; cases d2; simp)

(* ================================================================= *)
(* Section 6: Theorem 1 — Soundness (thm:soundness)                 *)
(* If verdict = Conflict, no element is in both denotations.         *)
(* ================================================================= *)

theorem soundness:
  assumes "verdict_of (Classical s1) (Classical s2) = Conflict"
  shows "s1 \<inter> s2 = {}"
  using assms by (simp split: if_splits)

theorem soundness_witness:
  assumes "verdict_of (Classical s1) (Classical s2) = Conflict"
  shows "\<not> (\<exists>x. x \<in> s1 \<and> x \<in> s2)"
  using soundness[OF assms] by blast

(* ================================================================= *)
(* Section 7: Denotation helpers for isA, hasPart, eq, neq          *)
(* ================================================================= *)

definition denot_isA :: "'c \<Rightarrow> 'c denotation" where
  "denot_isA g = Classical {x \<in> C. leq x g}"

definition denot_hasPart :: "'c \<Rightarrow> 'c denotation" where
  "denot_hasPart g = Classical {x \<in> C. leq g x}"

definition denot_eq :: "'c \<Rightarrow> 'c denotation" where
  "denot_eq g = Classical {g}"

definition denot_neq :: "'c \<Rightarrow> 'c denotation" where
  "denot_neq g = Classical (C - {g})"

definition denot_isAnyOf :: "'c list \<Rightarrow> 'c denotation" where
  "denot_isAnyOf gs = Classical (\<Union>g \<in> set gs. {x \<in> C. leq x g})"

definition denot_isAllOf :: "'c list \<Rightarrow> 'c denotation" where
  "denot_isAllOf gs = Classical {x \<in> C. \<forall>g \<in> set gs. leq x g}"

definition denot_isNoneOf :: "'c list \<Rightarrow> 'c denotation" where
  "denot_isNoneOf gs = Classical (C - (\<Union>g \<in> set gs. {x \<in> C. leq x g}))"

(* General grounding: if gamma returns None, denotation is Top *)
definition ground :: "'v \<Rightarrow> ('c \<Rightarrow> 'c denotation) \<Rightarrow> 'c denotation" where
  "ground v f = (case \<gamma> v of None \<Rightarrow> Top | Some g \<Rightarrow> f g)"

lemma ground_none: "\<gamma> v = None \<Longrightarrow> ground v f = Top"
  by (simp add: ground_def)

lemma ground_some: "\<gamma> v = Some g \<Longrightarrow> ground v f = f g"
  by (simp add: ground_def)

(* ================================================================= *)
(* Section 8: Top never produces Conflict                            *)
(* (Foundation for soundness chain)                                  *)
(* ================================================================= *)

lemma top_never_conflict:
  "verdict_of Top d = Unknown"
  "verdict_of d Top = Unknown"
  by (cases d; simp)+

lemma ungrounded_never_conflict:
  assumes "\<gamma> v = None"
  shows "verdict_of (ground v f) d2 = Unknown"
  using assms by (simp add: ground_def)

(* ================================================================= *)
(* Section 9: Constraint Subsumption (Definition 7)                  *)
(* ================================================================= *)

fun subsumption_verdict :: "'c denotation \<Rightarrow> 'c denotation \<Rightarrow> subsum_verdict"
  where
    "subsumption_verdict (Classical s1) (Classical s2) =
       (if s1 \<subseteq> s2 then Confirmed else Refuted)"
  | "subsumption_verdict _ _ = SubUnknown"

(* ================================================================= *)
(* Section 10: Lemma — Conflict Propagation (lem:conflict-propagation)*)
(* If c1 refines c2 and c2 conflicts with c3, then c1 conflicts      *)
(* with c3.                                                           *)
(* ================================================================= *)

theorem conflict_propagation:
  assumes sub: "subsumption_verdict (Classical s1) (Classical s2) = Confirmed"
    and conf: "verdict_of (Classical s2) (Classical s3) = Conflict"
  shows "verdict_of (Classical s1) (Classical s3) = Conflict"
proof -
  from sub have "s1 \<subseteq> s2" by (simp split: if_splits)
  from conf have "s2 \<inter> s3 = {}" by (simp split: if_splits)
  from \<open>s1 \<subseteq> s2\<close> \<open>s2 \<inter> s3 = {}\<close> have "s1 \<inter> s3 = {}" by blast
  then show ?thesis by simp
qed

(* ================================================================= *)
(* Section 11: Composition (Definition 6)                            *)
(* ================================================================= *)

fun verdict_and :: "verdict list \<Rightarrow> verdict" where
  "verdict_and vs =
    (if Conflict \<in> set vs then Conflict
     else if \<forall>v \<in> set vs. v = Compatible then Compatible
     else Unknown)"

fun verdict_or :: "verdict list \<Rightarrow> verdict" where
  "verdict_or vs =
    (if Compatible \<in> set vs then Compatible
     else if \<forall>v \<in> set vs. v = Conflict then Conflict
     else Unknown)"

fun verdict_xone :: "verdict list \<Rightarrow> verdict" where
  "verdict_xone vs =
    (if (\<exists>i < length vs. vs ! i = Compatible \<and>
         (\<forall>j < length vs. j \<noteq> i \<longrightarrow> vs ! j = Conflict))
     then Compatible
     else if \<forall>v \<in> set vs. v = Conflict then Conflict
     else Unknown)"

(* ================================================================= *)
(* Section 12: Theorem 2 — Composition Soundness                     *)
(* (thm:composition-soundness)                                       *)
(* ================================================================= *)

text \<open>
  For conjunction: if verdict_and = Conflict, then at least one
  per-operand verdict is Conflict. By Theorem 1 (soundness),
  that operand pair has no satisfying value. By operand independence,
  the conjunction fails.
\<close>

theorem composition_soundness_and:
  assumes "verdict_and vs = Conflict"
  shows "Conflict \<in> set vs"
  using assms by (simp split: if_splits)

text \<open>
  For disjunction: if verdict_or = Conflict, then every
  per-operand verdict is Conflict.
\<close>

theorem composition_soundness_or:
  assumes "verdict_or vs = Conflict"
  shows "\<forall>v \<in> set vs. v = Conflict"
  using assms by (simp split: if_splits)

text \<open>
  For exclusive disjunction: if verdict_xone = Conflict, then every
  per-operand verdict is Conflict. This reduces to the or case.
\<close>

theorem composition_soundness_xone:
  assumes "verdict_xone vs = Conflict"
  shows "\<forall>v \<in> set vs. v = Conflict"
  using assms by (simp split: if_splits)

text \<open>
  xone Compatible requires exactly one Compatible and all others
  Conflict — provable non-overlap of non-selected branches.
\<close>

theorem xone_compatible_requires_exclusivity:
  assumes "verdict_xone vs = Compatible"
  shows "\<exists>i < length vs. vs ! i = Compatible \<and>
         (\<forall>j < length vs. j \<noteq> i \<longrightarrow> vs ! j = Conflict)"
  using assms by (auto split: if_splits)

(* ================================================================= *)
(* Section 13: Constraint Satisfaction and Runtime Soundness          *)
(* (Definition 10, Theorem 3: thm:refined-soundness)                 *)
(* ================================================================= *)

text \<open>
  An execution context omega maps operands to values.
  Satisfaction: omega satisfies c = (ell, op, v) if:
    - omega(ell) is defined and groundable
    - either the denotation is Top (conservative) or
      gamma(omega(ell)) is in the denotation
\<close>

definition satisfies :: "'c \<Rightarrow> 'c denotation \<Rightarrow> bool" where
  "satisfies val d = (case d of Top \<Rightarrow> True | Classical s \<Rightarrow> val \<in> s)"

theorem runtime_soundness:
  assumes conf: "verdict_of (Classical s1) (Classical s2) = Conflict"
  shows "\<not> (\<exists>val. satisfies val (Classical s1) \<and> satisfies val (Classical s2))"
proof -
  from soundness[OF conf] have "s1 \<inter> s2 = {}" .
  then show ?thesis by (auto simp: satisfies_def)
qed

text \<open>
  Key property: Top never produces Conflict, so the permissive
  interpretation of Top in satisfies cannot mask a statically
  detected Conflict.
\<close>

lemma top_satisfies_all:
  "satisfies val Top = True"
  by (simp add: satisfies_def)

lemma conflict_requires_classical:
  assumes "verdict_of d1 d2 = Conflict"
  shows "\<exists>s1 s2. d1 = Classical s1 \<and> d2 = Classical s2"
  using assms by (cases d1; cases d2; simp)

(* ================================================================= *)
(* Section 14: Proposition — Decidability (prop:decidability)        *)
(* ================================================================= *)

text \<open>
  Over finite C, every denotation is a finite subset of C.
  Decidability follows from the definitional structure: verdict_of
  is defined by pattern matching on datatypes with computable
  set operations over finite C. No separate theorem is needed;
  the following lemma witnesses finiteness of denotations.
\<close>

lemma denot_isA_finite: "finite (case denot_isA g of Classical s \<Rightarrow> s | Top \<Rightarrow> {})"
  using finite_C by (simp add: denot_isA_def)

end (* knowledge_base locale *)

(* ================================================================= *)
(* Section 15: KB Monotonicity (prop:kb-monotonicity)                *)
(* Proper locale: same C and leq, extended disj and gamma.           *)
(* ================================================================= *)

locale kb_extension =
  KB: knowledge_base C leq disj \<gamma> +
  KB_plus: knowledge_base C leq disj_plus \<gamma>_plus
  for C :: "'c set" and leq :: "'c \<Rightarrow> 'c \<Rightarrow> bool"
  and disj :: "'c \<Rightarrow> 'c \<Rightarrow> bool" and \<gamma> :: "'v \<Rightarrow> 'c option"
  and disj_plus :: "'c \<Rightarrow> 'c \<Rightarrow> bool" and \<gamma>_plus :: "'v \<Rightarrow> 'c option" +
  assumes disj_extends: "disj x y \<Longrightarrow> disj_plus x y"
    and gamma_extends: "\<gamma> v = Some g \<Longrightarrow> \<gamma>_plus v = Some g"

context kb_extension
begin

text \<open>
  Core lemma: for values grounded in KB, the ground function
  produces the same result in KB and KB+ because gamma extends
  and C/leq are unchanged.
\<close>

lemma ground_preserved:
  assumes "\<gamma> v = Some g"
  shows "KB.ground v f = KB_plus.ground v f"
  using assms gamma_extends[OF assms]
  by (simp add: KB.ground_def KB_plus.ground_def)

lemma grounded_denotation_stable:
  assumes "\<gamma> v = Some g"
  shows "\<gamma>_plus v = Some g"
  using gamma_extends[OF assms] .

text \<open>
  KB Monotonicity (1) and (2): Conflict and Compatible are preserved.
  Since ground produces the same denotation for grounded values,
  verdict_of receives identical arguments and returns identical results.
\<close>

theorem kb_monotonicity_verdict:
  assumes "\<gamma> v1 = Some g1"
    and "\<gamma> v2 = Some g2"
  shows "KB.verdict_of (KB.ground v1 f) (KB.ground v2 f) =
         KB_plus.verdict_of (KB_plus.ground v1 f) (KB_plus.ground v2 f)"
  using ground_preserved[OF assms(1)] ground_preserved[OF assms(2)]
  by simp

text \<open>
  KB Monotonicity (3): Unknown can resolve.
  If gamma was undefined in KB but becomes defined in KB+,
  Top becomes Classical, enabling a definite verdict.
\<close>

theorem kb_monotonicity_unknown_resolves:
  assumes "\<gamma> v = None"
  shows "KB.ground v f = Top"
  using assms by (simp add: KB.ground_def)

theorem kb_monotonicity_grounding_enables:
  assumes "\<gamma> v = None"
    and "\<gamma>_plus v = Some g"
  shows "KB_plus.ground v f = f g"
  using assms(2) by (simp add: KB_plus.ground_def)

text \<open>
  Combined: if one operand was ungrounded in KB (forcing Unknown),
  extending gamma can yield a definite verdict in KB+, provided
  the denotation constructor f produces Classical results (which
  all concrete operators — denot_isA, denot_eq, etc. — do).
\<close>

theorem kb_monotonicity_resolves_unknown:
  assumes "\<gamma> v1 = None"
    and "\<gamma>_plus v1 = Some g1"
    and "\<gamma> v2 = Some g2"
    and classical1: "f g1 = Classical s1"
    and classical2: "f g2 = Classical s2"
  shows "KB.verdict_of (KB.ground v1 f) (KB.ground v2 f) = Unknown"
    and "KB_plus.verdict_of (KB_plus.ground v1 f) (KB_plus.ground v2 f) \<noteq> Unknown"
proof -
  from assms(1) have "KB.ground v1 f = Top" by (simp add: KB.ground_def)
  then show "KB.verdict_of (KB.ground v1 f) (KB.ground v2 f) = Unknown"
    by (simp add: KB.top_never_conflict)
next
  from assms(2) have "KB_plus.ground v1 f = f g1" by (simp add: KB_plus.ground_def)
  from assms(3) have "\<gamma>_plus v2 = Some g2" using gamma_extends by simp
  then have "KB_plus.ground v2 f = f g2" by (simp add: KB_plus.ground_def)
  show "KB_plus.verdict_of (KB_plus.ground v1 f) (KB_plus.ground v2 f) \<noteq> Unknown"
    using \<open>KB_plus.ground v1 f = f g1\<close> \<open>KB_plus.ground v2 f = f g2\<close>
          classical1 classical2
    by simp
qed

text \<open>
  Concrete instantiation: denot_isA produces the same denotation
  in KB and KB+ because it depends only on C and leq, which are
  shared by the kb_extension locale.
\<close>

lemma denot_isA_shared:
  "KB.denot_isA g = KB_plus.denot_isA g"
  by (simp add: KB.denot_isA_def KB_plus.denot_isA_def)

corollary kb_monotonicity_isA:
  assumes "\<gamma> v1 = Some g1" and "\<gamma> v2 = Some g2"
  shows "KB.verdict_of (KB.denot_isA g1) (KB.denot_isA g2) =
         KB_plus.verdict_of (KB_plus.denot_isA g1) (KB_plus.denot_isA g2)"
  using denot_isA_shared by simp

end (* kb_extension locale *)

(* ================================================================= *)
(* Section 16: Cross-Dataspace Alignment                             *)
(* (Definitions 8-9, Lemma 2, Proposition 2, Corollary 1)           *)
(* ================================================================= *)

locale alignment =
  KB_A: knowledge_base C\<^sub>A leq\<^sub>A disj\<^sub>A \<gamma>\<^sub>A +
  KB_B: knowledge_base C\<^sub>B leq\<^sub>B disj\<^sub>B \<gamma>\<^sub>B
  for C\<^sub>A :: "'c set" and leq\<^sub>A and disj\<^sub>A and \<gamma>\<^sub>A :: "'v \<Rightarrow> 'c option"
  and C\<^sub>B :: "'c set" and leq\<^sub>B and disj\<^sub>B and \<gamma>\<^sub>B :: "'v \<Rightarrow> 'c option" +
  fixes \<alpha> :: "'c \<Rightarrow> 'c option"
  assumes inj: "\<lbrakk>\<alpha> x = Some a; \<alpha> y = Some a\<rbrakk> \<Longrightarrow> x = y"
    and order_preserve:
      "\<lbrakk>\<alpha> x = Some x'; \<alpha> y = Some y'\<rbrakk>
        \<Longrightarrow> (leq\<^sub>A x y \<longleftrightarrow> leq\<^sub>B x' y')"
    and disj_preserve:
      "\<lbrakk>\<alpha> x = Some x'; \<alpha> y = Some y'; disj\<^sub>A x y\<rbrakk>
        \<Longrightarrow> disj\<^sub>B x' y'"

text \<open>
  Note: disj_preserve is one-directional (A implies B) by design.
  The target KB may assert additional disjointness beyond the source.
  This is safe because verdicts are determined by denotations (which
  depend on leq, not disj), and leq is preserved biconditionally.
  The following lemma gives disj_preserve its intended use:
  disjointness-derived conflicts in A transfer to B.
\<close>

context alignment
begin

lemma disj_conflict_transfers:
  assumes "disj\<^sub>A x y"
    and "\<alpha> x = Some x'" and "\<alpha> y = Some y'"
  shows "disj\<^sub>B x' y'"
  using assms disj_preserve by blast

(* ================================================================= *)
(* Lemma 2: Denotation Preservation (lem:denotation-equality)        *)
(* For isA: alpha(denot_A) = denot_B(alpha(g))                       *)
(* ================================================================= *)

text \<open>
  We verify the core property: for the isA operator, if all elements
  of the A-denotation are in dom(alpha), then the image under alpha
  equals the B-denotation of the aligned grounding value.
\<close>

lemma denotation_preservation_isA:
  assumes g_map: "\<alpha> g = Some g'"
    and all_mapped: "\<forall>x \<in> {x \<in> C\<^sub>A. leq\<^sub>A x g}. \<exists>x'. \<alpha> x = Some x'"
  shows "(\<lambda>x. the (\<alpha> x)) ` {x \<in> C\<^sub>A. leq\<^sub>A x g} =
         {y. \<exists>x \<in> C\<^sub>A. \<alpha> x = Some y \<and> leq\<^sub>B y g'}"
proof (rule equalityI; rule subsetI)
  fix y
  assume "y \<in> (\<lambda>x. the (\<alpha> x)) ` {x \<in> C\<^sub>A. leq\<^sub>A x g}"
  then obtain x where x_in: "x \<in> C\<^sub>A" and x_leq: "leq\<^sub>A x g"
    and y_eq: "y = the (\<alpha> x)" by blast
  from all_mapped x_in x_leq obtain x' where x_map: "\<alpha> x = Some x'" by blast
  from y_eq x_map have "y = x'" by simp
  from order_preserve[OF x_map g_map] x_leq have "leq\<^sub>B x' g'" by simp
  with x_in x_map \<open>y = x'\<close> show "y \<in> {y. \<exists>x \<in> C\<^sub>A. \<alpha> x = Some y \<and> leq\<^sub>B y g'}" by blast
next
  fix y
  assume "y \<in> {y. \<exists>x \<in> C\<^sub>A. \<alpha> x = Some y \<and> leq\<^sub>B y g'}"
  then obtain x where x_in: "x \<in> C\<^sub>A" and x_map: "\<alpha> x = Some y"
    and y_leq: "leq\<^sub>B y g'" by blast
  from order_preserve[OF x_map g_map] y_leq have "leq\<^sub>A x g" by simp
  with x_in have "x \<in> {x \<in> C\<^sub>A. leq\<^sub>A x g}" by blast
  from x_map have "the (\<alpha> x) = y" by simp
  with \<open>x \<in> {x \<in> C\<^sub>A. leq\<^sub>A x g}\<close>
  show "y \<in> (\<lambda>x. the (\<alpha> x)) ` {x \<in> C\<^sub>A. leq\<^sub>A x g}" by blast
qed

(* ================================================================= *)
(* Proposition 2: Verdict Preservation (prop:alignment)              *)
(* Conflict preservation under total alignment of denotations        *)
(* ================================================================= *)

text \<open>
  If both denotations are fully within dom(alpha), and they are
  disjoint in KB_A, then their images are disjoint in KB_B.
  This uses injectivity of alpha.
\<close>

theorem verdict_preservation_conflict:
  assumes disj_sets: "s1 \<inter> s2 = {}"
    and s1_mapped: "\<forall>x \<in> s1. \<exists>x'. \<alpha> x = Some x'"
    and s2_mapped: "\<forall>x \<in> s2. \<exists>x'. \<alpha> x = Some x'"
  shows "(\<lambda>x. the (\<alpha> x)) ` s1 \<inter> (\<lambda>x. the (\<alpha> x)) ` s2 = {}"
proof (rule ccontr)
  assume "\<not> ?thesis"
  then obtain y where y_in1: "y \<in> (\<lambda>x. the (\<alpha> x)) ` s1"
    and y_in2: "y \<in> (\<lambda>x. the (\<alpha> x)) ` s2" by blast
  from y_in1 obtain a where a_in: "a \<in> s1" and a_map: "the (\<alpha> a) = y"
    by (auto simp: image_iff)
  from y_in2 obtain b where b_in: "b \<in> s2" and b_map: "the (\<alpha> b) = y"
    by (auto simp: image_iff)
  from s1_mapped a_in obtain a' where alpha_a: "\<alpha> a = Some a'" by blast
  from s2_mapped b_in obtain b' where alpha_b: "\<alpha> b = Some b'" by blast
  from a_map alpha_a have "a' = y" by simp
  from b_map alpha_b have "b' = y" by simp
  with \<open>a' = y\<close> have "\<alpha> a = Some y" "\<alpha> b = Some y"
    using alpha_a alpha_b by simp_all
  from inj[OF this] have "a = b" .
  with a_in b_in disj_sets show False by blast
qed

text \<open>
  Full verdict-level theorem: Conflict verdict is preserved through
  alignment. This connects the set-level proof above to verdict_of.
\<close>

theorem verdict_preservation_conflict_full:
  assumes "knowledge_base.verdict_of (Classical s1) (Classical s2) = Conflict"
    and s1_mapped: "\<forall>x \<in> s1. \<exists>x'. \<alpha> x = Some x'"
    and s2_mapped: "\<forall>x \<in> s2. \<exists>x'. \<alpha> x = Some x'"
  shows "knowledge_base.verdict_of
           (Classical ((\<lambda>x. the (\<alpha> x)) ` s1))
           (Classical ((\<lambda>x. the (\<alpha> x)) ` s2)) = Conflict"
proof -
  from assms(1) have "s1 \<inter> s2 = {}" by (simp split: if_splits)
  from verdict_preservation_conflict[OF this s1_mapped s2_mapped]
  have "(\<lambda>x. the (\<alpha> x)) ` s1 \<inter> (\<lambda>x. the (\<alpha> x)) ` s2 = {}" .
  then show ?thesis by simp
qed

(* ================================================================= *)
(* Corollary 1: Subsumption Preservation (cor:subsumption-preservation)*)
(* ================================================================= *)

theorem subsumption_preservation:
  assumes sub: "s1 \<subseteq> s2"
    and s1_mapped: "\<forall>x \<in> s1. \<exists>x'. \<alpha> x = Some x'"
    and s2_mapped: "\<forall>x \<in> s2. \<exists>x'. \<alpha> x = Some x'"
  shows "(\<lambda>x. the (\<alpha> x)) ` s1 \<subseteq> (\<lambda>x. the (\<alpha> x)) ` s2"
  using sub by blast

text \<open>
  Full verdict-level corollary: Confirmed subsumption is preserved
  through alignment.
\<close>

theorem subsumption_preservation_verdict:
  assumes "knowledge_base.subsumption_verdict (Classical s1) (Classical s2) = Confirmed"
    and s1_mapped: "\<forall>x \<in> s1. \<exists>x'. \<alpha> x = Some x'"
    and s2_mapped: "\<forall>x \<in> s2. \<exists>x'. \<alpha> x = Some x'"
  shows "knowledge_base.subsumption_verdict
           (Classical ((\<lambda>x. the (\<alpha> x)) ` s1))
           (Classical ((\<lambda>x. the (\<alpha> x)) ` s2)) = Confirmed"
proof -
  from assms(1) have "s1 \<subseteq> s2" by (simp split: if_splits)
  from subsumption_preservation[OF this s1_mapped s2_mapped]
  have "(\<lambda>x. the (\<alpha> x)) ` s1 \<subseteq> (\<lambda>x. the (\<alpha> x)) ` s2" .
  then show ?thesis by simp
qed

end (* alignment locale *)

(* ================================================================= *)
(* Section 17: Summary of verified results                           *)
(* ================================================================= *)

text \<open>
  Machine-verified meta-theorems:

  In knowledge_base locale:
    1. disj_order_consistency    (Lemma: Disjointness-Order Consistency)
    2. soundness                 (Theorem 1: Soundness)
    3. soundness_witness         (Theorem 1, witness form)
    4. runtime_soundness         (Theorem 3: Runtime Soundness)
    5. conflict_propagation      (Lemma: Conflict Propagation)
    6. top_never_conflict        (Foundation: Top never yields Conflict)
    7. conflict_requires_classical (Foundation: Conflict requires Classical)
    8. composition_soundness_and  (Theorem 2: Composition — conjunction, structural)
    9. composition_soundness_or   (Theorem 2: Composition — disjunction, structural)
   10. composition_soundness_xone (Theorem 2: Composition — xone, structural)
   11. xone_compatible_requires_exclusivity (xone requires provable non-overlap)

  In kb_extension locale:
   12. ground_preserved           (grounded values yield same denotation in KB+)
   13. kb_monotonicity_verdict    (Proposition 3: verdict identical for grounded pairs)
   14. denot_isA_shared           (concrete: denot_isA identical in KB and KB+)
   15. kb_monotonicity_isA        (Proposition 3: instantiated for isA operator)
   16. kb_monotonicity_resolves_unknown (Proposition 3: extending gamma resolves Unknown)

  In alignment locale:
   17. disj_conflict_transfers          (disjointness transfers through alignment)
   18. denotation_preservation_isA      (Lemma 2: Denotation Preservation)
   19. verdict_preservation_conflict    (Proposition 2: set-level disjointness preserved)
   20. verdict_preservation_conflict_full (Proposition 2: verdict_of Conflict preserved)
   21. subsumption_preservation         (Corollary 1: set-level inclusion preserved)
   22. subsumption_preservation_verdict (Corollary 1: Confirmed verdict preserved)

  Composition soundness theorems verify the structural decomposition
  (Conflict in composition implies per-operand Conflict). The semantic
  lift to execution contexts requires operand independence (Assumption 2),
  which is argued in the paper but not modeled in Isabelle.

  Decidability follows from the definitional structure of verdict_of
  (pattern matching over finite datatypes) and is not stated as a
  separate theorem.

  All proofs are fully mechanized with no sorry.
\<close>

end
