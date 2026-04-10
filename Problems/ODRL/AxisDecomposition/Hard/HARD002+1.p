%--------------------------------------------------------------------------
% File     : HARD002+1.p
% Domain   : Axis Decomposition (ODRL)
% Problem  : Unknown verdict does NOT imply Conflict under any completion
%            — the Compatible completion always exists.  This is a
%            DISCRIMINATING (non-theorem) problem: the conjecture is false,
%            and the prover must find a countermodel.
% Version  : [vldb2027] axioms.
% English  :
%   The conjecture claims: whenever boxV = Unknown, every completion
%   yields Conflict.  This is FALSE by thm:unknown-sound (the Compatible
%   completion always exists).  A model-finding ATP (Paradox, Mace4) must
%   exhibit a completion that yields Compatible.
%
%   Why this is hard for resolution provers:
%     A resolution prover attempting to prove the (false) conjecture will
%     exhaust a large portion of the search space before timing out.
%     The axiom set is large (ORD000 + ORD001 + AXIS000 + COMPL000) and
%     all four axiom files interact. The prover must eventually saturate
%     without finding a proof — which is expensive.
%
%   Why this is hard for model finders:
%     The countermodel must simultaneously satisfy:
%       (1) The full total-order axioms (ORD000)
%       (2) The density axiom (ORD001) — requires an infinite domain or
%           a domain of size >= 3 with the right ordering
%       (3) completion_compatible firing for some V in [ninf,nsup]
%       (4) axis_compatible witnessing overlap in the Compatible completion
%     This forces a domain of size >= 3 (ninf, V, nsup with
%     ninf < V < nsup — requires density), making the model non-trivial.
%
% Refs     :  Axis decomposition tier. arXiv:2602.19878.
% Source   : Generated for PAAR 2026 TPTP benchmark
% Names    :
% Status   : CounterSatisfiable
% Rating   : TBD  (expected: hard — large axiom set, requires dense model)
% Syntax   : Number of formulae    :   5 (hypotheses) + 1 (conjecture)
%            Number of axiom files :   4
% SPC      : FOF_CSA_RFO_SEQ
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

fof(h_inf_0,  hypothesis, less(ninf,n0)).
fof(h_0_sup,  hypothesis, less(n0,nsup)).
fof(h_inf_lb, hypothesis, ![X]: leq(ninf,X)).
fof(h_sup_ub, hypothesis, ![X]: leq(X,nsup)).

% The box verdict is Unknown (both axes have at least one policy absent).
fof(h_unknown, hypothesis, box_verdict(unknown,unknown) = unknown).

% ==========================================================================
% Conjecture (FALSE — countermodel exists):
% Claim: Unknown implies ALL completions yield Conflict.
%
% This is refuted by completion_compatible(n0,ninf,nsup):
%   leq(ninf,n0) [h_inf_lb] & leq(n0,nsup) [h_sup_ub]
%   => completion_compatible(n0,ninf,nsup) fires.
% A Compatible completion EXISTS, so not all completions yield Conflict.
% ==========================================================================

fof(false_conjecture, conjecture,
    % Claim: for all values V in [ninf,nsup], the completion is a Conflict.
    % This is false: V=n0 gives a Compatible completion.
    ![V]:
      ((leq(ninf,V) & leq(V,nsup))
       => ~completion_compatible(V,ninf,nsup))).

%--------------------------------------------------------------------------
% Expected behaviour:
%   Resolution prover (Vampire, E): should NOT prove this.
%     Expected outcome: SZS status CounterSatisfiable (or Timeout).
%   Model finder (Paradox, Mace4): should find a model of size >= 3
%     with ninf < n0 < nsup satisfying density + completion_compatible.
%
% The countermodel construction (hint for model finders):
%   Domain: {ninf, n0, nsup}
%   less: ninf<n0, n0<nsup, ninf<nsup  (strict total order)
%   leq:  reflexive closure of less
%   dense: satisfied trivially (no pair with less(X,Y) and no Z between
%          in a 3-element domain — BUT density fails for ninf<nsup with
%          no Z strictly between ninf and nsup other than n0).
%          Paradox may need domain size 4 or larger to satisfy density fully.
%   completion_compatible(n0,ninf,nsup): fires since leq(ninf,n0)&leq(n0,nsup).
%   ~completion_compatible(n0,ninf,nsup): required by conjecture. Contradiction.
%   => conjecture is falsified by this interpretation.
%--------------------------------------------------------------------------
