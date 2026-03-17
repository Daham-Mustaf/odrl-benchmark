%--------------------------------------------------------------------------
% File     : GRND008-regimented-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : Regimented prohibition: contradiction
% Status   : Unsatisfiable
% Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
% Generated: 2026-03-17 by gen_foundation_problems.py v1.3
%
% % Regimented axiom: ~does when prohibited.
% % Ground witness: does(alice,distribute,d1). Contradiction.
%--------------------------------------------------------------------------

% Layer 0: Signature (sorts, rfr/decl, position disjointness)
include('Axioms/Layer0-Signature/GRND000-0.ax').

% Layer 1: Problem-specific axioms (subset of Ax5.1-5.10)

%--------------------------------------------------------------------------
% Appendix A.0 extra predicates (declared via axiom context in Layer1)
%   norm_state_change(X,A,T,Q)  -- position Q changes for X over (A,T)
%   inst_event(E)               -- E is an institutional event
%   triggers(E,X,A,T,Q)         -- E triggers the change of Q
%   competent_for(Y,E)          -- Y is competent to perform E
%   about_event(Pos,E)          -- position Pos concerns event E
%   does(X,A,T)                 -- X performs A on T
%   duty_rem                    -- constant: token for remedy-duty position
%   odrl_rel(Rho)               -- Rho is a relator founded by an ODRL rule
%--------------------------------------------------------------------------

%--------------------------------------------------------------------------
% Ground instance (gamma)
%--------------------------------------------------------------------------
fof(agent_alice,       axiom, agent(alice)).
fof(action_distribute, axiom, action(distribute)).
fof(target_d1,         axiom, target(d1)).
fof(rule_f1,           axiom, rule(f1)).
fof(event_e1,          axiom, event(e1)).
fof(proh_f1,           axiom, proh(f1)).
fof(rem_f1,            axiom, has_rem(f1)).
fof(act_f1,            axiom, act(f1, distribute)).
fof(aee_f1,            axiom, aee(f1, alice)).
fof(act_e1_f1,         axiom, activates(e1, f1)).
fof(regimented, axiom,
    ! [X, A, T, F, E] :
      ( ( proh(F) & aee(F,X) & act(F,A) & activates(E,F) )
     => ~ does(X,A,T) )).
fof(alice_does, axiom, does(alice, distribute, d1)).
