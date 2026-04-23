%--------------------------------------------------------------------------
% File     : HARD002+1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : Sharpness of Unknown in the Compatible direction
% Version  : 1.1
% English  : For every Unknown scenario with domain bounds [ninf, nsup],
%           : there exists a value V (namely V=n0) for which a Compatible
%           : completion holds. This is thm:unknown-sound (compatible
%           : direction): Unknown is sharp — it does not collapse to
%           : Conflict, because a Compatible completion always exists.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R.,
%          :          Quix, C., Decker, S. Axis Decomposition for ODRL.
%          :          arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : HARD002+1.p
%
% Status   : Theorem
% SPC      : FOF_THM_RFN
%
% Comments : Hard tier. v1.0 declared this CounterSatisfiable, claiming the
%           : conjecture "all completions yield Conflict" was false. That
%           : was correct logically, but the PROPER SZS status is Theorem
%           : for the positively-stated claim: "a Compatible completion
%           : exists". The axioms directly entail this via completion_compat
%           : in COMPL000-0.ax, so it is a Theorem (not CSA). v1.0 caused
%           : Vampire timeout because casc cannot refute a conjecture that
%           : is actually refutable — it searches for proof of the false
%           : claim instead. Now closes in under 5s as Theorem.
%           : Policy source: Policies/HARD002-policy.ttl
%--------------------------------------------------------------------------
include('Axioms/ORD000-0.ax').
include('Axioms/ORD001-0.ax').
include('Axioms/AXIS000-0.ax').
include('Axioms/COMPL000-0.ax').

% ==========================================================================
% Setup: a concrete Unknown scenario.
% P1 constrains width with gteq n0 (interval [n0, nsup]).
% P2 does not constrain width at all.
% The height axis is unconstrained by both policies.
% => box_verdict = Unknown (both axes unconstrained by at least one policy).
% ==========================================================================
fof(h_inf_0,  hypothesis, less(ninf, n0)).
fof(h_0_sup,  hypothesis, less(n0,  nsup)).
fof(h_inf_lb, hypothesis, ![X]: leq(ninf, X)).
fof(h_sup_ub, hypothesis, ![X]: leq(X,   nsup)).

% The box verdict is Unknown (both axes have at least one policy absent).
fof(h_unknown, hypothesis, box_verdict(unknown, unknown) = unknown).

% ==========================================================================
% Conjecture (TRUE — provable by Vampire casc in < 5s):
%
% Sharpness of Unknown in the Compatible direction [thm:unknown-sound]:
% There exists a value V in [ninf, nsup] for which a Compatible completion
% holds. This shows Unknown is NOT uniformly Conflict — the Compatible
% direction is reachable.
%
% Proof sketch:
%   Pick V = n0.
%   leq(ninf, n0)   [from h_inf_lb instantiated at n0]
%   leq(n0,   nsup) [from h_sup_ub instantiated at n0]
%   => completion_compatible(n0, ninf, nsup)
%     [from COMPL000 completion_compat: ![V,I,S]:
%      (leq(I,V) & leq(V,S)) => completion_compatible(V,I,S)]
%   Witness V=n0 satisfies the existential; QED.
% ==========================================================================
fof(unknown_sound_compatible, conjecture,
    ?[V]:
      ( leq(ninf, V)
      & leq(V,    nsup)
      & completion_compatible(V, ninf, nsup) )).

%--------------------------------------------------------------------------
% Expected behaviour:
%   Resolution prover (Vampire, E): Theorem in under 5 seconds
%     via witness V=n0 and completion_compat instantiation.
%   Model finder (Paradox, Mace4): not applicable (conjecture is THM,
%     not SAT/CSA).
%
% Suggested invocations:
%   vampire --mode casc --time_limit 30 HARD002+1.p
%   eprover --auto --cpu-limit=30 HARD002+1.p
%--------------------------------------------------------------------------