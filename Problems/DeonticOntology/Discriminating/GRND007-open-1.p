%--------------------------------------------------------------------------
% File     : GRND007-open-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : Open-world: uncovered action entails Liberty by default
% Status   : Theorem
% Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
% Generated: 2026-03-17 by gen_foundation_problems.py v1.3
%
% % Open-world closure added. No proh for 'modify'.
% % Liberty(alice,modify,d1) is derivable.
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
fof(agent_alice,        axiom, agent(alice)).
fof(agent_acme,         axiom, agent(acme)).
fof(action_modify,      axiom, action(modify)).
fof(target_d1,          axiom, target(d1)).
fof(no_proh_modify,     axiom,
    ~ ? [F, E] : ( proh(F) & aee(F,alice) & act(F,modify) & activates(E,F) )).
fof(open_world_closure, axiom,
    ! [X, A, T] :
      ( ( agent(X) & action(A) & target(T)
        & ~ ? [F, E] : ( proh(F) & aee(F,X) & act(F,A) & activates(E,F) ) )
     => ? [L] : ( liberty(L) & bearer(L,X) & cnt(L,A,T) ) )).

%--------------------------------------------------------------------------
% Conjecture
%--------------------------------------------------------------------------
fof(conjecture, conjecture,
    ( ? [L] : ( liberty(L) & bearer(L, alice) & cnt(L, modify, d1) ) )).