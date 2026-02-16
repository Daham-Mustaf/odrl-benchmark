(* ════════════════════════════════════════════════════════════════════ *)
(* ADD inside your existing knowledge_base context, after              *)
(* disj_order_consistency. These are the ONLY new lines.              *)
(*                                                                    *)
(* Assumes your locale has:                                           *)
(*   disj_downward: ⟦ disj x y; leq x' x ⟧ ⟹ disj x' y            *)
(*   disj_irrefl:   ¬ disj x x   (or: disj x x ⟹ False)            *)
(*                                                                    *)
(* If your disj_downward takes 3 premises instead of 2, replace the  *)
(* two-step proof with:                                               *)
(*   using disj_downward[OF assms(3) assms(1) assms(2)]              *)
(*         disj_irrefl by blast                                       *)
(* ════════════════════════════════════════════════════════════════════ *)

(* Multi-parent concepts with disjoint parents make the KB 
   inconsistent. Benchmark: ODRL094-100. 
   
   Two-step: disj(a,b) + leq(m,a) → disj(m,b)
             disj(m,b) + leq(m,b) → disj(m,m) → False              *)
theorem multi_parent_inconsistency:
  assumes "leq m a" "leq m b" "disj a b"
  shows   False
proof -
  from disj_downward[OF assms(3) assms(1)] have "disj m b" .
  from disj_downward[OF this assms(2)] have "disj m m" .
  with disj_irrefl show False by blast
qed

(* Any proposition follows from an inconsistent KB. *)
corollary ex_falso_verdict:
  assumes "leq m a" "leq m b" "disj a b"
  shows   "P"
  using multi_parent_inconsistency[OF assms] by blast

(* Downward closure: ↓x = {y ∈ C | y ≤ x} *)
definition down :: "'a ⇒ 'a set" where
  "down x = {y ∈ C. leq y x}"

(* If a multi-parent witness exists, asserting disj causes contradiction.
   This IS the DAG-safe criterion: don't assert disj(a,b) if ∃m ≤ a ∧ m ≤ b. *)
theorem dag_unsafe_disj:
  assumes "m ∈ C" "leq m a" "leq m b" "disj a b"
  shows   False
  using multi_parent_inconsistency[OF assms(2) assms(3) assms(4)] .

(* Converse: if downsets don't overlap, no witness exists *)
theorem dag_safe_guard:
  assumes "down a ∩ down b = {}" "m ∈ C" "leq m a" "leq m b"
  shows   False
  using assms unfolding down_def by auto

(* A common descendant lands in both downsets *)
theorem dag_unsafe_witness:
  assumes "m ∈ C" "leq m a" "leq m b"
  shows   "m ∈ down a ∩ down b"
  using assms unfolding down_def by auto
