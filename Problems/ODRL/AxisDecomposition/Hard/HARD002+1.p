%--------------------------------------------------------------------------
% File     : HARD002+1.p
% Domain   : ODRL Policy / Axis Decomposition
% Problem  : Unknown does NOT imply all completions yield Conflict
% Version  : 1.0
% English  : The conjecture claims every completion of an Unknown scenario
%           : yields Conflict. This is FALSE: compatible completion always
%           : exists (thm:unknown-sound). Resolution provers timeout;
%           : model finders find a 3-element countermodel.
%
% Refs     : [Mus+26] Mustafa, D., Collarana, D., Lange, C., Peng, Y., Haque, R.,
%          :          Quix, C., Decker, S. Axis Decomposition for ODRL.
%          :          arXiv:2602.19878. https://arxiv.org/abs/2602.19878
% Source   : Mustafa, D. (2026)
% Authors  : Mustafa, D. & Sutcliffe, G.
% Names    : HARD002+1.p
%
% Status   : CounterSatisfiable
% SPC      : FOF_CSA_RFN
%
% Comments : Hard tier — discriminating (non-theorem) problem.
%           : Expected: CounterSatisfiable from model finder (Paradox/Mace4).
%           : Resolution provers (Vampire/E) expected to timeout.
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
