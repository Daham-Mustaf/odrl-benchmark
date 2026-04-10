%--------------------------------------------------------------------------
% File     : HARD001+1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : Full reasoning chain across 6 axiom files
% Version  : 1.0
% English  : Six properties derived from ordering chain n0<n3<n5<n10<n20:
%           : conflict propagation, density witness, open-interval criterion,
%           : conflict completion, compatible completion, box verdict.
%           : No intermediate results given — prover derives everything
%           : from first principles across ORD000+ORD001+AXIS000+PREC000+COMPL000.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R.,
%          :          Quix, C., Decker, S. Axis Decomposition for ODRL.
%          :          arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : HARD001+1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Hard tier — requires all 5 axiom files simultaneously.
%           : Conjecture is 6-way conjunction; each part tests one paper theorem.
%           : Policy source: Policies/HARD001-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/ORD001-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/PREC000-0.ax').
include('Axioms/COMPL000-0.ax').

% ==========================================================================
% Hypotheses: raw ordering facts + domain bounds only.
% No axis_conflict, axis_subsumes, or completion facts are given.
% ==========================================================================

% Ordering chain: n0 < n3 < n5 < n10 < n20
fof(h_0_3,   hypothesis, less(n0,n3)).
fof(h_3_5,   hypothesis, less(n3,n5)).
fof(h_5_10,  hypothesis, less(n5,n10)).
fof(h_10_20, hypothesis, less(n10,n20)).

% Domain bounds: ninf is the infimum, nsup is the supremum.
% Every domain value lies in [ninf, nsup].
fof(h_inf_lb, hypothesis, ![X]: leq(ninf,X)).
fof(h_sup_ub, hypothesis, ![X]: leq(X,nsup)).

% Width policy intervals (endpoints only — no verdict asserted):
%   P1  width: [n0, n5]   (gteq n0 and lteq n5)
%   P1' width: [n0, n3]   (gteq n0 and lteq n3)  -- stricter than P1
%   P2  width: [n10, n20] (gteq n10 and lteq n20)
%   Open-P1 width: (n5, nsup]  (gt n5)
%   Open-P2 width: [ninf, n10) (lt n10)

% ==========================================================================
% Conjecture: six properties derived from the ordering chain above.
% ==========================================================================

fof(hard_chain, conjecture, (

  % ------------------------------------------------------------------
  % Part A: Conflict propagation through subsumption
  % [Paper: lem:conflict-propagation, prop:monotone]
  %
  % Proof sketch:
  %   1. axis_subsumes(n0,n3,n0,n5):
  %      For any X: leq(n0,X) & leq(X,n3)
  %        => leq(X,n3) & less(n3,n5) => less(X,n5) [less_leq_trans inverted]
  %           Wait: less_leq_trans: leq(X,Y) & less(Y,Z) => less(X,Z).
  %           Here: leq(X,n3) & less(n3,n5) => less(X,n5) => leq(X,n5).
  %        => in_closed(X,n0,n5). QED.
  %   2. axis_conflict(n0,n5,n10,n20):
  %      Assume witness W: leq(n0,W) & leq(W,n5) & leq(n10,W) & leq(W,n20).
  %      leq(W,n5) & leq(n10,W) => leq(n10,n5) [leq_trans, need it].
  %      less(n5,n10) => leq(n5,n10) [less_implies_leq].
  %      leq(n10,n5) & leq(n5,n10) => n10=n5 [leq_antisym].
  %      less(n5,n10) = less(n5,n5) [by n10=n5] => ~less(n5,n5) [irreflexive].
  %      Contradiction => ~exists W. QED.
  %   3. monotone_conflict fires: gives axis_conflict(n0,n3,n10,n20).
  % ------------------------------------------------------------------
  axis_conflict(n0,n3,n10,n20)

  &

  % ------------------------------------------------------------------
  % Part B: Density witness inside open interval (n5, n10)
  % [Paper: implicit in def:interval-denotation for lt/gt operators]
  %
  % Proof sketch:
  %   less(n5,n10) + dense => ?[Z]: less(n5,Z) & less(Z,n10). Direct.
  % ------------------------------------------------------------------
  ( ?[Z]: (less(n5,Z) & less(Z,n10)) )

  &

  % ------------------------------------------------------------------
  % Part C: Open intervals (n5,nsup] and [ninf,n10) are not disjoint
  % [Paper: thm:criterion with open endpoints]
  %
  % Proof sketch:
  %   disjoint(n5,nsup,o,c, ninf,n10,c,o)
  %     <=> prec(nsup,ninf,c,c) | prec(n10,n5,o,o)
  %     <=> less(nsup,ninf) | leq(n10,n5).
  %
  %   ~less(nsup,ninf):
  %     leq(ninf,n5) [h_inf_lb] & less(n5,n10) & leq(n10,nsup) [h_sup_ub]
  %     => less(ninf,nsup) [chain via leq_less_trans + less_leq_trans].
  %     less(ninf,nsup) & less(nsup,ninf) => less(ninf,ninf) [transitive]
  %     => ~less(ninf,ninf) [irreflexive]. Contradiction.
  %
  %   ~leq(n10,n5):
  %     leq(n10,n5) & leq(n5,n10) [from less(n5,n10)+less_implies_leq]
  %     => n10=n5 [leq_antisym].
  %     less(n5,n10) = less(n5,n5) [subst n10=n5] => contradiction [irreflexive].
  %
  %   => ~disjoint(...). QED.
  % ------------------------------------------------------------------
  ~disjoint(n5,nsup,o,c, ninf,n10,c,o)

  &

  % ------------------------------------------------------------------
  % Part D: Conflict completion exists for an unconstrained axis
  % [Paper: def:completion, thm:unknown-sound conflict direction]
  %
  % Proof sketch:
  %   completion_conflict(n5,n10,ninf,nsup) requires:
  %     leq(ninf,n5)  [h_inf_lb instantiated at n5]
  %     leq(n5,nsup)  [h_sup_ub instantiated at n5]
  %     leq(ninf,n10) [h_inf_lb instantiated at n10]
  %     leq(n10,nsup) [h_sup_ub instantiated at n10]
  %     less(n5,n10)  [h_5_10]
  %   All five antecedents satisfied => completion_conflict fires.
  % ------------------------------------------------------------------
  completion_conflict(n5,n10,ninf,nsup)

  &

  % ------------------------------------------------------------------
  % Part E: Compatible completion exists for an unconstrained axis
  % [Paper: def:completion, thm:unknown-sound compatible direction]
  %
  % Proof sketch:
  %   completion_compatible(n5,ninf,nsup) requires:
  %     leq(ninf,n5) [h_inf_lb] & leq(n5,nsup) [h_sup_ub].
  %   Both satisfied => completion_compatible fires.
  % ------------------------------------------------------------------
  completion_compatible(n5,ninf,nsup)

  &

  % ------------------------------------------------------------------
  % Part F: Conflict dominates Unknown in box aggregation
  % [Paper: def:box-verdict, Strong Kleene min]
  %
  % Proof sketch:
  %   box_conflict axiom: (is_verdict(V1) & is_verdict(V2) &
  %     (V1=conflict | V2=conflict)) => box_verdict(V1,V2)=conflict.
  %   V1=conflict (from Part A, width axis) & V2=unknown (height axis,
  %   unconstrained by one policy) => box_verdict(conflict,unknown)=conflict.
  %   is_verdict(conflict) and is_verdict(unknown) from AXIS000 Section C.
  %   Trivial once conflict and unknown are recognised as verdicts.
  % ------------------------------------------------------------------
  box_verdict(conflict,unknown) = conflict

)).

%--------------------------------------------------------------------------
% Proof difficulty breakdown by part:
%
%   Part  Axiom files         Key challenge                  Est. steps
%   ----  ------------------  -----------------------------  ----------
%   A     ORD000+AXIS000+     Universal quantifier inst.     ~15
%         COMPL000            + contradiction via ordering
%   B     ORD000+ORD001       Existential from dense         ~2
%   C     ORD000+PREC000      Two-branch negation proof      ~8
%   D     ORD000+COMPL000     5-antecedent instantiation     ~3
%   E     ORD000+COMPL000     2-antecedent instantiation     ~2
%   F     AXIS000             is_verdict + box_conflict      ~1
%
% Part A is the performance bottleneck.  An ATP that handles it will
% handle the rest; the conjunction forces all 6 parts to be closed
% before the proof is complete.
%
% Suggested Vampire invocation:
%   vampire --mode casc --time_limit 300 HARD001+1.p
% Suggested E invocation:
%   eprover --auto --cpu-limit=300 HARD001+1.p
%--------------------------------------------------------------------------
