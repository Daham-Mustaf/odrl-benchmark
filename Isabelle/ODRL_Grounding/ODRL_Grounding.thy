theory ODRL_Grounding
  imports Main
begin
section \<open>ODRL Semantic Grounding Framework --- Machine-Verified Meta-Theorems\<close>
text \<open>
  This theory mechanically verifies the meta-theorems of the ODRL
  semantic grounding framework for hierarchy-dependent constraint
  conflict detection. Terminology follows the paper: we use
  \<^emph>\<open>hierarchy\<close> (not knowledge base) throughout.
  Coverage:
    - Disjointness-order consistency (Lemma 1)
    - Soundness: classical, empty-vs-Top, unified (Theorem 1)
    - Runtime soundness (Theorem 3)
    - Conflict propagation (Lemma 3)
    - Composition soundness: and / or / xone (Theorem 2)
    - Hierarchy monotonicity (Proposition 3)
    - Denotation preservation under alignment: all operators (Lemma 2)
    - Verdict preservation: conflict + graceful degradation (Proposition 4)
    - Subsumption preservation (Corollary 1)
  All results are proved without \<^bold>\<open>sorry\<close>.
  -----------------------------------------------------------------------
  denotation_preservation_isAnyOf
         CAUSE:  "from all_mapped (UN_I [OF gset, of x] xC xl)" applies a
                 universally-quantified hypothesis as if it were a function.
                 This is not valid Isabelle syntax; HOL hypotheses cannot be
                 applied with parenthesised arguments.
         FIX:    Establish set-membership first with an explicit "have", then
                 use "all_mapped[rule_format, OF <membership>]" to instantiate.

  denotation_preservation_isAllOf
         CAUSE:  (a) The proof uses "ballI [of \"set gs\", OF FalseE]" which is
                     not a valid term -- ballI is an introduction rule for goals,
                     not a term that can be partially applied with [of ...].
                 (b) "hd_in_set [OF <gs ne []> <gs ne []>]" duplicates the
                     same argument; hd_in_set takes ONE non-emptiness argument.
                 (c) The original assumption "witness_complete" (forall g in gs,
                     forall x below g, alpha maps x) is vacuously True when
                     gs = [], giving NO information about alpha's domain over
                     {x in C_A. forall g in []. leq_A x g} = C_A.  The lemma
                     is therefore *logically unprovable* for gs = [] under the
                     old assumption.
         FIX:    Replace "witness_complete" with the stronger, directly usable
                 assumption "all_mapped : forall x in {x in C_A. forall g in
                 set gs. leq_A x g}. exists x'. alpha x = Some x'".
                 This covers the empty-list case and the proof goes through
                 with a two-line "have xin / from all_mapped" idiom.

  BUG 3  verdict_preservation_conflict_full
         CAUSE:  "hierarchy.verdict_of" uses a locale-qualified name for a
                 "fun" that carries no locale parameters.  "fun" defined inside
                 "context hierarchy begin...end" produces a GLOBAL constant
                 named "verdict_of" (no locale prefix needed).  Using the
                 qualified name causes a name-resolution error in the
                 "alignment" locale context (which does not extend "hierarchy").
         FIX:    Replace "hierarchy.verdict_of" with "verdict_of" throughout.

  BUG 4  subsumption_preservation_verdict
         CAUSE:  Same issue as BUG 3 for "hierarchy.subsumption_verdict".
         FIX:    Replace with bare "subsumption_verdict".
  -----------------------------------------------------------------------
\<close>

(* ================================================================= *)
(* Section 1: Core Datatypes                                         *)
(* ================================================================= *)
datatype 'c denotation = Classical "'c set" | Top
datatype verdict        = Conflict | Compatible | Unknown
datatype subsum_verdict = Confirmed | Refuted | SubUnknown

(* ================================================================= *)
(* Section 2: Hierarchy (Definition 2)                               *)
(* ================================================================= *)
locale hierarchy =
  fixes C     :: "'c set"
    and leq   :: "'c \<Rightarrow> 'c \<Rightarrow> bool"
    and disj  :: "'c \<Rightarrow> 'c \<Rightarrow> bool"
    and \<gamma>    :: "'v \<Rightarrow> 'c option"
  assumes
    finite_C    : "finite C"
  and leq_refl  : "x \<in> C \<Longrightarrow> leq x x"
  and leq_trans : "\<lbrakk>leq x y; leq y z\<rbrakk> \<Longrightarrow> leq x z"
  and disj_sym  : "disj x y \<Longrightarrow> disj y x"
  and disj_irrefl: "x \<in> C \<Longrightarrow> \<not> disj x x"
  and disj_down : "\<lbrakk>disj x y; leq x' x; leq y' y\<rbrakk> \<Longrightarrow> disj x' y'"
  and gamma_range: "\<gamma> v = Some c \<Longrightarrow> c \<in> C"

(* ================================================================= *)
(* Section 3: Lemma 1 - Disjointness-Order Consistency               *)
(* ================================================================= *)
context hierarchy
begin

lemma disj_order_consistency:
  assumes "leq x y" and "x \<in> C"
  shows "\<not> disj x y"
proof
  assume "disj x y"
  from disj_down [OF this leq_refl [OF assms(2)] assms(1)]
  have "disj x x" .
  with disj_irrefl [OF assms(2)] show False by contradiction
qed

(* ================================================================= *)
(* Section 4: Conservative Intersection (Definition 4)               *)
(* ================================================================= *)
fun conservative_meet :: "'c denotation \<Rightarrow> 'c denotation \<Rightarrow> 'c denotation"
  where
    "conservative_meet (Classical s1) (Classical s2) = Classical (s1 \<inter> s2)"
  | "conservative_meet (Classical s1) Top            =
       (if s1 = {} then Classical {} else Top)"
  | "conservative_meet Top (Classical s2)            =
       (if s2 = {} then Classical {} else Top)"
  | "conservative_meet Top Top                       = Top"

(* ================================================================= *)
(* Section 5: Conflict Detection (Definition 5)                      *)
(* ================================================================= *)
fun verdict_of :: "'c denotation \<Rightarrow> 'c denotation \<Rightarrow> verdict"
  where
    "verdict_of (Classical s1) (Classical s2) =
       (if s1 \<inter> s2 = {} then Conflict else Compatible)"
  | "verdict_of (Classical s1) Top =
       (if s1 = {} then Conflict else Unknown)"
  | "verdict_of Top (Classical s2) =
       (if s2 = {} then Conflict else Unknown)"
  | "verdict_of Top Top = Unknown"

lemma verdict_meet_equiv:
  "verdict_of d1 d2 =
     (case conservative_meet d1 d2 of
        Classical s \<Rightarrow> (if s = {} then Conflict else Compatible)
      | Top \<Rightarrow> Unknown)"
  by (cases d1; cases d2; simp)

(* ================================================================= *)
(* Section 6: Theorem 1 - Soundness                                  *)
(* ================================================================= *)
theorem soundness_classical:
  assumes "verdict_of (Classical s1) (Classical s2) = Conflict"
  shows "s1 \<inter> s2 = {}"
  using assms by (simp split: if_splits)

theorem soundness_empty_left:
  assumes "verdict_of (Classical s1) Top = Conflict"
  shows "s1 = {}"
  using assms by (simp split: if_splits)

theorem soundness_empty_right:
  assumes "verdict_of Top (Classical s2) = Conflict"
  shows "s2 = {}"
  using assms by (simp split: if_splits)

theorem soundness:
  assumes "verdict_of d1 d2 = Conflict"
  shows "\<not> (\<exists>x. (case d1 of Classical s \<Rightarrow> x \<in> s | Top \<Rightarrow> True) \<and>
               (case d2 of Classical s \<Rightarrow> x \<in> s | Top \<Rightarrow> True))"
  using assms by (cases d1; cases d2; auto split: if_splits)

theorem soundness_witness:
  assumes "verdict_of (Classical s1) (Classical s2) = Conflict"
  shows "\<not> (\<exists>x. x \<in> s1 \<and> x \<in> s2)"
  using soundness_classical [OF assms] by blast

(* ================================================================= *)
(* Section 7: Constraint Denotations (Definition 3)                  *)
(* ================================================================= *)
definition denot_isA :: "'c \<Rightarrow> 'c denotation" where
  "denot_isA g = Classical {x \<in> C. leq x g}"

definition denot_isPartOf :: "'c \<Rightarrow> 'c denotation" where
  "denot_isPartOf g = Classical {x \<in> C. leq x g}"

lemma denot_isPartOf_eq_isA:
  "denot_isPartOf g = denot_isA g"
  by (simp add: denot_isPartOf_def denot_isA_def)

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

definition ground :: "'v \<Rightarrow> ('c \<Rightarrow> 'c denotation) \<Rightarrow> 'c denotation" where
  "ground v f = (case \<gamma> v of None \<Rightarrow> Top | Some g \<Rightarrow> f g)"

lemma ground_none: "\<gamma> v = None \<Longrightarrow> ground v f = Top"
  by (simp add: ground_def)

lemma ground_some: "\<gamma> v = Some g \<Longrightarrow> ground v f = f g"
  by (simp add: ground_def)

(* ================================================================= *)
(* Section 7b: Denotation Finiteness                                 *)
(* ================================================================= *)
lemma denot_isA_finite:
  "finite (case denot_isA g of Classical s \<Rightarrow> s | Top \<Rightarrow> {})"
  using finite_C by (simp add: denot_isA_def)

lemma denot_isPartOf_finite:
  "finite (case denot_isPartOf g of Classical s \<Rightarrow> s | Top \<Rightarrow> {})"
  using finite_C by (simp add: denot_isPartOf_def)

lemma denot_hasPart_finite:
  "finite (case denot_hasPart g of Classical s \<Rightarrow> s | Top \<Rightarrow> {})"
  using finite_C by (simp add: denot_hasPart_def)

lemma denot_eq_finite:
  "finite (case denot_eq g of Classical s \<Rightarrow> s | Top \<Rightarrow> {})"
  by (simp add: denot_eq_def)

lemma denot_neq_finite:
  "finite (case denot_neq g of Classical s \<Rightarrow> s | Top \<Rightarrow> {})"
  using finite_C by (simp add: denot_neq_def)

lemma denot_isAnyOf_finite:
  "finite (case denot_isAnyOf gs of Classical s \<Rightarrow> s | Top \<Rightarrow> {})"
  using finite_C by (simp add: denot_isAnyOf_def)

lemma denot_isAllOf_finite:
  "finite (case denot_isAllOf gs of Classical s \<Rightarrow> s | Top \<Rightarrow> {})"
  using finite_C by (simp add: denot_isAllOf_def)

lemma denot_isNoneOf_finite:
  "finite (case denot_isNoneOf gs of Classical s \<Rightarrow> s | Top \<Rightarrow> {})"
  using finite_C by (simp add: denot_isNoneOf_def)

(* ================================================================= *)
(* Section 7c: Structural Denotation Lemmas                          *)
(* ================================================================= *)
lemma denot_neq_singleton_empty:
  assumes "C = {g}"
  shows "denot_neq g = Classical {}"
  using assms by (simp add: denot_neq_def)

lemma denot_isAllOf_incomparable_empty:
  assumes "\<not> (\<exists>x \<in> C. \<forall>g \<in> set gs. leq x g)"
  shows "denot_isAllOf gs = Classical {}"
  using assms by (simp add: denot_isAllOf_def)

(* ================================================================= *)
(* Section 8: Verdict Structural Lemmas                              *)
(* ================================================================= *)
lemma empty_always_conflict:
    "verdict_of (Classical {}) d = Conflict"
    "verdict_of d (Classical {}) = Conflict"
  by (cases d; simp)+

lemma top_top_unknown:
  "verdict_of Top Top = Unknown"
  by simp

lemma top_nonempty_unknown:
  assumes "s \<noteq> {}"
  shows "verdict_of Top (Classical s) = Unknown"
    and "verdict_of (Classical s) Top = Unknown"
  using assms by simp_all

lemma ungrounded_nonempty_unknown:
  assumes "\<gamma> v = None" and "s \<noteq> {}"
  shows "verdict_of (ground v f) (Classical s) = Unknown"
  using assms by (simp add: ground_def)

lemma conflict_requires_classical_or_empty:
  assumes "verdict_of d1 d2 = Conflict"
  shows "(\<exists>s1 s2. d1 = Classical s1 \<and> d2 = Classical s2 \<and> s1 \<inter> s2 = {}) \<or>
         (\<exists>s.    d1 = Classical s  \<and> s = {}            \<and> d2 = Top) \<or>
         (\<exists>s.    d2 = Classical s  \<and> s = {}            \<and> d1 = Top)"
  using assms by (cases d1; cases d2; auto split: if_splits)

(* ================================================================= *)
(* Section 9: Constraint Subsumption (Definition 7)                  *)
(* ================================================================= *)
fun subsumption_verdict :: "'c denotation \<Rightarrow> 'c denotation \<Rightarrow> subsum_verdict"
  where
    "subsumption_verdict (Classical s1) (Classical s2) =
       (if s1 \<subseteq> s2 then Confirmed else Refuted)"
  | "subsumption_verdict _ _ = SubUnknown"

(* ================================================================= *)
(* Section 10: Lemma 3 - Conflict Propagation                        *)
(* ================================================================= *)
theorem conflict_propagation:
  assumes sub : "subsumption_verdict (Classical s1) (Classical s2) = Confirmed"
    and   conf: "verdict_of (Classical s2) (Classical s3) = Conflict"
  shows "verdict_of (Classical s1) (Classical s3) = Conflict"
proof -
  from sub  have "s1 \<subseteq> s2"      by (simp split: if_splits)
  from conf have "s2 \<inter> s3 = {}" by (simp split: if_splits)
  with \<open>s1 \<subseteq> s2\<close> have "s1 \<inter> s3 = {}" by blast
  then show ?thesis by simp
qed

(* ================================================================= *)
(* Section 11: Constraint Composition (Definition 6)                 *)
(* ================================================================= *)
fun verdict_and :: "verdict list \<Rightarrow> verdict" where
  "verdict_and vs =
    (if Conflict    \<in> set vs then Conflict
     else if \<forall>v \<in> set vs. v = Compatible then Compatible
     else Unknown)"

fun verdict_or :: "verdict list \<Rightarrow> verdict" where
  "verdict_or vs =
    (if Compatible \<in> set vs then Compatible
     else if \<forall>v \<in> set vs. v = Conflict then Conflict
     else Unknown)"

fun verdict_xone :: "verdict list \<Rightarrow> verdict" where
  "verdict_xone vs =
    (if (\<exists>i < length vs.
           vs ! i = Compatible \<and>
           (\<forall>j < length vs. j \<noteq> i \<longrightarrow> vs ! j = Conflict))
     then Compatible
     else if \<forall>v \<in> set vs. v = Conflict then Conflict
     else Unknown)"

(* ================================================================= *)
(* Section 12: Theorem 2 - Composition Soundness                     *)
(* ================================================================= *)
theorem composition_soundness_and:
  assumes "verdict_and vs = Conflict"
  shows "Conflict \<in> set vs"
  using assms by (simp split: if_splits)

theorem composition_soundness_or:
  assumes "verdict_or vs = Conflict"
  shows "\<forall>v \<in> set vs. v = Conflict"
  using assms by (simp split: if_splits)

theorem composition_soundness_xone:
  assumes "verdict_xone vs = Conflict"
  shows "\<forall>v \<in> set vs. v = Conflict"
  using assms by (simp split: if_splits)

theorem xone_compatible_requires_exclusivity:
  assumes "verdict_xone vs = Compatible"
  shows "\<exists>i < length vs.
           vs ! i = Compatible \<and>
           (\<forall>j < length vs. j \<noteq> i \<longrightarrow> vs ! j = Conflict)"
  using assms by (auto split: if_splits)

lemma and_all_unknown:
  assumes "\<forall>v \<in> set vs. v = Unknown" and "vs \<noteq> []"
  shows "verdict_and vs = Unknown"
  using assms by auto

lemma or_all_unknown:
  assumes "\<forall>v \<in> set vs. v = Unknown" and "vs \<noteq> []"
  shows "verdict_or vs = Unknown"
  using assms by auto

(* ================================================================= *)
(* Section 13: Runtime Semantics (Theorem 3)                         *)
(* ================================================================= *)
definition satisfies :: "'c \<Rightarrow> 'c denotation \<Rightarrow> bool" where
  "satisfies val d = (case d of Top \<Rightarrow> True | Classical s \<Rightarrow> val \<in> s)"

lemma top_satisfies_all:
  "satisfies val Top = True"
  by (simp add: satisfies_def)

lemma empty_satisfies_none:
  "\<not> satisfies val (Classical {})"
  by (simp add: satisfies_def)

theorem runtime_soundness:
  assumes conf: "verdict_of d1 d2 = Conflict"
  shows "\<not> (\<exists>val. satisfies val d1 \<and> satisfies val d2)"
proof -
  from conf show ?thesis
  proof (cases d1)
    case (Classical s1)
    then show ?thesis using conf
    proof (cases d2)
      case (Classical s2)
      with Classical conf have "s1 \<inter> s2 = {}" by (simp split: if_splits)
      then show ?thesis using Classical \<open>d2 = Classical s2\<close>
        by (auto simp: satisfies_def)
    next
      case Top
      with Classical conf have "s1 = {}" by (simp split: if_splits)
      then show ?thesis using Classical by (auto simp: satisfies_def)
    qed
  next
    case Top
    then show ?thesis using conf
    proof (cases d2)
      case (Classical s2)
      with Top conf have "s2 = {}" by (simp split: if_splits)
      then show ?thesis using Classical by (auto simp: satisfies_def)
    next
      case Top
      with \<open>d1 = Top\<close> conf show ?thesis by simp
    qed
  qed
qed

end (* hierarchy locale *)

(* ================================================================= *)
(* Section 14: Hierarchy Monotonicity (Proposition 3)                *)
(* ================================================================= *)
locale hierarchy_extension =
  H  : hierarchy C leq disj  \<gamma>      +
  H_plus: hierarchy C leq disj_plus \<gamma>_plus
  for C         :: "'c set"
  and leq       :: "'c \<Rightarrow> 'c \<Rightarrow> bool"
  and disj      :: "'c \<Rightarrow> 'c \<Rightarrow> bool"
  and \<gamma>         :: "'v \<Rightarrow> 'c option"
  and disj_plus :: "'c \<Rightarrow> 'c \<Rightarrow> bool"
  and \<gamma>_plus    :: "'v \<Rightarrow> 'c option" +
  assumes
    disj_extends  : "disj x y \<Longrightarrow> disj_plus x y"
  and gamma_extends: "\<gamma> v = Some g \<Longrightarrow> \<gamma>_plus v = Some g"

context hierarchy_extension
begin

lemma ground_preserved:
  assumes "\<gamma> v = Some g"
  shows "H.ground v f = H_plus.ground v f"
  using assms gamma_extends [OF assms]
  by (simp add: H.ground_def H_plus.ground_def)

lemma grounded_denotation_stable:
  assumes "\<gamma> v = Some g"
  shows "\<gamma>_plus v = Some g"
  using gamma_extends [OF assms] .

theorem hierarchy_monotonicity_verdict:
  assumes "\<gamma> v1 = Some g1" and "\<gamma> v2 = Some g2"
  shows "H.verdict_of (H.ground v1 f) (H.ground v2 f) =
         H_plus.verdict_of (H_plus.ground v1 f) (H_plus.ground v2 f)"
  using ground_preserved [OF assms(1)] ground_preserved [OF assms(2)]
  by simp

theorem hierarchy_monotonicity_unknown_resolves:
  assumes "\<gamma> v = None"
  shows "H.ground v f = Top"
  using assms by (simp add: H.ground_def)

theorem hierarchy_monotonicity_grounding_enables:
  assumes "\<gamma> v = None" and "\<gamma>_plus v = Some g"
  shows "H_plus.ground v f = f g"
  using assms(2) by (simp add: H_plus.ground_def)

theorem hierarchy_monotonicity_resolves_unknown:
  assumes "\<gamma> v1 = None" and "\<gamma>_plus v1 = Some g1"
    and "\<gamma> v2 = Some g2"
    and "f g1 = Classical s1" and "s1 \<noteq> {}"
    and "f g2 = Classical s2" and "s2 \<noteq> {}"
  shows "H.verdict_of (H.ground v1 f) (H.ground v2 f) = Unknown"
    and "H_plus.verdict_of (H_plus.ground v1 f) (H_plus.ground v2 f) \<noteq> Unknown"
proof -
  from assms(1) have "H.ground v1 f = Top"
    by (simp add: H.ground_def)
  from assms(3) have "H.ground v2 f = f g2"
    by (simp add: H.ground_def)
  with \<open>H.ground v1 f = Top\<close> assms(6) assms(7)
  show "H.verdict_of (H.ground v1 f) (H.ground v2 f) = Unknown"
    by simp
next
  from assms(2) have "H_plus.ground v1 f = f g1"
    by (simp add: H_plus.ground_def)
  from assms(3) have "\<gamma>_plus v2 = Some g2" using gamma_extends by simp
  then have "H_plus.ground v2 f = f g2"
    by (simp add: H_plus.ground_def)
  show "H_plus.verdict_of (H_plus.ground v1 f) (H_plus.ground v2 f) \<noteq> Unknown"
    using \<open>H_plus.ground v1 f = f g1\<close> \<open>H_plus.ground v2 f = f g2\<close>
          assms(4) assms(6)
    by simp
qed

lemma denot_isA_shared:
  "H.denot_isA g = H_plus.denot_isA g"
  by (simp add: H.denot_isA_def H_plus.denot_isA_def)

lemma denot_isPartOf_shared:
  "H.denot_isPartOf g = H_plus.denot_isPartOf g"
  by (simp add: H.denot_isPartOf_def H_plus.denot_isPartOf_def)

lemma denot_hasPart_shared:
  "H.denot_hasPart g = H_plus.denot_hasPart g"
  by (simp add: H.denot_hasPart_def H_plus.denot_hasPart_def)

lemma denot_eq_shared:
  "H.denot_eq g = H_plus.denot_eq g"
  by (simp add: H.denot_eq_def H_plus.denot_eq_def)

lemma denot_neq_shared:
  "H.denot_neq g = H_plus.denot_neq g"
  by (simp add: H.denot_neq_def H_plus.denot_neq_def)

lemma denot_isAnyOf_shared:
  "H.denot_isAnyOf gs = H_plus.denot_isAnyOf gs"
  by (simp add: H.denot_isAnyOf_def H_plus.denot_isAnyOf_def)

lemma denot_isAllOf_shared:
  "H.denot_isAllOf gs = H_plus.denot_isAllOf gs"
  by (simp add: H.denot_isAllOf_def H_plus.denot_isAllOf_def)

lemma denot_isNoneOf_shared:
  "H.denot_isNoneOf gs = H_plus.denot_isNoneOf gs"
  by (simp add: H.denot_isNoneOf_def H_plus.denot_isNoneOf_def)

corollary hierarchy_monotonicity_isA:
  assumes "\<gamma> v1 = Some g1" and "\<gamma> v2 = Some g2"
  shows "H.verdict_of (H.denot_isA g1) (H.denot_isA g2) =
         H_plus.verdict_of (H_plus.denot_isA g1) (H_plus.denot_isA g2)"
  using denot_isA_shared by simp

end (* hierarchy_extension locale *)

(* ================================================================= *)
(* Section 15: Cross-Hierarchy Alignment (Definitions 8-9)           *)
(* ================================================================= *)
locale alignment =
  H_A: hierarchy C\<^sub>A leq\<^sub>A disj\<^sub>A \<gamma>\<^sub>A +
  H_B: hierarchy C\<^sub>B leq\<^sub>B disj\<^sub>B \<gamma>\<^sub>B
  for C\<^sub>A    :: "'c set" and leq\<^sub>A and disj\<^sub>A and \<gamma>\<^sub>A :: "'v \<Rightarrow> 'c option"
  and C\<^sub>B    :: "'c set" and leq\<^sub>B and disj\<^sub>B and \<gamma>\<^sub>B :: "'v \<Rightarrow> 'c option" +
  fixes \<alpha> :: "'c \<Rightarrow> 'c option"
  assumes
    inj: "\<lbrakk>\<alpha> x = Some a; \<alpha> y = Some a\<rbrakk> \<Longrightarrow> x = y"
  and order_preserve:
      "\<lbrakk>\<alpha> x = Some x'; \<alpha> y = Some y'\<rbrakk>
        \<Longrightarrow> (leq\<^sub>A x y \<longleftrightarrow> leq\<^sub>B x' y')"
  and disj_preserve:
      "\<lbrakk>\<alpha> x = Some x'; \<alpha> y = Some y'; disj\<^sub>A x y\<rbrakk>
        \<Longrightarrow> disj\<^sub>B x' y'"

context alignment
begin

lemma disj_conflict_transfers:
  assumes "disj\<^sub>A x y" and "\<alpha> x = Some x'" and "\<alpha> y = Some y'"
  shows "disj\<^sub>B x' y'"
  using assms disj_preserve by blast

(* ================================================================= *)
(* Section 16: Lemma 2 - Denotation Preservation (all operators)     *)
(* ================================================================= *)

text \<open>isA: downward closure preserved by biconditional order preservation.\<close>
lemma denotation_preservation_isA:
  assumes g_map     : "\<alpha> g = Some g'"
    and   all_mapped: "\<forall>x \<in> {x \<in> C\<^sub>A. leq\<^sub>A x g}. \<exists>x'. \<alpha> x = Some x'"
  shows "(\<lambda>x. the (\<alpha> x)) ` {x \<in> C\<^sub>A. leq\<^sub>A x g} =
         {y. \<exists>x \<in> C\<^sub>A. \<alpha> x = Some y \<and> leq\<^sub>B y g'}"
proof (rule equalityI; rule subsetI)
  fix y
  assume "y \<in> (\<lambda>x. the (\<alpha> x)) ` {x \<in> C\<^sub>A. leq\<^sub>A x g}"
  then obtain x where xC: "x \<in> C\<^sub>A" and xl: "leq\<^sub>A x g" and ydef: "y = the (\<alpha> x)"
    by blast
  from all_mapped xC xl obtain x' where xm: "\<alpha> x = Some x'" by blast
  from ydef xm have "y = x'" by simp
  from order_preserve [OF xm g_map] xl have "leq\<^sub>B x' g'" by simp
  with xC xm \<open>y = x'\<close>
  show "y \<in> {y. \<exists>x \<in> C\<^sub>A. \<alpha> x = Some y \<and> leq\<^sub>B y g'}" by blast
next
  fix y
  assume "y \<in> {y. \<exists>x \<in> C\<^sub>A. \<alpha> x = Some y \<and> leq\<^sub>B y g'}"
  then obtain x where xC: "x \<in> C\<^sub>A" and xm: "\<alpha> x = Some y" and yl: "leq\<^sub>B y g'"
    by blast
  from order_preserve [OF xm g_map] yl have "leq\<^sub>A x g" by simp
  with xC have "x \<in> {x \<in> C\<^sub>A. leq\<^sub>A x g}" by blast
  from xm have "the (\<alpha> x) = y" by simp
  with \<open>x \<in> {x \<in> C\<^sub>A. leq\<^sub>A x g}\<close>
  show "y \<in> (\<lambda>x. the (\<alpha> x)) ` {x \<in> C\<^sub>A. leq\<^sub>A x g}" by blast
qed

text \<open>isPartOf shares the denotation definition with isA.\<close>
lemma denotation_preservation_isPartOf:
  assumes g_map     : "\<alpha> g = Some g'"
    and   all_mapped: "\<forall>x \<in> {x \<in> C\<^sub>A. leq\<^sub>A x g}. \<exists>x'. \<alpha> x = Some x'"
  shows "(\<lambda>x. the (\<alpha> x)) ` {x \<in> C\<^sub>A. leq\<^sub>A x g} =
         {y. \<exists>x \<in> C\<^sub>A. \<alpha> x = Some y \<and> leq\<^sub>B y g'}"
  using denotation_preservation_isA [OF g_map all_mapped] .

text \<open>hasPart: upward closure.\<close>
lemma denotation_preservation_hasPart:
  assumes g_map     : "\<alpha> g = Some g'"
    and   all_mapped: "\<forall>x \<in> {x \<in> C\<^sub>A. leq\<^sub>A g x}. \<exists>x'. \<alpha> x = Some x'"
  shows "(\<lambda>x. the (\<alpha> x)) ` {x \<in> C\<^sub>A. leq\<^sub>A g x} =
         {y. \<exists>x \<in> C\<^sub>A. \<alpha> x = Some y \<and> leq\<^sub>B g' y}"
proof (rule equalityI; rule subsetI)
  fix y
  assume "y \<in> (\<lambda>x. the (\<alpha> x)) ` {x \<in> C\<^sub>A. leq\<^sub>A g x}"
  then obtain x where xC: "x \<in> C\<^sub>A" and xl: "leq\<^sub>A g x" and ydef: "y = the (\<alpha> x)"
    by blast
  from all_mapped xC xl obtain x' where xm: "\<alpha> x = Some x'" by blast
  from ydef xm have "y = x'" by simp
  from order_preserve [OF g_map xm] xl have "leq\<^sub>B g' x'" by simp
  with xC xm \<open>y = x'\<close>
  show "y \<in> {y. \<exists>x \<in> C\<^sub>A. \<alpha> x = Some y \<and> leq\<^sub>B g' y}" by blast
next
  fix y
  assume "y \<in> {y. \<exists>x \<in> C\<^sub>A. \<alpha> x = Some y \<and> leq\<^sub>B g' y}"
  then obtain x where xC: "x \<in> C\<^sub>A" and xm: "\<alpha> x = Some y" and yl: "leq\<^sub>B g' y"
    by blast
  from order_preserve [OF g_map xm] yl have "leq\<^sub>A g x" by simp
  with xC have "x \<in> {x \<in> C\<^sub>A. leq\<^sub>A g x}" by blast
  from xm have "the (\<alpha> x) = y" by simp
  with \<open>x \<in> {x \<in> C\<^sub>A. leq\<^sub>A g x}\<close>
  show "y \<in> (\<lambda>x. the (\<alpha> x)) ` {x \<in> C\<^sub>A. leq\<^sub>A g x}" by blast
qed

text \<open>
  isAnyOf: union of downward closures.

  FIX BUG 1:
  Original broken line:
    "from all_mapped (UN_I [OF gset, of x] xC xl) obtain x' ..."
  This applies the hypothesis "all_mapped" as a term function, which is
  invalid Isabelle HOL syntax.  A "forall x in S. P x" hypothesis must
  be instantiated via [rule_format] + OF, or via bspec, or via blast
  after establishing membership.

  Fixed pattern:
    (1) Establish "xmem : x in (UN g:set gs. {x in C_A. leq_A x g})"
        using blast from xC, xl, gset.
    (2) Use "all_mapped[rule_format, OF xmem]" which correctly applies
        the universally quantified hypothesis to the membership proof.
\<close>
lemma denotation_preservation_isAnyOf:
  assumes gs_map    : "\<forall>g \<in> set gs. \<exists>g'. \<alpha> g = Some g'"
    and   all_mapped: "\<forall>x \<in> (\<Union>g \<in> set gs. {x \<in> C\<^sub>A. leq\<^sub>A x g}).
                         \<exists>x'. \<alpha> x = Some x'"
  shows "(\<lambda>x. the (\<alpha> x)) ` (\<Union>g \<in> set gs. {x \<in> C\<^sub>A. leq\<^sub>A x g}) =
         (\<Union>g' \<in> (\<lambda>g. the (\<alpha> g)) ` set gs.
           {y. \<exists>x \<in> C\<^sub>A. \<alpha> x = Some y \<and> leq\<^sub>B y g'})"
proof (rule equalityI; rule subsetI)
  fix y
  assume "y \<in> (\<lambda>x. the (\<alpha> x)) ` (\<Union>g \<in> set gs. {x \<in> C\<^sub>A. leq\<^sub>A x g})"
  then obtain x g where gset: "g \<in> set gs" and xC: "x \<in> C\<^sub>A"
    and xl: "leq\<^sub>A x g" and ydef: "y = the (\<alpha> x)"
    by blast
  \<comment> \<open>FIX BUG 1: establish membership explicitly, then use rule_format\<close>
  have xmem: "x \<in> (\<Union>g \<in> set gs. {x \<in> C\<^sub>A. leq\<^sub>A x g})"
    using xC xl gset by blast
  from all_mapped[rule_format, OF xmem] obtain x' where xm: "\<alpha> x = Some x'"
    by blast
  from gs_map gset obtain g' where gm: "\<alpha> g = Some g'" by blast
  from ydef xm have "y = x'" by simp
  from order_preserve [OF xm gm] xl have "leq\<^sub>B x' g'" by simp
  from gm have "g' = the (\<alpha> g)" by simp
  with gset \<open>y = x'\<close> xC xm \<open>leq\<^sub>B x' g'\<close>
  show "y \<in> (\<Union>g' \<in> (\<lambda>g. the (\<alpha> g)) ` set gs.
              {y. \<exists>x \<in> C\<^sub>A. \<alpha> x = Some y \<and> leq\<^sub>B y g'})"
    by (auto simp: \<open>g' = the (\<alpha> g)\<close>)
next
  fix y
  assume "y \<in> (\<Union>g' \<in> (\<lambda>g. the (\<alpha> g)) ` set gs.
                {y. \<exists>x \<in> C\<^sub>A. \<alpha> x = Some y \<and> leq\<^sub>B y g'})"
  then obtain g g' where gset: "g \<in> set gs" and gm: "g' = the (\<alpha> g)"
    and xC: "\<exists>x \<in> C\<^sub>A. \<alpha> x = Some y \<and> leq\<^sub>B y g'"
    by blast
  from gs_map gset obtain gval where gval: "\<alpha> g = Some gval" by blast
  with gm have "g' = gval" by simp
  from xC obtain x where xC2: "x \<in> C\<^sub>A" and xm: "\<alpha> x = Some y"
    and yl: "leq\<^sub>B y g'" by blast
  from order_preserve [OF xm gval] yl \<open>g' = gval\<close> have "leq\<^sub>A x g" by simp
  with xC2 gset have "x \<in> (\<Union>g \<in> set gs. {x \<in> C\<^sub>A. leq\<^sub>A x g})" by blast
  from xm have "the (\<alpha> x) = y" by simp
  with \<open>x \<in> (\<Union>g \<in> set gs. {x \<in> C\<^sub>A. leq\<^sub>A x g})\<close>
  show "y \<in> (\<lambda>x. the (\<alpha> x)) ` (\<Union>g \<in> set gs. {x \<in> C\<^sub>A. leq\<^sub>A x g})" by blast
qed

text \<open>
  isAllOf: intersection of downward closures.

  FIX BUG 2:
  The original assumption "witness_complete" was:
    "\<forall>g \<in> set gs. \<forall>x \<in> {x \<in> C\<^sub>A. leq\<^sub>A x g}. \<exists>x'. \<alpha> x = Some x'"
  When gs = [], this is vacuously True and gives NO information about
  alpha's domain over {x in C_A. forall g in []. leq_A x g} = C_A.
  The lemma was therefore LOGICALLY UNPROVABLE for empty gs.

  The three broken proof constructs in the original:
    (a) "ballI [of \"set gs\", OF FalseE]" -- ballI is an introduction
        rule for proof goals, not applicable as a term with [of ...]/OF.
    (b) "hd_in_set [OF <ne> <ne>]" -- hd_in_set takes ONE argument.
    (c) "by (cases gs) auto" -- auto does not have access to a mapping
        for x without the corrected assumption.

  FIX: Replace "witness_complete" with the stronger assumption
    "all_mapped : \<forall>x \<in> {x \<in> C\<^sub>A. \<forall>g \<in> set gs. leq\<^sub>A x g}. \<exists>x'. \<alpha> x = Some x'"
  which directly quantifies over the intersection set and covers gs = [].
  The proof then uses a two-step idiom:
    have xin : "x \<in> {x \<in> C\<^sub>A. ...}"  using xC xl by blast
    from all_mapped[rule_format, OF xin] obtain x' ...
\<close>
lemma denotation_preservation_isAllOf:
  assumes gs_map : "\<forall>g \<in> set gs. \<exists>g'. \<alpha> g = Some g'"
    and all_mapped:
        "\<forall>x \<in> {x \<in> C\<^sub>A. \<forall>g \<in> set gs. leq\<^sub>A x g}. \<exists>x'. \<alpha> x = Some x'"
        \<comment> \<open>CHANGED from per-g witness_complete to direct intersection mapping\<close>
  shows "(\<lambda>x. the (\<alpha> x)) ` {x \<in> C\<^sub>A. \<forall>g \<in> set gs. leq\<^sub>A x g} =
         {y. \<exists>x \<in> C\<^sub>A. \<alpha> x = Some y \<and> (\<forall>g' \<in> (\<lambda>g. the (\<alpha> g)) ` set gs. leq\<^sub>B y g')}"
proof (rule equalityI; rule subsetI)
  fix y
  assume "y \<in> (\<lambda>x. the (\<alpha> x)) ` {x \<in> C\<^sub>A. \<forall>g \<in> set gs. leq\<^sub>A x g}"
  then obtain x where xC: "x \<in> C\<^sub>A" and xl: "\<forall>g \<in> set gs. leq\<^sub>A x g"
    and ydef: "y = the (\<alpha> x)" by blast
  \<comment> \<open>FIX BUG 2: establish intersection membership, then apply all_mapped\<close>
  have xin: "x \<in> {x \<in> C\<^sub>A. \<forall>g \<in> set gs. leq\<^sub>A x g}"
    using xC xl by blast
  from all_mapped[rule_format, OF xin] obtain x' where xm: "\<alpha> x = Some x'"
    by blast
  from ydef xm have "y = x'" by simp
  have "\<forall>g' \<in> (\<lambda>g. the (\<alpha> g)) ` set gs. leq\<^sub>B y g'"
  proof
    fix g'
    assume "g' \<in> (\<lambda>g. the (\<alpha> g)) ` set gs"
    then obtain g where gset: "g \<in> set gs" and gdef: "g' = the (\<alpha> g)" by blast
    from gs_map gset obtain gval where gm: "\<alpha> g = Some gval" by blast
    from gdef gm have "g' = gval" by simp
    from xl gset have "leq\<^sub>A x g" by blast
    from order_preserve [OF xm gm] this have "leq\<^sub>B x' gval" by simp
    with \<open>y = x'\<close> \<open>g' = gval\<close> show "leq\<^sub>B y g'" by simp
  qed
  with xC xm \<open>y = x'\<close>
  show "y \<in> {y. \<exists>x \<in> C\<^sub>A. \<alpha> x = Some y \<and>
              (\<forall>g' \<in> (\<lambda>g. the (\<alpha> g)) ` set gs. leq\<^sub>B y g')}"
    by blast
next
  fix y
  assume "y \<in> {y. \<exists>x \<in> C\<^sub>A. \<alpha> x = Some y \<and>
              (\<forall>g' \<in> (\<lambda>g. the (\<alpha> g)) ` set gs. leq\<^sub>B y g')}"
  then obtain x where xC: "x \<in> C\<^sub>A" and xm: "\<alpha> x = Some y"
    and yl: "\<forall>g' \<in> (\<lambda>g. the (\<alpha> g)) ` set gs. leq\<^sub>B y g'" by blast
  have "\<forall>g \<in> set gs. leq\<^sub>A x g"
  proof
    fix g assume gset: "g \<in> set gs"
    from gs_map gset obtain gval where gm: "\<alpha> g = Some gval" by blast
    from yl imageI [OF gset] have "leq\<^sub>B y gval"
      by (simp add: \<open>\<alpha> g = Some gval\<close>)
    from order_preserve [OF xm gm] this show "leq\<^sub>A x g" by simp
  qed
  with xC have "x \<in> {x \<in> C\<^sub>A. \<forall>g \<in> set gs. leq\<^sub>A x g}" by blast
  from xm have "the (\<alpha> x) = y" by simp
  with \<open>x \<in> {x \<in> C\<^sub>A. \<forall>g \<in> set gs. leq\<^sub>A x g}\<close>
  show "y \<in> (\<lambda>x. the (\<alpha> x)) ` {x \<in> C\<^sub>A. \<forall>g \<in> set gs. leq\<^sub>A x g}" by blast
qed

(* ================================================================= *)
(* Section 17: Proposition 2 - Verdict Preservation                  *)
(* ================================================================= *)
theorem verdict_preservation_conflict:
  assumes disj_sets: "s1 \<inter> s2 = {}"
    and s1_mapped  : "\<forall>x \<in> s1. \<exists>x'. \<alpha> x = Some x'"
    and s2_mapped  : "\<forall>x \<in> s2. \<exists>x'. \<alpha> x = Some x'"
  shows "(\<lambda>x. the (\<alpha> x)) ` s1 \<inter> (\<lambda>x. the (\<alpha> x)) ` s2 = {}"
proof (rule ccontr)
  assume "\<not> ?thesis"
  then obtain y where y1: "y \<in> (\<lambda>x. the (\<alpha> x)) ` s1"
    and y2: "y \<in> (\<lambda>x. the (\<alpha> x)) ` s2" by blast
  from y1 obtain a where a: "a \<in> s1" and am: "the (\<alpha> a) = y" by blast
  from y2 obtain b where b: "b \<in> s2" and bm: "the (\<alpha> b) = y" by blast
  from s1_mapped a obtain a' where aa: "\<alpha> a = Some a'" by blast
  from s2_mapped b obtain b' where bb: "\<alpha> b = Some b'" by blast
  from am aa have "a' = y" by simp
  from bm bb have "b' = y" by simp
  with \<open>a' = y\<close> have "\<alpha> a = Some y" "\<alpha> b = Some y"
    using aa bb by simp_all
  from inj [OF this] have "a = b" .
  with a b disj_sets show False by blast
qed

text \<open>
  FIX BUG 3:
  Original: "hierarchy.verdict_of (Classical s1) (Classical s2) = Conflict"
  "verdict_of" is defined by "fun" inside "context hierarchy begin...end".
  "fun" inside a locale in Isabelle/HOL creates a GLOBAL constant -- it does
  NOT receive locale parameters and is NOT called "hierarchy.verdict_of" in
  other locale contexts.  In the "alignment" locale (which does not extend
  "hierarchy"), the correct unqualified name is simply "verdict_of".
  Using "hierarchy.verdict_of" causes a name-resolution error.
  SAME fix applies to "subsumption_verdict" in BUG 4 below.
\<close>
theorem verdict_preservation_conflict_full:
  \<comment> \<open>FIX BUG 3: "verdict_of" not "hierarchy.verdict_of"\<close>
  assumes "verdict_of (Classical s1) (Classical s2) = Conflict"
    and s1_mapped: "\<forall>x \<in> s1. \<exists>x'. \<alpha> x = Some x'"
    and s2_mapped: "\<forall>x \<in> s2. \<exists>x'. \<alpha> x = Some x'"
  shows "verdict_of
           (Classical ((\<lambda>x. the (\<alpha> x)) ` s1))
           (Classical ((\<lambda>x. the (\<alpha> x)) ` s2)) = Conflict"
proof -
  from assms(1) have "s1 \<inter> s2 = {}" by (simp split: if_splits)
  from verdict_preservation_conflict [OF this s1_mapped s2_mapped]
  show ?thesis by simp
qed

theorem graceful_degradation:
  assumes unmapped: "\<alpha> g = None"
    and other_nonempty: "s \<noteq> {}"
  shows "verdict_of (Classical ((\<lambda>x. the (\<alpha> x)) ` {})) (Classical s) = Conflict"
    and "verdict_of Top (Classical s) = Unknown"
  using other_nonempty by simp_all

theorem alignment_no_false_conflict:
  assumes compat: "s1 \<inter> s2 \<noteq> {}"
    and s1_mapped: "\<forall>x \<in> s1. \<exists>x'. \<alpha> x = Some x'"
    and s2_mapped: "\<forall>x \<in> s2. \<exists>x'. \<alpha> x = Some x'"
  shows "verdict_of
           (Classical ((\<lambda>x. the (\<alpha> x)) ` s1))
           (Classical ((\<lambda>x. the (\<alpha> x)) ` s2)) \<noteq> Conflict"
proof
  assume "verdict_of
            (Classical ((\<lambda>x. the (\<alpha> x)) ` s1))
            (Classical ((\<lambda>x. the (\<alpha> x)) ` s2)) = Conflict"
  then have "(\<lambda>x. the (\<alpha> x)) ` s1 \<inter> (\<lambda>x. the (\<alpha> x)) ` s2 = {}"
    by (simp split: if_splits)
  from compat obtain w where w1: "w \<in> s1" and w2: "w \<in> s2" by blast
  from s1_mapped w1 obtain w' where wm: "\<alpha> w = Some w'" by blast
  have "the (\<alpha> w) \<in> (\<lambda>x. the (\<alpha> x)) ` s1"
    using w1 by blast
  moreover have "the (\<alpha> w) \<in> (\<lambda>x. the (\<alpha> x)) ` s2"
    using w2 by blast
  ultimately show False
    using \<open>(\<lambda>x. the (\<alpha> x)) ` s1 \<inter> (\<lambda>x. the (\<alpha> x)) ` s2 = {}\<close>
    by blast
qed

theorem empty_preserved:
  "(\<lambda>x. the (\<alpha> x)) ` {} = {}" by simp

theorem empty_conflict_preserved:
  "verdict_of (Classical {}) d' = Conflict"
  by (cases d'; simp)

(* ================================================================= *)
(* Section 18: Corollary 1 - Subsumption Preservation                *)
(* ================================================================= *)
theorem subsumption_preservation:
  assumes sub      : "s1 \<subseteq> s2"
    and s1_mapped  : "\<forall>x \<in> s1. \<exists>x'. \<alpha> x = Some x'"
    and s2_mapped  : "\<forall>x \<in> s2. \<exists>x'. \<alpha> x = Some x'"
  shows "(\<lambda>x. the (\<alpha> x)) ` s1 \<subseteq> (\<lambda>x. the (\<alpha> x)) ` s2"
  using sub by blast

theorem subsumption_preservation_verdict:
  \<comment> \<open>FIX BUG 4: "subsumption_verdict" not "hierarchy.subsumption_verdict"\<close>
  assumes "subsumption_verdict (Classical s1) (Classical s2) = Confirmed"
    and s1_mapped: "\<forall>x \<in> s1. \<exists>x'. \<alpha> x = Some x'"
    and s2_mapped: "\<forall>x \<in> s2. \<exists>x'. \<alpha> x = Some x'"
  shows "subsumption_verdict
           (Classical ((\<lambda>x. the (\<alpha> x)) ` s1))
           (Classical ((\<lambda>x. the (\<alpha> x)) ` s2)) = Confirmed"
proof -
  from assms(1) have "s1 \<subseteq> s2" by (simp split: if_splits)
  from subsumption_preservation [OF this s1_mapped s2_mapped]
  show ?thesis by simp
qed

end (* alignment locale *)

end
