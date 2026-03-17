%--------------------------------------------------------------------------
% File     : GRND005-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : Liberty-Duty conflict detection (single relator)
% Status   : Unsatisfiable
% Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
% Generated: 2026-03-17 by gen_foundation_problems.py v1.3
%
% % Liberty(l,alice,read,d1) and Duty(d,alice,rfr(read),d1) in same rho.
% % Ax5.8 derives False.
%--------------------------------------------------------------------------

% Layer 0: Signature (sorts, rfr/decl, position disjointness)
include('Axioms/Layer0-Signature/GRND000-0.ax').

% Layer 1: Problem-specific axioms (subset of Ax5.1-5.10)
fof(ax_cross_relator_consistency, axiom,
    ! [L, D, X, A, T] :
      ( ( liberty(L) & bearer(L,X) & cnt(L,A,T)
        & duty(D)    & bearer(D,X) & cnt(D,rfr(A),T) )
     => $false )).

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
fof(agent_alice, axiom, agent(alice)).
fof(action_read, axiom, action(read)).
fof(target_d1,   axiom, target(d1)).
fof(pos_l,       axiom, position(l)).
fof(pos_d,       axiom, position(d)).
fof(rel_rho1,    axiom, legal_relator(rho1)).
fof(liberty_l,   axiom, liberty(l)).
fof(duty_d,      axiom, duty(d)).
fof(bearer_l,    axiom, bearer(l, alice)).
fof(bearer_d,    axiom, bearer(d, alice)).
fof(cnt_l,       axiom, cnt(l, read, d1)).
fof(cnt_d,       axiom, cnt(d, rfr(read), d1)).
fof(partof_l,    axiom, part_of(l, rho1)).
fof(partof_d,    axiom, part_of(d, rho1)).
