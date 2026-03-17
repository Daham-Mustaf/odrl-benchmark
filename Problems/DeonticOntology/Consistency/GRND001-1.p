%--------------------------------------------------------------------------
% File     : GRND001-1.p
% Domain   : Deontic Ontology / ODRL Grounding
% Problem  : Full axiom set consistency
% Status   : Satisfiable
% Refs     : Mohammed et al., What Does ODRL Mean? FOIS 2026
% Generated: 2026-03-17 by gen_foundation_problems.py v1.3
%
% % The full axiom set (Ax5.1-5.10, A1-A3, B1-B3) is satisfiable.
% % Minimal model: one perm rule, one agent pair, one action, one target.
%--------------------------------------------------------------------------

% Layer 0: Signature (sorts, rfr/decl, position disjointness)
include('Axioms/Layer0-Signature/GRND000-0.ax').

% Layer 1: Problem-specific axioms (subset of Ax5.1-5.10)
fof(ax_perm_relator_basic, axiom,
    ! [P, X, Y, A, T, E] :
      ( ( perm(P) & aee(P,X) & aer(P,Y) & act(P,A) & tgt(P,T) & activates(E,P) )
     => ? [Rho, L, N] :
          ( founds(E,Rho,P)
          & liberty(L)  & bearer(L,X) & cnt(L,A,T)  & part_of(L,Rho)
          & no_right(N) & bearer(N,Y) & cnt(N,A,T)  & part_of(N,Rho) ) )).

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
fof(agent_alice,  axiom, agent(alice)).
fof(agent_acme,   axiom, agent(acme)).
fof(action_read,  axiom, action(read)).
fof(target_d1,    axiom, target(d1)).
fof(rule_p1,      axiom, rule(p1)).
fof(event_e1,     axiom, event(e1)).
fof(perm_p1,      axiom, perm(p1)).
fof(aee_p1,       axiom, aee(p1, alice)).
fof(aer_p1,       axiom, aer(p1, acme)).
fof(act_p1,       axiom, act(p1, read)).
fof(tgt_p1,       axiom, tgt(p1, d1)).
fof(act_e1_p1,    axiom, activates(e1, p1)).
